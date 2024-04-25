<template>
  <div class="blog-card" @click="goToBlogCardView">
    <div class="user-info">
      <div class="left-section">
        <img :src="userAvatarUrl" :alt="userName" class="user-avatar"/>
        <div class="user-details">
          <span class="user-name">{{ userName }}</span>
          <span class="time">{{ time }}</span>
        </div>
      </div>
      <div class="tag-container">
        <v-chip
            v-for="(tag, index) in this.tags.filter(tag => this.tagList.includes(tag.tagName))"
            :key="index"
            :color="tag.tagColor"
            text-color="white"
            label
            outlined
        >
          {{ tag.tagName }}
        </v-chip>
      </div>
    </div>
    <div class="title">
      {{ title }}
    </div>
    <div class="content">
      {{ truncatedContent }}
    </div>
  </div>
</template>

<script>
export default {
  name: "BlogShow",

  props: {
    blogId: {
      type: String,
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
    }
  },

  data() {
    return {
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

  computed: {
    truncatedContent() {
      if (this.content.length > 200) {
        return this.content.substring(0, 200) + "...";
      } else {
        return this.content;
      }
    }
  },

  methods: {
    goToBlogCardView() {
      const blogId = this.$props.blogId;
      this.$router.push({name: 'blogView', params: {id: blogId}});
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
  align-items: center;
  margin-bottom: 10px;
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
