import os
import httplib2
import oauth2client
import datetime
import time
import csv
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from collections import defaultdict

# Global Constants
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Quickstart'

# Helper Functions
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

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

def build_service():
    """Build a Google Calendar API query endpoint"""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    return service

def get_start_date(startDate):
    """
    Given a string startDate in the format of YYYY-mm-dd
    return a datetime object with the proper time zone
    """
    return (datetime.datetime
                    .strptime(startDate, "%Y-%m-%d")
                    .isoformat() + 'Z')

def get_now_date():
    """Return a datetime object of current time"""
    return (datetime.datetime.utcnow()
                    .isoformat() + 'Z')

def get_end_date():
    pass

def get_ts_from_datetime(start, end):
    """convert datetime string into a time event
       so we can perform time arithmetic on them"""

    if start[-2:] == '00':
        startHr = datetime.datetime.strptime(start[:-6], "%Y-%m-%dT%H:%M:%S")
    elif start[-1] == 'Z':
        startHr = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
    else:
        startHr = datetime.datetime.strptime(start, "%Y-%m-%d")
        
    if end[-2:] == '00':
        endHr = datetime.datetime.strptime(end[:-6], "%Y-%m-%dT%H:%M:%S")
    elif end[-1] == 'Z':
        endHr = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%SZ")
    else: 
        endHr = datetime.datetime.strptime(end, "%Y-%m-%d")

    startTS = time.mktime(startHr.timetuple())
    endTS = time.mktime(endHr.timetuple())
    return (startTS, endTS)

def get_calendar_list_map(service):
    """Get the list of Calendar Names, and store their corresponding ids"""
    
    calendarMap = defaultdict()
    page_token = None
    
    calendars = (service.calendarList()
                        .list(pageToken = page_token).execute())
      
    for calendar in calendars['items']:
        id = calendar.get('id', None)
        summary = calendar.get('summary', None)
        calendarMap[summary] = id
    return calendarMap

def get_events_in_calendar(calendarName, startDate, endDate=None):
    """Get all the events in a calendar for a specific time period"""

    print '\nGet ' + calendarName + ' Events Since the beginning of the year.............'
    startDate = get_start_date(startDate)
    endDate = get_now_date()
    service = build_service()
    calendarMap = get_calendar_list_map(service)
    calendarId = calendarMap.get(calendarName)
    eventsResult = (service.events().list(
                                        calendarId = calendarId, 
                                        timeMin = startDate, 
                                        timeMax = endDate,
                                        maxResults = 1000, 
                                        singleEvents = True,
                                        orderBy = 'startTime')
                                    .execute())
    
    events = eventsResult.get('items', [])
    events_list = []

    if not events:
        print 'No events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        startTS, endTS = get_ts_from_datetime(start, end)
        
        duration = (endTS - startTS) / 60
        event_type = calendarName
        
        eventTitle = event['summary']
        event_name = ''.join([i if ord(i) < 128 else '' for i in eventTitle.replace(',','')])

        #print start[:10], duration, event_type, event_name
    
        events_list.append([start[:10], duration, event_type, event_name])
    return events_list

def write_events_to_csv(events_list):
    with open('events.csv', 'a') as events_csv:
        writer = csv.writer(events_csv)
        for each_event in events_list:
            writer.writerow(each_event)

def main():
    """Main Entry Point of the App"""

    service = build_service()
    calendarMap = get_calendar_list_map(service)

    for calendarName in calendarMap:
        events_list = get_events_in_calendar(calendarName, '2013-01-01')
        write_events_to_csv(events_list)

if __name__ == '__main__':
    main()
