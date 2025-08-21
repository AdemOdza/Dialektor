import requests
from uuid import uuid4
from test.generators import generateCountry


# Get country by ID
def test_getCountry_unknownId_404():
    dummyId = uuid4()
    r = requests.get(f"http://localhost:3000/countries/{dummyId}")
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Country with ID {dummyId} not found."


def test_getCountry_ideal_200():
    country = generateCountry()
    r = requests.get(f"http://localhost:3000/countries/{country['id']}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(country["id"])
    assert data["name"] == country["name"]


# Get all countries
def test_getCountries_noCountries_200():
    r = requests.get(f"http://localhost:3000/countries/")
    assert r.status_code == 200

    data = r.json()
    assert data == []


def test_getCountries_ideal_200():
    ids = [
        uuid4(),
        uuid4(),
        uuid4(),
        uuid4(),
    ]

    names = [
        generateCountry(id=ids[0])["name"],
        generateCountry(id=ids[1])["name"],
        generateCountry(id=ids[2])["name"],
        generateCountry(id=ids[3])["name"],
    ]

    r = requests.get(f"http://localhost:3000/countries/")
    assert r.status_code == 200

    data = r.json()
    for i in range(4):
        assert data[i]["id"] == str(ids[i])
        assert data[i]["name"] == names[i]
