import requests
from uuid import uuid4
from test.common import queryOne
from test.generators import generateCountry


def test_deleteCountry_ideal_returnsId_200():
    country = generateCountry(name="oldCountry")
    r = requests.delete(f"http://localhost:3000/countries/{country['id']}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(country["id"])

    # Check database
    dbResult = queryOne(
        """
        SELECT *
        FROM countries
        WHERE id = %s;
    """,
        (country["id"],),
    )
    assert dbResult is None


def test_deleteCountry_doesntExist_returnsId_200():
    dummyId = uuid4()
    r = requests.delete(f"http://localhost:3000/countries/{dummyId}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(dummyId)

    # Check database
    dbResult = queryOne(
        """
        SELECT *
        FROM countries
        WHERE id = %s;
    """,
        (dummyId,),
    )
    assert dbResult is None
