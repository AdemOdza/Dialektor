from uuid import UUID
from flask import Blueprint, jsonify, request
from common import toJson
from countries import countryDIs
from regions import Region, regionDIs

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
    result = [
        *map(
            lambda country: {"id": toJson(country.id), "name": toJson(country.name)},
            countries,
        )
    ]
    return jsonify(toJson(result))


def createCountry(body: dict):
    if body.get("name") is None:
        return {"error": 'Error creating country: "name" field missing'}, 400

    try:
        result = countryDIs.insertCountry(body["name"])
        if result is None:
            raise Exception("Error inserting country")

        return result.toJson()
    except Exception as e:
        print(
            f"Error inserting country into database: {str(e)}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500


@countryRouter.route("/<id>", methods=("GET", "PATCH", "DELETE"))
def countryByIdResource(id: UUID):
    existingCountry = countryDIs.selectCountryByID(id)
    if request.method == "DELETE":
        if existingCountry is not None:
            deleteCountry(id)
        return {"id": id}

    if request.method == "GET":
        if existingCountry is None:
            return {"error": f"Country with ID {id} not found."}, 404
        return jsonify(existingCountry.toJson())
    elif request.method == "PATCH":
        body = request.get_json(force=True)
        return updateCountry(id, body)

    return {"error": "Not Implemented"}, 501


# def getCountry(id: UUID):
#     country = countryDIs.selectCountryByID(id)
#     if country is None:
#         return toJson({"error": f"Country with ID {id} not found."}), 404
#     return country.toJson()


def updateCountry(id: UUID, body: dict):
    country = countryDIs.selectCountryByID(id)
    if country is None:
        return {"error": f"Error updating: country with ID {id} not found."}, 404

    try:
        result = countryDIs.updateCountry(id, body.get("name", country.name))
        if result is None:
            raise Exception("Error updating country")

        return jsonify(result.toJson()), 200
    except Exception as e:
        print(
            f"Error updating country: {str(e)}",
            flush=True,
        )
        return {"error": "Internal Server Error"}, 500


def deleteCountry(id: UUID):
    try:
        countryDIs.deleteCountry(id)
    except Exception as e:
        print(
            f"Error deleting country: {str(e)}",
            flush=True,
        )


@countryRouter.route("/<countryId>/regions", methods=("GET", "POST"))
def countryRegionsResource(countryId: UUID):
    country = countryDIs.selectCountryByID(countryId)
    if country is None:
        return {"error": f"Country with ID {id} not found."}, 404

    if request.method == "GET":
        return getCountryRegions(countryId)
    elif request.method == "POST":
        body = request.get_json(force=True)
        return createCountryRegion(countryId, body)

    return {"error": "Not Implemented"}, 501


def getCountryRegions(countryId: UUID):
    result = regionDIs.selectRegionsByCountryId(countryId)
    return [*map(lambda r: r.toJson(), result)]


def createCountryRegion(countryId: UUID, body: dict):
    if body.get("name") is None:
        return {"error": 'Missing required field "name".'}, 400

    result = regionDIs.insertRegion(countryId=countryId, name=body["name"])
    if result is None:
        return {"error": "Error adding region to country"}, 500

    return result.toJson()


@countryRouter.route(
    "/<countryId>/regions/<regionId>", methods=("GET", "PATCH", "DELETE")
)
def countryRegionResource(countryId: UUID, regionId: UUID):
    country = countryDIs.selectCountryByID(countryId)
    if country is None:
        return {"error": f"Country with ID {countryId} not found."}, 404

    region = regionDIs.selectRegionById(regionId)
    if request.method == "DELETE":
        if region is not None:
            if regionDIs.deleteRegion(regionId) is None:
                print(
                    f"Error deleting region {regionId} from country {countryId}",
                    flush=True,
                )
        return {"countryId": countryId, "regionId": regionId}

    if region is None or str(country.id) != str(region.country):
        return {
            "error": f"Region with ID {regionId} not found for country {countryId}."
        }, 404

    if request.method == "GET":
        return region.toJson()
    elif request.method == "PATCH":
        body = request.get_json(force=True)
        return updateCountryRegion(countryId, regionId, body)

    return {"error": "Not Implemented"}, 501


def updateCountryRegion(countryId: UUID, regionId: UUID, body: dict):
    region = regionDIs.selectRegionById(regionId)
    if region is None:
        return {"error": f"Region with ID {regionId} not found."}, 404

    result = regionDIs.updateRegion(
        regionId=regionId, countryId=countryId, name=body.get("name", region.name)
    )
    if result is None:
        return {"error": "Error updating country region"}, 500

    return jsonify(toJson(result))
