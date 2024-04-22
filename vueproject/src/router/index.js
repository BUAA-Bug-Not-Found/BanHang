import {createRouter, createWebHistory} from 'vue-router';

import HelpCenter from "@/components/HelpCenter/HelpCenter.vue";
import BlogList from "@/components/AnonymousBlog/BlogList.vue";
import BlogView from "@/components/AnonymousBlog/BlogView.vue";
import BlogNew from "@/components/AnonymousBlog/BlogNew.vue";
import HomeIndex from "@/components/index.vue";

const routes = [
    { path: '/helpCenter', component: HelpCenter },
    { path: '/blogList', component: BlogList },
    { path: '/blogView/:id', component: BlogView},
    { path: '/blogNew', component: BlogNew},
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
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    next()
})

export default router