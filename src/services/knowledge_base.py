"""Role archetype knowledge base loader for job role recommender"""

import yaml
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
from ..models.role_recommendation import RecommendedRole


class RoleArchetype:
    """Represents a role archetype with its requirements and characteristics"""

    def __init__(self, data: Dict[str, Any]):
        self.title = data.get('title', '')
        self.industry = data.get('industry', '')
        self.description = data.get('description', '')
        self.required_skills = data.get('required_skills', [])
        self.preferred_skills = data.get('preferred_skills', [])
        self.technologies = data.get('technologies', [])
        self.responsibilities = data.get('responsibilities', [])
        self.seniority_requirements = data.get('seniority_requirements', {})
        self.role_signals = data.get('role_signals', {})


class RoleArchetypeLoader:
    """Loads and manages role archetypes from YAML files"""

    def __init__(self, base_path: str = "./src/knowledge"):
        self.base_path = Path(base_path)
        self.archetypes: Dict[str, RoleArchetype] = {}
        self.archetype_cache: Dict[str, RoleArchetype] = {}
        self.industry_cache: Dict[str, List[RoleArchetype]] = {}
        self.last_load_time = 0
        self.cache_ttl = 300  # Cache TTL in seconds (5 minutes)
        self.logger = logging.getLogger(__name__)

    def load_archetypes(self) -> Dict[str, RoleArchetype]:
        """Load all archetypes from the knowledge base with caching"""
        import time

        current_time = time.time()

        # Check if cache is still valid
        if current_time - self.last_load_time < self.cache_ttl and self.archetypes:
            self.logger.debug("Using cached archetypes")
            return self.archetypes

        self.logger.info("Loading archetypes from knowledge base...")
        start_time = time.time()

        self.archetypes = {}

        # Load base archetypes
        base_archetypes_path = self.base_path / "archetypes.yaml"
        if base_archetypes_path.exists():
            self.archetypes.update(self._load_from_file(base_archetypes_path))

        # Load industry-specific archetypes
        industries_path = self.base_path / "industries"
        if industries_path.exists():
            for yaml_file in industries_path.glob("*.yaml"):
                self.archetypes.update(self._load_from_file(yaml_file))

        self.last_load_time = current_time

        load_duration = time.time() - start_time
        self.logger.info(f"Loaded {len(self.archetypes)} archetypes in {load_duration:.2f}s")

        # Clear industry cache as archetypes have changed
        self.industry_cache.clear()

        return self.archetypes

    def _load_from_file(self, file_path: Path) -> Dict[str, RoleArchetype]:
        """Load archetypes from a single YAML file"""
        import time

        archetypes = {}
        try:
            start_time = time.time()

            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not data:
                return archetypes

            # Handle different YAML structures
            if 'archetypes' in data:
                # YAML has a top-level archetypes key
                archetype_list = data['archetypes']
            elif isinstance(data, list):
                # YAML is a list of archetypes
                archetype_list = data
            else:
                # YAML has individual archetypes at top level
                archetype_list = [data] if isinstance(data, dict) else []

            for archetype_data in archetype_list:
                if not isinstance(archetype_data, dict):
                    continue

                archetype = RoleArchetype(archetype_data)
                key = f"{archetype.industry}_{archetype.title.lower().replace(' ', '_')}"
                archetypes[key] = archetype

            load_duration = time.time() - start_time
            self.logger.debug(f"Loaded {len(archetypes)} archetypes from {file_path.name} in {load_duration:.3f}s")

        except Exception as e:
            self.logger.error(f"Error loading archetypes from {file_path}: {e}")

        return archetypes

    def get_archetype(self, industry: str, role_title: str) -> Optional[RoleArchetype]:
        """Get a specific archetype by industry and role title"""
        key = f"{industry}_{role_title.lower().replace(' ', '_')}"
        return self.archetypes.get(key)

    def get_archetypes_by_industry(self, industry: str) -> List[RoleArchetype]:
        """Get all archetypes for a specific industry with caching."""
        import time

        # Check cache first
        if industry in self.industry_cache:
            cached_result = self.industry_cache[industry]
            self.logger.debug(f"Retrieved {len(cached_result)} archetypes for {industry} from cache")
            return cached_result

        # Not in cache, compute and store
        start_time = time.time()
        industry_archetypes = []
        for archetype in self.archetypes.values():
            if archetype.industry.lower() == industry.lower():
                industry_archetypes.append(archetype)

        # Cache the result
        self.industry_cache[industry] = industry_archetypes

        duration = time.time() - start_time
        self.logger.debug(f"Computed {len(industry_archetypes)} archetypes for {industry} in {duration:.3f}s")

        return industry_archetypes

    def search_archetypes(self, keywords: List[str]) -> List[RoleArchetype]:
        """Search archetypes by keywords in title, skills, or description"""
        import time

        start_time = time.time()
        matching_archetypes = []
        keywords_lower = [kw.lower() for kw in keywords]

        for archetype in self.archetypes.values():
            # Check if any keyword appears in the archetype
            text_to_search = (
                archetype.title.lower() +
                archetype.description.lower() +
                ' '.join(archetype.required_skills).lower() +
                ' '.join(archetype.preferred_skills).lower() +
                ' '.join(archetype.technologies).lower()
            )

            if any(keyword in text_to_search for keyword in keywords_lower):
                matching_archetypes.append(archetype)

        duration = time.time() - start_time
        self.logger.debug(f"Found {len(matching_archetypes)} matching archetypes in {duration:.3f}s")

        return matching_archetypes

    def validate_knowledge_base(self) -> Dict[str, Any]:
        """
        Validate the knowledge base for integrity and consistency.

        Returns:
            Dict with validation results including errors, warnings, and statistics
        """
        self.logger.info("Starting knowledge base validation...")

        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {
                'total_archetypes': 0,
                'by_industry': {},
                'missing_fields': 0,
                'duplicate_titles': []
            }
        }

        # Reload archetypes to ensure we're working with fresh data
        archetypes = self.load_archetypes()
        validation_results['statistics']['total_archetypes'] = len(archetypes)

        # Track titles by industry to detect duplicates
        titles_by_industry = {}

        for key, archetype in archetypes.items():
            # Check required fields
            if not archetype.title:
                validation_results['errors'].append(f"Archetype {key} missing title")
                validation_results['statistics']['missing_fields'] += 1

            if not archetype.industry:
                validation_results['errors'].append(f"Archetype {key} missing industry")
                validation_results['statistics']['missing_fields'] += 1

            if not archetype.description:
                validation_results['warnings'].append(f"Archetype {key} missing description")

            if not archetype.required_skills:
                validation_results['warnings'].append(f"Archetype {key} has no required skills")

            # Track industry statistics
            industry = archetype.industry
            if industry not in validation_results['statistics']['by_industry']:
                validation_results['statistics']['by_industry'][industry] = 0
            validation_results['statistics']['by_industry'][industry] += 1

            # Track titles for duplicate checking
            if industry not in titles_by_industry:
                titles_by_industry[industry] = []

            title_lower = archetype.title.lower()
            if title_lower in titles_by_industry[industry]:
                validation_results['statistics']['duplicate_titles'].append(
                    f"Duplicate title '{archetype.title}' in industry '{industry}'"
                )
            else:
                titles_by_industry[industry].append(title_lower)

        # Check for critical errors that make the KB invalid
        if validation_results['errors']:
            validation_results['valid'] = False

        self.logger.info(f"Knowledge base validation completed: {len(validation_results['errors'])} errors, {len(validation_results['warnings'])} warnings")

        return validation_results

    def update_knowledge_base_quarterly(self) -> bool:
        """
        Utility for quarterly updates to the knowledge base.

        This method would typically be called to refresh the knowledge base
        with updated role information, new technologies, or changed requirements.

        Returns:
            bool: True if update was successful, False otherwise
        """
        self.logger.info("Starting quarterly knowledge base update process...")

        try:
            # Validate current knowledge base before update
            validation_before = self.validate_knowledge_base()

            if not validation_before['valid']:
                self.logger.warning(f"Knowledge base has issues before update: {len(validation_before['errors'])} errors")

            # In a real implementation, this would:
            # 1. Fetch updated data from authoritative sources
            # 2. Merge new information with existing data
            # 3. Apply any transformation rules
            # 4. Validate the updated knowledge base

            # For now, just reload and validate again
            self.load_archetypes()
            validation_after = self.validate_knowledge_base()

            if validation_after['valid']:
                self.logger.info("Quarterly knowledge base update completed successfully")
                return True
            else:
                self.logger.error(f"Knowledge base update failed validation: {len(validation_after['errors'])} errors")
                return False

        except Exception as e:
            self.logger.error(f"Error during quarterly knowledge base update: {e}")
            return False


# Global loader instance
knowledge_base = RoleArchetypeLoader()


def get_role_archetype_loader() -> RoleArchetypeLoader:
    """Get the global role archetype loader instance"""
    return knowledge_base