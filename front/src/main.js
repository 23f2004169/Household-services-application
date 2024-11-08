// all configurations for frontend
import { createApp } from 'vue'
import './style.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import App from './App.vue'
import router from './router'
// import PrimeVue from 'primevue/config';
// import Aura from '@primevue/themes/aura';
// import 'primeicons/primeicons.css'
// import Button from 'primevue/button';
// import Tooltip from 'primevue/tooltip';
// import Menubar from 'primevue/menubar';
// import InputText from 'primevue/inputtext';
// import Badge from 'primevue/badge';
// import Avatar from 'primevue/avatar';

const app = createApp(App)

app.use(router)
// app.use(PrimeVue, {
//     theme: {
//         preset: Aura
//     }
// });
 
// app.directive('tooltip', Tooltip);
// app.component('Button', Button)
// app.component('InputText', InputText)
// app.component('Badge', Badge)
// app.component('Avatar', Avatar)
// app.component('Menubar', Menubar)
app.mount('#app')