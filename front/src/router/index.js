import { createRouter, createWebHistory } from 'vue-router';
import LandPage from '../views/LandPage.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: LandPage
        }
    ]
})

export default router;