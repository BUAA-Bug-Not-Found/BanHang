<template>
    <v-container>
      <div>
        <!-- <input id="fileInput" type="file" @change="handleFileUpload" accept="image/*" multiple class="image-upload-input"> -->
        <v-card style="margin-bottom: 20px; height: auto;">
            <!-- div好像是行内的 -->
            <div style="text-align: center;">
              <v-toolbar density="compact" style="background-color:aliceblue;">
                <v-spacer></v-spacer>
                <v-btn icon @click="clickMyInterest">
                  <v-icon color="red">mdi-heart</v-icon>
                </v-btn>

                <v-btn icon @click="clickUpdateInfo">
                  <v-icon color="blue">mdi-pencil</v-icon>
                </v-btn>

                <v-btn icon @click="clickQuitLogin">
                  <v-icon color="grey">mdi-logout</v-icon>
                </v-btn>
              </v-toolbar>
            </div>
            
            <div style="text-align: center;">
              <!-- 头像 -->
              <v-avatar size="80" style="margin-top: 10px;">
                <img :src=headUrl alt="Avatar">
              </v-avatar>
            </div>
            <div style="margin-top: 10px;">
              <span class="nickname">{{ nickname }}</span>
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
          color="red darken-4"
          fixed-tabs
        >
          <v-tab value="one">匿名贴</v-tab>
          <v-tab value="two">互助贴</v-tab>
        </v-tabs>
        <!-- <span v-if="helpBlogs.length === 2">测试v-if</span> -->
        
        <v-card-text>
          <v-window v-model="tab">
            <!-- 该window展示匿名贴的内容 -->
            <v-window-item value="one">
              <v-list>
                <v-list-item v-for="(content, index) in waterBlogs" :key="index" @click="clickItem" style="cursor: pointer;">
                  <span style="vertical-align: middle; font-size: 15px; font-weight: bold;">{{ content.blogTitle }}</span>
                  <div style="text-align: center; font-size: 0px;">
                    <img :src="content.firstPhotoUrl" style=" margin-left: 10px; margin-top: 10px;"/>
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
                <v-list-item v-for="(content, index) in helpBlogs" :key="index" @click="clickItem" style="cursor: pointer;">
                  <span style="vertical-align: middle; font-size: 15px; font-weight: bold;">{{ content.blogTitle }}</span>
                  <div style="text-align: center; font-size: 0px;">
                    <img :src="content.firstPhotoUrl" style=" margin-left: 10px; margin-top: 10px;"/>
                  </div>
                  <div style="text-align: right; margin-top: 10px;">
                    <v-text class="time" style=" margin-right: 5px;">{{ this.formatDateTime(content.time) }}</v-text>
                  </div>
                  <!-- 分隔线 -->
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
  import {getHelpBlogs, getWaterBlogs} from "./PersonalCenterAPI";

  export default {
    created() {
      // 切入本页面后自动执行本函数
      // 加载数据
      // 为什么不会立即回显???? TODO
      // console.log("这里是personCenter的mounted!!")
      // console.log(this.helpBlogs.length)
      this.headUrl = userStateStore().headImage;
      this.nickname = userStateStore().nickname;
      this.email = userStateStore().email;
      this.sign = userStateStore().sign;
      if (!this.email) {
        router.replace({path: "loginPage"})
      }
      // console.log("user.sign-> " + this.sign)
      if (this.sign === "" || !this.sign) {
        this.sign = "快介绍一下自己吧~"
      }
      // 加载一下匿名贴和互助贴
      getHelpBlogs(userStateStore().email).then((res) => {
        this.helpBlogs = res
      })
      getWaterBlogs(userStateStore().email).then((res) => {
        this.waterBlogs = res
      })
      // this.helpBlogs = get
    },
    data() {
      return {
        tab: 'one', // 这里指定一个默认值, 上面点了才会有效果
        headUrl: "",
        nickname: "",
        email: "",
        sign: "",
        posts: [
          { content: "这是第一条动态" },
          { content: "这是第二条动态" },
          { content: "这是第三条动态" },
          { content: "这是第三条动态" },
          { content: "这是第三条动态" },
        ],
        helpBlogs: [
          // 
        ],
        waterBlogs: [
          // 
        ],
        images: [
          'https://via.placeholder.com/150',
          'https://via.placeholder.com/150',
          'https://via.placeholder.com/150',
          'https://via.placeholder.com/150',
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
        // router.push({path: "/loginPage"})
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
