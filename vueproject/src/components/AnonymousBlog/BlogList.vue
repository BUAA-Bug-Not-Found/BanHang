<template>
  <v-layout class="rounded rounded-md">

    <v-navigation-drawer align="start" width="160">
      <v-list dense>
        <v-list-item v-for="tag in tags" :key="tag.tagId">
          <v-list-item-content>
            <v-btn @click="swithConcernedTag(tag.tagName)" class="ma-1">{{ tag.tagName }}
              <v-icon
                  :icon= "tag.tagIcon"
                  :color="tag.tagColor"
                  end
              ></v-icon>
            </v-btn>

<!--            <v-icon :color="tag.tagColor">{{ tag.tagIcon }}</v-icon>-->
<!--            <v-list-item-title>{{ tag.tagName }}</v-list-item-title>-->
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main style="min-height: 300px;" align="start">
      <v-btn @click="goToNewBlog" class="ma-5" color="blue">发帖
        <v-icon
            icon="mdi-send"
            end
        ></v-icon>
      </v-btn>
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
        />

        <button @click="loadMore" class="load-more-button">加载更多</button>
      </div>
    </v-main>
  </v-layout>

</template>

<script>
import BlogShow from './BlogShow.vue';
import {getBlogs} from "@/components/AnonymousBlog/api";

export default {
  name: 'BlogList',

  components: {
    BlogShow,
  },

  data() {
    return {
      //todo 调试
      blogs: [
        {
          blogId: '1',
          userName: 'Alice',
          userAvatarUrl: 'https://argithun-blog-1321510384.cos.ap-beijing.myqcloud.com/OO1.jpg',
          title: 'My First Blog!!!',
          content: 'This is the first post.',
          time: "2024.04.21-15:30",
          tagList: ["学习生活", "情感交流"]
        },
        {
          blogId: '2',
          userName: 'Bob',
          userAvatarUrl: 'https://argithun-blog-1321510384.cos.ap-beijing.myqcloud.com/OO2.jpg',
          title: 'My Second Blog!!!',
          content: 'This is the second post.',
          time: "2024.04.21-15:30",
          tagList: ["学习生活", "日常事务"]
        },
        {
          blogId: '3',
          userName: 'Charlie',
          userAvatarUrl: 'https://argithun-blog-1321510384.cos.ap-beijing.myqcloud.com/OO3.jpg',
          title: 'My Third Blog!!!',
          content: 'This is the third post.',
          time: "2024.04.21-15:30",
          tagList: ["学习生活", "灌水吐槽", "寻欢作乐"]
        }
      ],
      pageno: 1,
      pagesize: 15,
      nowtag: "",
      tags: [
        {
          tagId: 1,
          tagName: '学习生活',
          tagIcon: 'mdi-clock',
          tagColor: 'blue-darken-1'
        },
        {
          tagId: 2,
          tagName: '日常事务',
          tagIcon: 'mdi-account',
          tagColor: 'cyan-darken-1'
        },
        {
          tagId: 3,
          tagName: '情感交流',
          tagIcon: 'mdi-heart',
          tagColor: 'red-darken-1'
        },
        {
          tagId: 4,
          tagName: '灌水吐槽',
          tagIcon: 'mdi-comment-alert-outline',
          tagColor: 'green-darken-1'
        },
        {
          tagId: 5,
          tagName: '寻欢作乐',
          tagIcon: 'mdi-emoticon-outline',
          tagColor: 'purple-darken-1'
        },
      ]
    };
  },

  created() {
    this.nowtag = ""
    this.pageno = 1
    // todo this.blogs = []
    // todo this.fetchBlogListAPage();
  },

  methods: {
    fetchBlogListAPage() {
      // 发起后端数据请求，获取一页的博客简要信息
      getBlogs(this.pageno, this.pagesize, this.nowtag).then(
          (data) => {
            this.blogs = this.blogs.concat(data.map(blog => ({
              userName: blog.userName,
              userAvatarUrl: blog.userAvatarUrl,
              blogId: blog.blogId,
              title: blog.title,
              content: blog.content,
              time: blog.time,
              tagList: blog.tagList
            })));
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

</style>
