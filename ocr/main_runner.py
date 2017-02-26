from __future__ import print_function
import io

# Imports the Google Cloud client library
from google.cloud import vision
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# __________________ Google Cloud Vision API OCR ___________


IMAGE_PATH = '/Users/akshungupta/git/Hackillinois2017/ocr/test.png'

def detect_text(path):
	"""Detects text in the file."""
	vision_client = vision.Client()

	with io.open(path, 'rb') as image_file:
	    content = image_file.read()

	image = vision_client.image(content=content)

	texts = image.detect_text()
	result = [text.description for text in texts]
	index_medicine = result.index("Medicine:")
	result = result[index_medicine:]

	return result

# _____________________________ PARSING ______________________________

TIMEZONE = 'America/Los_Angeles'
START_TIME = 'T09:00:00-07:00'

def get_events(data):
	indices = [i for i, x in enumerate(data) if x == "Medicine:"]
	indices.append(len(data))

	events = []
	print(indices)
	for i in range(len(indices) - 1):
		lo = indices[i]
		hi = indices[i + 1]
		event = []
		for k in range(lo + 1, hi):
			event.append(data[k])
		events.append(event)
	return events

def create_event_dicts(events):
	ret_events = []
	for array in events:
		new_event = {}
		new_event['summary'] = array[0]
		new_event['start'] = {'dateTime': datetime.strptime(array[1], '%m/%d/%Y').strftime('%Y-%m-%d') + START_TIME, 'timeZone': TIMEZONE}
		new_event['end'] = {'dateTime': datetime.strptime(array[2], '%m/%d/%Y').strftime('%Y-%m-%d') + START_TIME, 
							'timeZone': TIMEZONE}
		new_event['recurrence'] = ['RRULE:FREQ=%s;COUNT=1' % array[3].upper()]
		new_event['reminders'] = {'useDefault': True}

		ret_events.append(new_event)
	return ret_events

# ______________________ Google Calendar API __________________________

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/google-apps/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

def create_event(service, events):

	for event in events:
		created_event = service.events().insert(calendarId='primary', body=event).execute()
    	# print ('Event created: %s' % (event.get('htmlLink')))


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def add_calendar_events(events):
	''' events is a list event dictionaries'''
	
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)
	create_event(service, events)

def main():
	words_in_file = detect_text(IMAGE_PATH)
	events = get_events(words_in_file)
	events_calendar = create_event_dicts(events) # list of events to be passed into google calendar api 
	add_calendar_events(events_calendar)
	print("Your prescriptions will be ")

if __name__ == '__main__':
	main()