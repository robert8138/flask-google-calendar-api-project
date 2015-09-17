from flask import Flask
from flask import request
from flask import render_template
from models import *
import sqlite3
import datetime

webapp = Flask(__name__)
webapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events_all.sqlite3'
db.init_app(webapp)

@webapp.route('/', methods=['GET','POST'])
def index():
  db = sqlite3.connect("events.sqlite3")
  cur = db.execute('select * from events')
  rows = cur.fetchall()
  return render_template('index.html', rows = rows)

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

if __name__ == '__main__':

  webapp.debug = True
  webapp.run()
