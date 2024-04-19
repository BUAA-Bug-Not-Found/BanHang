import {createRouter, createWebHistory} from 'vue-router';

import HelpCenter from "@/components/HelpCenter/HelpCenter.vue";

const routes = [
    { path: '/helpCenter', component: HelpCenter }
]


const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    next()
})

export default router