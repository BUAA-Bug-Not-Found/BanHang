<template>
  <div class="comment-card">
    <div class="user-info" >
      <div v-if="this.userId !== -1" style="display:flex; justify-content: end;align-content: center">
        <UserAvatar :userId="this.userId"></UserAvatar>
      </div>
      <div v-if="this.userId === -1" style="display:flex; justify-content: end;align-content: center">
        <v-avatar style="margin-top:8px">
          <v-img :src="this.userAvatarUrl"></v-img>
        </v-avatar>
      </div>
      <div class="user-details">
        <span class="user-name">{{ userName }}</span>
        <span class="time">{{ formatDate(time) }}</span>
      </div>
    </div>
    <div class="content">
      {{ content }}
    </div>
  </div>
</template>

<script>
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";

export default {
  name: "ReplyShow",
  components: {UserAvatar},

  props: {
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
  },

  methods: {
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
}
</script>


<style scoped>

.comment-card {
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
  margin-bottom: 4px;
}

.user-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  margin-right: 5px;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 12px;
  font-weight: bold;
  text-align: left;
}

.time {
  font-size: 8px;
  color: #888;
}

.content {
  word-wrap: break-word;
  text-align: left;
}

</style>