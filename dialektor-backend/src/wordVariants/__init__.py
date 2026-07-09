from dataclasses import dataclass
from uuid import UUID
from common import toJson


@dataclass
class WordVariant:
    id: UUID
    word: str
    baseWord: UUID
    dialect: UUID

    def toJson(self):
        return {
            "id": toJson(self.id),
            "word": self.word,
            "base_word": toJson(self.baseWord),
            "dialect": toJson(self.dialect),
        }
