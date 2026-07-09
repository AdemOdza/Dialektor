from uuid import UUID
from datetime import datetime
from flask import Blueprint, jsonify, request
from sessionTokens import sessionTokenDIs

sessionTokenRouter = Blueprint("session_tokens", __name__, url_prefix="/session_tokens")


# TODO: When to check for and delete expired tokens efficiently?
@sessionTokenRouter.route("/", methods=("GET", "POST"))
def sessionTokensResource():
    if request.method == "GET":
        return getSessionTokens()
    elif request.method == "POST":
        body = request.get_json(force=True)
        return createSessionToken(body)
    return {"error": "Not Implemented"}, 501


def getSessionTokens():
    tokens = sessionTokenDIs.selectSessionTokens()
    return jsonify([*map(lambda t: t.toJson(), tokens)])


def createSessionToken(body: dict):
    errors: list[str] = []
    if body.get("user_id") is None:
        errors.append("user_id")
    if body.get("token") is None:
        errors.append("token")
    if body.get("expires") is None:
        errors.append("expires")

    if len(errors) > 0:
        return {
            "error": f'Missing required field{"s" if len(errors) > 1 else ""}: {", ".join(errors)}'
        }, 400

    try:
        result = sessionTokenDIs.insertSessionToken(
            userId=UUID(body["user_id"]),
            token=body["token"],
            expires=datetime.fromisoformat(body["expires"]),
        )
        if result is None:
            raise Exception("Error inserting session token")

        return jsonify(result.toJson()), 200
    except Exception as e:
        print(
            f"Error inserting session token into database: {str(e)}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500


@sessionTokenRouter.route("/<id>", methods=("GET", "DELETE"))
def sessionTokenByIdResource(id: UUID):
    token = sessionTokenDIs.selectSessionToken(id)

    if request.method == "DELETE":
        if token is not None:
            sessionTokenDIs.deleteSessionToken(id)
        return {"id": id}

    if token is None:
        return {"error": f"Session token with ID {id} not found."}, 404

    if request.method == "GET":
        return jsonify(token.toJson())

    return {"error": "Not Implemented"}, 501
