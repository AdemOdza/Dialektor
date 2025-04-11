from uuid import UUID
from flask import Blueprint, request
from common import toJson
from languages import languageDIs


languageRouter = Blueprint("languages", __name__, url_prefix="/languages")


@languageRouter.route("/", methods=("GET", "POST"))
def languageResource():
    if request.method == "GET":
        return getLanguages()
    elif request.method == "POST":
        body = request.get_json(force=True)
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
