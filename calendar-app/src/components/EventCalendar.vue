<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'

export default {
  components: {
    FullCalendar
  },
  data() {
    return {
      calendarOptions: {
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        eventDrop: this.onEventDrop,
        allDaySlot: false,
        initialView: 'dayGridMonth',
        selectable: true,
        editable: true,
        dragRevertDuration:'00:00:08',
        events: []
      },
      newEvent: {
        title: '',
        date: '',
        time: ''
      }
    };
  },
  mounted() {
    this.fetchEvents();
    this.calendarOptions.eventClick = this.onEventClick;
  },
  methods: {
    async fetchEvents() {
      try {
        const response = await fetch('http://localhost:5000/events');
        const data = await response.json();

        if (Array.isArray(data)) {
          const events = data.map(item => ({  id: item.id, title: item.title,  start: item.date + 'T' + item.time }));
          this.calendarOptions.events = events;
        }
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    },
    async createEvent() {
      try {
        const response = await fetch('http://localhost:5000/events', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.newEvent)
        });

        if (response.ok) {
          // Event created successfully, update the calendar
          await this.fetchEvents();
          this.resetForm();
           // Display event creation success message
        window.alert('Event successfully created!');
        } else {
          console.error('Failed to create event.');
        }
      } catch (error) {
        console.error('Error creating event:', error);
      }
    },
    
    async onEventDrop(info) {
    try {
      const eventId = info.event.id;
      console.log('Event ID:', eventId);
      const eventToUpdate = {
        title: info.event.title,
        // Extract YYYY-MM-DD from ISO string
        date: info.event.start.toISOString().substr(0, 10), 
        // Extract HH:mm from ISO string
        time: info.event.start.toISOString().substr(11, 5), 
      };

      const response = await fetch(`http://localhost:5000/events/${eventId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(eventToUpdate)
      });

      if (response.ok) {
        // Event updated successfully, update the calendar
        await this.fetchEvents();
      } else {
        console.error('Failed to update event.');
      }
    } catch (error) {
      console.error('Error updating event:', error);
    }
  },
  
    onEventClick(eventClickInfo) {
    const eventId = eventClickInfo.event.id;

    // Show confirmation popup
    if (window.confirm('Are you sure you want to delete this event?')) {
      this.deleteEvent(eventId);
    }
  },

  async deleteEvent(eventId) {
    try {
      const response = await fetch(`http://localhost:5000/events/${eventId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        // Event deleted successfully, update the calendar
        await this.fetchEvents();
      } else {
        console.error('Failed to delete event.');
      }
    } catch (error) {
      console.error('Error deleting event:', error);
    }
  },
    resetForm() {
      this.newEvent.title = '';
      this.newEvent.date = '';
      this.newEvent.time = '';
    }
  }
}
</script>

<template>
  <div class="sidebar-layout">
    <div class="sidebar">
      <div class="form-container">
        <h3>Create Event</h3>
        <form @submit.prevent="createEvent">
          <div class="form-group">
            <label for="title">Title: </label>
            <input type="text" class="form-control" id="title" v-model="newEvent.title" required>
          </div>

          <div class="form-group">
            <label for="date">Date: </label>
            <input type="date" class="form-control" id="date" v-model="newEvent.date" required>
          </div>

          <div class="form-group">
            <label for="time">Time: </label>
            <input type="time" class="form-control" id="time" v-model="newEvent.time" >
          </div>

          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
    <div class="main-content">
      <!-- FullCalendar component -->
      <FullCalendar :options="calendarOptions" />
    </div>
  </div>
</template>

<style>
/* Custom CSS for the sidebar layout */
.sidebar-layout {
  display: flex;
  min-height: 100%;
  font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
  font-size: 14px;
}

.sidebar {
  
  width: 300px;
  line-height: 1.5;
  background: #eaf9ff;
  border-right: 1px solid #d3e2e8;
}

.main-content {
  flex-grow: 1;
  padding: 3em;
}


.fc { /* the calendar root */
  max-width: 1100px;
  margin: 0 auto;
}

h3 {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
}


.form-container {
}

.form-group {
  margin-bottom: 15px;
}


.form-control {
}

body {
  margin: 0;
  padding: 0;
}
</style>





