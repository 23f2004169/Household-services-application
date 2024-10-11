import { createApp } from 'vue'
import './style.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import Button from 'primevue/button';
import Tooltip from 'primevue/tooltip';

const app = createApp(App)

app.use(router)
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.directive('tooltip', Tooltip);
app.component('Button', Button)
app.mount('#app')
