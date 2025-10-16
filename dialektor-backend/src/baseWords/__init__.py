from dataclasses import dataclass
import uuid
from common import toJson


@dataclass
class BaseWord:
    id: uuid.UUID
    word: str
    languageId: uuid.UUID

    def toJson(self):
        return {
            "id": toJson(self.id),
            "word": self.word,
            "language_id": toJson(self.languageId),
        }
