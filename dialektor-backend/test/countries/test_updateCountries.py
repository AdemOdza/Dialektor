import requests
from uuid import uuid4
from test.common import queryOne
from test.generators import generateCountry


def test_updateCountry_ideal_returnsCountry_200():
    oldCountry = generateCountry(name="oldCountry")
    r = requests.patch(
        f"http://localhost:3000/countries/{oldCountry['id']}",
        json={"name": "newCountry"},
    )
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(oldCountry["id"])
    assert data["name"] == "newCountry"

    # Check database
    dbResult = queryOne(
        """
        SELECT *
        FROM countries
        WHERE id = %s;
    """,
        (oldCountry["id"],),
    )
    assert dbResult is not None
    assert dbResult["name"] == "newCountry"


def test_updateCountry_noName_returnsCountryIdempotent_200():
    oldCountry = generateCountry(name="oldCountry")
    r = requests.patch(f"http://localhost:3000/countries/{oldCountry['id']}", json={})
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(oldCountry["id"])
    assert data["name"] == oldCountry["name"]

    # Check database
    dbResult = queryOne(
        """
        SELECT *
        FROM countries
        WHERE id = %s;
    """,
        (oldCountry["id"],),
    )
    assert dbResult is not None
    assert dbResult["name"] == oldCountry["name"]


def test_updateCountry_idDoesntExist_returnsError_404():
    dummyId = uuid4()
    r = requests.patch(
        f"http://localhost:3000/countries/{dummyId}", json={"name": "newCountry"}
    )
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Error updating: country with ID {dummyId} not found."
