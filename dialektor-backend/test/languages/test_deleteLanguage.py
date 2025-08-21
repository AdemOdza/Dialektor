import requests
from uuid import uuid4
from test.generators import generateLanguage


def test_deleteLanguage_ideal_returnsId_200():
    oldLanguage = generateLanguage(script="LATIN")

    r = requests.delete(
        f"http://localhost:3000/languages/{oldLanguage["id"]}",
    )
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(oldLanguage["id"])


def test_deleteLanguage_languageDoesntExist_returnsId_200():
    dummyId = uuid4()
    r = requests.delete(
        f"http://localhost:3000/languages/{dummyId}",
    )
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(dummyId)
