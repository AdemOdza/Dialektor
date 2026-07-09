import requests
from uuid import uuid4
from test.generators import generateUser


# Get all users
def test_getUsers_empty_200():
    r = requests.get("http://localhost:3000/users/")
    assert r.status_code == 200

    data = r.json()
    assert data == []


def test_getUsers_ideal_200():
    users = [
        generateUser(),
        generateUser(),
        generateUser(),
    ]

    r = requests.get("http://localhost:3000/users/")
    assert r.status_code == 200

    data = r.json()
    assert len(data) == len(users)
    for i in range(len(users)):
        assert data[i]["id"] == str(users[i]["id"])
        assert data[i]["username"] == users[i]["username"]
        assert data[i]["email"] == users[i]["email"]
        assert "password_hash" not in data[i]


# Get user by ID
def test_getUser_ideal_200():
    user = generateUser()
    r = requests.get(f"http://localhost:3000/users/{user['id']}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(user["id"])
    assert data["username"] == user["username"]
    assert data["email"] == user["email"]
    assert "password_hash" not in data


def test_getUser_unknownId_404():
    dummyId = uuid4()
    r = requests.get(f"http://localhost:3000/users/{dummyId}")
    assert r.status_code == 404

    data = r.json()
    assert data["error"] == f"User with ID {dummyId} not found."
