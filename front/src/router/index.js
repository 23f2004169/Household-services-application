import { createRouter, createWebHistory } from 'vue-router';
import LandPage from '../views/LandPage.vue';
// import register from '../components/register.vue'; 
// import Register from '../views/Register.vue'; 


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: LandPage
     }
        // {
        //     path: '/register ', 
        //     name: 'register',  
        //     component: register 
        // }
        
        
        
    ]
})

export default router;