import requests
from uuid import uuid4
from test.generators import generateRequestedWord


# Get all requested words
def test_getRequestedWords_empty_200():
    r = requests.get("http://localhost:3000/requested_words/")
    assert r.status_code == 200

    data = r.json()
    assert data == []


def test_getRequestedWords_ideal_200():
    words = [
        generateRequestedWord(),
        generateRequestedWord(),
        generateRequestedWord(),
    ]

    r = requests.get("http://localhost:3000/requested_words/")
    assert r.status_code == 200

    data = r.json()
    assert len(data) == len(words)
    for i in range(len(words)):
        assert data[i]["id"] == str(words[i]["id"])
        assert data[i]["word"] == words[i]["word"]
        assert data[i]["country"] == str(words[i]["country"])
        assert data[i]["requested_by"] == words[i]["requested_by"]


# Get requested word by ID
def test_getRequestedWord_ideal_200():
    word = generateRequestedWord()
    r = requests.get(f"http://localhost:3000/requested_words/{word['id']}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(word["id"])
    assert data["word"] == word["word"]
    assert data["country"] == str(word["country"])
    assert data["requested_by"] == word["requested_by"]


def test_getRequestedWord_unknownId_404():
    dummyId = uuid4()
    r = requests.get(f"http://localhost:3000/requested_words/{dummyId}")
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Requested word with ID {dummyId} not found."
