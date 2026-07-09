import requests
from uuid import uuid4
from test.common import queryOne
from test.generators import generateWordVariant


def test_deleteWordVariant_ideal_200():
    variant = generateWordVariant()

    r = requests.delete(f"http://localhost:3000/word_variants/{variant['id']}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(variant["id"])

    # Check database
    dbResult = queryOne(
        """
        SELECT * FROM word_variants WHERE id = %s;
    """,
        (variant["id"],),
    )
    assert dbResult is None


def test_deleteWordVariant_doesntExist_200():
    dummyId = uuid4()
    r = requests.delete(f"http://localhost:3000/word_variants/{dummyId}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == str(dummyId)
