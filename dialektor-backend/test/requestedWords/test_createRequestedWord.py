import requests
from uuid import UUID
from test.common import queryOne
from test.generators import generateCountry, generateRegion


def test_createRequestedWord_ideal_200():
    country = generateCountry()

    r = requests.post(
        "http://localhost:3000/requested_words/",
        json={
            "word": "bukë",
            "country": str(country["id"]),
            "requested_by": "testuser",
        },
    )
    assert r.status_code == 200

    data = r.json()
    assert UUID(data["id"])
    assert data["word"] == "bukë"
    assert data["country"] == str(country["id"])
    assert data["requested_by"] == "testuser"

    # Check database
    dbResult = queryOne(
        """
        SELECT * FROM requested_words WHERE id = %s;
    """,
        (data["id"],),
    )
    assert dbResult is not None
    assert dbResult["word"] == "bukë"


def test_createRequestedWord_withOptionalFields_200():
    country = generateCountry()
    region = generateRegion(country=country["id"])

    r = requests.post(
        "http://localhost:3000/requested_words/",
        json={
            "word": "bukë",
            "variant": "buk",
            "country": str(country["id"]),
            "region": str(region["id"]),
            "requested_by": "testuser",
        },
    )
    assert r.status_code == 200

    data = r.json()
    assert data["variant"] == "buk"
    assert data["region"] == str(region["id"])


def test_createRequestedWord_missingWord_400():
    country = generateCountry()

    r = requests.post(
        "http://localhost:3000/requested_words/",
        json={
            "country": str(country["id"]),
            "requested_by": "testuser",
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: word"


def test_createRequestedWord_missingCountry_400():
    r = requests.post(
        "http://localhost:3000/requested_words/",
        json={
            "word": "bukë",
            "requested_by": "testuser",
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: country"


def test_createRequestedWord_missingRequestedBy_400():
    country = generateCountry()

    r = requests.post(
        "http://localhost:3000/requested_words/",
        json={
            "word": "bukë",
            "country": str(country["id"]),
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: requested_by"


def test_createRequestedWord_emptyBody_400():
    r = requests.post(
        "http://localhost:3000/requested_words/",
        json={},
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required fields: word, country, requested_by"
