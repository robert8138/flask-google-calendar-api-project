from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from apiclient import discovery
from oauth2client import client
from flask.ext.cors import CORS
from oauth2client import client
from sqlalchemy import * 
from models.models import *
from models.calendarapi import *
from models.loadcsv import *
import sqlite3
import datetime
import os
import flask
import httplib2

webapp = Flask(__name__)
webapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/events_all_2014.sqlite3'
webapp.config['SESSION_TYPE'] = 'filesystem'
webapp.config['SECRET_KEY'] = 'super secret key'
CORS(webapp)
db.init_app(webapp)

# event_type_map = {'studytime': 'Study Time',
#                   'outsidereading': 'Outside Reading',
#                   'birthdays': 'Birthdays',
#                   'misc': 'Misc',
#                   'deadline': 'Deadline',
#                   'exercise': 'Exercise'}

@webapp.route('/', methods=['GET','POST'])
def index():
  return render_template('index.html')

@webapp.route('/login')
def login():
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    if os.path.exists("events.csv") and os.path.exists("db/events_all_2014.sqlite3"):
      os.remove("events.csv")
      os.remove("db/events_all_2014.sqlite3")
    
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http = http_auth)
    global calendarMap
    calendarMap = get_calendar_list_map(service)

    for calendarName in calendarMap:
        print "processing..." + calendarName + ".........."
        events_list = get_events_in_calendar(calendarName, calendarMap, service, '2014-01-01')
        write_events_to_csv(events_list)
    
    load_csv_to_db("events.csv")
    str = '\n'.join([calendar for calendar in calendarMap])

    return str

@webapp.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope='https://www.googleapis.com/auth/calendar',
      redirect_uri=flask.url_for('oauth2callback', _external=True))

  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('finishoauth'))

@webapp.route('/finishoauth')
def finishoauth():
  return render_template('finishoauth.html')

# Regular Views
@webapp.route('/dbdisplay')
def display():
  return render_template("dbdisplay.html",
                         events = Events.query.all())  

@webapp.route('/dbdisplay/<event_type>')
def display_by_event_type(event_type):
  # event_type = event_type_map[event_type]
  return render_template("dbdisplay.html",
                         events = Events.query.filter_by(event_type = event_type).all()) 

@webapp.route('/dbdisplay/<year>/<month>/<day>')
def display_by_date(year, month, day):
  date = datetime.date(int(year), int(month), int(day))
  return render_template("dbdisplay.html",
                         events = Events.query.filter_by(date = date).all())   

@webapp.route('/dbdisplay/duration/<duration>')
def display_duration_greater_than(duration):
  return render_template("dbdisplay.html",
                         events = Events.query.filter(Events.duration > float(duration)).all())

@webapp.route('/distinct')
def distinct():
  #TODO: load all the calendarNames from the db using SQLAlchemy
  return ''.join([event_type for event_type in event_types])

# API endpoints
@webapp.route('/api/all')
def api_all():
  events = Events.query.all()
  return jsonify(json_list = [event.serialize for event in events])

@webapp.route('/api/<event_type>')
def api_by_event_type(event_type):
  # event_type = event_type_map[event_type]
  events = Events.query.filter_by(event_type = event_type).all()
  return jsonify(json_list = [event.serialize for event in events])

@webapp.route('/api/<year>/<month>/<day>')
def api_by_date(year, month, day):
  date = datetime.date(int(year), int(month), int(day))
  events = Events.query.filter_by(date = date).all()
  return jsonify(json_list = [event.serialize for event in events])

@webapp.route('/api/duration/<duration>')
def api_by_duration(duration):
  events = Events.query.filter(Events.duration > float(duration)).all()
  return jsonify(json_list = [event.serialize for event in events])

# Plotting endpoints
@webapp.route('/bars')
def plot_d3_bars():
  return render_template("bars.html", calendarMap = calendarMap)

@webapp.route('/calendar')
def plot_d3_calendar():
  return render_template("calendar.html", calendarMap = calendarMap)

@webapp.route('/test')
def test():
  str = '\n'.join([calendar for calendar in calendarMap])
  return str

if __name__ == '__main__':
  
  # EVENTS_CSV_FILE = "events.csv"
  # DB_FILE = "db/events_all_2014.sqlite3"
  
  # if not os.path.exists(EVENTS_CSV_FILE) and not os.path.exists(DB_FILE):

  #   service = build_service()
  #   calendarMap = get_calendar_list_map(service)

  #   for calendarName in calendarMap:
  #       events_list = get_events_in_calendar(calendarName, calendarMap, service, '2014-01-01')
  #       write_events_to_csv(events_list)
    
  #   load_csv_to_db("events.csv")

  webapp.debug = True
  webapp.run()