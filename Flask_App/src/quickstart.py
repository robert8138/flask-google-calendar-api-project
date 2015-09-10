import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Quickstart'


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
                                   'calendar-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    1. Output 10 events from primary calendar.
    2. Output all events from study time calendar in the past 100 days
    3. Output all events from outside thinking and the description texts
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print 'Getting the upcoming 10 events'
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print start, event['summary']

    #Print Study Events from the past 100 days
    epoch_time = time.time()
    start_time = epoch_time - 3600 * 24 * 100
    tz_offset = - time.altzone / 3600
    if tz_offset < 0:
        tz_offset_str = "-%02d00" % abs(tz_offset)
    else:
        tz_offset_str = "+%02d00" % abs(tz_offset)
    start_time = datetime.datetime.fromtimestamp(start_time).strftime("%Y-%m-%dT%H:%M:%S") + tz_offset_str
    end_time = datetime.datetime.fromtimestamp(epoch_time).strftime("%Y-%m-%dT%H:%M:%S") + tz_offset_str

    print '\nGetting Study Events from the past 100 days.............'
    eventsResult = service.events().list(
        calendarId='n2i7ecc8gsj4lnp2fllu59mkg8@group.calendar.google.com', 
        timeMin=start_time, 
        timeMax=end_time,
        maxResults=1000, 
        singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print start, event['summary']

    # Grab all the outside thinking events and the notes within them
    print '\nGetting Outside Thinking Events from the past 100 days.............'
    eventsResult = service.events().list(
        calendarId='u67t9i3r7v4jhfsbqkum39asc0@group.calendar.google.com', 
        timeMin=start_time, 
        timeMax=end_time,
        maxResults=1000, 
        singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])    

    if not events:
        print 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if event.get('description'):
            print start, event['summary'], event['description']
        else:
            print start, event['summary'], '| No Description'

if __name__ == '__main__':
    main()
