<script>
import { ref, onMounted, onBeforeUnmount } from "vue";
import router from "@/router";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";

export default {
  name: "RecQuesCard",
  components: {UserAvatar},
  props: ["question", "tags"],
  emits: ["refresh"],
  setup(props, context) {
    const truncate = (content) => {
      const strippedContent = content.replace(/<[^>]*>/g, "");
      if (strippedContent.length > 10) {
        return `${strippedContent.slice(0, 10)}...`;
      }
      return strippedContent;
    };

    const disTags = ref([])

    const init = () => {
      for(let i = 0;i < props.question.tagIdList.length;i++) {
        for(let j = 0; j < props.tags.length;j++) {
          if (props.tags[j].tagId === props.question.tagIdList[i]) {
            disTags.value.push(props.tags[j])
          }
        }
      }
    }

    init()

    const menuClick = ref(false);

    function handleClickOutside(event) {
      if (!event.composedPath().includes(this.$el)) {
        menuClick.value = false;
      }
    }

    onMounted(() => {
      document.addEventListener("click", handleClickOutside);
    });

    onBeforeUnmount(() => {
      document.removeEventListener("click", handleClickOutside);
    });

    const goto = () => {
      router.push("/QuesInfo/" + props.question.quesId).then(
          context.emit("refresh", props.question.quesId)
      )
    }

    return { truncate, menuClick, disTags, goto};
  },
};
</script>

<template>
  <v-hover v-slot="{ isHovering, props }">
    <v-card
        class="mx-auto"
        width="w-75"
        :class="`cursor-pointer`"
        :color="isHovering ? 'cyan-lighten-5' : undefined"
        v-bind="props"
        @click="goto()"
    >
      <v-row>
        <v-col cols="4" style="display: flex;justify-content: end;margin-top: 8px;">
          <UserAvatar :userId="question.userId" style="padding-left: 8px;"></UserAvatar>
        </v-col>
        <v-col cols="8" style="text-align: left;" @click="goto">
          <div style="margin-top: 10px;font-size: 13px">
            {{ truncate(question.quesContent.content) }}
          </div>
          <div>
            <v-btn :prepend-icon="question.ifUserLike === 1 ?
                  'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text" size="small"
                   color="blue-grey-lighten-2">
              {{ question.likeSum }}
            </v-btn>
            <v-btn variant="text" prepend-icon="mdi-message-reply-text" size="small" color="blue-grey-lighten-2">
              {{ question.ansSum }}
            </v-btn>
          </div>
        </v-col>
      </v-row>
      <div style="margin-bottom: 10px;transform: translateX(5%)">
        <v-chip v-for="tag in disTags" size="x-small" :key="question.quesId + '-' + tag.tagId" :color="tag.tagColor">
          <v-icon>{{tag.tagIcon}}</v-icon>
          {{tag.tagName}}
        </v-chip>
      </div>
    </v-card>
  </v-hover>
</template>

<style scoped>

</style>