from dataclasses import dataclass
from uuid import UUID
from common import toJson


@dataclass
class Dialect:
    id: UUID
    name: str
    languageId: UUID

    def toJson(self):
        return {
            "id": toJson(self.id),
            "name": self.name,
            "languageId": toJson(self.languageId),
        }
