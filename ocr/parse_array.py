from datetime import datetime

data = ['Medicine:', 'Advil', '03/01/2017', '03/08/2017', 'Daily', 'Medicine:', 'Hersheys', '03/01/2017', '03/15/2017', 'Weekly', 
		'Medicine:', 'Soylent', '03/21/2017', '03/28/2017', 'Weekly']
# 'timeZone': 'America/Los_Angeles'
# T09:00:00-07:00
timezone = 'America/Los_Angeles'
start_time = 'T09:00:00-07:00'

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
		new_event['start'] = {'dateTime': datetime.strptime(array[1], '%m/%d/%Y').strftime('%Y-%m-%d') + start_time,								'timeZone': timezone}
		new_event['end'] = {'dateTime': datetime.strptime(array[2], '%m/%d/%Y').strftime('%Y-%m-%d') + start_time, 
							'timeZone': timezone}
		new_event['recurrence'] = ['RRULE:FREQ=%s;COUNT=1' % array[3].upper()]

		ret_events.append(new_event)
	return ret_events

events = get_events(data)
event_dicts = create_event_dicts(events)
print(event_dicts)