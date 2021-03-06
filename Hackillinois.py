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

from ocr.main_runner import main

app = Flask(__name__)

app.database = "doctors.db"

responseVal = []


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
        new_data['IMOTitle'] = curr_problem['IMOTitle']
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
        doctor_name = doctor_names[(i + 1) % len(doctor_names)]
        params = (category, doctor_name)
        curr.execute("INSERT INTO category_doctor VALUES (?, ?)", params)
        g.db.commit()

    curr.close()
    print ('Created Table')


def get_doctors_from_response(response_data):
    doctors = []
    g.db = connect_db()
    c = g.db.cursor()

    for data in response_data:
        category_name = data['CategoryTitle']
        query = "SELECT doctor FROM category_doctor WHERE category=\'%s\'" % category_name
        cur = c.execute(query)
        for doc_name in cur.fetchall():
            doctors.append((category_name, doc_name[0]))

    return doctors


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

    global responseVal

    response_data = process_response(r.json())

    doctors = get_doctors_from_response(response_data)

    responseVal = response_data

    return doctors


@app.route('/', methods=['GET', 'POST'])
def index():
    setup_doctor_database()
    return render_template('test.html')


@app.route('/doctor_list', methods=['GET', 'POST'])
def doctor_list():
    jsdata = request.form.listvalues()
    jsdata = [key for key in jsdata][0]
    symptoms = jsdata
    doctors = make_imo_categories_request(symptoms)
    docs = doctors
    print (doctors)
    return render_template('doctors.html', doc=docs)


@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    print (responseVal)
    return render_template("doc_dashboard.html", res=responseVal)

@app.route('/send_file', methods=['GET', 'POST'])
def send_file():
    main()
    return "Your patient's calendar is updated!"


def connect_db():
    return sl.connect(app.database)


if __name__ == '__main__':
    app.run(debug=True)
