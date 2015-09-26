from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask.ext.cors import CORS
from models.models import *
import sqlite3
import datetime

webapp = Flask(__name__)
CORS(webapp)
webapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/events_all.sqlite3'
db.init_app(webapp)

# Regular Views
@webapp.route('/', methods=['GET','POST'])
def index():
  return render_template('index.html')

@webapp.route('/dbdisplay')
def display():
  return render_template("dbdisplay.html",
                         events = Events.query.all())  

@webapp.route('/dbdisplay/<event_type>')
def display_by_event_type(event_type):
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

# API endpoints
@webapp.route('/api/all')
def api_all():
  events = Events.query.all()
  return jsonify(json_list = [event.serialize for event in events])

@webapp.route('/api/<event_type>')
def api_by_event_type(event_type):
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
  return render_template("bars.html")

@webapp.route('/calendar')
def plot_d3_calendar():
  return render_template("calendar.html")


if __name__ == '__main__':
  webapp.debug = True
  webapp.run()
