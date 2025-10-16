import requests
from test.generators import generateLanguage, generateBaseWord
from uuid import uuid4


# Get base word by ID
def test_getBaseWord_ideal_returnsBaseWord():
    word = generateBaseWord()

    r = requests.get(
        f"http://localhost:3000/base_words/{word["id"]}",
    )
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(word["id"])
    assert data["word"] == str(word["word"])
    assert data["language_id"] == str(word["language_id"])


def test_getBaseWord_unknownId_returns404():
    dummyId = uuid4()
    r = requests.get(
        f"http://localhost:3000/base_words/{dummyId}",
    )
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Base Word {dummyId} not found."


# Get base word by language
def test_getBaseWordByLanguage_ideal_returnsBaseWord():
    language = generateLanguage()
    word = generateBaseWord(languageId=language["id"])

    r = requests.get(
        f"http://localhost:3000/languages/{language["id"]}/base_words/{word["id"]}",
    )
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(word["id"])
    assert data["word"] == str(word["word"])
    assert data["language_id"] == str(word["language_id"])


def test_getBaseWordByLanguage_unknownBaseWord_returns404():
    language = generateLanguage()
    dummyId = str(uuid4())

    r = requests.get(
        f"http://localhost:3000/languages/{language["id"]}/base_words/{dummyId}",
    )
    assert r.status_code == 404

    data = r.json()
    assert (
        data["error"]
        == f"Base word {dummyId} not associated with language {language["id"]}"
    )


def test_getBaseWordByLanguage_unknownLanguage_returns404():
    dummyId = str(uuid4())

    r = requests.get(
        f"http://localhost:3000/languages/{dummyId}/base_words/{dummyId}",
    )
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == "Language not found"


# Get all base words
def test_getBaseWords_ideal_returnsBaseWords():
    words = [
        generateBaseWord(),
        generateBaseWord(),
        generateBaseWord(),
    ]

    r = requests.get(
        f"http://localhost:3000/base_words/",
    )
    assert r.status_code == 200

    data = r.json()
    assert len(data) == len(words)

    for i in range(len(words)):
        assert data[i]["id"] == str(words[i]["id"])
        assert data[i]["word"] == str(words[i]["word"])
        assert data[i]["language_id"] == str(words[i]["language_id"])


def test_getBaseWordsByLanguage_ideal_returnsBaseWords():
    language = generateLanguage()
    words = [
        generateBaseWord(languageId=language["id"]),
        generateBaseWord(languageId=language["id"]),
        generateBaseWord(languageId=language["id"]),
    ]

    r = requests.get(
        f"http://localhost:3000/languages/{language["id"]}/base_words/",
    )
    assert r.status_code == 200

    data = r.json()
    for i in range(len(words)):
        assert data[i]["id"] == str(words[i]["id"])
        assert data[i]["word"] == str(words[i]["word"])
        assert data[i]["language_id"] == str(words[i]["language_id"])
