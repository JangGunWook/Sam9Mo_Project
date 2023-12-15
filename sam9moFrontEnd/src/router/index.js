import {createRouter, createWebHashHistory} from "vue-router";
import Dashboard from "@/views/Dashboard.vue";
import Billing from "@/views/News.vue";
// import VirtualReality from "@/views/VirtualReality.vue";
import Profile from "@/views/Profile.vue";
import Rtl from "@/views/Rtl.vue";
import SignIn from "@/views/SignIn.vue";
import SignUp from "@/views/SignUp.vue";
import Tables from "@/views/Tables.vue";


const routes = [
    {
        path: "/",
        name: 'Home',
        component: SignIn,
    },
    // {
    //     path: "/",
    //     name: "/",
    //     redirect: "/signin",
    // },
    {
        path: "/dashboard",
        name: "Dashboard",
        component: Dashboard,
    },
    {
        path: "/tables",
        name: "Tables",
        component: Tables,
    },
    {
        path: "/billing",
        name: "Billing",
        component: Billing,
    },
    // {
    //     path: "/virtual-reality",
    //     name: "Virtual Reality",
    //     component: VirtualReality,
    // },
    {
        path: "/profile",
        name: "Profile",
        component: Profile,
    },
    {
        path: "/rtl-page",
        name: "Rtl",
        component: Rtl,
    },
    {
        path: "/sign-in",
        name: "Sign In",
        component: SignIn,
    },
    {
        path: "/sign-up",
        name: "Sign Up",
        component: SignUp,
    },


];

const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes,
    linkActiveClass: "active",
});

export default router;
