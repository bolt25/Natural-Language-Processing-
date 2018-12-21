from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

def auth():
	# func is to take access from user if didn`t given
	SCOPES = 'https://www.googleapis.com/auth/calendar'

	store = file.Storage('token.json')
	creds = store.get()
	if not creds or creds.invalid:
	    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
	    creds = tools.run_flow(flow, store)
	service = build('calendar', 'v3', http=creds.authorize(Http()))
	return service


def event(service,sum,start,end):
	EVENT = {
        'summary': sum,
        'start': {'dateTime': start},
        'end': {'dateTime': end}
    }

	e = service.events().insert(calendarId='primary',
        sendNotifications=True,body=EVENT).execute()
	print("Event created")


def upcomingEvent(service):
	# Call the Calendar API
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	print('Getting the upcoming 10 events')
	events_result = service.events().list(calendarId='primary', timeMin=now,maxResults=10, singleEvents=True,orderBy='startTime').execute()
	events = events_result.get('items', [])

	if not events:
	    print('No upcoming events found.')
	for event in events:
	    start = event['start'].get('dateTime', event['start'].get('date'))
	    print(start, event['summary'])

