import os
import httplib2
import oauth2client
import datetime
import time
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
    """
    Return a datetime object of current time 
    """
    return (datetime.datetime.utcnow()
                  .isoformat() + 'Z')

def get_end_date():
    pass

def get_calendar_list_map(service):
    
    calendarMap = defaultdict()
    page_token = None
    
    calendars = (service.calendarList()
                          .list(pageToken = page_token).execute())
      
    for calendar in calendars['items']:
        id = calendar.get('id', None)
        summary = calendar.get('summary', None)
        calendarMap[summary] = id
        #print summary + " | " + calendarMap[summary]
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

    if not events:
        print 'No events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        eventTitle = event['summary']
        
        # if start[-2:] == '00':
        #     startHr = datetime.datetime.strptime(start[:-6], "%Y-%m-%dT%H:%M:%S")
        # else:
        #     startHr = datetime.datetime.strptime(start, "%Y-%m-%d")
        
        # if end[-2:] == '00':
        #     endHr = datetime.datetime.strptime(end[:-6], "%Y-%m-%dT%H:%M:%S")
        # else: 
        #     endHr = datetime.datetime.strptime(end, "%Y-%m-%d")

        # startTS = time.mktime(startHr.timetuple())
        # endTS = time.mktime(endHr.timetuple())
        # hrSpent = (endTS - startTS) / 60

        print eventTitle

def main():
    """Main Entry Point of the App"""

    service = build_service()
    calendarMap = get_calendar_list_map(service)

    for calendarName in calendarMap:
        get_events_in_calendar(calendarName, '2015-01-01')    

if __name__ == '__main__':
    main()
