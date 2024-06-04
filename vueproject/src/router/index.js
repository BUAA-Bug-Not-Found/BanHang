// 路由:
// import .vue
// routes

// const routes = [
//     { path: '/helpCenter', component: HelpCenter },
//     { path: '/loginPage', component: LoginPage},
//     { path: '/registerPage', component: RegisterPage},
//     { path: '/resetPassword', component: ResetPassword}
// ]

import HelpCenter from "@/components/HelpCenter/HelpCenter.vue";
import HomeIndex from "@/components/index.vue";
import PersonalCenter from "@/components/PersonalCenter/PersonalCenter";
import LearnScroll from "@/components/test/LearnScroll.vue";
import RegisterPage from "@/components/AccountManagement/RegisterPage";
import EditPersonalInfo from '@/components/PersonalCenter/EditPersonalInfo.vue';
import LoginPage from '@/components/AccountManagement/LoginPage';
import OthersCenter from '@/components/PersonalCenter/OthersCenter.vue';
import InterestList from '@/components/PersonalCenter/InterestList.vue';
import BlogList from "@/components/AnonymousBlog/BlogList.vue";
import BlogView from "@/components/AnonymousBlog/BlogView.vue";
import BlogNew from "@/components/AnonymousBlog/BlogNew.vue";
import QuesInfo from "@/components/HelpCenter/QuesInfo.vue";
import MessageContainer from '@/components/Message/MessageContainer.vue';
import {createRouter, createWebHashHistory} from 'vue-router';
import ResetPassword from "@/components/AccountManagement/ResetPassword.vue";
import SearchList from "@/components/AdvanceSearch/SearchList.vue";
import SpocIndex from "@/components/ToolBox/Spoc/SpocIndex.vue";
import VacentIndex from "@/components/ToolBox/VacentClassroom/VacentIndex.vue";

import ToolCenter from '@/components/ToolCenter/ToolCenter.vue';
const routes = [
    {
        path: '/',
        name: "index",
        component: HomeIndex,
        children: [
            {
                path: '/Helpcenter/:tagId',
                name: "Helpcenter",
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
                path: '/othersCenter/:id',
                name: 'othersCenter',
                component: OthersCenter
            },
            {
                path: '/interestList',
                name: 'interestList',
                component: InterestList
            },
            {
                path: '/QuesInfo/:qid/:opId',
                name: "QuesInfo",
                component: QuesInfo
            },
            {
                path: '/blogList/:tagId',
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
            },
            {
                path: '/resetPassword',
                name: "resetPassword",
                component: ResetPassword
            },
            {
                path: '/message',
                name: "message",
                component: MessageContainer
            },
            {
                path: '/searchList/:keywords',
                name: "searchList",
                component: SearchList
            },
            {
                path: '/toolCenter',
                name: 'toolCenter',
                component: ToolCenter,
            },
            {
                path: '/spoc',
                name: 'spoc',
                component: SpocIndex
            },
            {
                path: '/vacentClassroom',
                name: 'vacentClassroom',
                component: VacentIndex
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
