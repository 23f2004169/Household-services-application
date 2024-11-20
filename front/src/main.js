// all configurations for frontend (sets up and initializes the Vue app )
import { createApp } from 'vue'
import './style.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js'; 
import App from './App.vue'
import router from './router'
import Datepicker from 'vue3-datepicker';

// Creates the Vue application instance with the App component as the root.
const app = createApp(App)
// Register Datepicker globally
app.component('Datepicker', Datepicker);
// Registers the router with the Vue application instance, enabling navigation and routing functionalities.
app.use(router)
// Mounts the Vue app to an HTML element  with the id "app"
app.mount('#app')
