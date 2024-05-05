<script>
import {useDisplay} from 'vuetify'
import {useRouter} from 'vue-router'
import {ref} from "vue";
import userStateStore from '@/store';
import { $bus } from '@/store';
import { isApp } from '@/store';
// import axios from 'axios';

export default {
  name: 'HomeIndex',
  setup() {
    console.log('indexSetUp')
    const store = userStateStore()
    const display = useDisplay()
    const isLogin = ref(store.isAuthentic);
    const user_name = ref(store.user_name);
    const avatar = ref(store.headImage);

    const searchContent = ref("")

    const router = useRouter()

    const goto = (route) => {
      router.push(route)
    }
    const updateData = (data) => {
      isLogin.value = data.isLogin
      user_name.value = data.user_name
      avatar.value = data.avatar
    }
    $bus.on('updateIndexData', updateData);


    const downloadApk = () => {
      const url = '/path/to/your/app.apk'; // 替换为实际的 APK 文件路径
      const link = document.createElement('a');
      link.href = url;
      link.download = 'app.apk';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
    // axios.get('/getCurrentUserInfo', {}).then(response => {
    //       const storage = userStateStore()
    //       storage.login_store_info(response.data, response.data.email)
    //       this.user_name.value = response.data.user_name
    //       this.isLogin.value = true
    //       this.avatar.value = response.data.url
    //   }).catch(error=>{
    //       console.log(error)
    //   })
    return {display, user_name, isLogin, avatar, goto, searchContent, updateData, downloadApk, isApp}
  },
  unmounted() {
    $bus.off('updateIndexData', this.updateData)
  },
  methods: {
    navigateToSearchList() {
      if (this.searchContent.trim() !== '') {
        this.$router.push({
          name: 'searchList',
          params: {keywords: this.searchContent.trim()}
        });
      }
    },
    gotoLoginOrPersonalIndex() {
      const store = userStateStore()
      if (store.isAuthentic) {
        this.goto('/personalCenter')
      } else {
        this.goto('/loginPage')
      }
    },
  }
}
</script>

<template>
  <!-- <div> -->
  <img v-if="!display.smAndDown.value" src='@/assets/images/background.png' style="position: fixed;width: 100%;height: 100%;">
  <v-app-bar :elevation="1"
             v-if="!display.smAndDown.value">
    <template v-slot:prepend>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
    </template>
    <v-app-bar-title>伴航</v-app-bar-title>
    <v-col col="4">
      <v-text-field
          density="compact"
          label="搜索"
          variant="solo"
          hide-details
          single-line
          v-model="searchContent"
          @keyup.enter="navigateToSearchList"
          style="margin-left: 10px; margin-right: 10px"
      >
        <template v-slot:append-inner>
          <v-icon @click="navigateToSearchList">mdi-magnify</v-icon>
        </template>
      </v-text-field>
    </v-col>
    <v-btn @click="goto('/HelpCenter')">
      <v-icon>mdi-help-box</v-icon>
      互助中心
    </v-btn>

    <v-btn @click="goto('/blogList')">
      <v-icon>mdi-account-cowboy-hat-outline</v-icon>
      匿名空间
    </v-btn>

    <v-btn @click="goto('/tool_box')">
      <v-icon>mdi-toolbox</v-icon>
      工具箱
    </v-btn>

    <v-btn @click="gotoLoginOrPersonalIndex()">
      <v-icon>mdi-account</v-icon>
      用户中心
    </v-btn>

    <div style="align-content: center">
      <v-divider style="height:20px" vertical></v-divider>
    </div>
    <template v-slot:append>
      <v-btn @click="goto('/message')">
          <v-icon>mdi-email-outline</v-icon>
      </v-btn>
      <v-col v-if="isLogin">
        <v-avatar color="surface-variant" size="32" style="margin-right: 5px" @click="gotoLoginOrPersonalIndex()">
          <v-img :src="this.avatar"/>
        </v-avatar>
        {{ user_name }}
      </v-col>
      <v-col v-else>
        <v-btn elevation="2" color="blue-darken-2" variant="flat" class="text-none" @click="gotoLoginOrPersonalIndex()">Login</v-btn>
      </v-col>
    </template>
  </v-app-bar>

  <v-app-bar :elevation="1" density="compact"
             v-if="display.smAndDown.value">
    <v-avatar color="surface-variant" style="margin-left: 15px" size="32" @click="gotoLoginOrPersonalIndex()">
      <v-img :src="this.avatar"/>
    </v-avatar>
    <v-col cols="7">
      <v-text-field
          density="compact"
          class="w-80"
          label="搜索"
          variant="outlined"
          hide-details
          single-line
          v-model="searchContent"
          @keyup.enter="navigateToSearchList"
          style="margin-left: 10px; margin-right: 10px"
      >
        <template v-slot:append-inner>
          <v-icon @click="navigateToSearchList">mdi-magnify</v-icon>
        </template>
      </v-text-field>
    </v-col>
<!--    <v-btn v-if="!isApp" color="primary" @click="downloadApk">Download APK</v-btn>-->
    <template v-slot:append>
      <v-btn @click="goto('/message')">
        <v-icon>mdi-email-outline</v-icon>
      </v-btn>
    </template>
  </v-app-bar>
  <div :class="{ 'pc-router': !display.smAndDown.value, 'pe-router': display.smAndDown.value }">
    <router-view ></router-view>
  </div>
  <v-bottom-navigation
      color="primary"
      active
      v-if="display.smAndDown.value"
  >
    <v-btn @click="goto('/HelpCenter')">
      <v-icon>mdi-help-box</v-icon>
      互助中心
    </v-btn>

    <v-btn @click="goto('/blogList')">
      <v-icon>mdi-account-cowboy-hat-outline</v-icon>
      匿名空间
    </v-btn>

    <v-btn @click="goto('/tool_box')">
      <v-icon>mdi-toolbox</v-icon>
      工具箱
    </v-btn>
    <v-btn @click="gotoLoginOrPersonalIndex()">
      <v-icon>mdi-account</v-icon>
      用户中心
    </v-btn>
  </v-bottom-navigation>
<!-- </div> -->
</template>

<style scoped>
.pc-router {
  margin-top: 63px;
  height: calc(100vh - 64px);
}
.pe-router {
  margin-top: 48px; 
  height: calc(100% - 104px)
}
</style>