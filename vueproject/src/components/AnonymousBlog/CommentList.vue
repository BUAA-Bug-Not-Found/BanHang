<template>
  <div class="comment-list">
    <CommentShow
        v-for="(comment, index) in comments"
        :key="index"
        :blog-id="comment.blogId"
        :comment-id="comment.commentId"
        :user-name="comment.userName"
        :user-avatar-url="comment.userAvatarUrl"
        :content="comment.content"
        :time="comment.time"
        :reply-to-comment-id="comment.replyToCommentId"
        :replies="getReplies(comment.commentId)"
    />
  </div>
</template>

<script>
import CommentShow from "@/components/AnonymousBlog/CommentShow.vue";

export default {
  name: "CommentList",
  components: {CommentShow},
  props: {
    comments: {
      type: Array,
      required: true,
    },
  },
  methods: {
    getReplies(commentId) {
      // 根据 commentId 计算该评论的回复列表
      return this.comments.filter(comment => comment.replyToCommentId == commentId);
    }
  }
}
</script>

<style scoped>
.comment-list {
  display: flex;
  flex-direction: column;
  margin-bottom: 200px;
}
</style>
