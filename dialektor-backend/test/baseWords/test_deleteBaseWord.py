import requests
from uuid import uuid4
from test.common import queryOne
from test.generators import generateBaseWord


def deleteBaseWord_ideal_returns200():
    word = generateBaseWord()

    r = requests.delete(f"http://localhost:3000/base_words/{word["id"]}")

    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(word["id"])

    dbResult = queryOne(
        """
        SELECT *
        FROM base_words
        WHERE id = %s;
    """,
        (word["id"],),
    )
    assert dbResult is None


def deleteBaseWord_wordNotFound_returns200():
    dummyId = uuid4()

    r = requests.delete(f"http://localhost:3000/base_words/{dummyId}")

    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(dummyId)

    dbResult = queryOne(
        """
        SELECT *
        FROM base_words
        WHERE id = %s;
    """,
        (dummyId,),
    )
    assert dbResult is None
