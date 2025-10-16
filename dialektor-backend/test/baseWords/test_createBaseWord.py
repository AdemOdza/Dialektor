import requests
from test.generators import generateLanguage
from uuid import UUID


def test_createBaseWord_ideal_returnsBaseWord():
    word = "mir"
    language = generateLanguage(name="Shqip")

    r = requests.post(
        f"http://localhost:3000/base_words/",
        json={
            "word": "mir",
            "language_id": str(language["id"]),
        },
    )
    assert r.status_code == 200

    data = r.json()
    assert UUID(data["id"])
    assert data["word"] == word
    assert data["language_id"] == str(language["id"])


def test_createBaseWord_emptyBody_badRequest():
    r = requests.post(
        f"http://localhost:3000/base_words/",
        json={},
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required fields: word, language_id"


def test_createBaseWord_noBody_badRequest():
    r = requests.post(
        f"http://localhost:3000/base_words/",
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Bad Request"


def test_createBaseWord_noLanguage_badRequest():
    word = "mir"

    r = requests.post(
        f"http://localhost:3000/base_words/",
        json={"word": word},
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: language_id"


def test_createBaseWord_noWord_badRequest():
    language = generateLanguage(name="Shqip")

    r = requests.post(
        f"http://localhost:3000/base_words/",
        json={"language_id": str(language["id"])},
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: word"
