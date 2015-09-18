from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Float

db = SQLAlchemy()

class Events(db.Model):
	__tablename__ = 'events_full'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	duration = Column(Float)
	event_type = Column(String)
	event_name = Column(String)

	def __init__(self, date, duration, event_type, event_name):
		self.date = date
		self.duration = duration
		self.event_type = event_type
		self.event_name = event_name

	def __repr__(self):
		return '<Events %r>' % (self.id)

	@property 
	def serialize(self):
		'''return as a json object so we can use it in RESTful API'''
		return {'id': self.id, 
		        'date': self.date.strftime("%Y-%m-%d"), 
		        'duration': self.duration, 
		        'event_type': self.event_type, 
		        'event_name': self.event_name }
		
