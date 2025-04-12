from dataclasses import dataclass
from uuid import UUID
from common import toJson


@dataclass
class Language:
    id: UUID
    name: str
    script: str

    def toJson(self):
        return {
            "id": toJson(self.id),
            "name": self.name,
            "script": self.script,
        }
