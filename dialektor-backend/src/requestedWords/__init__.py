from dataclasses import dataclass
from uuid import UUID
from common import toJson


@dataclass
class RequestedWord:
    id: UUID
    word: str
    variant: str | None
    country: UUID
    region: UUID | None
    requestedBy: str

    def toJson(self):
        return {
            "id": toJson(self.id),
            "word": self.word,
            "variant": self.variant,
            "country": toJson(self.country),
            "region": toJson(self.region) if self.region else None,
            "requested_by": self.requestedBy,
        }
