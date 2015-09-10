from flask import Flask, request
from collections import namedtuple
webapp = Flask(__name__)

data = [('Robert', 'Chang', '@rchang'),
        ('Simeon', 'Franklin', '@sfranklin'),
        ('Jack', 'Dorsey', '@jack')]

@webapp.route('/', methods=['GET','POST'])
def hello_world():
  if request.method == 'POST':
    return 'Good Morning!' + request.form.get('username', '')
  else:
    return 'Hello World!'

@webapp.route('/users')
def users():
  rows = []
  for user in data:
    user_dict = dict(first=user[0], last=user[1], handle=user[2])
    rows.append("""<tr><td>{first}</td>
                   <td>{last}</td>
                   <td><a href="/users/{handle}">{handle}</a></td></tr>""".format(**user_dict))
  return "<table border=1>{}</table>".format("\n".join(rows))

@webapp.route('/users/<username>')
def user(username):
  rows = []
  for user in [user for user in data if user[-1]==username]:
    user_dict = dict(first=user[0], last=user[1], handle=user[2])
    rows.append("""<tr><td>{first}</td>
                       <td>{last}</td>
                       <td>{handle}</td></tr>""".format(**user_dict))
  return "<table border=1>{}</table>".format("\n".join(rows))

# @webapp.route('/users')
# @webapp.route('/users/<username>')
# def users(username=None):
#   if username:
#     users = [user for user in data if user[-1] == username]
#   else:
#     users = data
#   return "<br>".join([" ".join(user) for user in users])

if __name__ == '__main__':
  webapp.debug = True
  webapp.run()
