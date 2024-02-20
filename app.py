import os
from flask import Flask, request, Response
from bs4 import BeautifulSoup
import requests
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

class CustomJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        kwargs['ensure_ascii'] = False
        super(CustomJSONEncoder, self).__init__(*args, **kwargs)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

@app.route('/', methods=['POST'])
def fetch_data():
    req_data = request.get_json()
    url = req_data.get('url')
    data = req_data.get('data')
    method = req_data.get('method')

    key = os.getenv('cryptokey').encode()
    iv = b64decode(req_data.get('iv'))
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_data = unpad(cipher.decrypt(b64decode(data['txtPwd'])), AES.block_size).decode('utf-8')
    data['txtPwd'] = decrypted_data

    response = requests.post(url, data=data, allow_redirects=False)
    response.encoding = 'utf-8'

    if method == 'materials':
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
        return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')
    elif method == 'login':
        if response.status_code == 200:
            return 'wrongCred'
        elif response.status_code == 302:
            response = requests.post(url, data=data)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            nameArr = soup.find_all('span')
            name = nameArr[5].text
            materialsSoup = soup.find_all('th', {'class': 'rotate'})
            materialsArr = []
            for material in materialsSoup[1:]:
                tempName = material.get('name')
                materialsArr.append({'material': material.text.strip(), 'id': tempName[1:]})
            data = {
                'name': name,
                'materials': materialsArr
            }
            return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')
    else:
        return 'Invalid method'

app.run()
