<template>
  <v-btn-toggle v-model="nowSearchObj" mandatory shaped>
    <v-btn value="ques" @click="reloadBySearchObj('ques')">
      <v-icon>mdi-help-box</v-icon>
      互助帖
    </v-btn>

    <v-btn value="blog" @click="reloadBySearchObj('blog')">
      <v-icon>mdi-account-cowboy-hat-outline</v-icon>
      匿名帖
    </v-btn>

    <v-btn value="user" @click="reloadBySearchObj('user')">
      <v-icon>mdi-account</v-icon>
      用户
    </v-btn>
  </v-btn-toggle>

  <v-btn-toggle v-if="false" v-model="nowSortMethod" mandatory shaped>
    <v-btn value="byRelation" @click="reloadBySortMethod('byRelation')">
      <v-icon color="blue">mdi-link</v-icon>
      相关度
    </v-btn>

    <v-btn value="byPopularity" @click="reloadBySortMethod('byPopularity')">
      <v-icon color="red">mdi-fire</v-icon>
      热度
    </v-btn>

    <v-btn value="byTime" @click="reloadBySortMethod('byTime')">
      <v-icon color="green">mdi-clock</v-icon>
      时间
    </v-btn>
  </v-btn-toggle>

  <v-divider></v-divider>
  <div v-if="this.nowSearchObj==='ques'">
    <div class="blog-list">
      <PlainQuesCard style="margin-bottom: 5px" v-for="ques in searchQuesList" :key="ques.quesId"
                     :tags="tags"
                     :question="ques"/>
    </div>

  </div>
  <div v-if="this.nowSearchObj==='blog'">
    <div class="blog-list">
      <BlogShow
          v-for="(post, index) in searchBlogList"
          :key="index"
          :blog-id="post.blogId"
          :user-name="post.userName"
          :user-avatar-url="post.userAvatarUrl"
          :title="post.title"
          :content="post.content"
          :time="post.time"
          :tag-list="post.tagList"
          :user-id="post.userId"
      />
    </div>
  </div>
  <div v-if="this.nowSearchObj==='user'">
    <!--    todo 显示用户列表 -->
    <div>
      <UserShow
          v-for="(post, index) in searchUserList"
          :key="index"
          :nickname="post.nickname"
          :sign="post.sign"
          :email="post.email"
          :headImage="post.url"
      >
        <!-- <v-divider style="margin-top: 0px;"></v-divider> -->

      </UserShow>
    </div>
  </div>

  <button @click="loadMore" class="load-more-button">加载更多</button>
</template>

<script>
import {searchBlogAPage, searchQuesAPage, searchUserAPage} from "@/components/AdvanceSearch/api";
import BlogShow from "@/components/AnonymousBlog/BlogShow.vue";
import UserShow from "@/components/PersonalCenter/UserShow.vue";
import {useRouter} from "vue-router";
import {getTagsApi} from "@/components/HelpCenter/api";
import PlainQuesCard from "@/components/HelpCenter/PlainQuesCard.vue";

