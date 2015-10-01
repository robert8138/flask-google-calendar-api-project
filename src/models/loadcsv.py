from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, create_session
import datetime
import csv

def load_csv_to_db(CSV_FILE):
  
  #CSV_FILE = 'events.csv'
  engine = create_engine('sqlite:///db/events_all_2014.sqlite3') # memory-only database

  table = None
  metadata = MetaData(bind=engine)


  with open(CSV_FILE) as f:
      # assume first line is header
      cf = csv.DictReader(f, 
                          fieldnames = ('date', 'duration', 'event_type', 'event_name'), 
                          delimiter=',')
      print "Ready to write into db..................................."
      for row in cf:
          if table is None:
              # create the table
              table = Table('events_full', metadata, 
                            Column('id', Integer, primary_key=True),
                            Column('date', Date),
                            Column('duration', Float),
                            Column('event_type', String),
                            Column('event_name', String)
                           )
              table.create()
          # insert data into the table
          date = row['date']
          duration = row['duration']
          event_type = row['event_type']
          event_name = row['event_name'].replace(',', '')
          year, month, day = [int(elem) for elem in date.split('-')]
          date = datetime.date(year, month, day)
          table.insert().values(date = date, 
                                duration = duration, 
                                event_type = event_type, 
                                event_name = event_name).execute()