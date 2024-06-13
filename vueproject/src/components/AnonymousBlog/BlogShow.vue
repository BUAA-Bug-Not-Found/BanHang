<template>

  <!--  <div class="blog-card" @click="goToBlogCardView">-->
  <!--    <div class="user-info">-->
  <!--      <v-col cols="7" style="text-align: left;">-->
  <!--        <div class="left-section">-->
  <!--          <img :src="userAvatarUrl" :alt="userName" class="user-avatar"/>-->
  <!--          <div class="user-details">-->
  <!--            <span class="user-name">{{ userName }}</span>-->
  <!--            <span class="time">{{ time }}</span>-->
  <!--          </div>-->
  <!--        </div>-->
  <!--      </v-col>-->
  <!--      <v-col cols="4" style="text-align: left">-->
  <!--        <div class="tag-container">-->
  <!--          <v-btn :prepend-icon="'mdi-thumb-up'" variant="text" size="small"-->
  <!--                 color="blue-grey-lighten-2">-->
  <!--            {{ 1 }}-->
  <!--          </v-btn>-->
  <!--          <v-btn variant="text" prepend-icon="mdi-message-text" size="small" color="blue-grey-lighten-2">-->
  <!--            {{ 2 }}-->
  <!--          </v-btn>-->
  <!--        </div>-->
  <!--        <div class="tag-container">-->
  <!--          <v-chip-->
  <!--              v-for="(tag, index) in this.tags.filter(tag => this.tagList.includes(tag.tagId))"-->
  <!--              size="x-small"-->
  <!--              :key="index"-->
  <!--              :color="tag.tagColor"-->
  <!--              text-color="white"-->
  <!--              label-->
  <!--              outlined-->
  <!--          >-->
  <!--            {{ tag.tagName }}-->
  <!--          </v-chip>-->
  <!--        </div>-->
  <!--      </v-col>-->
  <!--    </div>-->
  <!--    <div class="title">-->
  <!--      {{ title }}-->
  <!--    </div>-->
  <!--    <div class="content">-->
  <!--      {{ truncatedContent }}-->
  <!--    </div>-->
  <!--  </div>-->

  <v-hover v-slot="{ isHovering, props }">
    <v-card
        class="mx-auto"
        width="96%"
        :color="isHovering ? 'grey-lighten-3' : 'white'"
        v-bind="props"
    >
      <v-row>
        <v-col :cols="useDisplay().smAndDown.value ? 3 : 1">
          <div v-if="this.userId !== -1" style="display:flex; justify-content: end;align-content: center">
            <UserAvatar :userId="this.userId"></UserAvatar>
          </div>
          <div v-if="this.userId === -1" style="display:flex; justify-content: end;align-content: center">
            <v-avatar v-bind="props" style="margin-top:8px">
              <v-img :src="this.userAvatarUrl"></v-img>
            </v-avatar>
          </div>
        </v-col>
        <v-col cols="6" style="text-align: left;" :class="`cursor-pointer`" @click="goToBlogCardView">
          <div style="margin-top: 10px;">
            {{ title }}
          </div>
          <div style="font-size: 12px;color: darkgray">
            {{ userName }} 发表于 {{ formatDate(time) }}
          </div>
        </v-col>
        <v-col cols="3" style="text-align: right; justify-content: end; margin-top: 3px">
          <v-btn variant="text" prepend-icon="mdi-message-text" size="small" color="blue-grey-lighten-2"
                 @click="goToBlogCardView">
            {{ this.commentNum }}
          </v-btn>
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
              <v-list-item density="compact" v-if="this.isCurUser || userStateStore().isManager">
                <div style="color: red; font-size: 16px" @click="delDialog = !delDialog">
                  删除
                </div>
              </v-list-item>
              <v-list-item density="compact">
                <div style="color: black; font-size: 16px" @click="showComplainWindow">
                  举报
                </div>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-col>
      </v-row>

      <div style="margin-left: 5%; margin-right: 2%;margin-bottom: 3px; font-size: 12px; color: gray" @click="goToBlogCardView">
        {{ truncatedContent }}
      </div>

      <div style="margin-left: 5%; margin-bottom: 5px">
        <span style="margin-bottom: 10px">
          <v-chip
              v-for="(tag, index) in this.tagList"
              size="x-small"
              :key="index"
              :color="tag.tagColor"
              text-color="white"
              label
              outlined
              @click="gotoBlogList(tag.tagId)"
          >
            {{ tag.tagName }}
          </v-chip>
          <v-chip v-if="this.tagList.length === 0" color="transparent" size="x-small">
          </v-chip>
          </span>
      </div>
    </v-card>
  </v-hover>

  <v-dialog
      v-model="delDialog"
      width="auto"
  >
    <v-card
        max-width="400"
        min-width="200"
        prepend-icon="mdi-delete-clock"
        text="您的帖子将会被删除，确认嘛？"
        title="删除帖子"
    >
      <template v-slot:actions>
        <div style="display: flex; justify-content: center;">
          <v-btn
              variant="flat"
              density="compact"
              text="确认"
              color="red-darken-1"
              @click="delBlog"
          ></v-btn>

          <v-btn
              text="取消"
              density="compact"
              @click="delDialog = false"
          ></v-btn>
        </div>
      </template>
    </v-card>

  </v-dialog>

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
import {deleteBlogByBlogId, goToOtherUser, submitComplainForBlog} from "@/components/AnonymousBlog/api";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";
import {useDisplay} from "vuetify";
import UserStateStore, {userStateStore} from "@/store"
import {ElMessage} from "element-plus";

