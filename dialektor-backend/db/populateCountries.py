# from src.common.database import updateMany
import pandas as pd
import requests
from bs4 import BeautifulSoup

baseUrl = 'http://localhost:3000'

countries = ['Albania', 'Kosova', 'Greece', 'North Macedonia', 'Turkey', 'Italy', 'Montenegro', 'Serbia']

# regions = {
#     'Albania': [],
#     'Kosova': [],
#     'North Macedonia': [],
#     'Turkey': [],
#     'Italy': [],
#     'Montenegro': [],
#     'Serbia': [],
# }

# Albania
page = requests.get('https://en.wikipedia.org/wiki/Municipalities_of_Albania').text
soup = BeautifulSoup(page, 'html.parser')
table = soup.find('table', class_="sortable wikitable")

df = pd.read_html(str(table))
df = pd.concat(df)

body = requests.post(
        url = f'{baseUrl}/countries',
        json = {
            'name': 'Albania'
        },
    ).json()

for _, row in df.iterrows():
    region = row['Municipality']['Municipality']
    if not region.isalpha():
        print(f'Invalid region: {region}')
        continue
    
    requests.post(
        url = f'{baseUrl}/countries/{body['id']}',
        json = {
            'name': region
        }
    )


# Kosove https://en.wikipedia.org/wiki/Municipalities_of_Kosovo
# Macedonia https://en.wikipedia.org/wiki/Municipalities_of_North_Macedonia