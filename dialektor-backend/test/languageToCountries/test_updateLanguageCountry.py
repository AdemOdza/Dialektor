import requests
from test.generators import generateLanguageToCountry, generateCountry, generateLanguage
from uuid import uuid4


def test_updateLanguageCountry_ideal_200():
    link = generateLanguageToCountry(official=False)

    r = requests.patch(
        "http://localhost:3000/language_countries/",
        json={
            "country_id": str(link["country_id"]),
            "language_id": str(link["language_id"]),
            "official": True,
        },
    )
    assert r.status_code == 200

    data = r.json()
    assert data["country_id"] == str(link["country_id"])
    assert data["language_id"] == str(link["language_id"])
    assert data["official"] is True


def test_updateLanguageCountry_linkDoesntExist_404():
    country = generateCountry()
    language = generateLanguage()

    r = requests.patch(
        "http://localhost:3000/language_countries/",
        json={
            "country_id": str(country["id"]),
            "language_id": str(language["id"]),
            "official": True,
        },
    )
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == "Language-country link not found"


def test_updateLanguageCountry_missingCountryId_400():
    r = requests.patch(
        "http://localhost:3000/language_countries/",
        json={
            "language_id": str(uuid4()),
            "official": True,
        },
    )
    assert r.status_code == 400


def test_updateLanguageCountry_missingOfficial_400():
    r = requests.patch(
        "http://localhost:3000/language_countries/",
        json={
            "country_id": str(uuid4()),
            "language_id": str(uuid4()),
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: official"
