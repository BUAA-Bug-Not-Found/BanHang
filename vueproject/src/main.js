import { createApp } from 'vue'
import App from './App.vue'
import axios from "axios";
import { createPinia } from "pinia";
import router from './router'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

let isLocal = false
axios.defaults.timeout = 10000;
//TODO:设置后端远程端口和本地端口
axios.defaults.baseURL = isLocal? 'http://127.0.0.1:8000/': 'http://127.0.0.1:8000/';

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

app.use(vuetify)

app.mount('#app')
