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
        style="text-align: left"
        :class="`cursor-pointer`"
        :color="isHovering ? 'cyan-lighten-5' : undefined"
        v-bind="props"
        @click="goToBlogCardView"
    >
      <v-row>
        <v-col cols="1" style="min-width: 50px">
          <v-avatar color="surface-variant" style="margin-top: 15px;margin-left: 10px" size="33"></v-avatar>
        </v-col>
        <v-col cols="5" style="text-align: left;">
          <div style="margin-top: 10px;">
            {{ truncatedContent }}
          </div>
          <div style="font-size: 12px;color: grey">
            {{ userName }} 发表于 {{ formatDate(time) }}
          </div>
        </v-col>
        <v-col cols="4" style="text-align: right;margin-top: 3px">
          <v-btn :prepend-icon="'mdi-thumb-up'" variant="text" size="small"
                 color="blue-grey-lighten-2">
            {{ 1 }}
          </v-btn>
          <v-btn variant="text" prepend-icon="mdi-message-text" size="small" color="blue-grey-lighten-2">
            {{ 2 }}
          </v-btn>
        </v-col>
      </v-row>
      <div style="margin-left: 10px;margin-bottom: 10px">
        <span style="margin-bottom: 10px">
          <v-chip
              v-for="(tag, index) in this.tags.filter(tag => this.tagList.includes(tag.tagId))"
              size="x-small"
              :key="index"
              :color="tag.tagColor"
              text-color="white"
              label
              outlined
          >
            {{ tag.tagName }}
          </v-chip>
          </span>
      </div>
    </v-card>
  </v-hover>

</template>

<script>
export default {
  name: "BlogShow",

  props: {
    blogId: {
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
    },

    formatDate(time) {
      let date = new Date(Date.parse(time))
      let year = date.getFullYear();
      let month = ('0' + (date.getMonth() + 1)).slice(-2); // 月份从0开始，需要加1，并且保证两位数
      let day = ('0' + date.getDate()).slice(-2); // 保证两位数
      let hours = ('0' + date.getHours()).slice(-2); // 保证两位数
      let minutes = ('0' + date.getMinutes()).slice(-2); // 保证两位数

      return `${year}.${month}.${day}-${hours}:${minutes}`
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
