import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import RegisterCust from "../views/RegisterCust.vue";
import AdminDash from "../views/AdminDash.vue";
import LoginView from "../views/LoginView.vue";
import CustDash from  "../views/CustDash.vue"
import ProfDash from  "../views/ProfDash.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "HomeView",
      component: HomeView,
    },
    {
      path: "/register_cust",
      name: "RegisterCust",
      component: RegisterCust,
    },
    {
      path: "/register_prof",
      name: "RegisterProf",
      component: () => import("../views/RegisterProf.vue"),
    },
    {
      path: "/login",
      name: "LoginView",
      component: LoginView,
    },
    {
      path: "/admin_dashboard",
      name: "AdminDash",
      component: AdminDash,
    },
    {
      path: "/cust_dashboard",
      name: "CustDash",
      component:CustDash,
      props: (route) => ({ email: route.query.email })
    },
    {
      path: "/prof_dashboard",
      name: "ProfDash",
      component:ProfDash,
      props: (route) => ({ email: route.query.email })

    },
    { path: '/services/:category',
      name: 'CustServices',
      component:()=> import("../views/CustServices.vue"),
      props: (route) => ({ category: route.params.category, email: route.query.email })
    },
    {
      path:'/admin_summary',
      name:'AdminSummary',
      component:()=> import("../views/AdminSummary.vue"),
    },
    { 
      path: '/cust_summary',
      name:'CustSummary',
      component:()=> import("../views/CustSummary.vue"),
      props: (route) => ({ email: route.query.email })
    },
    {
      path: '/prof_summary',
      name:'ProfSummary',
      component:()=> import("../views/ProfSummary.vue"),
      props: (route) => ({ email: route.query.email })
    },
    {
      path:'/cust_search',
      name:'CustSearch',
      component:()=> import("../views/CustSearch.vue"), 
      props: (route) => ({ email: route.query.email })
    },
    {
      path:'/prof_search',
      name:'ProfSearch',
      component:()=> import("../views/ProfSearch.vue"),
      props: (route) => ({ email: route.query.email })
    },
    {
      path:'/admin_search',
      name:'AdminSearch',
      component:()=> import("../views/AdminSearch.vue"),
    },
    {path:'/extended_view',
      name:'ExtendedView',
      component:()=> import("../views/ExtendedView.vue"),
    }

  ],

});

export default router;

//path route, variable name, imported name -- exported name --component
//schema ,fetch exist back--front , db query
