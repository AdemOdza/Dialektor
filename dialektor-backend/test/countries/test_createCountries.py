import requests
from test.common import queryOne
from uuid import UUID


# Create country with POST call
def test_createCountry_ideal_200():
    r = requests.post(f"http://localhost:3000/countries/", json={"name": "newCountry"})
    assert r.status_code == 200

    data = r.json()
    assert UUID(data["id"])
    assert data["name"] == "newCountry"

    # Check database
    dbResult = queryOne(
        """
        SELECT *
        FROM countries
        WHERE id = %s;
    """,
        (data["id"],),
    )
    assert dbResult is not None
    assert dbResult["name"] == "newCountry"


def test_createCountry_nameEmpty_400():
    r = requests.post(f"http://localhost:3000/countries/", json={})
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == 'Error creating country: "name" field missing'
