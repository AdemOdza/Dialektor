import requests
from uuid import uuid4


def test_getScripts_ideal_returnsScripts():
    r = requests.get(f"http://localhost:3000/scripts/")
    assert r.status_code == 200

    scripts = ["LATIN", "CYRILLIC", "GREEK", "ARABIC"]

    data = r.json()
    for i in scripts:
        assert {"name": i} in data
