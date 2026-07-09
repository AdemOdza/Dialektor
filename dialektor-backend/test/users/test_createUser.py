import requests
from uuid import UUID
from test.common import queryOne
from test.generators import generateDialect


def test_createUser_ideal_200():
    r = requests.post(
        "http://localhost:3000/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": "hashed_pw_123",
        },
    )
    assert r.status_code == 200

    data = r.json()
    assert UUID(data["id"])
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password_hash" not in data

    # Check database
    dbResult = queryOne(
        """
        SELECT * FROM users WHERE id = %s;
    """,
        (data["id"],),
    )
    assert dbResult is not None
    assert dbResult["username"] == "testuser"
    assert dbResult["password_hash"] == "hashed_pw_123"


def test_createUser_withDefaultDialect_200():
    dialect = generateDialect()

    r = requests.post(
        "http://localhost:3000/users/",
        json={
            "username": "testuser2",
            "email": "test2@example.com",
            "password_hash": "hashed_pw_456",
            "default_dialect": str(dialect["id"]),
        },
    )
    assert r.status_code == 200

    data = r.json()
    assert data["default_dialect"] == str(dialect["id"])


def test_createUser_missingUsername_400():
    r = requests.post(
        "http://localhost:3000/users/",
        json={
            "email": "test@example.com",
            "password_hash": "hashed_pw",
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: username"


def test_createUser_missingEmail_400():
    r = requests.post(
        "http://localhost:3000/users/",
        json={
            "username": "testuser",
            "password_hash": "hashed_pw",
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: email"


def test_createUser_missingPasswordHash_400():
    r = requests.post(
        "http://localhost:3000/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
        },
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required field: password_hash"


def test_createUser_emptyBody_400():
    r = requests.post(
        "http://localhost:3000/users/",
        json={},
    )
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == "Missing required fields: username, email, password_hash"
