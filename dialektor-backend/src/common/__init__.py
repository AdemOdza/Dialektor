import datetime
import os
import dataclasses
from typing import Optional
from uuid import UUID


def getEnv(key: str, default: Optional[str] = None):
    return os.environ.get(key, default)


def toJson(val):
    if dataclasses.is_dataclass(val):
        # If the dataclass instance has a toJson method, use it
        if hasattr(val, "toJson") and callable(getattr(val, "toJson")):
            return val.toJson()  # type: ignore
        raise Exception("toJson not implemented in dataclass.")

    match val:
        case datetime.datetime():
            return val.isoformat()
        case UUID():
            return str(val)
        case dict():
            return {key: toJson(value) for key, value in val.items()}
        case list() | tuple():
            return [toJson(item) for item in val]
        case int() | str() | float() | bool() | None:
            return val
        case _:
            raise Exception(f"Unhandled JSON Type: {type(val)}")
