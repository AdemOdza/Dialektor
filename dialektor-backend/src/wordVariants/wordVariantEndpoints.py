from uuid import UUID
from flask import Blueprint, jsonify, request
from wordVariants import wordVariantDIs

wordVariantRouter = Blueprint("word_variants", __name__, url_prefix="/word_variants")


@wordVariantRouter.route("/", methods=("GET", "POST"))
def wordVariantsResource():
    if request.method == "GET":
        return getWordVariants()
    elif request.method == "POST":
        body = request.get_json(force=True)
        return createWordVariant(body)
    return {"error": "Not Implemented"}, 501


def getWordVariants():
    variants = wordVariantDIs.selectWordVariants()
    return jsonify([*map(lambda v: v.toJson(), variants)])


def createWordVariant(body: dict):
    errors: list[str] = []
    if body.get("word") is None:
        errors.append("word")
    if body.get("base_word") is None:
        errors.append("base_word")
    if body.get("dialect") is None:
        errors.append("dialect")

    if len(errors) > 0:
        return {
            "error": f'Missing required field{"s" if len(errors) > 1 else ""}: {", ".join(errors)}'
        }, 400

    try:
        result = wordVariantDIs.insertWordVariant(
            word=body["word"],
            baseWord=UUID(body["base_word"]),
            dialect=UUID(body["dialect"]),
        )
        if result is None:
            raise Exception("Error inserting word variant")

        return jsonify(result.toJson()), 200
    except Exception as e:
        print(
            f"Error inserting word variant into database: {str(e)}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500


@wordVariantRouter.route("/<id>", methods=("GET", "PATCH", "DELETE"))
def wordVariantByIdResource(id: UUID):
    variant = wordVariantDIs.selectWordVariant(id)

    if request.method == "DELETE":
        if variant is not None:
            wordVariantDIs.deleteWordVariant(id)
        return {"id": id}

    if variant is None:
        return {"error": f"Word variant with ID {id} not found."}, 404

    if request.method == "GET":
        return jsonify(variant.toJson())
    elif request.method == "PATCH":
        body = request.get_json(force=True)
        return updateWordVariant(id, variant, body)

    return {"error": "Not Implemented"}, 501


def updateWordVariant(id: UUID, current, body: dict):
    result = wordVariantDIs.updateWordVariant(
        id=id,
        word=body.get("word") or current.word,
        baseWord=UUID(body["base_word"]) if body.get("base_word") else current.baseWord,
        dialect=UUID(body["dialect"]) if body.get("dialect") else current.dialect,
    )
    if result is None:
        return {"error": "Error updating word variant"}, 500

    return jsonify(result.toJson()), 200
