<template>
  <v-card class="blog-view">
    <!-- 用户信息部分 -->
    <div class="user-info" @click="goToOtherUser(userId)">
      <div v-if="this.userId !== -1" style="display:flex; justify-content: end;align-content: center">
        <UserAvatar :userId="this.userId"></UserAvatar>
      </div>
      <div v-if="this.userId === -1" style="display:flex; justify-content: end;align-content: center">
        <v-avatar style="margin-top:8px">
          <v-img :src="this.userAvatarUrl"></v-img>
        </v-avatar>
      </div>
    </div>
    <!-- 发帖时间 -->
    <div class="time"> {{ formatDate(time) }}</div>

    <!-- 内容部分 -->
    <div class="title">
      <p>{{ title }}</p>
    </div>

    <div class="content">
      <p>{{ content }}</p>
      <div class="image-list">
<!--        <img v-for="(image, index) in imageList" :key="index" :src="image" class="blog-image"/>-->

        <v-row>
          <v-col v-for="(image,index) in imageList"
                 :key="'image' + index" :cols="useDisplay().smAndDown.value? 4 : 3"
          >
            <div class="avatar-wrapper">
              <el-image
                  class="avatar"
                  :src="image"
                  :fit="'cover'"
                  @click="showPic(imageList)"
              />
            </div>
          </v-col>
        </v-row>
      </div>
    </div>

    <!-- 评论按钮 -->
    <div v-if="!showCommentInput" class="comment-input">
      <v-btn @click="toggleCommentInput" class="ma-2" color="blue">添加评论
        <v-icon
            icon="mdi-message-text"
            end
        ></v-icon>
      </v-btn>
    </div>
    <!-- 评论输入框 -->
    <div v-if="showCommentInput" class="comment-input">
      <v-textarea v-model="newComment" placeholder="输入您的评论"></v-textarea>
      <div class="anonymous-and-addbutton">
        <v-checkbox v-model="commentAnonymous" label="匿名发布" class="anonymous-checkbox"></v-checkbox>
        <v-btn @click="addComment(null)" class="ma-2" color="green">提交评论
          <v-icon
              icon="mdi-checkbox-marked-circle"
              end
          ></v-icon>
        </v-btn>
      </div>
    </div>

  </v-card>

  <!-- 评论列表 -->
  <CommentList :comments="comments"/>
</template>

<script>
import CommentList from "@/components/AnonymousBlog/CommentList.vue";
import {getBlogByBlogId, getCommentsByBlogId, goToOtherUser, uploadComment} from "@/components/AnonymousBlog/api";
import {ElMessage} from "element-plus";
import {useRouter} from "vue-router";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";
import UserStateStore from "@/store";
import {api as viewerApi} from "v-viewer";
import {useDisplay} from "vuetify";
import router from "@/router";

export default {
  name: "BlogView",
  components: {UserAvatar, CommentList},

  setup() {
    const showPic = (imgList) => {
      viewerApi({images: imgList})
    }

    return {
      showPic
    }
  },

  data() {
    return {
      blogId: '',
      userId: -1,
      userName: '',
      userAvatarUrl: '',
      title: '',
      content: '',
      imageList: [],
      time: "",
      tagList: [],
      comments: [],
      showCommentInput: false,
      newComment: '',
      commentAnonymous: false
    };
  },

  created() {
    let router = useRouter();
    this.blogId = router.currentRoute.value.params.id;
    this.fetchBlogInfo(); //todo
    this.fetchCommentInfo();  //todo
  },


  methods: {
    useDisplay,
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
    fetchBlogInfo() {
      // 该方法接受一个博客 ID，并返回博客信息
      getBlogByBlogId(this.blogId).then(
          (data) => {
            this.userName = data.userName
            this.userAvatarUrl = data.userAvatarUrl
            this.title = data.title
            this.content = data.content
            this.imageList = data.imageList
            this.time = data.time
            this.tagList = data.tagList
            this.userId = data.userId
          }
      )
    },
    fetchCommentInfo() {
      // 发起后端数据请求，获取博客对应的评论信息
      getCommentsByBlogId(this.blogId).then(
          (data) => {
            // this.comments = data.comments
            this.comments = data.map(comment => ({
              userId: comment.userId,
              userName: comment.userName,
              userAvatarUrl: comment.userAvatarUrl,
              blogId: this.blogId,
              commentId: comment.commentId,
              content: comment.commentContent,
              time: comment.time,
              replyToCommentId: comment.replyToCommentId,
            }))
          }
      )
    },
    toggleCommentInput() {
      const state = UserStateStore()
      if (!state.email) {
        ElMessage.error("请先登录")
        return
      }
      this.showCommentInput = !this.showCommentInput;
    },
    addComment(replyToId) {
      const state = UserStateStore()
      if (!state.email) {
        ElMessage.error("请先登录")
        return
      }
      // todo 提交评论的逻辑，读取评论和用户信息，存入数据库，同步加入 comments 列表
      if (this.newComment.trim().length !== 0) {
        // let form = new FormData
        // form.append('blogId', this.blogId)
        // form.append('commentContent', this.newComment)
        // form.append('ifAnonymous', this.commentAnonymous)
        // form.append('replyToCommentId', replyToId)

        let json_set = {
          'blogId': this.blogId,
          'commentContent': this.newComment,
          'ifAnonymous': this.commentAnonymous,
          'replyToCommentId': replyToId
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
      this.newComment = '';
      this.showCommentInput = false;
    },
  }
};
</script>

<style scoped>
.blog-view {
  margin-top: 20px;
  margin-left: 2%;
  margin-right: 2%;
  padding: 20px;
  border: 2px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 3px;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.user-name {
  font-size: 20px;
  font-weight: bold;
}

.title {
  font-weight: bold;
  font-size: 24px;
  line-height: 1.6;
  text-align: left;
}

.content {
  margin-top: 1%;
  line-height: 1.6;
  text-align: left;
}

.image-list {
  margin-top: 20px;
}

.blog-image {
  max-height: 150px;
  height: 100%;
  width: auto;
  margin-bottom: 10px;
}

.time {
  font-size: 14px;
  color: #888;
  margin-bottom: 20px;
  text-align: left;
}

.comment-input {
  display: flex;
  flex-direction: column;
  margin-top: 10px;
}

.anonymous-and-addbutton {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.anonymous-checkbox {
  margin-left: 1%;
}


</style>
