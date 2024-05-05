<template>
  <v-card class="comment-card" v-show="replyToCommentId === null">
    <div class="user-info">
      <div v-if="userId !== -1" style="display:flex; justify-content: end;align-content: center">
        <UserAvatar :userId="userId"></UserAvatar>
      </div>
      <div v-if="userId === -1" style="display:flex; justify-content: end;align-content: center">
        <v-avatar style="margin-top:8px">
          <v-img :src="userAvatarUrl"></v-img>
        </v-avatar>
      </div>
      <div class="user-details">
        <span class="user-name">{{ userName }}</span>
        <span class="time">{{ formatDate(time) }}</span>
      </div>
    </div>
    <div class="content" @click="showInput">
      {{ content }}
    </div>
    <div v-show="replyToCommentId === null && replies.length > 0" class="expand-button">
      <button @click="toggleReplies">{{ isOpen ? '收起回复' : '展开回复' }}</button>
    </div>
    <div v-show="isOpen && replies.length > 0">
      <ReplyList :comments="replies"/>
    </div>
    <div v-show="isInputVisible" class="reply-input">
      <v-textarea v-model="replyContent" placeholder="请输入回复内容"></v-textarea>
      <label>
        <input type="checkbox" v-model="isAnonymous"/>匿名发送
      </label>
      <v-btn @click.stop="sendReply" class="ma-2" color="green">发送
        <v-icon
            icon="mdi-checkbox-marked-circle"
            end
        ></v-icon>
      </v-btn>
    </div>
  </v-card>
</template>

<script>
import ReplyList from "@/components/AnonymousBlog/ReplyList.vue";
import {goToOtherUser, uploadComment} from "@/components/AnonymousBlog/api";
import {ElMessage} from "element-plus";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";
import UserStateStore from "@/store";
import router from "@/router";

export default {
  name: "CommentShow",
  components: {UserAvatar, ReplyList},
  props: {
    blogId: {
      type: Number,
      required: true
    },
    commentId: {
      type: Number,
      required: true
    },
    userId: {
      type: Number,
      required: true
    },
    userName: {
      type: String,
      required: true
    },
    userAvatarUrl: {
      type: String,
      required: true
    },
    content: {
      type: String,
      required: true
    },
    time: {
      type: String,
      required: true
    },
    replyToCommentId: {
      type: Number,
      required: true
    },
    replies: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      isOpen: false,
      isInputVisible: false,
      replyContent: "",
      isAnonymous: false
    };
  },
  methods: {
    goToOtherUser,
    formatDate(time) {
      let date = new Date(Date.parse(time))
      let year = date.getFullYear();
      let month = ('0' + (date.getMonth() + 1)).slice(-2); // 月份从0开始，需要加1，并且保证两位数
      let day = ('0' + date.getDate()).slice(-2); // 保证两位数
      let hours = ('0' + date.getHours()).slice(-2); // 保证两位数
      let minutes = ('0' + date.getMinutes()).slice(-2); // 保证两位数

      return `${year}.${month}.${day}-${hours}:${minutes}`
    },
    toggleReplies() {
      this.isOpen = !this.isOpen;
    },
    showInput() {
      const state = UserStateStore()
      if (!state.email) {
        ElMessage.error("请先登录")
        return
      }
      this.isInputVisible = true;
    },
    sendReply() {
      // 将回复内容和是否匿名发送提交给后端或其他逻辑处理
      if (this.replyContent.trim().length > 0) {

        let json_set = {
          'blogId': this.blogId,
          'commentContent': this.replyContent,
          'ifAnonymous': this.isAnonymous,
          'replyToCommentId': this.commentId
        }
        uploadComment(json_set).then(
            (res) => {
              if (res.response == "success") {
                ElMessage({
                  message: '评论成功',
                  showClose: true,
                  type: 'success',
                })
                router.go(0)
              } else {
                ElMessage({
                  message: '评论失败，请修改内容或稍后再试',
                  showClose: true,
                  type: 'error',
                })
              }
            }
        )
      }

      // 发送完毕后，清空输入框并隐藏输入模块
      this.replyContent = "";
      this.isAnonymous = false;
      this.isInputVisible = false;
    }
  }
}
</script>

<style scoped>
.comment-card {
  position: relative;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 1%;
  margin-left: 2%;
  margin-right: 2%;
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 5px;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: bold;
  text-align: left;
}

.time {
  font-size: 12px;
  text-align: left;
  color: #888;
}

.content {
  word-wrap: break-word;
  text-align: left;
  margin-bottom: 10px;
}

.expand-button {
  position: absolute;
  bottom: 0;
  right: 0;
  margin: 10px;
}

.reply-input {
  margin-left: 2%;
  margin-right: 2%;
  margin-bottom: 2%;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  z-index: 1; /* 确保在其他内容之上 */
}

.reply-input textarea {
  width: 100%;
  margin-bottom: 10px;
}

.reply-input button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 5px 10px;
  cursor: pointer;
}

.reply-input label {
  margin-left: 5px;
}
</style>
