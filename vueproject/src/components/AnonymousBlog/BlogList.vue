<template>
  <v-layout class="rounded rounded-md">

    <v-navigation-drawer align="start" width="160" style="position: fixed; margin-top: 60px">
      <v-list dense>
        <v-list-item>
          <v-btn @click="goToNewBlog" class="w-100" color="blue">发帖
            <v-icon
                icon="mdi-send"
                end
            ></v-icon>
          </v-btn>
        </v-list-item>

        <v-list-item v-for="tag in tags" :key="tag.tagId">
          <v-list-item-content>
            <v-btn @click="swithConcernedTag(tag.tagId)" class="w-100">{{ tag.tagName }}
              <v-icon
                  :icon="tag.tagIcon"
                  :color="tag.tagColor"
                  end
              ></v-icon>
            </v-btn>
          </v-list-item-content>
        </v-list-item>

      </v-list>
    </v-navigation-drawer>

    <v-main style="min-height: 300px; height: 100%; overflow: auto" align="start">
      <div class="blog-list">
        <BlogShow
            v-for="(post, index) in blogs"
            :key="index"
            :blog-id="post.blogId"
            :user-name="post.userName"
            :user-avatar-url="post.userAvatarUrl"
            :title="post.title"
            :content="post.content"
            :time="post.time"
            :tag-list="post.tagList"
            :comment-num="post.commentNum"
            :user-id="post.userId"
            :tags = "this.tags"
        />

        <button @click="loadMore" class="load-more-button">加载更多</button>
      </div>

      <div v-if="useDisplay().smAndDown.value" class="left-buttons">
        <div>
          <v-btn :icon="'mdi-plus'"
                 color="light-blue-darken-1"
                 size="small" @click="goToNewBlog"
          />
        </div>
      </div>
    </v-main>
  </v-layout>

</template>

<script>
import BlogShow from './BlogShow.vue';
import {getBlogs, getTags} from "@/components/AnonymousBlog/api";
import {useDisplay} from "vuetify";

export default {
  name: 'BlogList',

  components: {
    BlogShow,
  },

  data() {
    return {
      //todo 调试
      blogs: [],
      pageno: 1,
      pagesize: 15,
      nowtag: -1,
      tags: [],
      isFetching: false // 是否正在请求数据的标志位
    };
  },

  created() {
    this.nowtag = -1
    this.pageno = 1
    this.blogs = []
    this.fetchBlogListAPage();
    getTags().then(tags => {
      console.log("Tags:", tags); // 检查getTags()返回的标签列表
      this.tags = tags;
      // localStorage.setItem("blogTags", tags)
    }).catch(error => {
      console.error("Failed to fetch tags:", error);
    });
  },

  methods: {
    useDisplay,
    fetchBlogListAPage() {
      // 如果正在请求数据，则直接返回，避免多次请求
      if (this.isFetching) {
        return;
      }
      // 设置标志位为 true，表示正在请求数据
      this.isFetching = true;
      // 发起后端数据请求，获取一页的博客简要信息
      getBlogs(this.pageno, this.pagesize, this.nowtag).then(
          (data) => {
            // this.blogs.concat(data.blogs)
            this.blogs = this.blogs.concat(data.map(blog => ({
              userId: blog.userId,
              userName: blog.userName,
              userAvatarUrl: blog.userAvatarUrl,
              blogId: blog.blogId,
              title: blog.title,
              content: blog.content,
              time: blog.time,
              tagList: blog.tagList,
              commentNum: blog.commentNum
            })));
            this.isFetching = false;
          }
      )
    },

    loadMore() {
      this.pageno++;
      this.fetchBlogListAPage();
    },

    swithConcernedTag(changToTag) {
      this.pageno = 1
      this.nowtag = changToTag
      this.blogs = []
      this.fetchBlogListAPage()
    },

    goToNewBlog() {
      this.$router.push({path: `/blogNew`});
    },
  }

};
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

.left-buttons {
  position: fixed;
  z-index: 888;
  top: 80%;
  right: 2%;
  transform: translateY(-50%);
}

</style>
