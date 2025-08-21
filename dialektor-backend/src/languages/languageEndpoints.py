from typing import get_args
from uuid import UUID
from flask import Blueprint, request
from languages import validScripts, languageDIs
from dialects import dialectDIs
from common import toJson

languageRouter = Blueprint("languages", __name__, url_prefix="/languages")


@languageRouter.route("/", methods=("GET", "POST"))
def languageResource():
    if request.method == "GET":
        return getLanguages()
    elif request.method == "POST":
        body = request.get_json(force=True)  # , silent=True)

        # Not getting triggered?
        if body is None or body == {}:
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

    if body.get("script") not in validScripts:
        return {"error": f"Invalid Script"}, 400

    result = languageDIs.insertLanguage(name=body["name"], script=body["script"])

    if result is None:
        return {"error": "Error creating language"}, 500

    return result.toJson()


@languageRouter.route("/<id>", methods=("GET", "PATCH", "DELETE"))
def languageByIdResource(id: UUID):
    language = languageDIs.selectLanguageByID(id)

    if request.method == "DELETE":
        if language is not None:
            languageDIs.deleteLanguage(id)
        return {"id": id}

    if request.method == "PATCH":
        body = request.get_json(force=True)
        return updateLanguage(id, body)
    elif request.method == "GET":
        if language is None:
            return {"error": f"Language {id} not found."}, 404
        return language.toJson()
    return {"error": "Not Implemented"}, 501


def updateLanguage(id: UUID, body: dict):
    oldLanguage = languageDIs.selectLanguageByID(id)

    if oldLanguage is None:
        return {"error": f"Language {id} not found."}, 404

    if body.get("script") is not None and body.get("script") not in validScripts:
        return {"error": f"Invalid Script"}, 400

    result = languageDIs.updateLanguage(
        id,
        name=body.get("name") or oldLanguage.name,
        script=body.get("script") or oldLanguage.script,
    )
    if result is None:
        return {"error": "Error updating language"}, 500

    return result.toJson()


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

    result = dialectDIs.insertDialect(languageId, body["name"])
    if result is None:
        return {"error": "Error creating dialect"}, 500
    return result.toJson()


@languageRouter.route(
    "/<languageId>/dialects/<dialectId>", methods=("PATCH", "DELETE", "GET")
)
def languageDialectResource(languageId: UUID, dialectId: UUID):
    lang = languageDIs.selectLanguageByID(languageId)
    if lang is None:
        return {"error": f"Language not found"}, 404

    if request.method == "PATCH":
        body = request.get_json(force=True)
        if body is None:
            return {"error": "Missing Body"}, 400
        return updateLanguageDialect(languageId, dialectId, body)
    elif request.method == "DELETE":
        result = dialectDIs.deleteDialect(dialectId, languageId)
        if result is None:
            print("Error deleting dialect", flush=True)
        return {"id": dialectId, "languageId": languageId}
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

    result = dialectDIs.updateDialect(
        dialectId, languageId, body.get("name", oldDialect.name)
    )
    if result is None:
        return {"error", "Error updating dialect"}, 500

    return result.toJson()
