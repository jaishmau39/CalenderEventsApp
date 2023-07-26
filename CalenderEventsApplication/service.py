from model import CalendarModel
from dto import EventDTO
from datetime import datetime

class CalendarService:
    def __init__(self):
        self.model = CalendarModel()


    # Creating events table in the database
    def create_tables(self):
        self.model.create_tables()

    def create_event(self, event_dto: EventDTO):
        
        if not event_dto.title or not event_dto.date or not event_dto.time:
            # Raise error if title, date or time is missing 
            raise ValueError("Missing required fields (title, date, or time)")
        return self.model.create_event(event_dto)


    def update_event(self, event_id, event_dto: EventDTO):
        
        # Check if event ID privided is a valid integer
        try:
            event_id = int(event_id)
        except ValueError:
            # Raise error is provided event Id is not an integer
            raise ValueError("Invalid event ID. ID must be an integer.")

        # Check if the event with the given ID exists in the database
        if not self.model.get_event_by_id(event_id):
            # Raise error if the event Id  privided does not exist in the database
            raise ValueError("Event with ID {} does not exist.".format(event_id))

        self.model.update_event(event_id, event_dto)


    def get_events(self):
        return self.model.get_events()

