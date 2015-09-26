DROP TABLE IF EXISTS events;
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    duration REAL,
    event_type TEXT,
    event_name TEXT 
);
