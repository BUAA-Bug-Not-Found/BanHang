import {createRouter, createWebHashHistory} from 'vue-router';

import HelpCenter from "@/components/HelpCenter/HelpCenter.vue";
import ToolBox from "@/components/ToolBox/ToolBox.vue"
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
            {
                path: '/tool_box',
                name: 'tool_box',
                component: ToolBox
            }
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