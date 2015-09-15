from flask import Flask
from flask import request
from flask import render_template
import sqlite3

webapp = Flask(__name__)

data = [('Robert', 'Chang', '@rchang'),
        ('Simeon', 'Franklin', '@sfranklin'),
        ('Jack', 'Dorsey', '@jack')]

@webapp.route('/', methods=['GET','POST'])
def index():
  db = sqlite3.connect("events.sqlite3")
  cur = db.execute('select * from events')
  rows = cur.fetchall()
  return render_template('hello.html', rows = rows)

@webapp.route('/users')
def users():
  return render_template("users.html", users = data)

@webapp.route('/users/<username>')
def user(username):
  rows = []
  users = [user for user in data if user[-1]==username]
  return render_template("user.html", users = users)

if __name__ == '__main__':
  webapp.debug = True
  webapp.run()
