import requests
from uuid import uuid4
from test.common import queryOne
from test.generators import generateSessionToken


def test_deleteSessionToken_ideal_200():
    token = generateSessionToken()

    r = requests.delete(f"http://localhost:3000/session_tokens/{token['id']}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(token["id"])

    # Check database
    dbResult = queryOne(
        """
        SELECT * FROM session_tokens WHERE id = %s;
    """,
        (token["id"],),
    )
    assert dbResult is None


def test_deleteSessionToken_doesntExist_200():
    dummyId = uuid4()
    r = requests.delete(f"http://localhost:3000/session_tokens/{dummyId}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(dummyId)
