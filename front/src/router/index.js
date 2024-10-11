import { createRouter, createWebHistory } from 'vue-router';
import LandPage from '../views/LandPage.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: LandPage
        },
        {
            path: '/register', // New route for the register page
            name: 'register',  // Give it a unique name
            component: register // The component to render
        }
    ]
})

export default router;