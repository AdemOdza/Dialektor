from uuid import UUID
from flask import Blueprint, jsonify, request
from users import userDIs

userRouter = Blueprint("users", __name__, url_prefix="/users")


@userRouter.route("/", methods=("GET", "POST"))
def usersResource():
    if request.method == "GET":
        return getUsers()
    elif request.method == "POST":
        # TODO: Add Argon2 hashing to password
        body = request.get_json(force=True)
        return createUser(body)
    return {"error": "Not Implemented"}, 501


def getUsers():
    users = userDIs.selectUsers()
    return jsonify([*map(lambda u: u.toJson(), users)])


def createUser(body: dict):
    errors: list[str] = []
    if body.get("username") is None:
        errors.append("username")
    if body.get("email") is None:
        errors.append("email")
    if body.get("password_hash") is None:
        errors.append("password_hash")

    if len(errors) > 0:
        return {
            "error": f'Missing required field{"s" if len(errors) > 1 else ""}: {", ".join(errors)}'
        }, 400

    try:
        result = userDIs.insertUser(
            username=body["username"],
            email=body["email"],
            passwordHash=body["password_hash"],
            defaultDialect=(
                UUID(body["default_dialect"]) if body.get("default_dialect") else None
            ),
        )
        if result is None:
            raise Exception("Error inserting user")

        return jsonify(result.toJson()), 200
    except Exception as e:
        print(
            f"Error inserting user into database: {str(e)}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500


@userRouter.route("/<id>", methods=("GET", "PATCH", "DELETE"))
def userByIdResource(id: UUID):
    user = userDIs.selectUserByID(id)

    if request.method == "DELETE":
        if user is not None:
            userDIs.deleteUser(id)
        return {"id": id}

    if user is None:
        return {"error": f"User with ID {id} not found."}, 404

    if request.method == "GET":
        return jsonify(user.toJson())
    elif request.method == "PATCH":
        body = request.get_json(force=True)
        return updateUser(id, user, body)

    return {"error": "Not Implemented"}, 501


def updateUser(id: UUID, current, body: dict):
    result = userDIs.updateUser(
        id=id,
        username=body.get("username") or current.username,
        email=body.get("email") or current.email,
        defaultDialect=(
            UUID(body["default_dialect"])
            if body.get("default_dialect")
            else current.defaultDialect
        ),
    )
    if result is None:
        return {"error": "Error updating user"}, 500

    return jsonify(result.toJson()), 200
