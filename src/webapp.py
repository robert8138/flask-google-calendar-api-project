from flask import Flask
from flask import request
from flask import render_template

webapp = Flask(__name__)

data = [('Robert', 'Chang', '@rchang'),
        ('Simeon', 'Franklin', '@sfranklin'),
        ('Jack', 'Dorsey', '@jack')]

@webapp.route('/', methods=['GET','POST'])
def hello():
  return render_template('hello.html', greeting='hello')


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
