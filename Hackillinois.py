import base64

from pandas import json

from flask import Flask

from flask import render_template
<<<<<<< Updated upstream
from flask import g
from requests.auth import HTTPBasicAuth
import base64
import pprint
import requests

import sqlite3 as sl

app = Flask(__name__)

app.database = "doctors.db"

=======

import pprint

from flask import request
>>>>>>> Stashed changes

import requests

from requests.auth import HTTPBasicAuth

app = Flask(__name__)

<<<<<<< Updated upstream
def setup_doctor_database():
    doctor_names = [
        "Tracey Coleman","Katherine Wright","David Lewis","David Oliver","Ian Butler","Joan Forsyth","Chloe Mitchell","Nicola Clark","Lauren McGrath","Victoria Lewis","Carolyn Paige","Katherine Sutherland","Joshua Hughes","Ian Young","Jonathan Abraham"
    ]
    all_categories = ["Advance Directives", "Allergies and Adverse Reactions", "Cardiac and Vasculature", "Coag and Thromboembolic", "Endocrine and Metabolic", "ENT", "Eye", "Gastrointestinal and Abdominal", "Genitourinary and Reproductive", "Gravid and Perinatal", "Infectious Diseases", "Mental Health", "Multi-system (Lupus, Sarcoid...)", "Musculoskeletal and Injuries", "Neuro", "Pulmonary and Pneumonias", "Sleep", "Skin", "Symptoms and Signs", "Tobacco", "Health Encounters", "Family History", "Toxicities and Envenomations"]

    g.db = connect_db()
    curr = g.db.cursor()
    curr.execute("DROP TABLE IF EXISTS category_doctor;")
    curr.execute("CREATE TABLE category_doctor (category TEXT, doctor TEXT);")

    g.db.commit()

    curr = g.db.cursor()

    for i, category in enumerate(all_categories):
    	doctor_name = doctor_names[i%len(doctor_names)]
    	params = (category, doctor_name)
    	curr.execute("INSERT INTO category_doctor VALUES (?, ?)", params)
    	g.db.commit()

    curr.close()
    print ('Created Table')

def make_imo_categories_request(symptopms):
=======
symptoms = []

@app.route('/', methods=['GET', 'POST'])
def hello_world():
>>>>>>> Stashed changes
    api_key = 'b954cfcb00914f98a08be7cbfb51d0a2'
    api_sec = '5E5FCD8E015DCCD7D3B252B1C58447E0A7B6155646643983C8BE8E97D2B6ADF9'
    payload = {'Problems' : []}
    for symptopm in symptopms:
    	payload['Problems'].append(
    		{'FreeText' : symptopm}
    	)
    api_URL = 'https://ipl-nonproduction-customer_validation.e-imo.com/api/v3/actions/categorize'
    r = requests.post(api_URL, auth=HTTPBasicAuth(api_key, api_sec), json=payload)
<<<<<<< Updated upstream

    response_data = process_response(r.json())

    pprint.pprint(response_data)


@app.route('/')
def index():
    setup_doctor_database()
    symptopms = ['runny nose', 'cold']
    make_imo_categories_request(symptopms)

    return 'Hello World!'
=======
    #print pprint.pprint(r.json())
    return render_template('test.html', sym=symptoms)
>>>>>>> Stashed changes

@app.route('/doctor_list', methods=['GET', 'POST'])
def doc():
    jsdata = request.form['data']
    print jsdata

def connect_db():
	return sl.connect(app.database)


if __name__ == '__main__':
    app.run()
