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
    return '{"name": "KOVÁCS KRISZTIÁN-HUNOR", "premium": false, "materials": [{"material": "Test1", "id": "1"}, {"material": "Test2", "id": "2"}], "absences": [[["31.01", true]], [["31.01", false]]], "grades": [[["10", "07.03"], ["8", "06.04"]], [["8", "11.10"]]]}'

app.run()
