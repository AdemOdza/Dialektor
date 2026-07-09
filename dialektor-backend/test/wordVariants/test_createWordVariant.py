import requests
from uuid import UUID
from test.common import queryOne
from test.generators import generateBaseWord, generateDialect


def test_createWordVariant_ideal_200():
    baseWord = generateBaseWord()
    dialect = generateDialect()

    r = requests.post(
        "http://localhost:3000/word_variants/",
        json={
            "word": "mirëdita",
            "base_word": str(baseWord["id"]),
            "dialect": str(dialect["id"]),
        },
    )
    assert r.status_code == 200

    data = r.json()
    assert UUID(data["id"])
    assert data["word"] == "mirëdita"
    assert data["base_word"] == str(baseWord["id"])
    assert data["dialect"] == str(dialect["id"])

    # Check database
    dbResult = queryOne(
        """
        SELECT * FROM word_variants WHERE id = %s;
    """,
        (data["id"],),
    )
    assert dbResult is not None
    assert dbResult["word"] == "mirëdita"


def test_createWordVariant_missingWord_400():
    baseWord = generateBaseWord()
    dialect = generateDialect()

    r = requests.post(
        "http://localhost:3000/word_variants/",
        json={
            "base_word": str(baseWord["id"]),
            "dialect": str(dialect["id"]),
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: word"


def test_createWordVariant_missingBaseWord_400():
    dialect = generateDialect()

    r = requests.post(
        "http://localhost:3000/word_variants/",
        json={
            "word": "mirëdita",
            "dialect": str(dialect["id"]),
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: base_word"


def test_createWordVariant_missingDialect_400():
    baseWord = generateBaseWord()

    r = requests.post(
        "http://localhost:3000/word_variants/",
        json={
            "word": "mirëdita",
            "base_word": str(baseWord["id"]),
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: dialect"


def test_createWordVariant_emptyBody_400():
    r = requests.post(
        "http://localhost:3000/word_variants/",
        json={},
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required fields: word, base_word, dialect"
