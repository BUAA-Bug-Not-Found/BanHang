import {createRouter, createWebHashHistory} from 'vue-router';

import HelpCenter from "@/components/HelpCenter/HelpCenter.vue";
import BlogList from "@/components/AnonymousBlog/BlogList.vue";
import BlogView from "@/components/AnonymousBlog/BlogView.vue";
import BlogNew from "@/components/AnonymousBlog/BlogNew.vue";
import HomeIndex from "@/components/index.vue";
import ToolBox from "@/components/ToolBox/ToolBox.vue";
import QuesInfo from "@/components/HelpCenter/QuesInfo.vue";


const routes = [
    // { path: '/blogView/:id', component: BlogView},
    // { path: '/blogNew', component: BlogNew},
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
            },
            {
                path: '/blogList',
                name: "blogList",
                component: BlogList
            },
            {
                path: '/blogView/:id',
                name: "blogView",
                component: BlogView
            },
            {
                path: '/blogNew',
                name: "blogNew",
                component: BlogNew
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