from uuid import UUID
from flask import Blueprint, jsonify, request
from languageToCountries import languageToCountryDIs

languageToCountryRouter = Blueprint(
    "language_countries", __name__, url_prefix="/language_countries"
)


@languageToCountryRouter.route("/", methods=("GET", "POST", "PATCH", "DELETE"))
def languageCountriesResource():
    if request.method == "GET":
        return getLanguageCountries()
    elif request.method == "POST":
        body = request.get_json(force=True)
        return createLanguageCountry(body)
    elif request.method == "PATCH":
        body = request.get_json(force=True)
        return updateLanguageCountry(body)
    elif request.method == "DELETE":
        body = request.get_json(force=True)
        return deleteLanguageCountry(body)
    return {"error": "Not Implemented"}, 501


def getLanguageCountries():
    links = languageToCountryDIs.selectLanguageToCountries()
    return jsonify([*map(lambda l: l.toJson(), links)])


def createLanguageCountry(body: dict):
    errors: list[str] = []
    if body.get("country_id") is None:
        errors.append("country_id")
    if body.get("language_id") is None:
        errors.append("language_id")

    if len(errors) > 0:
        return {
            "error": f'Missing required field{"s" if len(errors) > 1 else ""}: {", ".join(errors)}'
        }, 400

    try:
        result = languageToCountryDIs.insertLanguageToCountry(
            countryId=UUID(body["country_id"]),
            languageId=UUID(body["language_id"]),
            official=body.get("official", False),
        )
        if result is None:
            raise Exception("Error inserting language-country link")

        return jsonify(result.toJson()), 200
    except Exception as e:
        print(
            f"Error inserting language-country link into database: {str(e)}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500


def updateLanguageCountry(body: dict):
    errors: list[str] = []
    if body.get("country_id") is None:
        errors.append("country_id")
    if body.get("language_id") is None:
        errors.append("language_id")
    if body.get("official") is None:
        errors.append("official")

    if len(errors) > 0:
        return {
            "error": f'Missing required field{"s" if len(errors) > 1 else ""}: {", ".join(errors)}'
        }, 400

    result = languageToCountryDIs.updateLanguageToCountry(
        countryId=UUID(body["country_id"]),
        languageId=UUID(body["language_id"]),
        official=body["official"],
    )
    if result is None:
        return {"error": "Language-country link not found"}, 404

    return jsonify(result.toJson()), 200


def deleteLanguageCountry(body: dict):
    errors: list[str] = []
    if body.get("country_id") is None:
        errors.append("country_id")
    if body.get("language_id") is None:
        errors.append("language_id")

    if len(errors) > 0:
        return {
            "error": f'Missing required field{"s" if len(errors) > 1 else ""}: {", ".join(errors)}'
        }, 400

    languageToCountryDIs.deleteLanguageToCountry(
        countryId=UUID(body["country_id"]),
        languageId=UUID(body["language_id"]),
    )
    return {
        "country_id": body["country_id"],
        "language_id": body["language_id"],
    }
