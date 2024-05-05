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
                <v-icon :class="{'redHeart': isStar, 'greyHeart': !isStar}">mdi-heart</v-icon>
              </v-btn>
            </v-toolbar>
          </div>
          <div style="text-align: center;">
            <!-- 头像 -->
            <v-avatar color="surface-variant"
             style="margin-top: 15px;margin-left: 10px"
              size="80"
              :image="infos.url">
            </v-avatar>
          </div>
          <div style="margin-top: 10px;">
            <span class="nickname">{{ infos.nickname }}</span>
          </div>
          <div style="margin-bottom: 10px; font-size: 10px; text-align: center;">
            <span class="signature">{{ infos.sign }}</span>
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
              <v-list-item v-for="(content, index) in otherBlogs.slice().reverse()" :key="index" @click="clickHelpItem(content.blogId)" style="cursor: pointer;">
                
                <!-- <span style="vertical-align: middle; font-size: 15px; font-weight: bold;">{{ content.blogTitle }}</span>
                <div style="text-align: center; font-size: 0px;">
                  <img :src="firstPhotoUrl" style=" margin-left: 10px; margin-top: 10px;"/>
                </div> -->
                <div style="margin-top: 3px" v-dompurify-html="content.blogTitle"></div>

                <!-- 帖子的发表时间, 评论数量, 点赞数 -->
                <div style="text-align: right; margin-top: 10px;">
                  <v-text class="time" style=" margin-right: 5px;">{{ this.formatDateTime(content.time) }}</v-text>
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
import router from '@/router';
import {queryStar, setStarState} from '@/components/PersonalCenter/PersonalCenterAPI';
import userStateStore from '../../store';
import { getUserInfos, showTip } from '../AccountManagement/AccountManagementAPI';
import { getHelpBlogs } from './PersonalCenterAPI';
export default {
  created() {
    if (!userStateStore().email) {
      showTip("请首先登陆", false)
      router.replace({path: "/loginPage"})
    }
    this.otherEmail = router.currentRoute.value.params.e
    // 拉取该用户的信息
    getUserInfos(this.otherEmail).then((_infos) => {
      if (_infos === false) {
        showTip("应用出错!", false)
      } else {
        this.infos = _infos
      }
    })
    // 拉取该用户的互助贴
    getHelpBlogs(this.otherEmail).then((_helpBlogs) => {
      this.otherBlogs = _helpBlogs;
    })
    // 当用户没有登陆的时候，这时候是无法正常queryStar的
    queryStar(userStateStore().email, this.otherEmail).then((res) => {
      this.isStar = res.isStar
    }).catch(() => {
      showTip("应用出错!!", false)
    })
  },
  data() {
    return {
      tab: 'one', // 这里指定一个默认值, 上面点了才会有效果
      infos: {
        "headUrl": "",
        "nickname": "",
        "sign": "",
        "user_id": 8
      },
      otherBlogs: [],
      otherEmail: '', // TODO 这里要填充
      isStar: false,
      images: [
        'https://via.placeholder.com/150',
        // 添加更多图片链接...
      ],
    };
  },
  methods: {
    // 可以添加其他方法
    clickHeart() {
      const s = userStateStore()
      if (s.email === this.otherEmail) {
        showTip("不能关注自己!", false)
        return
      }
      setStarState(s.email, this.otherEmail, !this.isStar)
            .then((res) => {
              // 收到回复
              if (res.isSuccess) {
                // 成功设置
                if (this.isStar) {
                  // 取消关注的信息
                  this.isStar = false
                  showTip("成功取消关注!", true)
                } else {
                  // 加上关注的信息
                  this.isStar = true
                  showTip("成功关注!", true)
                }
              } else {
                showTip("操作失败!", false)
              }
            })
    }, 
    clickChat() {
      if (userStateStore().email === this.otherEmail) {
        showTip("不能和自己聊天!", false)
        return
      }
      // 跳转到聊天窗口, 传递一个参数
      localStorage.setItem('MessageInterface', JSON.stringify({
        user_id: this.infos.user_id,
        user_name: this.infos.nickname,
        avatar: this.infos.headUrl
      }))
      router.push('/message')
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
    clickHelpItem(_blogId) {
      // router.push({name: 'QuesInfo', params: {qid: _blogId}});
      console.log("_blogId-other -> " + _blogId)
      router.push('/QuesInfo/' + _blogId);
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
