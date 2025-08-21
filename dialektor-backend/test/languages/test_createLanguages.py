import requests
from uuid import UUID

# from test.generators import generateScript


def test_createLanguage_ideal_returnsLanguage():

    r = requests.post(
        f"http://localhost:3000/languages/",
        json={
            "name": "testLang",
            "script": "LATIN",
        },
    )
    assert r.status_code == 200

    data = r.json()
    print(data)
    assert UUID(data["id"])
    assert data["name"] == "testLang"
    assert data["script"] == "LATIN"


def test_createLanguage_emptyBody_badRequest():
    r = requests.post(
        f"http://localhost:3000/languages/",
        json={},
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing Body"


def test_createLanguage_noBody_badRequest():
    r = requests.post(
        f"http://localhost:3000/languages/",
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Bad Request"


def test_createLanguage_noName_badRequest():
    r = requests.post(
        f"http://localhost:3000/languages/",
        json={"script": "LATIN"},
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required fields: name"


def test_createLanguage_noScript_badRequest():
    r = requests.post(
        f"http://localhost:3000/languages/",
        json={"name": "testLang"},
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required fields: script"


def test_createLanguage_invalidScript_badRequest():
    r = requests.post(
        f"http://localhost:3000/languages/",
        json={"name": "GALACTIC_BASIC_STANDARD", "script": "AUREBESH"},
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Invalid Script"
