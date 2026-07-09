import requests
from uuid import uuid4
from test.generators import generateLanguage


# Get language by ID
def test_getLanguage_unknownId_404():
    dummyId = uuid4()
    r = requests.get(f"http://localhost:3000/languages/{dummyId}")
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Language {dummyId} not found."


def test_getLanguage_ideal_200():
    language = generateLanguage()
    r = requests.get(f"http://localhost:3000/languages/{language['id']}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(language["id"])
    assert data["name"] == language["name"]
    assert data["script"] == language["script"]


# Get all languages
def test_getLanguages_noLanguages_200():
    r = requests.get(f"http://localhost:3000/languages/")
    assert r.status_code == 200

    data = r.json()
    assert data == []


def test_getLanguages_ideal_200():
    ids = [
        uuid4(),
        uuid4(),
        uuid4(),
        uuid4(),
    ]

    languages = [
        generateLanguage(id=ids[0]),
        generateLanguage(id=ids[1]),
        generateLanguage(id=ids[2]),
        generateLanguage(id=ids[3]),
    ]

    r = requests.get(f"http://localhost:3000/languages/")
    assert r.status_code == 200

    data = r.json()
    for i in range(4):
        assert data[i]["id"] == str(ids[i])
        assert data[i]["name"] == languages[i]["name"]
        assert data[i]["script"] == languages[i]["script"]
