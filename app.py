from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['POST'])
def fetch_data():
    req_data = request.get_json()
    url = req_data.get('url')
    data = req_data.get('data')

    response = requests.post(url, data=data, allow_redirects=False)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        return 'fail'
    elif response.status_code == 302:
        response = requests.post(url, data=data)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        materials = soup.find_all('th', {'class': 'rotate'})
        data = []
        for material in materials[1:]:
            name = material.get('name')
            data.append({'material': material.text.strip(), 'id': name[1:]})
    return data

app.run()
