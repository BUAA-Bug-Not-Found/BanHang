import {createRouter, createWebHistory} from 'vue-router';

import HelpCenter from "@/components/HelpCenter/HelpCenter.vue";
import HomeIndex from "@/components/index.vue"
import QuesInfo from "@/components/HelpCenter/QuesInfo.vue";

const routes = [
    {
        path: '/',
        name: "index",
        component: HomeIndex,
        children: [
            {
                path: '/Helpcenter',
                name: "Helpcenter",
                component: HelpCenter
            },
            {
                path: '/QuesInfo/:qid',
                name: "QuesInfo",
                component: QuesInfo
            },
        ]
    },
]


const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    next()
})

export default router