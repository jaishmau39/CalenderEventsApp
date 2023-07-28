
#   Calender Events App

This is a calendar application built using Python (Flask) for the backend and Vue.js for the frontend. The application allows users to create, view, update and delete events on the calendar.

## Features
- Create new events with a title, date, and time.
- View events on the calendar with different views (month, week, day).
- Drag and drop events to reschedule them.
- Delete events by clicking on them.
## Dependencies

- Python
- Flask
- Flask-CORS
- sqlite3
- Vue.js
- FullCalendar (core, vue3, daygrid, timegrid, list, interaction)

## Installation

1. Clone the repository to your local machine.

```bash
  git clone https://github.com/jaishmau39/CalenderEventsApp.git
```

2. Backend Setup:
- Install Python.
- Install Flask and Flask-CORS using the following commands:
```bash
  pip install flask
  pip install -U flask-cors
```
- Go to the project directory and Navigate to the "CalenderEventsApplication" directory:

```bash
  cd CalenderEventsApp\CalenderEventsApplication
```

- Run the Flask backend server:
```bash
  python controller.py
```

3. Frontend Setup:

- Install Node.js and npm.
- Navigate to the "calendar-app" directory:
```bash
  cd calendar-app
```
- Install the required npm packages:
```bash
  npm install
```
- Start the Vue.js frontend development server

```bash
  npm run serve
```

4. Open your web browser and visit http://localhost:8080 to access the event calendar application.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
