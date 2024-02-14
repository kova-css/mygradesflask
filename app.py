from flask import Flask, request
import requests

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
        
        return response.text

app.run()
