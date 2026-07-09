import requests
from test.generators import generateLanguageToCountry, generateCountry, generateLanguage


# Get all language-country links
def test_getLanguageCountries_empty_200():
    r = requests.get("http://localhost:3000/language_countries/")
    assert r.status_code == 200

    data = r.json()
    assert data == []


def test_getLanguageCountries_ideal_200():
    links = [
        generateLanguageToCountry(),
        generateLanguageToCountry(),
        generateLanguageToCountry(),
    ]

    r = requests.get("http://localhost:3000/language_countries/")
    assert r.status_code == 200

    data = r.json()
    assert len(data) == len(links)
    for i in range(len(links)):
        assert data[i]["country_id"] == str(links[i]["country_id"])
        assert data[i]["language_id"] == str(links[i]["language_id"])
        assert data[i]["official"] == links[i]["official"]
