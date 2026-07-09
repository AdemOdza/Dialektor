import requests
from uuid import uuid4
from test.common import queryOne
from test.generators import generateLanguageToCountry, generateCountry, generateLanguage


def test_deleteLanguageCountry_ideal_200():
    link = generateLanguageToCountry()

    r = requests.delete(
        "http://localhost:3000/language_countries/",
        json={
            "country_id": str(link["country_id"]),
            "language_id": str(link["language_id"]),
        },
    )
    assert r.status_code == 200

    data = r.json()
    assert data["country_id"] == str(link["country_id"])
    assert data["language_id"] == str(link["language_id"])

    # Check database
    dbResult = queryOne(
        """
        SELECT * FROM language_to_countries
        WHERE country_id = %s AND language_id = %s;
    """,
        (link["country_id"], link["language_id"]),
    )
    assert dbResult is None


def test_deleteLanguageCountry_doesntExist_200():
    country = generateCountry()
    language = generateLanguage()

    r = requests.delete(
        "http://localhost:3000/language_countries/",
        json={
            "country_id": str(country["id"]),
            "language_id": str(language["id"]),
        },
    )
    assert r.status_code == 200


def test_deleteLanguageCountry_missingCountryId_400():
    r = requests.delete(
        "http://localhost:3000/language_countries/",
        json={
            "language_id": str(uuid4()),
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: country_id"


def test_deleteLanguageCountry_missingLanguageId_400():
    r = requests.delete(
        "http://localhost:3000/language_countries/",
        json={
            "country_id": str(uuid4()),
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: language_id"
