import requests
from test.common import queryOne


def test_deleteScript_ideal_200():
    # Create a script to delete
    requests.post("http://localhost:3000/scripts/", json={"name": "TEMP_SCRIPT"})

    r = requests.delete("http://localhost:3000/scripts/TEMP_SCRIPT")
    assert r.status_code == 200

    data = r.json()
    assert data["name"] == "TEMP_SCRIPT"

    # Check database
    dbResult = queryOne(
        """
        SELECT * FROM scripts WHERE name = %s;
    """,
        ("TEMP_SCRIPT",),
    )
    assert dbResult is None


def test_deleteScript_doesntExist_200():
    r = requests.delete("http://localhost:3000/scripts/NONEXISTENT")
    assert r.status_code == 200

    data = r.json()
    assert data["name"] == "NONEXISTENT"
