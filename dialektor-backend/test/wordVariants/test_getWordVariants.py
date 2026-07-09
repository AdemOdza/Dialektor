import requests
from uuid import uuid4
from test.generators import generateWordVariant


# Get all word variants
def test_getWordVariants_empty_200():
    r = requests.get("http://localhost:3000/word_variants/")
    assert r.status_code == 200

    data = r.json()
    assert data == []


def test_getWordVariants_ideal_200():
    variants = [
        generateWordVariant(),
        generateWordVariant(),
        generateWordVariant(),
    ]

    r = requests.get("http://localhost:3000/word_variants/")
    assert r.status_code == 200

    data = r.json()
    assert len(data) == len(variants)
    for i in range(len(variants)):
        assert data[i]["id"] == str(variants[i]["id"])
        assert data[i]["word"] == variants[i]["word"]
        assert data[i]["base_word"] == str(variants[i]["base_word"])
        assert data[i]["dialect"] == str(variants[i]["dialect"])


# Get word variant by ID
def test_getWordVariant_ideal_200():
    variant = generateWordVariant()
    r = requests.get(f"http://localhost:3000/word_variants/{variant['id']}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(variant["id"])
    assert data["word"] == variant["word"]
    assert data["base_word"] == str(variant["base_word"])
    assert data["dialect"] == str(variant["dialect"])


def test_getWordVariant_unknownId_404():
    dummyId = uuid4()
    r = requests.get(f"http://localhost:3000/word_variants/{dummyId}")
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Word variant with ID {dummyId} not found."
