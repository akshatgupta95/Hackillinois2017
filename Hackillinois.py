from pandas import json
from flask import Flask
from flask import render_template
from flask import request
from flask import g
from requests.auth import HTTPBasicAuth
import base64
import pprint
import requests

import sqlite3 as sl

app = Flask(__name__)

app.database = "doctors.db"


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


def setup_doctor_database():
    doctor_names = [
        "Tracey Coleman", "Katherine Wright", "David Lewis", "David Oliver", "Ian Butler", "Joan Forsyth",
        "Chloe Mitchell", "Nicola Clark", "Lauren McGrath", "Victoria Lewis", "Carolyn Paige", "Katherine Sutherland",
        "Joshua Hughes", "Ian Young", "Jonathan Abraham"
    ]
    all_categories = ["Advance Directives", "Allergies and Adverse Reactions", "Cardiac and Vasculature",
                      "Coag and Thromboembolic", "Endocrine and Metabolic", "ENT", "Eye",
                      "Gastrointestinal and Abdominal", "Genitourinary and Reproductive", "Gravid and Perinatal",
                      "Infectious Diseases", "Mental Health", "Multi-system (Lupus, Sarcoid...)",
                      "Musculoskeletal and Injuries", "Neuro", "Pulmonary and Pneumonias", "Sleep", "Skin",
                      "Symptoms and Signs", "Tobacco", "Health Encounters", "Family History",
                      "Toxicities and Envenomations"]

    g.db = connect_db()
    curr = g.db.cursor()
    curr.execute("DROP TABLE IF EXISTS category_doctor;")
    curr.execute("CREATE TABLE category_doctor (category TEXT, doctor TEXT);")

    g.db.commit()

    curr = g.db.cursor()

    for i, category in enumerate(all_categories):
        doctor_name = doctor_names[i % len(doctor_names)]
        params = (category, doctor_name)
        curr.execute("INSERT INTO category_doctor VALUES (?, ?)", params)
        g.db.commit()

    curr.close()
    print ('Created Table')


def make_imo_categories_request(symptoms):
    api_key = 'b954cfcb00914f98a08be7cbfb51d0a2'
    api_sec = '5E5FCD8E015DCCD7D3B252B1C58447E0A7B6155646643983C8BE8E97D2B6ADF9'
    payload = {'Problems': []}
    for symptom in symptoms:
        payload['Problems'].append(
            {'FreeText': symptom}
        )
    api_URL = 'https://ipl-nonproduction-customer_validation.e-imo.com/api/v3/actions/categorize'
    r = requests.post(api_URL, auth=HTTPBasicAuth(api_key, api_sec), json=payload)

    response_data = process_response(r.json())

    pprint.pprint(response_data)
    return


@app.route('/', methods=['GET', 'POST'])
def index():
    setup_doctor_database()
    return render_template('test.html')

@app.route('/doctor_list', methods=['GET', 'POST'])
def doctor_list():
    jsdata = request.form.listvalues()
    symptoms = jsdata[0]
    print (symptoms)
    make_imo_categories_request(symptoms)
    return 'Hello World'

def connect_db():
    return sl.connect(app.database)


if __name__ == '__main__':
    app.run()
