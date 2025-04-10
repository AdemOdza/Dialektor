from dataclasses import dataclass


@dataclass
class Script:
    name: str

    def toJson(self):
        return {"name": self.name}
