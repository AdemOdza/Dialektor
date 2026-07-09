from dataclasses import dataclass
from uuid import UUID
from common import toJson


@dataclass
class LanguageToCountry:
    countryId: UUID
    languageId: UUID
    official: bool

    def toJson(self):
        return {
            "country_id": toJson(self.countryId),
            "language_id": toJson(self.languageId),
            "official": self.official,
        }
