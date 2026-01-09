# Quickstart: Job Role Recommender

## Prerequisites

- Python 3.11+
- pip package manager
- Phase 1 (Resume Analyzer Core) installed and configured
- Phase 2 (Portfolio + LinkedIn / GitHub Integration) installed and configured
- SpeckitPlus/Claude CLI configured

## Installation

### 1. Install Additional Dependencies

```bash
pip install -r requirements.txt
```

New dependencies for Phase 3:
```txt
# Data validation
pydantic>=2.5.0

# YAML processing for knowledge base
pyyaml>=6.0.0

# Anonymization utilities
faker>=22.0.0  # For generating anonymous replacements
```

### 2. Environment Configuration

Add to your `.env` file:
```env
# Phase 3 Configuration
ROLE_INFERENCE_TIMEOUT=30        # Max seconds for role inference
MAX_ROLES_PER_INDUSTRY=5         # Maximum roles to recommend
MIN_ROLES_PER_INDUSTRY=2         # Minimum roles to recommend
CONSENT_STORAGE_HOURS=24         # Hours before auto-deletion
KNOWLEDGE_BASE_PATH=src/knowledge/  # Path to role archetypes
```

### 3. Initialize Knowledge Base

The knowledge base YAML files should be placed in `src/knowledge/industries/`:
```bash
mkdir -p src/knowledge/industries
```

Example industry file (`src/knowledge/industries/ai_ml.yaml`):
```yaml
industry: AI/ML
roles:
  - title: ML Engineer
    description: Builds and deploys machine learning models
    required_skills:
      - name: Python
        importance: CORE
      - name: TensorFlow/PyTorch
        importance: CORE
      - name: MLOps
        importance: PREFERRED
    seniority_indicators:
      junior: ["academic projects", "coursework", "bootcamp"]
      mid: ["production models", "team collaboration", "model optimization"]
      senior: ["architecture design", "team leadership", "strategic decisions"]
```

## Running the Application

### Development Mode
```bash
streamlit run src/main.py
```

The application will be available at `http://localhost:8501`

## Usage

### 1. Complete Phase 1 & 2 Analysis
- Upload your resume (Phase 1)
- Add your LinkedIn, GitHub, and Portfolio URLs (Phase 2)
- Complete the analysis for both phases

### 2. Select Target Industries
Navigate to the "Role Recommendations" tab:
- Select one or more industries (AI/ML, Software Engineering, Data, etc.)
- Optionally select specializations within industries
- Click "Get Role Recommendations"

### 3. Review Recommendations
For each recommended role, you'll see:
- **Role Title** with seniority level (Junior/Mid/Senior)
- **Why This Role Fits**: Justification bullets
- **Gap Analysis**: Missing skills and improvement suggestions
- **Confidence Indicator**: High/Medium/Low based on data completeness

### 4. Consent for Storage (Optional)
- If prompted, you can consent to temporary storage
- This enables improved recommendations if you return within 24 hours
- Data is anonymized and auto-deleted after 24 hours

## API Usage Examples

### Signal Aggregation
```python
from src.services.signal_aggregator import SignalAggregator

aggregator = SignalAggregator()
profile_signals = aggregator.aggregate(
    resume_analysis=phase1_result,
    profile_analyses=phase2_results
)
print(profile_signals.aggregated_skills)
```

### Role Inference
```python
from src.services.role_inferencer import RoleInferencer

inferencer = RoleInferencer()
recommendations = inferencer.infer_roles(
    profile_signals=profile_signals,
    industries=["AI/ML", "Software Engineering"]
)
for role in recommendations.roles:
    print(f"{role.role_title} ({role.seniority_level}): {role.fit_score}%")
```

### Seniority Detection
```python
from src.services.seniority_detector import SeniorityDetector

detector = SeniorityDetector()
seniority = detector.detect(profile_signals)
print(f"Detected seniority: {seniority}")  # JUNIOR, MID, or SENIOR
```

### Gap Analysis
```python
from src.services.gap_analyzer import GapAnalyzer

analyzer = GapAnalyzer()
gaps = analyzer.analyze(role_archetype, profile_signals)
for gap in gaps.missing_skills:
    print(f"{gap.skill_name}: {gap.importance_level}")
```

## Testing

### Run Unit Tests
```bash
pytest tests/unit/test_services/test_signal_aggregator.py
pytest tests/unit/test_services/test_role_inferencer.py
pytest tests/unit/test_services/test_seniority_detector.py
pytest tests/unit/test_services/test_gap_analyzer.py
```

### Run Integration Tests
```bash
pytest tests/integration/test_role_recommendation_flow.py
```

### Run All Tests
```bash
pytest tests/ -v
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Role inference timeout | Check Claude API connectivity; increase `ROLE_INFERENCE_TIMEOUT` |
| No roles recommended | Ensure Phase 1 & 2 analyses are complete |
| Low confidence warning | Add more profile data (LinkedIn, GitHub, Portfolio) |
| Knowledge base not found | Verify `KNOWLEDGE_BASE_PATH` and YAML files exist |

### Handling Minimal Data

When profile data is sparse:
- System provides best-effort recommendations
- Confidence indicator shows "Low"
- Suggestions for improving data completeness are displayed
- Gap analysis may be limited

### Handling Conflicting Signals

When profile signals suggest multiple directions:
- Multiple role paths are presented
- Each path explains which signals support it
- User can explore different career directions