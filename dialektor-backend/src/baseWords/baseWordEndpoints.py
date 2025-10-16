from uuid import UUID
from flask import Blueprint, request, jsonify
from baseWords import baseWordDIs

baseWordRouter = Blueprint("base_words", __name__, url_prefix="/base_words")


@baseWordRouter.route("/", methods=("GET", "POST"))
def baseWordsResource():
    if request.method == "GET":
        return getBaseWords()
    elif request.method == "POST":
        body = request.get_json(force=True)
        return createBaseWord(body)
    return {"error": "Not Implemented"}, 501


def getBaseWords():
    baseWords = baseWordDIs.selectBaseWords()
    result = [
        *map(
            lambda w: w.toJson(),
            baseWords,
        )
    ]
    return jsonify(result), 200


def createBaseWord(body: dict):
    errors: list[str] = []
    if body.get("word") is None:
        errors.append("word")

    if body.get("language_id") is None:
        errors.append("language_id")

    if len(errors) > 0:
        return {
            "error": f'Missing required field{"s" if len(errors) > 1 else ""}: {", ".join(errors)}'
        }, 400
    print("checkpoint 0", flush=True)
    try:
        print("checkpoint 1", flush=True)
        result = baseWordDIs.insertBaseWord(
            body["word"],
            UUID(body["language_id"]),
        )
        print("checkpoint 2", flush=True)
        if result is None:
            raise Exception("Error inserting base word")

        return jsonify(result.toJson()), 200
    except Exception as e:
        print(
            f"Error inserting base word into database: {str(e)}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500


@baseWordRouter.route("/<id>", methods=("GET", "DELETE", "PATCH"))
def baseWordIdResource(id: UUID):
    baseWord = baseWordDIs.selectBaseWord(id)
    if baseWord is None:
        return {"error": f"Base Word {id} not found."}, 404

    match request.method:
        case "GET":
            return jsonify(baseWord.toJson()), 200
        case "DELETE":
            return deleteBaseWord(id)
        case "PATCH":
            body = request.get_json(force=True)
            return updateBaseWord(id, body)
    return {"error": "Not Implemented"}, 501


def deleteBaseWord(id: UUID):
    result = baseWordDIs.deleteBaseWord(id)
    if result is None:
        print(f"error deleting base word {id}")

    return {"id": id}, 200


def updateBaseWord(id: UUID, body: dict = {}):
    baseWord = baseWordDIs.selectBaseWord(id)
    if baseWord is None:
        return {"error": f"Base Word {id} not found."}, 404

    result = baseWordDIs.updateBaseWord(
        id,
        body.get("word") or baseWord.word,
        body.get("language_id", baseWord.languageId),
    )

    if result is None:
        return {"error": f"Error updating Base Word {id}."}, 404

    return jsonify(result.toJson()), 200
