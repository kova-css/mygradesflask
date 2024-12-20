import os
from flask import Flask, request, Response
from bs4 import BeautifulSoup
import requests
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
import re

class CustomJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        kwargs['ensure_ascii'] = False
        super(CustomJSONEncoder, self).__init__(*args, **kwargs)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

@app.route('/', methods=['POST'])
def fetch_data():
    premiumUsers = ["kovacs30844", "kocsis2844"]
    req_data = request.get_json()
    url = req_data.get('url')
    data = req_data.get('data')
    method = req_data.get('method')
    username = data['txtUser']
    key = os.getenv('cryptokey').encode()
    if method == 'full':
        iv = b64decode(req_data.get('iv'))
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted_data = unpad(cipher.decrypt(b64decode(data['txtPwd'])), AES.block_size).decode('utf-8')
        data['txtPwd'] = decrypted_data

        response = requests.post(url, data=data, allow_redirects=False)
        response.encoding = 'utf-8'

    if method == 'full':
        if response.status_code == 200:
            return 'fail'
        elif response.status_code == 302:
            response = requests.post(url, data=data)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            nameArr = soup.find_all('span')
            if nameArr[0].text == "Toggle navigation":
                return '2fa'
            name = nameArr[5].text
            materialsSoup = soup.find_all('th', {'class': 'rotate'})
            materialsArr = []
            materialsInt = 0
            for material in materialsSoup[1:]:
                tempName = material.get('name')
                materialsArr.append({'material': material.text.strip(), 'id': tempName[1:]})
                materialsInt += 1
            
            absencesSoup = soup.find_all('td', id=lambda x: x and x.startswith('n'))
            absencesArr = []
            for absence in absencesSoup:
                child_table = absence.find('table', class_='tbNoteAbs')
                
                if child_table:
                    cabs_mot_tds = child_table.find_all('td', class_=['cAbsMot', 'cAbsNoMot'])
                    
                    text_bool_list = []
                    for td in cabs_mot_tds:
                        text = td.get_text(strip=True)
                        is_cabs_mot = td.has_attr('class') and 'cAbsMot' in td['class']
                        
                        text_bool_list.append((text, is_cabs_mot))
                    
                    absencesArr.append(text_bool_list)
           
            gradesArr = []
            for i in range(1, materialsInt + 1):
                grades = soup.find_all('td', {'name': ('n' + str(i))})
                data = []
                for grade in grades:
                    grade = grade.text.strip()
                    data.append(grade)
                data = re.findall(r'(\d+)\s+(\d+\.\d+)', data[1])
                gradesArr.append(data)
            premium = username in premiumUsers
            data = {
                'name': name,
                'premium': premium,
                'materials': materialsArr,
                'absences': absencesArr,
                'grades': gradesArr,
            }
            return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')
    elif method == 'premium':
            if username in premiumUsers:
                return 'True'
            else:
                return 'False'
    else:
        return 'Invalid method'

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
