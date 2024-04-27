// 路由:
// import .vue
// routes

// const routes = [
//     { path: '/helpCenter', component: HelpCenter },
//     { path: '/loginPage', component: LoginPage},
//     { path: '/registerPage', component: RegisterPage},
//     { path: '/resetPassword', component: ResetPassword}
// ]

import {createRouter, createWebHistory} from 'vue-router';

import HelpCenter from "@/components/HelpCenter/HelpCenter.vue";
import HomeIndex from "@/components/index.vue";
import PersonalCenter from "@/components/PersonalCenter/PersonalCenter";
import LearnScroll from "@/components/test/LearnScroll.vue";
import RegisterPage from "@/components/AccountManagement/RegisterPage";
import EditPersonalInfo from '@/components/PersonalCenter/EditPersonalInfo.vue';
import LoginPage from '@/components/AccountManagement/LoginPage';
import OthersCenter from '@/components/PersonalCenter/OthersCenter.vue';
import InterestList from '@/components/PersonalCenter/InterestList.vue';

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
                path: '/personalCenter',
                name: 'personalCenter',
                component: PersonalCenter
            },
            {
                path: '/editPersonalInfo',
                name: 'editPersonalInfo',
                component: EditPersonalInfo
            },
            {
                path: '/learnScroll',
                name: '/learnScroll',
                component: LearnScroll
            }, 
            {
                path: '/registerPage',
                name: "registerPage",
                component: RegisterPage
            },
            {
                path: '/loginPage',
                name: 'loginPage',
                component: LoginPage
            },
            {
                path: '/othersCenter',
                name: 'othersCenter',
                component: OthersCenter
            },
            {
                path: '/interestList',
                name: 'interestList',
                component: InterestList
            }
        ]
    },
    // {
        
    // }
]


const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    next()
})

export default router