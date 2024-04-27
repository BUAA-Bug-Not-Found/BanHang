<template>
    <v-container>
      <div>
        <v-card style="margin-bottom: 20px; height: auto;">
            <!-- div好像是行内的 -->
            <div style="text-align: center;">
              <v-toolbar density="compact" style="background-color:aliceblue;">
                <v-spacer></v-spacer>
                <v-btn icon @click="clickChat">
                  <v-icon color="blue">mdi-chat</v-icon>
                </v-btn>
                <v-btn icon @click="clickHeart">
                  <v-icon color="red">mdi-heart</v-icon>
                </v-btn>
              </v-toolbar>
            </div>
            <div style="text-align: center;">
              <!-- 头像 -->
              <v-avatar size="80" style="margin-top: 10px;">
                <img src="../../assets/nr/headImage.jpg" alt="Avatar">
              </v-avatar>
            </div>
            <div style="margin-top: 10px;">
              <span class="nickname">Goths</span>
            </div>
            <div style="margin-bottom: 10px; font-size: 10px; text-align: center;">
              <span class="signature">上网不涉密, 涉密不上网</span>
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
          <v-tab value="one">Ta的互助贴</v-tab>
          <!-- <v-tab value="two">互助贴</v-tab> -->
        </v-tabs>
        <v-card-text>
          <v-window v-model="tab">
            <!-- 该window展示匿名贴的内容 -->
            <v-window-item value="one">
              <v-list>
                <v-list-item v-for="(post, index) in posts" :key="index" @click="clickItem" style="cursor: pointer;">
                  
                  <span style="vertical-align: middle; font-size: 15px; font-weight: bold;">这里是标题{{ index }}</span>
                  <div style="text-align: center; font-size: 0px;">
                    <img src="../../assets/nr/headImage.jpg" style=" margin-left: 10px; margin-top: 10px;"/>
                  </div>

                  <!-- 帖子的发表时间, 评论数量, 点赞数 -->
                  <div style="text-align: right; margin-top: 10px;">
                    <v-text class="time" style=" margin-right: 5px;">2024-04-25 00:12</v-text>
                  </div>
                  <!-- 分隔线 -->
                  <v-divider style="margin-top: 0px;"></v-divider>
                </v-list-item>
              </v-list>
            </v-window-item>
            
            <!-- 该window展示互助贴的内容 -->
          </v-window>
        </v-card-text>
      </v-card>

    </v-container>
  </template>
  
  <script>
//   import router from '@/router';
  import {queryStar, setStarState} from '@/components/PersonalCenter/PersonalCenterAPI';
import userStateStore from '../../store';
  export default {
    data() {
      return {
        tab: 'one', // 这里指定一个默认值, 上面点了才会有效果
        posts: [
          { content: "这是第一条动态" },
          { content: "这是第二条动态" },
          { content: "这是第三条动态" },
        ],
        otherEmail: '', // TODO 这里要填充
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
      clickHeart() {
        const s = userStateStore()
        // 关注/取消关注
        queryStar(s.email, this.otherEmail).then((res) => {
          // if (res.isStar) {
            // 本来关注了, 现在取消
            setStarState(s.email, this.otherEmail, !res.isStar)
              .then((res) => {
                // 收到回复
                if (res.isSuccess) {
                  // 成功设置
                }
              })
        })
      }, 
      clickChat() {
        // 跳转到聊天窗口, 传递一个参数
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
</style>
  