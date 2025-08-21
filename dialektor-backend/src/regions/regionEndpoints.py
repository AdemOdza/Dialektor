from uuid import UUID
from flask import Blueprint, request
from common import toJson
from regions import regionDIs

regionsRouter = Blueprint("regions", __name__, url_prefix="/regions")


@regionsRouter.route("/", methods=("GET",))
def regionsResource():
    if request.method == "GET":
        result = regionDIs.selectRegions()
        return [*map(lambda r: r.toJson(), result)]
    return {"error": "Not Implemented"}, 501


@regionsRouter.route("/<id>", methods=("GET",))
def regionByIdResource(id: UUID):
    region = regionDIs.selectRegionById(id)
    if region is None:
        return {"error": f"Region {id} not found."}, 404

    if request.method == "GET":
        return toJson(region)
    return {"error": "Not Implemented"}, 501
