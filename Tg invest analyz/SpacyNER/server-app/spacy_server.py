import json
from typing import Union

import spacy
from flask import Flask, request

FLASK_DEBUG = False
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

app = Flask(__name__)
model = spacy.load("../models/model-best")


def json_to_string(json_object: Union[dict, list]) -> str:
    return json.dumps(json_object, ensure_ascii=False, indent=2, sort_keys=True)


@app.route("/recognize", methods=["GET", "POST"])
def recognize_e():
    # json_request {"text": 'str'}
    json_request = request.get_json()
    input_text = json_request["text"]
    doc = model(input_text)
    response = [{entity.label_: entity.text} for entity in doc.ents]
    str_json = json_to_string(response)
    return app.response_class(response=str_json, status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG, threaded=False)
