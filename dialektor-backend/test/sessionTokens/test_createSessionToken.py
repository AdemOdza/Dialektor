import requests
from uuid import UUID
from datetime import datetime, timedelta, timezone
from test.common import queryOne
from test.generators import generateUser


def test_createSessionToken_ideal_200():
    user = generateUser()
    expires = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()

    r = requests.post(
        "http://localhost:3000/session_tokens/",
        json={
            "user_id": str(user["id"]),
            "token": "abc123token",
            "expires": expires,
        },
    )
    assert r.status_code == 200

    data = r.json()
    assert UUID(data["id"])
    assert data["user_id"] == str(user["id"])
    assert data["token"] == "abc123token"
    assert "expires" in data

    # Check database
    dbResult = queryOne(
        """
        SELECT * FROM session_tokens WHERE id = %s;
    """,
        (data["id"],),
    )
    assert dbResult is not None
    assert dbResult["token"] == "abc123token"


def test_createSessionToken_missingUserId_400():
    expires = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()

    r = requests.post(
        "http://localhost:3000/session_tokens/",
        json={
            "token": "abc123token",
            "expires": expires,
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: user_id"


def test_createSessionToken_missingToken_400():
    user = generateUser()
    expires = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()

    r = requests.post(
        "http://localhost:3000/session_tokens/",
        json={
            "user_id": str(user["id"]),
            "expires": expires,
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: token"


def test_createSessionToken_missingExpires_400():
    user = generateUser()

    r = requests.post(
        "http://localhost:3000/session_tokens/",
        json={
            "user_id": str(user["id"]),
            "token": "abc123token",
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: expires"


def test_createSessionToken_emptyBody_400():
    r = requests.post(
        "http://localhost:3000/session_tokens/",
        json={},
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required fields: user_id, token, expires"
