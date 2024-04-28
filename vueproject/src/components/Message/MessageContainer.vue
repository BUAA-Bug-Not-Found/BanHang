<template>
  <div v-if="this.curUserId == '0'">
    <contactCard v-for="(item, index) in contactList" :key="index" :user_name="item.user_name" :user_id="item.user_id"
      @open-message="handleContactClicked" />
  </div>

  <div v-else>
    <v-btn @click="() => { this.curUserId = '0' }">
      返回上一级
    </v-btn>
    <div class="message-container" ref="container" style="height: 85%;">
      <div v-for="message in messages" :key="message.id">
        <div v-if="message.is_sender" class="message-right">
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
    </div>
    <div style="display: flex; justify-content: space-between;padding-bottom: 5px;">
      <v-text-field v-model="inputMessage" style="flex: 1;height: 32x;"></v-text-field>
      <v-btn @click="submitMessage" color="primary" style="height: 54px;">发送</v-btn>
    </div>
  </div>

</template>
<script>
/* eslint-disable */
import contactCard from './contactCard.vue';
export default {
  name: "MessageContainer",
  components: {
    contactCard,
  },
  data() {
    return {
      contactList: [
        {
          user_name: "123",
          user_id: "1"
        },
        {
          user_name: "234",
          user_id: "2"
        }
      ],
      curUserId: "0",
      messages: [
        {
          sender_name: "123",
          sender_id: "1",
          receiver_name: "234",
          receiver_id: "2",
          content: "content",
          time: "2004-4-15 12:12:12",
          read: false
        }
      ],
      messageLoaded: false,
      inputMessage: "",
    };
  },
  mounted() {
    console.log(this.contactList)
  },
  methods: {
    handleContactClicked(user_id) {
      this.curUserId = user_id
    },
    submitMessage() {
      console.log(this.inputMessage)
    }
  }
}
</script>


<style scoped>  .message-container {
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
}</style>