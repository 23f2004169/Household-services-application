// all configurations for frontend
import { createApp } from 'vue'
import './style.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import App from './App.vue'
import router from './router'
import Datepicker from 'vue3-datepicker';


const app = createApp(App)

app.use(router)

app.mount('#app')