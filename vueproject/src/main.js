import {createApp} from 'vue'
import App from './App.vue'
import axios from "axios";
import {createPinia} from "pinia";
import router from './router'
import 'vuetify/styles'
import {createVuetify} from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css' // 引入vuetify icon
import VueDOMPurifyHTML from 'vue-dompurify-html'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

router.beforeEach((to, from, next) => {
    // 如果当前路由为'/'，则跳转到'/blogList'路由
    if (to.path === '/') {
        next('/blogList');
    } else {
        next();
    }
});

// let isLocal = false
axios.defaults.timeout = 10000;
//TODO:设置后端远程端口和本地端口
axios.defaults.baseURL = "https://banhang.lyhtool.com:8000";
axios.defaults.withCredentials = true

const app = createApp(App)

//使用pinia进行状态管理
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
app.use(pinia)

app.use(router)


//引用vuetify3 组件库
const vuetify = createVuetify({
    components,
    directives,
})

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

import 'viewerjs/dist/viewer.css'
import VueViewer from 'v-viewer'

app.use(VueViewer, {
    defaultOptions: {
        zIndex: 1000000
    }
})

app.use(vuetify).use(VueDOMPurifyHTML, {
    default: {
        ADD_TAGS: ['iframe'],
    }}).use(ElementPlus)

app.mount('#app')



