import requests
from uuid import uuid4
from test.generators import generateRegion, generateCountry


def test_getAllRegions_ideal_returnsRegions():
    ids = [
        uuid4(),
        uuid4(),
        uuid4(),
        uuid4(),
    ]

    names = [
        generateRegion(id=ids[0])["name"],
        generateRegion(id=ids[1])["name"],
        generateRegion(id=ids[2])["name"],
        generateRegion(id=ids[3])["name"],
    ]

    r = requests.get("http://localhost:3000/regions/")
    assert r.status_code == 200

    data = r.json()
    for i in range(4):
        assert data[i]["id"] == str(ids[i])
        assert data[i]["name"] == names[i]


def test_getRegionById_ideal_returnsRegion():
    countryId = generateCountry()["id"]
    region = generateRegion(country=countryId)

    r = requests.get(f"http://localhost:3000/regions/{region["id"]}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(region["id"])
    assert data["name"] == region["name"]
    assert data["country"] == str(countryId)


def test_getRegionById_regionDoesntExist_404():
    dummyId = uuid4()

    r = requests.get(f"http://localhost:3000/regions/{dummyId}")
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Region {dummyId} not found."
