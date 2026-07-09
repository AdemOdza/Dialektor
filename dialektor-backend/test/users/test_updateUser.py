import requests
from uuid import uuid4
from test.generators import generateUser


def test_updateUser_ideal_200():
    user = generateUser(username="oldUser", email="old@test.com")

    r = requests.patch(
        f"http://localhost:3000/users/{user['id']}",
        json={"username": "newUser", "email": "new@test.com"},
    )
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(user["id"])
    assert data["username"] == "newUser"
    assert data["email"] == "new@test.com"
    assert "password_hash" not in data


def test_updateUser_emptyBody_idempotent_200():
    user = generateUser(username="unchanged")

    r = requests.patch(
        f"http://localhost:3000/users/{user['id']}",
        json={},
    )
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(user["id"])
    assert data["username"] == "unchanged"


def test_updateUser_unknownId_404():
    dummyId = uuid4()
    r = requests.patch(
        f"http://localhost:3000/users/{dummyId}",
        json={"username": "newUser"},
    )
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"User with ID {dummyId} not found."
