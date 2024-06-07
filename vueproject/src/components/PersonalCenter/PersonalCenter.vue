<template>
    <v-container>
      <v-dialog v-model="showDialog" max-width="300px">
        <v-card>
          <v-card-title class="headline">确认操作</v-card-title>
          <v-card-text>
            确定要退出登录吗？
          </v-card-text>
          <v-card-actions>
            <v-btn color="error" @click="clickQuitLogin">确认</v-btn>
            <v-btn color="blue darken-1" @click="showDialog = false">取消</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <div>
        <v-card style="margin-bottom: 20px; height: auto;">
            <!-- div好像是行内的 -->
            <div style="text-align: center;">
              <v-toolbar density="compact" style="background-color:aliceblue;">
                <v-btn v-if="this.isManager" style="vertical-align: center; background-color: #2a9af3;" @click="clickComplain">
                  <div>
                    <span style="color:white">举报待处理 </span>
                    <span style="font-weight: bold; color:aquamarine"> {{ complainAmount }}</span>
                    <span style="color:white"> 项</span>
                  </div>
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn icon @click="clickMyInterest">
                  <v-icon color="red">mdi-heart</v-icon>
                </v-btn>

                <v-btn icon @click="clickUpdateInfo">
                  <v-icon color="blue">mdi-pencil</v-icon>
                </v-btn>

                <v-btn icon @click="showDialog = true">
                  <v-icon color="grey">mdi-logout</v-icon>
                </v-btn>
              </v-toolbar>
            </div>
            
            <div style="text-align: center;">
              <v-menu rounded> 
                <template v-slot:activator="{ props }">
                  <v-avatar v-bind="props" color="surface-variant"
                    style="margin-top: 15px;margin-left: 10px; cursor: pointer;"
                    size="80"
                    :image="headUrl">
                  </v-avatar>
                </template>

                <!-- <v-card style="width: 330px;"> -->
                <v-card style="width: auto;">
                  <v-card-text>
                    <div style="display: flex; align-items: center;">
                      <span style="font-weight: bold; color:red;">Lv.{{ level }}</span>
                      <v-progress-linear style="margin-left: 10px; margin-right: 10px;" :model-value="100.0 * (currentExperience / (currentExperience + experienceNeeded))" color="success" height="5"></v-progress-linear>
                      <span style="font-weight: bold; color:grey;">Lv.{{ level + 1 }}</span>
                    </div>
                    <span style="font-size: 13px; color: grey; margin-top: 10px;">您已经获得{{ currentExperience }}经验, 距离下一级还需{{ experienceNeeded }}经验</span>
                  </v-card-text>
                </v-card>
              </v-menu>

            </div>
            <div style="margin-top: 10px;">
              <div style="display: flex; align-items: center; text-align: center; justify-content: center;">
                <span class="nickname"> {{ nickname }}</span>
                <span style="padding-left: 3px; padding-right: 3px; border-radius: 3px; margin-left: 5px; background-color:bisque; font-weight:bold; color:#2a9af3; font-size: 12px;">Lv.{{ level }}</span>
              </div>
              
            </div>
            <div style="margin-bottom: 10px; font-size: 10px; text-align: center;">
              <span class="signature">{{ sign }}</span>
            </div>
        </v-card>
      </div>
      <!-- 个人动态区域 -->
      <v-card>
        <v-tabs
          v-model="tab"
          color="blue"
          fixed-tabs
        >
          <v-tab value="one">匿名贴</v-tab>
          <v-tab value="two">互助贴</v-tab>
        </v-tabs>
        
        <v-card-text>
          <v-window v-model="tab">
            <!-- 该window展示匿名贴的内容 -->
            <v-window-item value="one">
              <v-list>
                <v-list-item v-for="(content, index) in waterBlogs.slice().reverse()" :key="index" @click="clickWaterItem(content.blogId)" style="cursor: pointer;">
                  <div style="text-align: left;">
                    <v-text style="vertical-align: middle; font-size: 18px; font-weight: bold;">{{ content.blogTitle }}</v-text>
                  </div>
                  <div style="text-align: left; margin-top: 10px;">
                    <v-text style="vertical-align: middle; font-size: 12px; color: grey;">{{ content.blogText }}</v-text>
                  </div>
                  <div style="text-align: right; margin-top: 10px;">
                    <v-text class="time" style=" margin-right: 5px;">{{ this.formatDateTime(content.time) }}</v-text>
                  </div>
                  <!-- 分隔线 -->
                  <v-divider style="margin-top: 0px;"></v-divider>
                </v-list-item>
              </v-list>
            </v-window-item>
            <!-- 该window展示互助贴的内容 -->
            <v-window-item value="two">
              <v-list>
                <v-list-item v-for="(content, index) in helpBlogs.slice().reverse()" :key="index" @click="clickHelpItem(content.blogId)" style="cursor: pointer;">
                  <div style="text-align: left;">{{ truncate(content.blogTitle) }}</div>
                  <div style="text-align: right; margin-top: 10px;">
                    <v-text class="time" style=" margin-right: 5px;">{{ this.formatDateTime(content.time) }}</v-text>
                  </div>
                  <v-divider style="margin-top: 0px;"></v-divider>
                </v-list-item>
              </v-list>
            </v-window-item>
          </v-window>
        </v-card-text>

      </v-card>
    </v-container>
  </template>
  
  <script>
  import router from '@/router';
  import userStateStore from '../../store';
  import {getComplainAmount, getCurrentExpById, getCurrentLevelById, getHelpBlogs, getWaterBlogs} from "./PersonalCenterAPI";
  import { showTip } from '../AccountManagement/AccountManagementAPI';
  
  export default {
    created() {
      // 这里放置需要延迟执行的代码
      this.headUrl = userStateStore().headImage;
        this.nickname = userStateStore().nickname;
        this.email = userStateStore().email;
        this.sign = userStateStore().sign;
        this.isManager = userStateStore().isManager;
        if (!this.email) {
          showTip("请首先登录", false)
          router.replace({path: "loginPage"})
        }
        if (this.sign === "" || !this.sign) {
          this.sign = "快介绍一下自己吧~"
        }
        // 加载一下匿名贴和互助贴

        getHelpBlogs(userStateStore().user_id).then((res) => {
          this.helpBlogs = res
        })

        getWaterBlogs(userStateStore().user_id).then((res) => {
          this.waterBlogs = res
        })

        Promise.all([
          getCurrentLevelById(userStateStore().user_id),
          getCurrentExpById(userStateStore().user_id)  
        ]).then(rets => {
          if (rets[0] === false) this.level = 0
          else this.level = rets[0]
          if (rets[1] === false) this.currentExperience = 0
          else this.currentExperience = rets[1]
          let exps = [0, 100, 500, 1500, 3000, 6000, 10500, 18000, 30000, 54000, 54000] // 经验阈值
          this.experienceNeeded = exps[this.level + 1] - this.currentExperience
        }).catch(() => {
          showTip("出现异常！", false)
        })
        
        // 加载待处理举报信息条数
        if (this.isManager) {
          getComplainAmount().then((res) => {
            if (res.count == 0)
              this.complainAmount = "" // 0条的话就不显示了
            else if (res.count <= 99)
              this.complainAmount = res.count;
            else 
              this.complainAmount = "99+"
          })
        }
    },
    data() {
      return {
        tab: 'one', // 这里指定一个默认值, 上面点了才会有效果
        headUrl: "",
        nickname: "",
        email: "",
        sign: "",
        level: 4, // 当前等级
        currentExperience: 8685, // 当前经验值
        experienceNeeded: 2115, // 升级所需的经验值
        // expPercent: ,
        isManager: false,
        complainAmount: "", // 待处理的举报信息数量, 显示
        showDialog: false,
        posts: [
          { content: "这是第一条动态" },
        ],
        helpBlogs: [
        ],
        waterBlogs: [
        ],
        images: [
          'https://via.placeholder.com/150',
          // 添加更多图片链接...
        ]
      };
    },
    methods: {
      // 可以添加其他方法
      clickUpdateInfo() {
        router.push({path: '/editPersonalInfo', ps: {id: '123'}})
      },
      clickMyInterest() {
        router.push({path: "/interestList"})
      },
      clickQuitLogin() {
        // 注销登录信息
        userStateStore().resetUserInfo()
        router.replace({path: "/loginPage"})
      },
      truncate(content) {
        const strippedContent = String(content).replace(/<[^>]*>/g, "")
        if (strippedContent.length > 20) {
          return `${strippedContent.slice(0, 20)}...`;
        }
        return strippedContent;
      },
      formatDateTime(dateTimeStr) {
        // 创建 Date 对象
        const dateTime = new Date(dateTimeStr);
        
        // 提取年月日时分秒
        const year = dateTime.getFullYear();
        const month = String(dateTime.getMonth() + 1).padStart(2, '0');
        const date = String(dateTime.getDate()).padStart(2, '0');
        const hours = String(dateTime.getHours()).padStart(2, '0');
        const minutes = String(dateTime.getMinutes()).padStart(2, '0');
        const seconds = String(dateTime.getSeconds()).padStart(2, '0');
        
        // 拼接成目标格式的字符串
        const formattedDateTime = `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`;
        
        return formattedDateTime;
      },
      clickWaterItem(_blogId) {
        router.push({name: 'blogView', params: {id: _blogId}});
      },
      clickHelpItem(_blogId) {
        router.push('/QuesInfo/' + _blogId + "/0");
      },
      clickComplain() {
        // 直接跳转到举报信息页面而不需要传参
        router.push("/complainInfos");
      }
    },
  };
  </script>
  
<style scoped>

.nickname {
  font-size: 20px;
  font-weight: bold;
}
.signature {
  font-size: 12px;
  color: gray;
}

.time {
  font-size: 10px;
  color: gray;
}

.redHeart {
  color: red;
}

.greyHeart {
  color: grey;
}

</style>
