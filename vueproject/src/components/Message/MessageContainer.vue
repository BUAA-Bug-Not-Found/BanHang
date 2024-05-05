<template>
  <v-card :class="{ 'pc-container': !display.smAndDown.valueOf(), 'pe-container': display.smAndDown.valueOf() }">
    <div v-if="this.myId == 1">
      <div>您还没有登陆</div>
    </div>
    <div v-else-if="this.curUserId == 0">
      <div v-if="this.contactList.lenth == 0">
        您还没有联系人
      </div>
      <contactCard v-for="(item, index) in contactList" :key="index" :user_name="item.userName" :user_id="item.userId"
        :avatar="item.userAvatarUrl" :last_message="item.lastMessage" @open-message="handleContactClicked" />
    </div>

    <div v-else style="height: 100%; display: flex; flex-direction: column;;">
      <div class="header-container">
        <button @click="() => { this.curUserId = 0 }" style="align-items: start; margin-left: 20px;">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40px" height="45px" style="margin-top: 3px;">
            <title>chevron-left</title>
            <path d="M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z" />
          </svg>
        </button>
        <h2 class="title">{{ this.curUserName }}</h2>
      </div>
      <div :class="{'message-container-pc': !display.smAndDown.valueOf(), 'message-container-pe': display.smAndDown.valueOf() }" ref="container">
        <div v-for="message in messages" :key="message.id">
          <div v-if="message.senderId == myId" class="message-right">
            <div style="display: flex;flex-direction: column;   align-items: flex-end; justify-content: flex-end;">
              <div class="time">{{ this.formatDateTime(message.time) }}</div>
              <div class="content">
                {{ message.content }}
              </div>
            </div>
            <img :src="myAvatar" class="profile-photo" />
          </div>
          <div v-else class="message-left">
            <img :src="curAvatar" class="profile-photo" />
            <div style="display: flex;flex-direction: column;   align-items: flex-start; justify-content: flex-start;">
              <div class="time">{{ this.formatDateTime(message.time) }}</div>
              <div class="content">
                {{ message.content }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="input">
        <v-text-field @keyup.enter="submitMessage" v-model="inputMessage" style="flex: 1;height: 32x;padding: 0;" hide-details=true></v-text-field>
        <v-btn @click="submitMessage" color="primary" style="height: 54px;">发送</v-btn>
      </div>
    </div>
  </v-card>

</template>
<script>
/* eslint-disable */
import contactCard from './contactCard.vue';
import axios from 'axios';
import userStateStore from '@/store';
import { useDisplay } from 'vuetify'

export default {
  name: "MessageContainer",
  components: {
    contactCard,
  },
  data() {
    const store = userStateStore()
    return {
      contactList: [],
      curUserId: 0,
      curUserName: "",
      curAvatar: "",
      messages: [],
      messageLoaded: false,
      inputMessage: "",
      timer: null,
      myAvatar: store.profile_photo,
      myId: store.user_id,
      display: useDisplay(),
      init: false,
    };
  },
  mounted() {
    let cur_user = localStorage.getItem("MessageInterface")
    if (cur_user != null) {
      localStorage.removeItem("MessageInterface")
      cur_user = JSON.parse(cur_user)
      this.curUserId = cur_user.user_id
      this.curUserName = cur_user.user_name
      this.curAvatar = cur_user.avatar
      this.updateData()
    } else {
      console.log(this.display.smAndDown.valueOf())
      this.updateData();
    }
  },
  beforeRouteLeave() {
    if (this.timer) {
      clearInterval(this.timer)
      this.timer = null;
    }
  },
  unmounted() {
    if (this.timer) {
      clearInterval(this.timer)
      this.timer = null;
    }
  },
  methods: {
    updateData() {
      if (this.myId != 1) {
        if (this.curUserId != 0) {
          axios.post('/getHistoryMessage', { targetUserId: this.curUserId })
            .then(response => {
              this.messages = response.data
              if (!this.init) {
                this.scrollToBottom()
                this.init=true
              }
            })
            .catch(error => {
              console.error(error);
            });
        } else {
          axios.post('/getReletedUser', {})
            .then(response => {
              this.contactList = response.data
            })
            .catch(error => {
              console.error(error);
            });
        }
      }
      if (this.timer == null)
        this.timer = setInterval(() => {
          this.updateData();
        }, 1000);
    },
    handleContactClicked(user_id, user_name, avatar) {
      this.curUserId = user_id
      this.curUserName = user_name
      this.curAvatar = avatar
      this.init = false
      this.updateData()
    },
    submitMessage() {
      axios.post('/sendMessage', { targetUserId: this.curUserId, content: this.inputMessage })
        .then(response => {
          this.inputMessage = ""
        })
        .catch(error => {
          console.error(error);
        })
    },
    scrollToBottom() {
        var container = this.$refs.container;
        if (container) {
          this.$nextTick(() => {
            container.scrollTop = container.scrollHeight;
          });
        }
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
  }
}
</script>


<style scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  background-color: rgb(205, 227, 234);
}
.message-container-pe {
  /* 可根据实际需要设置高度 */
  display: flex;
  flex-direction: column;
  flex:1;
  flex-grow: 1;
  overflow-y: auto;
  max-height: calc(100vh - 56px - 56px - 70px - 54px + 3px);
  background-color: rgb(238, 238, 238);
}

.message-container-pc {
  /* 可根据实际需要设置高度 */
  display: flex;
  flex-direction: column;
  flex:1;
  flex-grow: 1;
  overflow-y: auto;
  max-height: calc(100vh - 64px - 56px - 70px + 3px);
  background-color: rgb(238, 238, 238);
}
.input {
  height: 56px;
  display: flex;
  background-color: white;
}
.message-right {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-end;
  text-align: left;
}

.message-left {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  text-align: left;
}

.content {
  background-color: antiquewhite;
  padding: 5px;
  border-radius: 10px;
  font-weight: bold;
  word-wrap: break-word;
  max-width: 400px;
}

.profile-photo {
  width: 50px;
  height: 50px;
  object-fit: cover;
  margin-right: 10px;
  border-radius: 50%;
}

.time {
  font-size: 12px;
  /* 字体变小 */
  color: #999;
  /* 颜色变淡 */
  margin-top: 5px;
}


.title {
  position: absolute;
  left: 50%;
  top: 20px;
  transform: translate(-50%, 0);
  /* 水平垂直居中 */
}



.pc-container {
  width: 600px;
  margin-left: calc(50vw - 300px);
  height: calc(100vh - 65px);
  z-index: inherit;
  background-color: rgb(238, 238, 238);
}

.pe-container {
  width: 100%;
  height: 100%;
  max-height: 100%;
  background-color: rgb(238, 238, 238);
}
</style>