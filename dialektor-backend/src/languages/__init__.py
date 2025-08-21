from dataclasses import dataclass
from typing import Literal
from uuid import UUID
from common import toJson

validScripts = ["LATIN", "CYRILLIC", "GREEK", "ARABIC"]
Scripts = Literal["LATIN", "CYRILLIC", "GREEK", "ARABIC"]


@dataclass
class Language:
    id: UUID
    name: str
    script: Scripts

    def toJson(self):
        return {
            "id": toJson(self.id),
            "name": self.name,
            "script": self.script,
        }
