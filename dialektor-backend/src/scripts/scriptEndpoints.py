from uuid import UUID
from flask import Blueprint, request
from common import toJson
from scripts import scriptDIs

scriptRouter = Blueprint("scripts", __name__, url_prefix="/scripts")


@scriptRouter.route("/", methods=("GET", "POST"))
def scriptResource():
    if request.method == "GET":
        return getScripts()
    elif request.method == "POST":
        body = request.get_json(force=True)
        return createScript(body)
    return {"error": "Not Implemented"}, 501


def getScripts():
    result = scriptDIs.selectScripts()
    return [*map(lambda s: s.toJson(), result)]


def createScript(body: dict):
    if body.get("name") is None:
        return {"error": 'Error creating script: "name" field missing'}, 400

    try:
        return scriptDIs.insertScript(body["name"]).toJson()
    except Exception as e:
        print(
            f"Error inserting script into database: {e.message if hasattr(e, 'message') else e}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500


@scriptRouter.delete("/<name>")
def deleteScript(name: str):
    try:
        scriptDIs.deleteScript(name)
        return {"name": name}
    except Exception as e:
        print(
            f"Error deleting script: {e.message if hasattr(e, 'message') else e}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500
