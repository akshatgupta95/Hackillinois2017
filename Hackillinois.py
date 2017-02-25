import base64

from pandas import json

from flask import Flask

import pprint

import requests

from requests.auth import HTTPBasicAuth

app = Flask(__name__)


@app.route('/')
def hello_world():
    api_key = 'b954cfcb00914f98a08be7cbfb51d0a2'
    api_sec = '5E5FCD8E015DCCD7D3B252B1C58447E0A7B6155646643983C8BE8E97D2B6ADF9'
    payload = {"Problems": [{"FreeText": "runny nose"}, {"FreeText": "cold"}]}
    api_URL = 'https://ipl-nonproduction-customer_validation.e-imo.com/api/v3/actions/categorize'
    r = requests.post(api_URL, auth=HTTPBasicAuth(api_key, api_sec), json=payload)
    print pprint.pprint(r.json())

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
