import requests
from test.generators import generateBaseWord
from uuid import uuid4


def updateBaseWord_ideal_returns200():
    word = generateBaseWord(word="oldWord")

    r = requests.patch(
        f"http://localhost:3000/base_words/{word["id"]}", json={"word": "newWord"}
    )

    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(word["id"])
    assert data["word"] == "newWord"
    assert data["language_id"] == str(word["language_id"])


def updateBaseWord_noWord_idempotent():
    word = generateBaseWord(word="oldWord")

    r = requests.patch(
        f"http://localhost:3000/base_words/{word["id"]}",
    )

    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(word["id"])
    assert data["word"] == word["word"]
    assert data["language_id"] == str(word["language_id"])


def updateBaseWord_idDoesntExist_returns404():
    dummyId = uuid4()

    r = requests.patch(
        f"http://localhost:3000/base_words/{dummyId}",
    )

    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Base Word {dummyId} not found."
