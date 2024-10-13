import { createRouter, createWebHistory } from 'vue-router';
import LandPage from '../views/LandPage.vue';
import register from '../views/Register.vue'; 
import Admindash from '../views/Admindashboard.vue'
import Login from '../views/Login.vue'; 


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: LandPage
     }
    ,{
            path: '/register', 
            name: 'Register',  
            component: register 
        }
    ,{
        path:'/register_prof',
        name:'register_prof',
        component: () => import('../views/register_prof.vue')    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path:'/admin_dashboard',
        name:'Admindash',
        component:Admindash
    } 
        
        
    ]
})

export default router;

//path route, variable name, imported name -- exported name --component 
//schema ,fetch exist back--front , db query 