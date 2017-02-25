from pandas import json
from flask import Flask
from flask import render_template
from requests.auth import HTTPBasicAuth
import base64
import pprint
import requests

app = Flask(__name__)


def process_response(data_dict):
	response_data = []
	categories = data_dict['Categories']

	for category in categories:
		new_data = {}
		curr_problem = category['Problems'][0]
		curr_problem = curr_problem['Details']
		new_data['CategoryTitle'] = curr_problem['CategoryTitle']
		new_data['ICD10'] = curr_problem['ICD10']
		new_data['IMO'] = curr_problem['IMO']
		response_data.append(new_data)

	return response_data


@app.route('/')
def hello_world():
    api_key = 'b954cfcb00914f98a08be7cbfb51d0a2'
    api_sec = '5E5FCD8E015DCCD7D3B252B1C58447E0A7B6155646643983C8BE8E97D2B6ADF9'
    payload = {"Problems": [{"FreeText": "runny nose"}, {"FreeText": "cold"}]}
    api_URL = 'https://ipl-nonproduction-customer_validation.e-imo.com/api/v3/actions/categorize'
    r = requests.post(api_URL, auth=HTTPBasicAuth(api_key, api_sec), json=payload)
    
    response_data = process_response(r.json())

    pprint.pprint(response_data)



    return 'Hello World!'


if __name__ == '__main__':
    app.run()
