import requests
from uuid import uuid4
from test.generators import generateRequestedWord


def test_updateRequestedWord_ideal_200():
    word = generateRequestedWord(word="oldWord")

    r = requests.patch(
        f"http://localhost:3000/requested_words/{word['id']}",
        json={"word": "newWord"},
    )
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(word["id"])
    assert data["word"] == "newWord"


def test_updateRequestedWord_emptyBody_idempotent_200():
    word = generateRequestedWord(word="unchanged")

    r = requests.patch(
        f"http://localhost:3000/requested_words/{word['id']}",
        json={},
    )
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(word["id"])
    assert data["word"] == "unchanged"


def test_updateRequestedWord_unknownId_404():
    dummyId = uuid4()
    r = requests.patch(
        f"http://localhost:3000/requested_words/{dummyId}",
        json={"word": "newWord"},
    )
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Requested word with ID {dummyId} not found."
