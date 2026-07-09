from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from common import toJson


@dataclass
class SessionToken:
    id: UUID
    userId: UUID
    token: str
    expires: datetime

    def toJson(self):
        return {
            "id": toJson(self.id),
            "user_id": toJson(self.userId),
            "token": self.token,
            "expires": toJson(self.expires),
        }
