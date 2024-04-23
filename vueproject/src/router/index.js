import {createRouter, createWebHashHistory} from 'vue-router';

import HelpCenter from "@/components/HelpCenter/HelpCenter.vue";
import HomeIndex from "@/components/index.vue"

const routes = [
    {
        path: '/',
        name: "index",
        component: HomeIndex,
        children: [
            {
                path: '/help_center',
                name: "help_center",
                component: HelpCenter
            },
        ]
    },
]


const router = createRouter({
    history: createWebHashHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    next()
})

export default router