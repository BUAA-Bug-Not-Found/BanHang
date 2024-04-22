<script>
import {useDisplay} from 'vuetify'
  import { useRouter } from 'vue-router'

  export default {
    name: 'HomeIndex',
    setup() {
      const display = useDisplay()
      const isLogin = false
      const user_name = "user1"
      const search = () => {
        console.log("search")
      }

      const router = useRouter()

      const goto = (route) => {
        router.push(route)
      }

      return {display, search, user_name, isLogin, goto}
    }

}
</script>

<template>
  <h1 v-if="display.smAndDown.value">Home Center</h1>
  <v-app-bar :elevation="1"
             v-if="!display.smAndDown.value">
    <template v-slot:prepend>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
    </template>
    <v-app-bar-title>伴航</v-app-bar-title>
    <v-col col="4">
      <v-text-field
          append-inner-icon="mdi-magnify"
          density="compact"
          label="Search content"
          variant="solo"
          hide-details
          single-line
          @keyup.enter="search"
          style="margin-left: 10px; margin-right: 10px"
      ></v-text-field>
    </v-col>
    <v-btn @click="goto('/help_center')">
      <v-icon>mdi-help-box</v-icon>
      互助中心
    </v-btn>

    <v-btn>
      <v-icon>mdi-account-cowboy-hat-outline</v-icon>
      匿名空间
    </v-btn>

    <v-btn>
      <v-icon>mdi-toolbox</v-icon>
      工具箱
    </v-btn>
    <div style="align-content: center">
      <v-divider style="height:20px" vertical></v-divider>
    </div>

    <template v-slot:append>
      <v-col v-if="!isLogin">
        <v-avatar color="surface-variant" size="32" style="margin-right: 5px"></v-avatar>
        {{user_name}}
      </v-col>
      <v-col v-else>
        <v-btn elevation="2" color="blue-darken-2" variant="flat" class="text-none">Login</v-btn>
      </v-col>
    </template>
  </v-app-bar>

  <v-app-bar :elevation="1" density="compact"
             v-if="display.smAndDown.value">
    <v-avatar color="surface-variant" style="margin-left: 15px" size="32"></v-avatar>

    <v-col>
      <v-text-field
          append-inner-icon="mdi-magnify"
          density="compact"
          class="w-75"
          label="Search content"
          variant="outlined"
          hide-details
          single-line
          @keyup.enter="search"
          style="margin-left: 10px; margin-right: 10px"
      ></v-text-field>
    </v-col>
    <template v-slot:append>
      <v-badge :content="17" style="margin-right: 10px">
        <v-icon>mdi-email-outline</v-icon>
      </v-badge>
    </template>
  </v-app-bar>
  <router-view></router-view>
  <v-bottom-navigation
      color="primary"
      active
      v-if="display.smAndDown.value"
  >
    <v-btn @click="goto('/help_center')">
      <v-icon>mdi-help-box</v-icon>
      互助中心
    </v-btn>

    <v-btn>
      <v-icon>mdi-account-cowboy-hat-outline</v-icon>
      匿名空间
    </v-btn>

    <v-btn>
      <v-icon>mdi-toolbox</v-icon>
      工具箱
    </v-btn>
    <v-btn>
      <v-icon>mdi-account</v-icon>
      用户中心
    </v-btn>
  </v-bottom-navigation>
</template>

<style scoped>

</style>