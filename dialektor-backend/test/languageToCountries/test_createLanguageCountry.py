import requests
from test.common import queryOne
from test.generators import generateCountry, generateLanguage


def test_createLanguageCountry_ideal_200():
    country = generateCountry()
    language = generateLanguage()

    r = requests.post(
        "http://localhost:3000/language_countries/",
        json={
            "country_id": str(country["id"]),
            "language_id": str(language["id"]),
        },
    )
    assert r.status_code == 200

    data = r.json()
    assert data["country_id"] == str(country["id"])
    assert data["language_id"] == str(language["id"])
    assert data["official"] is False

    # Check database
    dbResult = queryOne(
        """
        SELECT * FROM language_to_countries
        WHERE country_id = %s AND language_id = %s;
    """,
        (country["id"], language["id"]),
    )
    assert dbResult is not None


def test_createLanguageCountry_withOfficial_200():
    country = generateCountry()
    language = generateLanguage()

    r = requests.post(
        "http://localhost:3000/language_countries/",
        json={
            "country_id": str(country["id"]),
            "language_id": str(language["id"]),
            "official": True,
        },
    )
    assert r.status_code == 200

    data = r.json()
    assert data["official"] is True


def test_createLanguageCountry_missingCountryId_400():
    language = generateLanguage()

    r = requests.post(
        "http://localhost:3000/language_countries/",
        json={
            "language_id": str(language["id"]),
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: country_id"


def test_createLanguageCountry_missingLanguageId_400():
    country = generateCountry()

    r = requests.post(
        "http://localhost:3000/language_countries/",
        json={
            "country_id": str(country["id"]),
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: language_id"


def test_createLanguageCountry_emptyBody_400():
    r = requests.post(
        "http://localhost:3000/language_countries/",
        json={},
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required fields: country_id, language_id"
