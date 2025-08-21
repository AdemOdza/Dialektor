import requests
from test.generators import generateVersion


def test_getVersion():
    version = generateVersion()["version"]
    r = requests.get("http://localhost:3000/version")
    data = r.json()
    assert data["version"] == version
