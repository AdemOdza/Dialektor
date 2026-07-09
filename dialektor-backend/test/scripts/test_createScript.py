import requests
from test.common import queryOne


def test_createScript_ideal_200():
    r = requests.post("http://localhost:3000/scripts/", json={"name": "DEVANAGARI"})
    assert r.status_code == 200

    data = r.json()
    assert data["name"] == "DEVANAGARI"

    # Check database
    dbResult = queryOne(
        """
        SELECT * FROM scripts WHERE name = %s;
    """,
        ("DEVANAGARI",),
    )
    assert dbResult is not None
    assert dbResult["name"] == "DEVANAGARI"


def test_createScript_noName_400():
    r = requests.post("http://localhost:3000/scripts/", json={})
    assert r.status_code == 400

    data = r.json()
    assert data["error"] == 'Error creating script: "name" field missing'
