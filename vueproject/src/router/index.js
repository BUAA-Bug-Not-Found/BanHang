import {createRouter, createWebHashHistory} from 'vue-router';

import HelpCenter from "@/components/HelpCenter/HelpCenter.vue";
import ToolBox from "@/components/ToolBox/ToolBox.vue"
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