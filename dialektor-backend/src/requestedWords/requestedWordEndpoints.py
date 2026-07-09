from uuid import UUID
from flask import Blueprint, jsonify, request
from requestedWords import requestedWordDIs

requestedWordRouter = Blueprint(
    "requested_words", __name__, url_prefix="/requested_words"
)


@requestedWordRouter.route("/", methods=("GET", "POST"))
def requestedWordsResource():
    if request.method == "GET":
        return getRequestedWords()
    elif request.method == "POST":
        body = request.get_json(force=True)
        return createRequestedWord(body)
    return {"error": "Not Implemented"}, 501


def getRequestedWords():
    words = requestedWordDIs.selectRequestedWords()
    return jsonify([*map(lambda w: w.toJson(), words)])


def createRequestedWord(body: dict):
    errors: list[str] = []
    if body.get("word") is None:
        errors.append("word")
    if body.get("country") is None:
        errors.append("country")
    if body.get("requested_by") is None:
        errors.append("requested_by")

    if len(errors) > 0:
        return {
            "error": f'Missing required field{"s" if len(errors) > 1 else ""}: {", ".join(errors)}'
        }, 400

    try:
        result = requestedWordDIs.insertRequestedWord(
            word=body["word"],
            country=UUID(body["country"]),
            requestedBy=body["requested_by"],
            variant=body.get("variant"),
            region=UUID(body["region"]) if body.get("region") else None,
        )
        if result is None:
            raise Exception("Error inserting requested word")

        return jsonify(result.toJson()), 200
    except Exception as e:
        print(
            f"Error inserting requested word into database: {str(e)}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500


@requestedWordRouter.route("/<id>", methods=("GET", "PATCH", "DELETE"))
def requestedWordByIdResource(id: UUID):
    word = requestedWordDIs.selectRequestedWord(id)

    if request.method == "DELETE":
        if word is not None:
            requestedWordDIs.deleteRequestedWord(id)
        return {"id": id}

    if word is None:
        return {"error": f"Requested word with ID {id} not found."}, 404

    if request.method == "GET":
        return jsonify(word.toJson())
    elif request.method == "PATCH":
        body = request.get_json(force=True)
        return updateRequestedWord(id, word, body)

    return {"error": "Not Implemented"}, 501


def updateRequestedWord(id: UUID, current, body: dict):
    result = requestedWordDIs.updateRequestedWord(
        id=id,
        word=body.get("word") or current.word,
        variant=body.get("variant", current.variant),
        country=UUID(body["country"]) if body.get("country") else current.country,
        region=UUID(body["region"]) if body.get("region") else current.region,
        requestedBy=body.get("requested_by") or current.requestedBy,
    )
    if result is None:
        return {"error": "Error updating requested word"}, 500

    return jsonify(result.toJson()), 200
