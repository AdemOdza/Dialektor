import requests
from uuid import uuid4
from test.common import queryOne
from test.generators import generateUser


def test_deleteUser_ideal_200():
    user = generateUser()

    r = requests.delete(f"http://localhost:3000/users/{user['id']}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(user["id"])

    # Check database
    dbResult = queryOne(
        """
        SELECT * FROM users WHERE id = %s;
    """,
        (user["id"],),
    )
    assert dbResult is None


def test_deleteUser_doesntExist_200():
    dummyId = uuid4()
    r = requests.delete(f"http://localhost:3000/users/{dummyId}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(dummyId)
