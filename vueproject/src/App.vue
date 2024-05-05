<template>
<v-app>
  <router-view></router-view>
</v-app>

</template>

<script>

import router from './router';

export default {
  name: 'App',
  created() {
    const curPath = this.$route.path
    console.log("cur->[" + curPath + "]")
    if (curPath === '/') {
      router.push({path: "/blogList"})
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;

}
</style>
