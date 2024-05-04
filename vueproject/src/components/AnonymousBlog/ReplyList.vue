<template>
  <div class="comment-list">
    <ReplyShow
        v-for="(comment, index) in comments"
        :key="index"
        :comment-id="comment.commentId"
        :user-id="comment.userId"
        :user-name="comment.userName"
        :user-avatar-url="comment.userAvatarUrl"
        :content="comment.content"
        :time="comment.time"
    />
  </div>
</template>

<script>
import ReplyShow from "@/components/AnonymousBlog/ReplyShow.vue";

export default {
  name: "ReplyList",
  components: {ReplyShow},
  props: {
    comments: {
      type: Array,
      required: true,
    },
  }
}
</script>

<style scoped>
.comment-list {
  display: flex;
  flex-direction: column;
  margin-bottom: 24px;
}
</style>