import requests
from uuid import uuid4
from test.generators import generateLanguage

def test_updateLanguage_ideal_returnsLanguage():
    oldLanguage = generateLanguage(script = "LATIN")

    r = requests.patch(
        f"http://localhost:3000/languages/{oldLanguage["id"]}",
        json={
            "name": "newName",
            "script": "GREEK",
        },
    )
    assert r.status_code == 200

    data = r.json()
    assert data["name"] != oldLanguage["name"]
    assert data["script"] != oldLanguage["script"]

def test_updateLanguage_idDoesntExist_returns404():
    oldLanguage = generateLanguage()

    r = requests.patch(
        f"http://localhost:3000/languages/{uuid4()}",
        json={
            "name": "newName",
            "script": "GREEK",
        },
    )
    assert r.status_code == 404


def test_updateLanguage_emptyBody_returnsOriginalLanguage():
    oldLanguage = generateLanguage()

    r = requests.patch(
        f"http://localhost:3000/languages/{oldLanguage["id"]}",
        json={},
    )
    assert r.status_code == 200

    data = r.json()
    assert data["name"] == oldLanguage["name"]
    assert data["script"] == oldLanguage["script"]

