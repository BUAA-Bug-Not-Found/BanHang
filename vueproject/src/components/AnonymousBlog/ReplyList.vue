<template>
  <div class="comment-list">
    <ReplyShow
        v-for="(comment, index) in comments.slice().reverse()"
        :key="index"
        :blog-id="comment.blogId"
        :comment-id="comment.commentId"
        :user-id="comment.userId"
        :user-name="comment.userName"
        :user-avatar-url="comment.userAvatarUrl"
        :content="comment.content"
        :time="comment.time"
        :reply-to-comment-id="comment.replyToCommentId"
        :reply-to-comment-name="getReplyToCommentName(comment.replyToCommentId)"
        :top-comment-id="this.topCommentId"
        @reply-list-show-new-comment="replyListHandleNewComment"
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
    topCommentId: {
      type: Number,
      required: true
    }
  },
  methods: {
    getReplyToCommentName(replyToCommentId) {
      const replyToComment = this.comments.find(comment => comment.commentId === replyToCommentId);
      return replyToComment ? replyToComment.userName : '';
    },

    replyListHandleNewComment(comment) {
      this.$emit('comment-show-new-comment', comment);
    }
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