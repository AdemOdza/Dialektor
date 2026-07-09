from dataclasses import dataclass
from uuid import UUID
from common import toJson


@dataclass
class User:
    id: UUID
    username: str
    email: str
    defaultDialect: UUID | None
    passwordHash: str

    def toJson(self):
        return {
            "id": toJson(self.id),
            "username": self.username,
            "email": self.email,
            "default_dialect": (
                toJson(self.defaultDialect) if self.defaultDialect else None
            ),
        }
