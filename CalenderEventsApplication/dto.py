
# Class representing event object in the Calender
class EventDTO:
    def __init__(self, title, date, time, event_id=None):
        self.id = event_id
        self.title = title
        self.date = date
        self.time = time

