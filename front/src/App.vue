<script>
import register from './components/register.vue';

export default {
  components: {
    register
  }
}
</script>

<template>
  <div id="app">
    <register />
    <router-view></router-view> 
  </div>
</template>

<style scoped>
</style>

