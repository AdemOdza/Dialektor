import requests
from test.generators import generateBaseWord
from uuid import uuid4


def test_updateBaseWord_ideal_returns200():
    word = generateBaseWord(word="oldWord")

    r = requests.patch(
        f"http://localhost:3000/base_words/{word["id"]}", json={"word": "newWord"}
    )

    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(word["id"])
    assert data["word"] == "newWord"
    assert data["language_id"] == str(word["language_id"])


def test_updateBaseWord_noWord_idempotent():
    word = generateBaseWord(word="oldWord")

    r = requests.patch(
        f"http://localhost:3000/base_words/{word["id"]}",
        json={},
    )

    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(word["id"])
    assert data["word"] == word["word"]
    assert data["language_id"] == str(word["language_id"])


def test_updateBaseWord_idDoesntExist_returns404():
    dummyId = uuid4()

    r = requests.patch(
        f"http://localhost:3000/base_words/{dummyId}",
        json={},
    )

    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Base Word {dummyId} not found."
