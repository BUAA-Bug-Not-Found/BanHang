<template>
  <div class="comment-list">
    <CommentShow
        v-for="(comment, index) in comments.filter(comment => comment.replyToCommentId === null).slice().reverse()"
        :key="index"
        :blog-id="comment.blogId"
        :comment-id="comment.commentId"
        :user-id="comment.userId"
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
      // 存储找到的所有回复评论
      const replies = [];

      // 递归函数来查找回复
      const findReplies = (id) => {
        // 找到直接回复当前评论的所有评论
        const directReplies = this.comments.filter(comment => comment.replyToCommentId === id);
        directReplies.forEach(reply => {
          replies.push(reply);
          // 递归查找当前回复的回复
          findReplies(reply.commentId);
        });
      };

      // 开始查找指定评论的所有回复
      findReplies(commentId);

      return replies;
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
