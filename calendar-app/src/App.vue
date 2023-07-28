<template>
  <EventCalendar msg="Welcome to Your Events App"/>
</template>

<script>
import EventCalendar from './components/EventCalendar.vue'

export default {
  name: 'App',
  components: {
    EventCalendar
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0;
  padding: 0;
  height: 100%;
}
</style>
