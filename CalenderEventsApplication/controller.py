from flask import Flask, request, jsonify
from service import CalendarService
from dto import EventDTO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
service = CalendarService()

# Get all calender events
@app.route('/events', methods=['GET'])
def get_events():
    events = service.get_events()

    # Convert events to a list of dictionaries (JSON serializable)
    event_list = []
    for event in events:
        event_dict = {
            'id': event.id,
            'title': event.title,
            'date': event.date,
            'time': event.time
        }
        event_list.append(event_dict)
    return jsonify(event_list)

# Create a new event
@app.route('/events', methods=['POST'])
def create_event():
  
    data = request.get_json()

    try:
        title = data['title']
        date = data['date']
        time = data['time']

        event_dto = EventDTO(title=title, date=date, time=time)
        service.create_event(event_dto)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

    return jsonify({"message": "Event created successfully"})



# Update an event using event Id
@app.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
   
    data = request.get_json()

    try:
        title = data['title']
        date = data['date']
        time = data['time']

        event_dto = EventDTO(title=title, date=date, time=time)
        service.update_event(event_id, event_dto)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except EventNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

    return jsonify({"message": "Event updated successfully"})

# Delete an event using  the event Id
@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        service.delete_event_by_id(event_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except EventNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

    return jsonify({"message": "Event deleted successfully"})

if __name__ == '__main__':
    # Create  events table in database
    service.create_tables()
    app.run(debug=True)
