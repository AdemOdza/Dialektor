import requests
from uuid import uuid4
from test.generators import generateDialect


# Get dialect by ID
def test_getDialect_unknownId_404():
    dummyId = uuid4()
    r = requests.get(f"http://localhost:3000/dialects/{dummyId}")
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Dialect with ID {dummyId} not found."


def test_getDialect_ideal_200():
    dialect = generateDialect()
    r = requests.get(f"http://localhost:3000/dialects/{dialect['id']}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(dialect["id"])
    assert data["name"] == dialect["name"]
    assert data["languageId"] == str(dialect["language_id"])


# Get all countries
def test_getDialects_noDialects_200():
    r = requests.get(f"http://localhost:3000/dialects/")
    assert r.status_code == 200

    data = r.json()
    assert data == []


def test_getDialects_ideal_200():
    ids = [
        str(uuid4()),
        str(uuid4()),
        str(uuid4()),
        str(uuid4()),
    ]

    dialects = [
        generateDialect(id=ids[0]),
        generateDialect(id=ids[1]),
        generateDialect(id=ids[2]),
        generateDialect(id=ids[3]),
    ]

    r = requests.get(f"http://localhost:3000/dialects/")
    assert r.status_code == 200

    data = r.json()
    for i in range(4):
        assert data[i]["id"] == ids[i]
        assert data[i]["name"] == dialects[i]["name"]
        assert data[i]["languageId"] == str(dialects[i]["language_id"])
