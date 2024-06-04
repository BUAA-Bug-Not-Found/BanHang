<template>
  <v-card :class="{ 'pc-container': !display.smAndDown.valueOf(), 'pe-container': display.smAndDown.valueOf() }">
    <div v-if="!isLogin">
      <div>您还没有登录</div>
    </div>
    <div v-else-if="this.curUserId == 0"
      :class="{ 'contact-container-pc': !display.smAndDown.valueOf(), 'contact-container-pe': display.smAndDown.valueOf() }">
      <div v-if="this.contactList.length == 0">
        您还没有联系人
      </div>
      <contactCard v-else v-for="(item, index) in contactList" :key="index" :user_name="item.userName"
        :user_id="item.userId" :avatar="item.userAvatarUrl" :last_message="item.lastMessage"
        :unreadMessageNum="item.unreadMessageNum" @open-message="handleContactClicked" />
    </div>

    <div v-else style="height: 100%; display: flex; flex-direction: column;;">
      <div class="header-container">
        <button @click="() => { this.curUserId = 0 }" style="align-items: start; margin-left: 20px;">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="40px" height="45px"
            style="margin-top: 3px;">
            <title>chevron-left</title>
            <path d="M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z" />
          </svg>
        </button>
        <h2 class="title">{{ this.curUserName }}</h2>
      </div>
      <div
        :class="{ 'message-container-pc': !display.smAndDown.valueOf(), 'message-container-pe': display.smAndDown.valueOf() }"
        ref="container">
        <div v-for="message in messages" :key="message.id">

          <div v-if="message.senderId == myId" class="message-right">
            <span style="display: grid; justify-items: end;">
              <div class="time">{{ this.formatDateTime(message.time) }}</div>
              <img v-if="isValidImg(message.content)" :src="message.content" class="content-image" @click="showPic(message.content)"/>
              <div class="content" v-else>
                {{ message.content }}
              </div>
            </span>
            <img :src="myAvatar" class="profile-photo" />
          </div>

          <div v-else class="message-left">
            <img :src="curAvatar" class="profile-photo" @click="gotoIndex()" />
            <span style="display: grid; justify-items: start;">
              <div class="time">{{ this.formatDateTime(message.time) }}</div>
              <img v-if="isValidImg(message.content)" :src="message.content" class="content-image" @click="showPic(message.content)"/>
              <div v-else class="content">
                {{ message.content }}
              </div>
            </span>
          </div>
        </div>
      </div>

      <div class="input">

        <div class="file-upload-container">
          <label for="fileInput" class="custom-file-upload">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" style="width: 100%">
              <title>image-outline</title>
              <path
                d="M19,19H5V5H19M19,3H5A2,2 0 0,0 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3M13.96,12.29L11.21,15.83L9.25,13.47L6.5,17H17.5L13.96,12.29Z" />
            </svg>
          </label>
          <input id="fileInput" type="file" @change="handleImageUpload" accept="image/*" multiple
            class="image-upload-input">
        </div>

        <v-text-field @keyup.enter="submitMessage" v-model="inputMessage" class="text-input" hide-details
          density="compact">
        </v-text-field>

        <v-btn @click="submitMessage" color="primary" style="height: 100%;">发送</v-btn>
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
import { $bus } from '@/store';
import router from "@/router";
import {api as viewerApi} from "v-viewer";

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
      // myAvatar: store.profile_photo,
      myAvatar: store.headImage,
      myId: store.user_id,
      myName: store.user_name,
      display: useDisplay(),
      init: false,
      isLogin: store.isAuthentic,
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
    gotoIndex() {
      router.push('/othersCenter/' + this.curUserId)
    },
    handleImageUpload(event) {
      const files = event.target.files;
      if (!files) return;
      if (files.length > 9) {
        showTip("图片上限为 9 张，请适当减少您的图片数量~", false)
        return;
      }
      // 遍历上传的图片文件，生成预览并存入图片预览数组
      for (let i = 0; i < files.length; i++) {
        let form = new FormData()
        form.append("file", files[i])

        // todo this.images
        axios({
          method: "post",
          url: "https://banhang.lyhtool.com:8000/uploadfile/",
          data: form,
          headers: { 'Content-Type': 'multipart/form-data' }
        }).then((res) => {
          const data = res.data
          if (data.response == 'success') {
            console.log(data.fileUrl)
            const url = data.fileUrl
            axios.post('/sendMessage', { targetUserId: this.curUserId, content: url })
              .then(response => {
                this.inputMessage = ""
              })
              .catch(error => {
                console.error(error);
              })
            this.messages.push({
              senderName: this.myName,
              senderId: this.myId,
              receiverName: this.curUserName,
              receiverId: this.curUserId,
              content: url,
              time: this.formatDateTime(new Date().toString()),
              read: false
            })
            this.scrollToBottom()
          } else {
            console.log(data.response)
          }
        }).catch((error) => {
          console.log(error)
        })
      }
    },
    updateData() {
      if (this.isLogin) {
        if (this.curUserId != 0) {
          axios.post('/getHistoryMessage', { targetUserId: this.curUserId })
            .then(response => {
              this.messages = response.data
              if (!this.init) {
                this.scrollToBottom()
                this.init = true
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
      setTimeout(() => {
        $bus.emit('updateUnreadData')
      }, 2000);
    },
    submitMessage() {
      if (this.inputMessage !== '') {
        axios.post('/sendMessage', { targetUserId: this.curUserId, content: this.inputMessage })
          .then(response => {
            this.inputMessage = ""
          })
          .catch(error => {
            console.error(error);
          })
        this.messages.push({
          senderName: this.myName,
          senderId: this.myId,
          receiverName: this.curUserName,
          receiverId: this.curUserId,
          content: this.inputMessage,
          time: this.formatDateTime(new Date().toString()),
          read: false
        })
        this.scrollToBottom()
      }
    },
    scrollToBottom() {
      var container = this.$refs.container;
      if (container) {
        this.$nextTick(() => {
          container.scrollTop = container.scrollHeight;
        });
      }
    },
    showPic(firstImg) {
      let imgList = this.messages.filter(x => this.isValidImg(x.content)).map(x => x.content)
      let index = imgList.indexOf(firstImg)
      console.log(index)
      viewerApi({images: imgList, options: {
        initialViewIndex:index,
      }})
    },
    isValidImg(content) {
      let urlPattern = /^https:\/\/banhang\.oss\.chlience\.com\/\d+\/file\/[a-fA-F0-9]{32}\.(png|jpe?g)$/; 
      return urlPattern.test(content)  
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
  flex: 1;
  flex-grow: 1;
  overflow-y: auto;
  max-height: calc(100vh - 56px - 56px - 70px - 54px + 3px);
  background-color: rgb(238, 238, 238);
}

.message-container-pc {
  /* 可根据实际需要设置高度 */
  display: flex;
  flex-direction: column;
  flex: 1;
  flex-grow: 1;
  overflow-y: auto;
  max-height: calc(100vh - 64px - 56px - 70px + 3px);
  background-color: rgb(238, 238, 238);
}

.contact-container-pe {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: auto;
  max-height: calc(100vh - 56px - 54px + 3px);
}

.contact-container-pc {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: auto;
  max-height: calc(100vh - 64px + 3px);
}


.input {
  height: 56px;
  display: flex;
  background-color: white;
  border-top-width: 5px;
  padding: 8px
}

.text-input {
  flex: 1;
  margin-right: 5px
}

.message-right {
  display: grid;
  grid-template-columns: 1fr auto;
  width: 100%;
  margin-bottom: 10px;
}

.message-left {
  display: grid;
  grid-template-columns: auto 1fr;
  width: 100%;
  margin-bottom: 10px;
}

.content {
  background-color: antiquewhite;
  padding: 5px;
  border-radius: 10px;
  font-weight: bold;
  word-break: break-all;
  text-align: left;
  max-width: 85%;
}
.content-image {
    max-width: 60%;
    max-height: 300px;
    width: auto;
    height: auto;
}

.profile-photo {
  width: 44px;
  height: 44px;
  margin: 3px;
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

.image-upload-input {
  display: none;
}

.custom-file-upload {
  border: none;
  cursor: pointer;
  height: 100%;
  align-items: center;
  display: flex;
  background-color: transparent
}

.file-upload-container {
  display: flex;
  height: 100%;
  width: 35px;
  margin-left: 5px;
  margin-right: 5px;
  background-color: transparent
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