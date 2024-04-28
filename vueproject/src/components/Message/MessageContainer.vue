<template>
  <div v-if="this.curUserId == '0'">
    <contactCard v-for="(item, index) in contactList" :key="index" :user_name="item.userName" :user_id="item.userId"
      :avatar="item.userAvatarUrl" @open-message="handleContactClicked" />
  </div>

  <div v-else>
    <v-btn @click="() => { this.curUserId = '0' }">
      返回上一级
    </v-btn>
    <div class="message-container" ref="container" style="height: 85%;">
      <div v-for="message in messages" :key="message.id">
        <div v-if="message.sender_id == myId" class="message-right">
          <div style="display: flex;flex-direction: column;   align-items: flex-end; justify-content: flex-end;">
            <div class="time">{{ message.time }}</div>
            <div class="content">
              {{ message.content }}
            </div>
          </div>
          <img src="@/assets/logo.png" alt="头像" class="profile-photo" />
        </div>
        <div v-else class="message-left">
          <img src="@/assets/logo.png" alt="头像" class="profile-photo" />
          <div style="display: flex;flex-direction: column;   align-items: flex-start; justify-content: flex-start;">
            <div class="time">{{ message.time }}</div>
            <div class="content">
              {{ message.content }}
            </div>
          </div>
        </div>
      </div>
    <div style="display: flex; justify-content: space-between;margin-top: auto;">
      <v-text-field v-model="inputMessage" style="flex: 1;height: 32x;"></v-text-field>
      <v-btn @click="submitMessage" color="primary" style="height: 54px;">发送</v-btn>
    </div>
    </div>
  </div>

</template>
<script>
/* eslint-disable */
import contactCard from './contactCard.vue';
import axios from 'axios';
import userStateStore from '@/store';

export default {
  name: "MessageContainer",
  components: {
    contactCard,
  },
  data() {
    const store = userStateStore()
    return {
      contactList: [],
      curUserId: "0",
      curUserName: "",
      curAvatar: "",
      messages: [],
      messageLoaded: false,
      inputMessage: "",
      timer: null,
      myAvatar: store.profile_photo,
      myId: store.user_id
    };
  },
  mounted() {
    let cur_user = localStorage.getItem("MessageInterface")
    console.log(cur_user)
    if (cur_user != null) {
      localStorage.removeItem("MessageInterface")
      cur_user = JSON.parse(cur_user)
      this.curUserId = cur_user.user_id
      this.curUserName = cur_user.user_name
      this.curAvatar = cur_user.avatar
      this.getMessages()
    }
    this.getRelatedPerson();
  },
  unmounted() {
    if (this.timer) {
      clearInterval(this.timer)
      this.timer = null;
    }
  },
  methods: {
    getRelatedPerson() {
      axios.post('/getReletedUser', {})
        .then(response => {
          this.contactList = response.data
        })
        .catch(error => {
          console.error(error);
        });
    },
    getMessages() {
      if (this.curUserId != "0") {
        axios.post('/getHistoryMessage', { targetUserId: this.curUserId })
          .then(response => {
            this.messages = response.data
          })
          .catch(error => {
            console.error(error);
          }).finally(() => {
            if (this.timer == null)
              this.timer = setInterval(() => {
                this.getMessages();
              }, 1000);
          });
      } else {
        if (this.timer) {
          clearInterval(this.timer)
          this.timer = null;
        }
      }
    },
    handleContactClicked(user_id, user_name, avatar) {
      this.curUserId = user_id
      this.curUserName = user_name
      this.curAvatar = avatar
      this.getMessages()
    },
    submitMessage() {
      axios.post('/sendMessage', { targetUserId: this.curUserId, content: this.inputMessage })
        .then(response => {
          this.inputMessage = ""
        })
        .catch(error => {
          console.error(error);
        })
    }
  }
}
</script>


<style scoped>
.message-container {
  /* 可根据实际需要设置高度 */
  height: 420px;
  line-height: 1.5;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: auto;
  padding-bottom: 70px;
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
</style>