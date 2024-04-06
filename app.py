from flask import Flask
import json

class CustomJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        kwargs['ensure_ascii'] = False
        super(CustomJSONEncoder, self).__init__(*args, **kwargs)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

@app.route('/', methods=['POST'])
def fetch_data():
    return '{"name": "KOVÁCS KRISZTIÁN-HUNOR", "premium": false, "materials": [{"material": "Test", "id": "1"}], "absences": [[["31.01", true]]], "grades": [[["8", "11.10"], ["6", "22.11"], ["7", "07.12"], ["9", "27.03"], ["10", "05.04"]]]}'

app.run()