export default {
  name: "BlogShow",
  components: {UserAvatar},

  props: {
    blogId: {
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
    title: {
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
    tagList: {
      type: Array,
      required: true
    },
    commentNum: {
      type: Number,
      required: true
    },
    tags: {
      type: Array,
      required: true
    }
  },

  data() {
    return {
      menuCLick: false,
      delDialog: false,
      isCurUser: false,
      showComplainWin: false,
      complainCause: "",
      randomColor: this.getRandomColor()
    }
  },

  created() {
    this.isCurUser = UserStateStore().getUserId === this.userId
    this.randomColor = this.getRandomColor()
  },

  computed: {
    truncatedContent() {
      if (this.content.length > 200) {
        return this.content.substring(0, 150) + "...";
      } else {
        return this.content;
      }
    }
  },

  methods: {
    userStateStore,
    useDisplay,
    goToOtherUser,
    goToBlogCardView() {
      const blogId = this.$props.blogId;
      this.$router.push({name: 'blogView', params: {id: blogId}});
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

    gotoBlogList(tagId) {
      this.$router.push({name: 'blogList', params: {tagId: tagId}})
    },

    delBlog() {
      deleteBlogByBlogId(this.blogId).then(
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
          "cause": this.complainCause
        }
        submitComplainForBlog(json_set).then(
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

    getRandomColor() {
      const colors = [
        'rgba(255, 182, 193, 0.2)',  // lightpink
        'rgba(173, 216, 230, 0.2)',  // lightblue
        'rgba(144, 238, 144, 0.2)',  // lightgreen
        'rgba(255, 255, 224, 0.2)',  // lightyellow
        'rgba(221, 160, 221, 0.2)',  // plum
        'rgba(240, 230, 140, 0.2)',  // khaki
        'rgba(135, 206, 250, 0.2)',  // light sky blue
        'rgba(255, 192, 203, 0.2)',  // pink
        'rgba(176, 224, 230, 0.2)',  // powder blue
      ];
      return colors[Math.floor(Math.random() * colors.length)];
    }
  }
};
</script>

<style scoped>
.blog-card {
  border: 2px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 1%;
  margin-left: 2%;
  margin-right: 2%;
  cursor: pointer;
}


.user-info {
  display: flex;
}

.left-section {
  display: flex;
  align-items: center;
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
  color: #888;
}

.tag-container {
  display: flex;
  justify-content: flex-end;
  flex-wrap: wrap; /* 允许多行布局 */
}

.title {
  font-weight: bold;
  word-wrap: break-word;
  text-align: left;
}

.content {
  word-wrap: break-word;
  text-align: left;
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

.comment-textarea {
  margin-bottom: 1px;
}

.button-container {
  display: flex;
  justify-content: flex-end;
}

.submit-button {
  height: 28px;
}

.transparent-bottom-sheet {
  background-color: transparent !important;
}

.white-background {
  background-color: white;
}

</style>
