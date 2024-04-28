<template>
  <div class="comment-card" >
    <div class="user-info">
      <img :src="userAvatarUrl" :alt="userName" class="user-avatar"/>
      <div class="user-details">
        <span class="user-name">{{ userName }}</span>
        <span class="time">{{ time }}</span>
      </div>
    </div>
    <div class="content">
      {{ content }}
    </div>
  </div>
</template>

<script>
export default {
  name: "ReplyShow",

  props: {
    commentId: {
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