from uuid import UUID
from flask import Blueprint, request
from languages import languageDIs
from dialects import dialectDIs
from common import toJson

languageRouter = Blueprint("languages", __name__, url_prefix="/languages")


@languageRouter.route("/", methods=("GET", "POST"))
def languageResource():
    if request.method == "GET":
        return getLanguages()
    elif request.method == "POST":
        body = request.get_json(force=True)
        if body is None:
            return {"error": "Missing Body"}, 400
        return createLanguage(body)
    return {"error": "Not Implemented"}, 501


def getLanguages():
    return [*map(lambda x: x.toJson(), languageDIs.selectLanguages())]


def createLanguage(body: dict):
    missingFields = []
    if body.get("name") is None:
        missingFields.append("name")
    if body.get("script") is None:
        missingFields.append("script")

    if len(missingFields) > 0:
        return {"error": f"Missing required fields: {','.join(missingFields)}"}, 400

    return languageDIs.insertLanguage(
        name=body.get("name"), script=body.get("script")
    ).toJson()


@languageRouter.route("/<id>", methods=("GET", "PATCH", "DELETE"))
def languageByIdResource(id: UUID):
    language = languageDIs.selectLanguageByID(id)
    if language is None:
        return {"error": f"Language {id} not found."}, 404

    if request.method == "PATCH":
        body = request.get_json(force=True)
        return updateLanguage(id, body)
    elif request.method == "DELETE":
        return {"id": languageDIs.deleteLanguage(id)}
    elif request.method == "GET":
        return languageDIs.selectLanguageByID(id).toJson()
    return {"error": "Not Implemented"}, 501


def updateLanguage(id: UUID, body: dict):
    oldLanguage = languageDIs.selectLanguageByID(id)

    return languageDIs.updateLanguage(
        id,
        name=body.get("name") or oldLanguage.name,
        script=body.get("script") or oldLanguage.script,
    ).toJson()


@languageRouter.route("/<id>/dialects", methods=("GET", "POST"))
def languageDialectsResource(id: UUID):
    language = languageDIs.selectLanguageByID(id)
    if language is None:
        return {"error": f"Language {id} not found."}, 404

    if request.method == "GET":
        return getLanguageDialects(id)
    elif request.method == "POST":
        body = request.get_json(force=True)
        if body is None:
            return {"error": "Missing Body"}, 400
        return createLanguageDialect(id, body)

    return {"error": "Not Implemented"}, 501


def getLanguageDialects(languageId: UUID):
    return [
        *map(
            lambda lang: lang.toJson(), dialectDIs.selectDialectsByLanguage(languageId)
        )
    ]


def createLanguageDialect(languageId: UUID, body: dict):
    if body.get("name") is None:
        return {"error": 'Missing required field: "name"'}, 400

    return dialectDIs.insertDialect(languageId, body["name"]).toJson()


@languageRouter.route(
    "/<languageId>/dialects/<dialectId>", methods=("PATCH", "DELETE", "GET")
)
def languageDialectResource(languageId: UUID, dialectId: UUID):
    print("TESTINETIUAHEFIJHDSBGOFJARKNBFDSUGHIFGFEAJR", flush=True)
    lang = languageDIs.selectLanguageByID(languageId)
    if lang is None:
        return {"error": f"Language not found"}, 404
    print(lang.toJson(), flush=True)
    if request.method == "PATCH":
        body = request.get_json(force=True)
        if body is None:
            return {"error": "Missing Body"}, 400
        return updateLanguageDialect(languageId, dialectId, body)
    elif request.method == "DELETE":
        return dialectDIs.deleteDialect(dialectId, languageId).toJson()
    elif request.method == "GET":
        result = dialectDIs.selectDialectById(dialectId)
        if result is None or str(result.languageId) != str(languageId):
            return {"error": f"Dialect not found"}, 404

        return result.toJson()
    return {"error": "Not Implemented"}, 501


def updateLanguageDialect(languageId: UUID, dialectId: UUID, body: dict):
    oldDialect = dialectDIs.selectDialectById(dialectId)

    if oldDialect is None or str(oldDialect.languageId) != str(languageId):
        return {"error": f"Dialect not found"}, 404

    return dialectDIs.updateDialect(
        dialectId, languageId, body.get("name", oldDialect.name)
    ).toJson()
