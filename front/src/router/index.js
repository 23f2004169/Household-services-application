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
    },
    {
      path: "/prof_dashboard",
      name: "ProfDash",
      component:ProfDash,
    },
  ],
});

export default router;

//path route, variable name, imported name -- exported name --component
//schema ,fetch exist back--front , db query
