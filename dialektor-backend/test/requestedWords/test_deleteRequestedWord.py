import requests
from uuid import uuid4
from test.common import queryOne
from test.generators import generateRequestedWord


def test_deleteRequestedWord_ideal_200():
    word = generateRequestedWord()

    r = requests.delete(f"http://localhost:3000/requested_words/{word['id']}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(word["id"])

    # Check database
    dbResult = queryOne(
        """
        SELECT * FROM requested_words WHERE id = %s;
    """,
        (word["id"],),
    )
    assert dbResult is None


def test_deleteRequestedWord_doesntExist_200():
    dummyId = uuid4()
    r = requests.delete(f"http://localhost:3000/requested_words/{dummyId}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(dummyId)