export default {
  name: "searchList",
  components: {PlainQuesCard, BlogShow, UserShow},

  data() {
    return {
      searchContent: "",
      nowSearchObj: "ques",
      nowSortMethod: "byTime",
      searchBlogList: [],
      searchQuesList: [],
      searchUserList: [],
      quesPageSize: 15,
      blogPageSize: 15,
      userPageSize: 15,
      quesPageNo: 1,
      blogPageNo: 1,
      userPageNo: 1,
      isFetchingQues: false,
      isFetchingBlog: false,
      isFetchingUser: false,
      tags: [],
    }
  },
  watch: {
    '$route'(to) {
      // Update searchContent when route changes
      this.searchContent = to.params.keywords || '';
      this.nowSearchObj = "ques"
      this.nowSortMethod = "byTime"
      this.searchQuesList = []
      this.searchBlogList = []
      this.searchUserList = []
      this.quesPageNo = 1
      this.blogPageNo = 1
      this.userPageNo = 1
      this.isFetchingBlog = false
      this.isFetchingQues = false
      this.isFetchingUser = false
      this.searchQues()
    }
  },
  created() {
    let router = useRouter()
    this.searchContent = router.currentRoute.value.params.keywords
    // this.searchContent = this.$props.keywords
    // console.log(this.searchContent)
    this.nowSearchObj = "ques"
    this.nowSortMethod = "byTime"
    this.searchQuesList = []
    this.searchBlogList = []
    this.searchUserList = []
    this.tags = []
    this.quesPageNo = 1
    this.blogPageNo = 1
    this.userPageNo = 1
    this.isFetchingBlog = false
    this.isFetchingQues = false
    this.isFetchingUser = false
    this.loadMore()
    // console.log("this.searchUserList")
    // console.log(this.searchUserList)
  },
  methods: {
    searchBlogs() {
      if (this.isFetchingBlog) {
        return
      }
      this.isFetchingBlog = true

      searchBlogAPage(this.searchContent, this.blogPageNo, this.blogPageSize, this.nowSortMethod).then(
          (data) => {
            // this.searchBlogList = this.searchBlogList.concat(data.blogs)
            this.searchBlogList = this.searchBlogList.concat(data.map(blog => ({
              userName: blog.userName,
              userAvatarUrl: blog.userAvatarUrl,
              blogId: blog.blogId,
              title: blog.title,
              content: blog.content,
              time: blog.time,
              tagList: blog.tagList,
              userId: blog.userId
            })));
            this.isFetchingBlog = false
          }
      )
    },

    searchQues() {
      if (this.isFetchingQues) {
        return
      }
      this.isFetchingQues = true
      searchQuesAPage(this.searchContent, this.quesPageNo, this.quesPageSize, this.nowSortMethod).then(
          (data) => {
            this.searchQuesList = this.searchQuesList.concat(data.questions)
            this.isFetchingQues = false
            getTagsApi().then(
                (data) => {
                  this.tags = data.tags
                }
            )
            // this.searchQuesList = this.searchQuesList.concat(data.map(ques => ({
            //   quesId: ques.quesId,
            //   userId: ques.userId,
            //   userName: ques.userName,
            //   quesContent: ques.quesContent,
            //   quesState: ques.quesState,
            //   quesTime: ques.quesTime,
            //   ifUserLike: ques.ifUserLike,
            //   ansSum: ques.ansSum,
            //   likeSum: ques.likeSum,
            //   tagIdList: ques.tagIdList
            // })));
          }
      )
    },

    searchUsers() {

      if (this.isFetchingUser) {
        return
      }
      this.isFetchingUser = true
      searchUserAPage(this.searchContent, this.userPageNo, this.userPageSize, this.nowSortMethod).then(
          (data) => {
            this.searchUserList = this.searchUserList.concat(data.users)
            this.isFetchingUser = false
          }
      )
    },

    loadMore() {
      if (this.nowSearchObj === "user") {
        this.searchUsers()
        this.userPageNo += 1
      } else if (this.nowSearchObj === "blog") {
        this.searchBlogs()
        this.blogPageNo += 1
      } else {
        this.searchQues()
        this.quesPageNo += 1
      }
      // console.log(this.userPageNo)
      // console.log(this.blogPageNo)
      // console.log(this.quesPageNo)
    },

    reloadBySortMethod(sortMethod) {
      this.nowSortMethod = sortMethod
      this.searchQuesList = []
      this.searchBlogList = []
      this.searchUserList = []
      this.quesPageNo = 1
      this.blogPageNo = 1
      this.userPageNo = 1
      this.loadMore()
    },

    reloadBySearchObj(searchObj) {
      this.nowSearchObj = searchObj
      this.searchQuesList = []
      this.searchBlogList = []
      this.searchUserList = []
      this.quesPageNo = 1
      this.blogPageNo = 1
      this.userPageNo = 1
      this.loadMore()
    }
  }
}
</script>

<style scoped>
.blog-list {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
}

.load-more-button {
  width: 96%;
  align-self: center;
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #0291ff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 100px;
}

.load-more-button:hover {
  background-color: #0056b3;
}
</style>