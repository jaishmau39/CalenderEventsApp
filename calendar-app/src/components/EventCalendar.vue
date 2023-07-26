
<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'

export default {
  components: {
  // make the <FullCalendar> tag available
    FullCalendar 
  },
  data() {
    return {
      calendarOptions: {
        plugins: [ dayGridPlugin, timeGridPlugin, interactionPlugin ],
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        initialView: 'dayGridMonth',
        selectable: true,
        events: []
      }
    }
  },
  mounted() {
    // Get list of events from call to Api endpoint
    this.fetchEvents();
  },
  methods: {
    async fetchEvents() {
      try {
        const response = await fetch('http://localhost:5000/events');
        const data = await response.json();

        // Extracting 'title' and 'date' properties from list of events
        if (Array.isArray(data)) {
          const events = data.map(item => ({ title: item.title, date: item.date }));
          this.calendarOptions.events = events;
        }
      } catch (error) {
        console.error('Error fetching events:', error);
      }
    }
  }
}
</script>

<template>
  <FullCalendar :options="calendarOptions" />
</template>