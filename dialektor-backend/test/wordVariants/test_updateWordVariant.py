import requests
from uuid import uuid4
from test.generators import generateWordVariant, generateBaseWord, generateDialect


def test_updateWordVariant_ideal_200():
    variant = generateWordVariant(word="oldWord")

    r = requests.patch(
        f"http://localhost:3000/word_variants/{variant['id']}",
        json={"word": "newWord"},
    )
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(variant["id"])
    assert data["word"] == "newWord"
    assert data["base_word"] == str(variant["base_word"])
    assert data["dialect"] == str(variant["dialect"])


def test_updateWordVariant_emptyBody_idempotent_200():
    variant = generateWordVariant(word="unchanged")

    r = requests.patch(
        f"http://localhost:3000/word_variants/{variant['id']}",
        json={},
    )
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(variant["id"])
    assert data["word"] == "unchanged"


def test_updateWordVariant_unknownId_404():
    dummyId = uuid4()
    r = requests.patch(
        f"http://localhost:3000/word_variants/{dummyId}",
        json={"word": "newWord"},
    )
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Word variant with ID {dummyId} not found."
