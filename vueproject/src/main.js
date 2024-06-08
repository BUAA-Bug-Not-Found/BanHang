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
        next('/blogList/-1');
    } else {
        next();
    }
});

router.afterEach( () => {
    setTimeout(()=>{
        var _hmt = _hmt || [];
        (function() {
            //每次执行前，先移除上次插入的代码
            document.getElementById('baidu_sdk') && document.getElementById('baidu_sdk').remove();
            var hm = document.createElement("script");
            hm.src = "https://hm.baidu.com/hm.js?68c71c552e46ad5e9749315567f36a65";
            hm.id = "baidu_sdk"
            var s = document.getElementsByTagName("script")[0];
            s.parentNode.insertBefore(hm, s);
        })();
    },0);
} );

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
import userStateStore from './store';
import { showTip, tryLogin } from './components/AccountManagement/AccountManagementAPI';

if (userStateStore().email) {
  // 登录一下
  tryLogin(userStateStore().email, userStateStore().hashPassword).then((res) => {
    if (!res.isSuccess)
      showTip("出现异常，请尝试刷新！", false)
  }).catch(() => {
    showTip("出现异常，请尝试刷新！", false)
  })
}

app.use(VueViewer, {
    defaultOptions: {
        zIndex: 1000000
    }
})

const iframeWhitelist = ['player.bilibili.com']
app.use(vuetify).use(VueDOMPurifyHTML, {
    default: {
        ADD_TAGS: ['iframe'],
    },
    hooks: {
      uponSanitizeElement: (currentNode) => {
        if (currentNode.nodeName == 'IFRAME') {
          let src = currentNode.getAttribute('src');
          if (!src.startsWith('https:')) {
            src = 'https:' + src
          }
          try {
            const hostname = new URL(src).hostname
            if (!iframeWhitelist.includes(hostname)) {
              currentNode.parentNode.removeChild(currentNode);
            }
          } catch {
            currentNode.parentNode.removeChild(currentNode);
          }
          return
        }
      },
    }}).use(ElementPlus)

app.mount('#app')



