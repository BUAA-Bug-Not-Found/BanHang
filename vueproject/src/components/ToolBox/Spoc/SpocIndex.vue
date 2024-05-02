<template>
  <div>
    <div style="display: flex; justify-content: space-between;padding-bottom: 5px;">
      <v-text-field v-model="inputCookie" label="修改Cookie" style="flex: 1;height: 32x;"></v-text-field>
      <v-btn @click="submitCookie" color="primary" style="height: 54px;">确定</v-btn>
      <v-btn @click="()=>{this.showInst = !this.showInst}" color="primary" style="height: 54px;">
        <div v-if="this.showInst">
          关闭说明
        </div>
        <div v-else>
          查看说明
        </div>
      </v-btn>
    </div>
    <div>{{ message }}</div>
    <div v-if="showInst">
      <div style="text-align: left;">
        <p class="has-line-data" data-line-start="0" data-line-end="3">
        <strong>本工具用于自动捕获spoc课程平台上的作业信息并进行统一展示，未来还预计提供作业提醒等服务，只能在App上使用</strong><br>
        <strong>本服务需要获取使用您登陆的cookie信息，该信息只会存在您自己的手机上，不会上传至我们的服务器。</strong><br>
        <strong>以下是获取cookie的方式，需要在电脑上进行。一般来说，设置一次cookie（约2min）可以使用很久。以下内容使用Edge浏览器演示，其余浏览器操作基本一致。</strong></p>
        <ol>
        <li>1. 登录spoc平台，进入作业页面点击右键，并选择检查，弹出右侧的窗口</li>
        <img src="@/assets/spocInst/1.png" style="max-width: 95%;"/>
        <li>2. 在右侧窗口选择网络项</li>
        <img src="@/assets/spocInst/2.png" style="max-width: 95%;"/>
        <li>3. 刷新一下页面，可以看到此时有了很多请求</li>
        <img src="@/assets/spocInst/3.png" style="max-width: 95%;"/>
        <li>4. 随便点开一个名称以.do结尾的请求，找到右侧的标头-请求标头-Cookie一项</li>
        <img src="@/assets/spocInst/4.png" style="max-width: 95%;"/>
        <li>5. 将这一项复制，并填写到本App中，即可自动查询作业信息。一个复制好的cookie大概长这样：INCO=258cxxxx5d4e0; JSESSIONID=42Dxxxx1B0</li>
        </ol>
        <div style="height: 100px;"></div>
      </div>
    </div>
    <div v-else>
      <TaskItem v-for="(item, index) in taskList" :key="index"
        :title="item.className" 
        :content="item.content"
        :startTime="item.startTime"
        :endTime="item.endTime"
      />
    </div>
  </div>
</template>
<script>
/* eslint-disable */
import TaskItem from "@/components/ToolBox/Spoc/TaskItem.vue"
export default {
  name: "SpocIndex",
  components: {
    TaskItem,
  },
  data() {
    return {
      message: "",
      cookie: "",
      inputCookie:"",
      taskList: [],
      showInst: false,
    };
  },
  mounted() {
    this.message = "加载数据中。。。"
    if (localStorage.getItem("spocCookie") !== undefined) {
      this.cookie = localStorage.getItem("spocCookie");
      if (localStorage.getItem("spocCache") !== undefined) {
        this.taskList = JSON.parse(localStorage.getItem("spocCache"))
      }
    } else {
      this.cookie = ""
    }
    this.queryTasks();
  },
  methods: {
    submitCookie() {
      this.cookie = this.inputCookie;
      localStorage.setItem("spocCookie", this.cookie)
      this.taskList = []
      localStorage.removeItem("spocCache")
      this.inputCookie = ""
      this.queryTasks();
    },
    queryTasks() {
      // 调用 ptest 插件的 coolMethod 方法
      if (typeof cordova !== 'undefined') {
          this.message = "Loading..."
          setTimeout(() => {
            cordova.plugins.ptest.coolMethod(this.cookie, this.successCallback, this.errorCallback);
          }, 1);
      } else {
        this.message = '不在App环境中'
      }
    },
    successCallback(result) {
      // 成功回调函数
      this.taskList = JSON.parse(result)
      this.taskList = this.taskList.filter(task => {
        const endTime = new Date(task.endTime);
        const oneDay = 24 * 60 * 60 * 1000; // 一天的毫秒数
        return endTime.getTime() + oneDay > new Date().getTime();
      });
      this.taskList.sort(function (a, b) {
        return new Date(a.endTime) - new Date(b.endTime);
      })
      localStorage.setItem("spocCache", result);
      this.message = ""
    },
    errorCallback(error) {
      // 失败回调函数
      this.message = 'Cookie未设置或错误'
      this.taskList = []
    }
  }
}
</script>

<style scoped></style>