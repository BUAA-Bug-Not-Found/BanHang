<template>
  <div>
    <div style="display: flex; justify-content: space-between;padding-bottom: 5px;">
      <v-text-field v-model="inputCookie" label="修改Cookie" style="flex: 1;height: 34x;"></v-text-field>
      <v-btn @click="submitCookie" color="primary" style="height: 50px;">确定</v-btn>
    </div>
    <div>{{ message }}</div>
    <div>
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
      message: '',
      cookie:"",
      inputCookie:"",
      taskList: [{
        className:"name",
        content:"<ul> <li><strong>模块</strong><strong>3</strong><strong>（实验与分析）作业要求</strong></li> <li>一、作业目标</li> <li>（1）学习实验基本方法</li> <li>（2）学习文献实验对学术贡献点的支撑</li> <li>二、作业内容</li> <li>（1）介绍论文的主要创新思想和学术贡献</li> <li>（2）介绍实验方法论、实验环境、测试程序集</li> <li>（3）展示主要实验结果，根据结果中的数据分析结论</li> <li>（4）<strong>明确说明</strong>实验结果如何支撑论文的创新思想和学术贡献（重要！没有这部分作业不得分）</li> <li>（5）撰写报告（中文，500字以上，1500字以内）并按照时间截点提交至课程中心</li> <li>（6）完成课堂汇报PPT（模板请见资源下载）</li> <li>（7）写作要求信息准确、陈述简洁、逻辑清晰、内容详实、表达流畅。</li> <li>三、作业要求</li> <li>（1）第一版，2024年4月25日23:59，提交地点：在线教学平台（待定）</li> <li>（2）最终版，2024年5月25日23:59，提交地点：在线教学平台（待定）</li> <li>（3）作业文件命名规则</li> <li>1）论文的实验与分析，文件名分别为：学号-姓名-模块3（实验与分析）-第一版.docx</li> <li>2）实验与分析的PPT，只需在5月29日提交最终版，文件名为：学号-姓名-模块3（实验与分析）-最终版.pptx</li> </ul>",
        startTime:"2024-01-01",
        endTime:"2024-7-16",
      }]
    };
  },
  mounted() {
    this.message = "加载数据中。。。"
    this.queryTasks()
  },
  methods: {
    submitCookie() {
      this.cookie = this.inputCookie;
      this.queryTasks();
    },
    queryTasks() {
      // 调用 ptest 插件的 coolMethod 方法
      this.taskList = []
      if (typeof cordova !== 'undefined') {
        setTimeout(() => {
          this.message = "准备请求数据"
          cordova.plugins.ptest.coolMethod(this.cookie, this.successCallback, this.errorCallback);
        }, 1);
      } else {
        this.message = '不在Cordova环境中'
      }
    },
    successCallback(result) {
      // 成功回调函数
      this.taskList = JSON.parse(result)
      this.taskList = this.taskList.filter(task => {
        const endTime = new Date(task.endTime);
        const oneDay = 24 * 60 * 60 * 1000; // 一天的毫秒数
        return endTime.getTime() + oneDay < currentDate.getTime();
      });
      this.taskList.sort(function (a, b) {
        return new Date(a.endTime) - new Date(b.endTime);
      })
      this.message = ""
    },
    errorCallback(error) {
      // 失败回调函数
      this.message = 'failed'
      console.error('调用失败：' + error);
    }
  }
}
</script>

<style scoped></style>