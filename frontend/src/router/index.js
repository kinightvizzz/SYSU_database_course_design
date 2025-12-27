import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import UserHome from "../views/UserHome.vue";
import StaffHome from "../views/StaffHome.vue";
import AdminHome from "../views/AdminHome.vue";
import Register from "../views/register.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/user", component: UserHome },
  { path: "/staff", component: StaffHome },
  { path: "/admin", component: AdminHome },
  { path: "/register", component: Register },
  {
    path: "/order/:orderId",
    component: () => import("../views/OrderDetail.vue"),
  },
  {
    path: "/staff/order/:orderId",
    component: () => import("../views/StaffOrderDetail.vue"),
  },
  {
    path: "/user/:userId",
    component: () => import("../views/UserDetail.vue"),
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
