<template>
  <v-hover v-slot="{ isHovering}">
    <v-card class="comment-card" v-show="replyToCommentId === null">
      <div class="user-info">
        <div v-if="userId !== -1" style="display:flex; justify-content: end;align-content: center">
          <UserAvatar :userId="userId"></UserAvatar>
          <span>
            <v-chip v-for="badge in badgeList" size="xsmall"
                    :key="badge.badgeId" :color="badge.badgeColor"
                    :class="`cursor-pointer`"
                    style="margin-left: 1%; margin-bottom: 5px;">
              {{ badge.badgeName }}
            </v-chip>
          </span>
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
      <v-row style="margin-bottom: 4px">
        <v-col :cols="useDisplay().smAndDown.value ? 10:10">
          <div v-if="!useDisplay().smAndDown.value">
            <div class="content" @click="showInput">
              <!--      <span style="white-space: pre-line" v-html="content"></span>-->
              <div style="white-space: pre-line" v-dompurify-html="content"/>
            </div>
          </div>
          <div v-else>
            <div class="content" @click="showBottomSheet">
              <!--      <span style="white-space: pre-line" v-html="content"></span>-->
              <div style="white-space: pre-line" v-dompurify-html="content"/>
            </div>
          </div>
        </v-col>
        <v-col cols="2" style="text-align: right; justify-content: end; margin-top: 3px">
          <v-menu v-show="isHovering || this.menuCLick" :location="'bottom'">
            <template v-slot:activator="{ props }">
              <v-btn
                  size="28px"
                  v-bind="props"
                  variant="text"
                  @click="this.menuCLick = !this.menuCLick"
                  class="rounded-circle"
              >
                <template v-slot:prepend>
                  <v-icon size="15">mdi-dots-vertical</v-icon>
                </template>
              </v-btn>
            </template>
            <v-list>
              <v-list-item density="compact">
                <div style="color: black; font-size: 16px" @click="showComplainWindow">
                  举报
                </div>
                <div v-if="userStateStore().isManager || this.isCurUser"
                     style="color: red; font-size: 16px" @click="delComment">
                  删除
                </div>
              </v-list-item>
            </v-list>
          </v-menu>

        </v-col>
      </v-row>
      <div v-show="replyToCommentId === null && replies.length > 0" class="expand-button">
        <button @click="toggleReplies" style="font-size: 12px; color: darkgray">{{
            isOpen ? '收起回复' : '展开回复'
          }}
        </button>
      </div>


      <div v-show="isInputVisible" class="reply-input">
        <v-textarea
            v-model="replyContent"
            placeholder="请输入回复内容"
            outlined
            rows="3"
            class="reply-textarea"
        ></v-textarea>
        <div class="anonymous-and-sendbutton">
          <v-checkbox
              v-model="isAnonymous"
              label="匿名发送"
              class="anonymous-checkbox"
              color="primary"
          ></v-checkbox>
          <v-btn @click.stop="sendReply" color="primary" class="send-button">
            发送
            <v-icon end>mdi-checkbox-marked-circle</v-icon>
          </v-btn>
        </div>
      </div>

      <div v-show="isOpen && replies.length > 0">
        <ReplyList :comments="replies" :top-comment-id="this.commentId"
                   @comment-show-new-comment="commentShowHandleNewComment"/>
      </div>

    </v-card>
  </v-hover>


  <v-bottom-sheet
      v-model="bottomSheet"
      v-if="useDisplay().smAndDown.value"
      class="transparent-bottom-sheet">
    <div class="reply-input">
      <v-textarea
          v-model="replyContent"
          placeholder="请输入回复内容"
          outlined
          rows="3"
          class="reply-textarea"
      ></v-textarea>
      <div class="anonymous-and-sendbutton">
        <v-checkbox
            v-model="isAnonymous"
            label="匿名发送"
            class="anonymous-checkbox"
            color="primary"
        ></v-checkbox>
        <v-btn @click.stop="sendReply" color="primary" class="send-button">
          发送
          <v-icon end>mdi-checkbox-marked-circle</v-icon>
        </v-btn>
      </div>
    </div>
  </v-bottom-sheet>

  <v-bottom-sheet
      v-model="showComplainWin"
      class="transparent-bottom-sheet">
    <div class="comment-input">
      <v-textarea
          v-model="complainCause"
          placeholder="输入您的举报理由"
          outlined
          rows="3"
          class="comment-textarea white-background"
      ></v-textarea>
      <div class="button-container">
        <v-btn @click="sendComplainMes()" color="red" class="submit-button">
          提交举报
          <v-icon end>mdi-alert-circle</v-icon>
        </v-btn>
      </div>
    </div>
  </v-bottom-sheet>

</template>

