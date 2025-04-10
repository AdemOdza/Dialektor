from dataclasses import dataclass
import uuid
from common import toJson


@dataclass
class Country:
    id: uuid.UUID
    name: str

    def toJson(self):
        return {"id": toJson(self.id), "name": self.name}
