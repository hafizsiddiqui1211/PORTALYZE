"""PII removal utilities for job role recommender"""

import re
from typing import Dict, List, Any, Union
import logging
from faker import Faker


class PIIAnonymizer:
    """Utility class for removing and anonymizing PII from profile data"""

    def __init__(self):
        self.fake = Faker()
        self.logger = logging.getLogger(__name__)

        # Regular expressions for PII detection
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        self.name_patterns = [
            # Basic name pattern - this is a simplified version
            # In a real implementation, you'd want more sophisticated NER
            re.compile(r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b'),
        ]
        self.location_patterns = [
            # Basic location pattern - again, simplified
            re.compile(r'\b([A-Z][a-z]+, [A-Z]{2})\b'),  # City, ST format
        ]

    def anonymize_text(self, text: str) -> str:
        """Anonymize PII in a text string"""
        if not text or not isinstance(text, str):
            return text

        anonymized_text = text

        # Anonymize emails
        emails = self.email_pattern.findall(anonymized_text)
        for email in emails:
            fake_email = self.fake.email()
            anonymized_text = anonymized_text.replace(email, fake_email)

        # Anonymize phone numbers
        phones = self.phone_pattern.findall(anonymized_text)
        for phone in phones:
            fake_phone = self.fake.phone_number()
            anonymized_text = anonymized_text.replace(phone, fake_phone)

        # Anonymize names (simplified approach)
        for pattern in self.name_patterns:
            names = pattern.findall(anonymized_text)
            for name in names:
                fake_name = self.fake.name()
                anonymized_text = anonymized_text.replace(name, fake_name)

        # Anonymize locations (simplified approach)
        for pattern in self.location_patterns:
            locations = pattern.findall(anonymized_text)
            for location in locations:
                fake_location = f"{self.fake.city()}, {self.fake.state_abbr()}"
                anonymized_text = anonymized_text.replace(location, fake_location)

        return anonymized_text

    def anonymize_profile_data(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize PII in a profile data dictionary"""
        anonymized_data = {}

        for key, value in profile_data.items():
            if isinstance(value, str):
                anonymized_data[key] = self.anonymize_text(value)
            elif isinstance(value, dict):
                anonymized_data[key] = self.anonymize_profile_data(value)
            elif isinstance(value, list):
                anonymized_data[key] = [
                    self.anonymize_profile_data(item) if isinstance(item, dict)
                    else self.anonymize_text(str(item)) if isinstance(item, str)
                    else item
                    for item in value
                ]
            else:
                anonymized_data[key] = value

        return anonymized_data

    def anonymize_company_names(self, text: str) -> str:
        """Anonymize company names in text"""
        # This is a simplified approach - in practice, you might want to use
        # a more sophisticated method like matching against a company database
        # or using NER models trained to identify company names
        anonymized_text = text
        # Look for common company name patterns (e.g., "Company Inc.", "Company LLC")
        company_pattern = re.compile(r'\b([A-Z][A-Za-z\s]+(?:Inc\.?|LLC|Ltd\.?|Corp\.?|Company))\b')
        companies = company_pattern.findall(anonymized_text)

        for company in companies:
            fake_company = self.fake.company()
            anonymized_text = anonymized_text.replace(company, fake_company)

        return anonymized_text

    def remove_pii_completely(self, text: str) -> str:
        """Remove PII from text instead of anonymizing"""
        cleaned_text = text

        # Remove emails
        cleaned_text = self.email_pattern.sub('[EMAIL_REMOVED]', cleaned_text)

        # Remove phone numbers
        cleaned_text = self.phone_pattern.sub('[PHONE_REMOVED]', cleaned_text)

        # Remove names (simplified)
        for pattern in self.name_patterns:
            cleaned_text = pattern.sub('[NAME_REMOVED]', cleaned_text)

        # Remove locations (simplified)
        for pattern in self.location_patterns:
            cleaned_text = pattern.sub('[LOCATION_REMOVED]', cleaned_text)

        # Remove company names
        company_pattern = re.compile(r'\b([A-Z][A-Za-z\s]+(?:Inc\.?|LLC|Ltd\.?|Corp\.?|Company))\b')
        cleaned_text = company_pattern.sub('[COMPANY_REMOVED]', cleaned_text)

        return cleaned_text


# Global anonymizer instance
anonymizer = PIIAnonymizer()


def get_anonymizer() -> PIIAnonymizer:
    """Get the global anonymizer instance"""
    return anonymizer