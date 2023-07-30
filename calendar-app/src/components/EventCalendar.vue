<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { format, utcToZonedTime } from 'date-fns-tz';


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
        allDaySlot: true,
        initialView: 'dayGridMonth',
        selectable: true,
        editable: true,
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
          const events = data.map(item => {
          // If the event has no time, make it an all-day event
          const start = item.time ? item.date + 'T' + item.time : item.date;
          return { id: item.id, title: item.title, start: start };
        });
        this.calendarOptions.events = events;
        }
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    },
    async createEvent() {
      try {


        // Check if time is provided, otherwise set it to an empty string
        if (!this.newEvent.time) {
          this.newEvent.time = '';
        }

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
        // window.alert('Event successfully created!');
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

    // Set date to local timezone
    const localTimeZone = 'America/New_York';
    const zonedDate = utcToZonedTime(info.event.start, localTimeZone);

    // Format date and time to ISO string with adjusted timezone
    const formattedDate = format(zonedDate, 'yyyy-MM-dd', { timeZone: localTimeZone });
    const formattedTime = format(zonedDate, 'HH:mm:ss', { timeZone: localTimeZone });

    const eventToUpdate = {
      title: info.event.title,
      date: formattedDate,
      time: formattedTime, // Include the formatted time in the eventToUpdate object
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

          <button type="submit" class="btn btn-formal">Submit</button>
        </form>
      </div>


      <div class="instructions">
        <h3>Instructions</h3>
        <ul>
          <li>Drag and drop event to rechedule.</li>
          <li>Click on an event to delete it.</li>
        </ul>
      </div>

    </div>
    <div class="main-content">
      <!-- FullCalendar component -->
      <FullCalendar :options="calendarOptions" />
    </div>
  </div>
</template>

<style>
@import './styles.css';
</style>

