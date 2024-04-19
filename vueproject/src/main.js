import { createApp } from 'vue'
import App from './App.vue'
import axios from "axios";
import { createPinia } from "pinia";
import router from './router'

let isLocal = false
axios.defaults.timeout = 10000;
//TODO:设置后端远程端口和本地端口
axios.defaults.baseURL = isLocal? 'http://127.0.0.1:8000/': 'http://127.0.0.1:8000/';

const app = createApp(App)

//使用pinia进行状态管理
const pinia = createPinia();
app.use(pinia)

app.use(router)

app.mount('#app')
