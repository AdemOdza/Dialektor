import datetime
import os
from uuid import UUID


def getEnv(key: str, default: str = None):
    return os.environ.get(key, default)


def toJson(val):
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
