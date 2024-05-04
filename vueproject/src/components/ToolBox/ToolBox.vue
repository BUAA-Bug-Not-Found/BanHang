<template>
  <SpocIndex v-if="isApp"></SpocIndex>
  <v-card v-if="!isApp" :class="{ 'pc-notice': !display.smAndDown.valueOf(), 'pe-notice': display.smAndDown.valueOf() }">
    <h1>工具箱使用说明</h1>
    <div>本工具箱致力于提供一系列工具，方便同学们日常学习生活</div>
    <div>目前上限内容有Spoc作业提醒服务，由于浏览器环境限制，目前只能在**手机App**中使用，效果如下图所示。未来将上限更多工具。</div>
    <img  src="@/assets/spocInst/example.jpg" style="width:100%"/>
  </v-card>
</template>
<script>
import { isApp } from "@/store";
import SpocIndex from "@/components/ToolBox/Spoc/SpocIndex.vue"
import { useDisplay } from 'vuetify'

export default {
  name: "ToolBox",
  components: {
    SpocIndex,
  },
  data() {
    return {
      isApp,
      display:useDisplay(),
    }
  }
}
</script>


<style scoped>
.pc-notice {
  margin: 0 auto; /* 设置左右外边距为auto */
  width: 50%; /* 设置 div 的宽度 */
  min-height: 100%; /* 设置 div 的高度 */
  padding-top: 30px;
  padding-left: 20px;
  padding-right: 20px;
}
.pe-notice {
  margin: 0 auto; /* 设置左右外边距为auto */
  width: 100%; /* 设置 div 的宽度 */
  min-height: 100%; /* 设置 div 的高度 */
  padding-top: 30px;
  padding-left: 20px;
  padding-right: 20px;
}
</style>