from uuid import UUID
from flask import Blueprint, request
from common import toJson
from countries import countryDIs

countryRouter = Blueprint("countries", __name__, url_prefix="/countries")


@countryRouter.route("/", methods=("GET", "POST"))
def countriesResource():
    if request.method == "GET":
        return getCountries()
    elif request.method == "POST":
        body = request.get_json(force=True)
        return createCountry(body)
    return {"error": "Not Implemented"}, 501


def getCountries():
    countries = countryDIs.selectCountries()
    result = [*map(lambda country: {"id": country.id, "name": country.name}, countries)]
    return toJson(result)


def createCountry(body: dict):
    if body.get("name") is None:
        return {"error": 'Error creating country: "name" field missing'}, 400

    try:
        return countryDIs.insertCountry(body["name"]).toJson()
    except Exception as e:
        print(
            f"Error inserting country into database: {e.message if hasattr(e, 'message') else e}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500


@countryRouter.route("/<id>", methods=("GET", "PATCH", "DELETE"))
def countryByIdResource(id: UUID):
    if request.method == "GET":
        return getCountry(id)
    elif request.method == "PATCH":
        body = request.get_json(force=True)

        if body.get("name") is None:
            return {"error": 'Error creating country: "name" field missing'}, 400

        return updateCountry(id, body)
    elif request.method == "DELETE":
        return deleteCountry(id)

    return {"error": "Not Implemented"}, 501


def getCountry(id: UUID):
    country = countryDIs.selectCountryByID(id)
    if country is None:
        return {"error": f"Country with ID {id} not found."}, 404

    return {"id": country.id, "name": country.name}


def updateCountry(id: UUID, body: dict):
    country = countryDIs.selectCountryByID(id)
    if country is None:
        return {"error": f"Country with ID {id} not found."}, 404

    try:
        result = countryDIs.updateCountry(id, body.get("name"))
        return result.toJson(), 200
    except Exception as e:
        print(
            f"Error updating country: {e.message if hasattr(e, 'message') else e}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500


def deleteCountry(id: UUID):
    try:
        countryDIs.deleteCountry(id)
        return {"id": id}, 200
    except Exception as e:
        print(
            f"Error deleting country: {e.message if hasattr(e, 'message') else e}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500
