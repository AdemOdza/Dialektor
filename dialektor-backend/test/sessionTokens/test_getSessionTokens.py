import requests
from uuid import uuid4
from test.generators import generateSessionToken


# Get all session tokens
def test_getSessionTokens_empty_200():
    r = requests.get("http://localhost:3000/session_tokens/")
    assert r.status_code == 200

    data = r.json()
    assert data == []


def test_getSessionTokens_ideal_200():
    tokens = [
        generateSessionToken(),
        generateSessionToken(),
        generateSessionToken(),
    ]

    r = requests.get("http://localhost:3000/session_tokens/")
    assert r.status_code == 200

    data = r.json()
    assert len(data) == len(tokens)
    for i in range(len(tokens)):
        assert data[i]["id"] == str(tokens[i]["id"])
        assert data[i]["user_id"] == str(tokens[i]["user_id"])
        assert data[i]["token"] == tokens[i]["token"]


# Get session token by ID
def test_getSessionToken_ideal_200():
    token = generateSessionToken()
    r = requests.get(f"http://localhost:3000/session_tokens/{token['id']}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(token["id"])
    assert data["user_id"] == str(token["user_id"])
    assert data["token"] == token["token"]
    assert "expires" in data


def test_getSessionToken_unknownId_404():
    dummyId = uuid4()
    r = requests.get(f"http://localhost:3000/session_tokens/{dummyId}")
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"Session token with ID {dummyId} not found."


# def test_getSessionToken_expiredToken_???
