import { createApp } from 'vue'
import App from './App.vue'
import axios from "axios";
import { createPinia } from "pinia";
import router from './router'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css' // 引入vuetify icon
import VueDOMPurifyHTML from 'vue-dompurify-html'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'

// let isLocal = false
axios.defaults.timeout = 10000;
//TODO:设置后端远程端口和本地端口
axios.defaults.baseURL = "https://banhang.lyhtool.com:8000";
axios.defaults.withCredentials=true

const app = createApp(App)

//使用pinia进行状态管理
const pinia = createPinia();
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

app.use(vuetify).use(VueDOMPurifyHTML).use(ElementPlus)

app.mount('#app')
