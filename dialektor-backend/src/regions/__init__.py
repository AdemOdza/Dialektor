from dataclasses import dataclass
from uuid import UUID
from common import toJson


@dataclass
class Region:
    id: UUID
    country: UUID
    name: str

    def toJson(self):
        return {
            "id": toJson(self.id),
            "country": toJson(self.country),
            "name": self.name,
        }