<script>
import ReplyList from "@/components/AnonymousBlog/ReplyList.vue";
import {
  deleteCommentByCommentId,
  goToOtherUser,
  submitComplainForBlogComment,
  uploadComment
} from "@/components/AnonymousBlog/api";
import {ElMessage} from "element-plus";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";
import UserStateStore, {userStateStore} from "@/store";
import {useDisplay} from "vuetify";
import {isShutUpByUserIdAPI} from "@/components/HelpCenter/api";
import {getBadgesByUserId} from "@/components/PersonalCenter/PersonalCenterAPI";

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
      isAnonymous: true,
      bottomSheet: false,
      menuCLick: false,
      showComplainWin: false,
      complainCause: "",
      badgeList: []
    };
  },

  created() {
    this.isCurUser = UserStateStore().getUserId === this.userId
    this.fetchBadgeInfo()
  },

  methods: {
    userStateStore,
    useDisplay,
    goToOtherUser,
    fetchBadgeInfo() {
      getBadgesByUserId(this.userId).then(
          (data) => {
            this.badgeList = data
          }
      )
    },
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
      isShutUpByUserIdAPI(userStateStore().user_id).then(
          (res) => {
            if (res.isShutUp) {
              ElMessage.error("您正处于禁言中，不能发布回答，请注意您的言论！")
            } else {
              this.isInputVisible = !this.isInputVisible;
            }
          }
      )
    },
    showBottomSheet() {
      const state = UserStateStore()
      if (!state.email) {
        ElMessage.error("请先登录")
        return
      }
      isShutUpByUserIdAPI(userStateStore().user_id).then(
          (res) => {
            if (res.isShutUp) {
              ElMessage.error("您正处于禁言中，不能发布回答，请注意您的言论！")
            } else {
              this.bottomSheet = !this.bottomSheet;
            }
          }
      )
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
                  message: '评论成功 ' + res.description,
                  showClose: true,
                  type: 'success',
                })
                location.reload()
              } else {
                ElMessage({
                  message: "内容违规：" + res.description,
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
    },

    showComplainWindow() {
      if (!UserStateStore().email) {
        ElMessage.error("请先登录")
        return
      }
      this.showComplainWin = !this.showComplainWin
    },

    sendComplainMes() {
      if (this.complainCause.length === 0) {
        ElMessage.error("举报原因不能为空！")
        return
      }
      const confirmSubmit = window.confirm("确定提交举报？我们承诺不向对方提供您的任何信息，但保留追究滥用举报行为的权力⚠");
      if (confirmSubmit) {
        let json_set = {
          "blogId": this.blogId,
          "commentId": this.commentId,
          "cause": this.complainCause
        }
        submitComplainForBlogComment(json_set).then(
            (res) => {
              if (res.response == "success") {
                ElMessage({
                  message: '举报成功！感谢您为论坛环境做出的贡献。',
                  showClose: true,
                  type: 'success',
                })
                this.complainCause = ""
                this.showComplainWin = false
              } else {
                ElMessage({
                  message: '举报失败，请修改内容或稍后再试...',
                  showClose: true,
                  type: 'error',
                })
              }
            }
        )
      }
    },

    delComment() {
      deleteCommentByCommentId(this.commentId).then(
          (res) => {
            if (res.response == "success") {
              ElMessage({
                message: '删除成功',
                showClose: true,
                type: 'success',
              })
              // this.$router.push({name: 'blogList', params: {tagId: -1}})
              location.reload()
            } else {
              ElMessage({
                message: '删除失败，请先登录或稍后再试',
                showClose: true,
                type: 'error',
              })
            }
          }
      )
    },

    commentShowHandleNewComment(comment) {
      this.$emit('comment-list-new-comment', comment);
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
  margin-left: 3px;
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
  margin: 3px;
}

.reply-input {
  margin-left: 1%;
  margin-right: 1%;
  margin-bottom: 15px;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 10px;
  z-index: 1; /* 确保在其他内容之上 */
}

.reply-textarea {
  margin-bottom: 1px;
}

.anonymous-and-sendbutton {
  margin-top: -15px;
  margin-bottom: -12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.anonymous-checkbox {
  margin-right: 10px;
}

.send-button {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 28px;
}

.transparent-bottom-sheet {
  background-color: transparent !important;
}

.comment-input {
  margin-left: 1%;
  margin-right: 1%;
  margin-bottom: 15px;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 10px;
  z-index: 1; /* 确保在其他内容之上 */
}

.white-background {
  background-color: white;
}

.button-container {
  display: flex;
  justify-content: flex-end;
}

.submit-button {
  height: 28px;
}

/*.reply-input textarea {*/
/*  width: 100%;*/
/*  margin-bottom: 10px;*/
/*}*/

/*.reply-input button {*/
/*  background-color: #007bff;*/
/*  color: #fff;*/
/*  border: none;*/
/*  border-radius: 3px;*/
/*  padding: 5px 10px;*/
/*  cursor: pointer;*/
/*}*/

/*.reply-input label {*/
/*  margin-left: 5px;*/
/*}*/
</style>
