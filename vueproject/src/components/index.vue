<script>
import {useDisplay} from 'vuetify'
import {useRouter} from 'vue-router'
import {ref} from "vue";

export default {
  name: 'HomeIndex',
  setup() {
    const display = useDisplay()
    const isLogin = false
    const user_name = "user1"
    const searchContent = ref("")
    const search = () => {
      console.log("search")
    }

    const router = useRouter()

    const goto = (route) => {
      router.push(route)
    }

    return {display, search, user_name, isLogin, goto, searchContent}
  },

  methods: {
    navigateToSearchList() {
      if (this.searchContent.trim() !== '') {
        this.$router.push({
          name: 'searchList',
          params: {keywords: this.searchContent.trim()}
        });
      }
    }
  }
}
</script>

<template>
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
          @keyup.enter="search"
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

    <v-btn @click="goto('/personalCenter')">
      <v-icon>mdi-account</v-icon>
      用户中心
    </v-btn>

    <div style="align-content: center">
      <v-divider style="height:20px" vertical></v-divider>
    </div>

    <template v-slot:append>
      <v-col v-if="!isLogin">
        <v-avatar color="surface-variant" size="32" style="margin-right: 5px" @click="goto('/loginPage')"></v-avatar>
        {{ user_name }}
      </v-col>
      <v-col v-else>
        <v-btn elevation="2" color="blue-darken-2" variant="flat" class="text-none">Login</v-btn>
      </v-col>
    </template>
  </v-app-bar>

  <v-app-bar :elevation="1" density="compact"
             v-if="display.smAndDown.value">
    <v-avatar color="surface-variant" style="margin-left: 15px" size="32" @click="goto('/loginPage')"></v-avatar>
    <v-col>
      <v-text-field
          density="compact"
          class="w-50"
          label="搜索"
          variant="outlined"
          hide-details
          single-line
          v-model="searchContent"
          @keyup.enter="search"
          style="margin-left: 10px; margin-right: 10px"
      >
        <template v-slot:append-inner>
          <v-icon @click="navigateToSearchList">mdi-magnify</v-icon>
        </template>
      </v-text-field>
    </v-col>
    <template v-slot:append>
      <v-btn @click="goto('/message')">
        <v-badge :content="0" style="margin-right: 10px">
          <v-icon>mdi-email-outline</v-icon>
        </v-badge>
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
    <v-btn @click="goto('/personalCenter')">
      <v-icon>mdi-account</v-icon>
      用户中心
    </v-btn>
  </v-bottom-navigation>
</template>

<style scoped>
.pc-router {
  margin-top: 48px;
}
.pe-router {
  margin-top: 48px; 
  height: calc(100% - 104px)
}
</style>