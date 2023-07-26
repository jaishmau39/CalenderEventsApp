import sqlite3
from dto import EventDTO

class CalendarModel:
    # Setting database name to events.db
    def __init__(self, db_name='events.db'):
        self.db_name = db_name

    def create_tables(self):

        # Connect to the events database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create events table 
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL
            )
        ''')

        conn.commit()

        # Close the database connection
        conn.close()

        print("Database tables created successfully!")

    def create_event(self, event_dto: EventDTO):
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Inserting new event into events table
        cursor.execute('''
            INSERT INTO events (title, date, time)
            VALUES (?, ?, ?)
        ''', (event_dto.title, event_dto.date, event_dto.time))

        conn.commit()

        # Get the last inserted event Id and set it to event object
        event_id = cursor.lastrowid
        event_dto.id = event_id

        conn.close()

        return event_dto

    def get_event_by_id(self, event_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Getting event by Id
        cursor.execute('SELECT * FROM events WHERE id=?', (event_id,))
        event = cursor.fetchone()

        conn.close()

        if not event:
            return None

        event_dto = EventDTO(event_id=event[0], title=event[1], date=event[2], time=event[3])
        return event_dto

    def update_event(self, event_id, event_dto: EventDTO):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Update event details in the events table by the event Id
        cursor.execute('''
            UPDATE events
            SET title=?, date=?, time=?
            WHERE id=?
        ''', (event_dto.title, event_dto.date, event_dto.time, event_id))

        conn.commit()
        conn.close()



    def get_events(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Get all events from events table
        cursor.execute('SELECT * FROM events')
        events = cursor.fetchall()

        # Events fetched from events table converted to list of event objects
        event_dtos = []
        for event in events:
            event_dto = EventDTO(event_id=event[0], title=event[1], date=event[2], time=event[3])
            event_dtos.append(event_dto)

        conn.close()

        return event_dtos


