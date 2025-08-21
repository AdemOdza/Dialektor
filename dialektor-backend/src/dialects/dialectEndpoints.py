from uuid import UUID
from flask import Blueprint, request
from dialects import dialectDIs
from common import toJson


dialectRouter = Blueprint("dialects", __name__, url_prefix="/dialects")


@dialectRouter.get("/")
def getDialects():
    dialects = dialectDIs.selectDialects()
    return [*map(lambda dialect: dialect.toJson(), dialects)]


@dialectRouter.get("/<id>")
def getDialect(id: UUID):
    dialect = dialectDIs.selectDialectById(id)

    if dialect is None:
        return {"error": f"Dialect with ID {id} not found."}, 404

    return dialect.toJson()
