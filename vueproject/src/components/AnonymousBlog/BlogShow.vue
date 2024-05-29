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
              <v-list-item density="compact" v-if="this.isCurUser">
                <div style="color: red; font-size: 16px" @click="delDialog = !delDialog">
                  删除
                </div>
              </v-list-item>
              <v-list-item density="compact">
                <div style="color: black; font-size: 16px" @click="sendReportMes">
                  举报
                </div>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-col>
      </v-row>

      <div style="margin-left: 2%; margin-bottom: 3px; font-size: 12px; color: gray" @click="goToBlogCardView">
        {{ truncatedContent }}
      </div>

      <div style="margin-left: 2%; margin-bottom: 5px">
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

</template>

<script>
import {deleteBlogByBlogId, goToOtherUser} from "@/components/AnonymousBlog/api";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";
import {useDisplay} from "vuetify";
import UserStateStore from "@/store"
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

    sendReportMes() {
      ElMessage({
        message: '感谢您对平台风气的关心和维护，举报自动处理功能尚在开发中...',
        showClose: true
      })
      ElMessage({
        message: '当前您可以直接联系开发人员进行举报和删帖，再次感谢！',
        showClose: true
      })
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

</style>
