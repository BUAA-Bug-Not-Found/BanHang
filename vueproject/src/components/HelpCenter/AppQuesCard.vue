<script>
import {ref, onMounted, onBeforeUnmount} from "vue";
import router from "@/router";

export default {
  name: "AppQuesCard",
  props: ["question", "tags"],
  setup(props) {
    const truncate = (content) => {
      const strippedContent = content.replace(/<[^>]*>/g, "");
      if (strippedContent.length > 20) {
        return `${strippedContent.slice(0, 20)}...`;
      }
      return strippedContent;
    };

    const disTags = ref([])

    const init = () => {
      for (let i = 0; i < props.question.tagIdList.length; i++) {
        for (let j = 0; j < props.tags.length; j++) {
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
      router.push("/QuesInfo/" + props.question.quesId);
    }

    return {truncate, menuClick, disTags, goto};
  },
};
</script>

<template>
  <v-hover v-slot="{ isHovering, props }">
    <v-card
        class="mx-auto"
        width="w-75"
        style="text-align: left"
        :class="`cursor-pointer`"
        :color="isHovering ? 'cyan-lighten-5' : undefined"
        v-bind="props"
        @click="goto()"
    >
      <v-row>
        <v-col cols="1" style="margin-right: 8px">
          <v-avatar color="surface-variant" style="margin-top: 15px;margin-left: 10px" size="33"></v-avatar>
        </v-col>
        <v-col cols="6" style="text-align: left;">
          <div style="margin-top: 10px;">
            {{ truncate(question.quesContent) }}
          </div>
          <div style="font-size: 12px;color: grey">
            {{ question.userName }}发表于{{ question.quesTime }}
          </div>
        </v-col>
        <v-col cols="4" style="text-align: right;margin-top: 3px">
          <v-btn :prepend-icon="question.ifUserLike === 1 ?
                  'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text" size="x-small"
                 color="blue-grey-lighten-2">
            {{ question.likeSum }}
          </v-btn>
          <v-btn variant="text" prepend-icon="mdi-reply" size="x-small" color="blue-grey-lighten-2">
            {{ question.ansSum }}
          </v-btn>
          <v-menu v-if="isHovering || menuClick" :location="'bottom'">
            <template v-slot:activator="{ props }">
              <v-btn
                  size="28px"
                  v-bind="props"
                  variant="text"
                  @click="menuClick = !menuClick"
                  class="rounded-circle"
              >
                <template v-slot:prepend>
                  <v-icon size="15">mdi-dots-vertical</v-icon>
                </template>
              </v-btn>
            </template>
            <v-list>
              <v-list-item density="compact">
                删除
              </v-list-item>
              <v-list-item>
                修改
              </v-list-item>
              <v-list-item>
                举报
              </v-list-item>
            </v-list>
          </v-menu>
        </v-col>
      </v-row>
      <div style="margin-left: 10px;margin-bottom: 10px">
        <span style="margin-bottom: 10px">
            <v-chip v-for="tag in disTags" size="x-small" :key="question.quesId + '-' + tag.tagId"
                    :color="tag.tagColor">
              <v-icon>{{ tag.tagIcon }}</v-icon>
              {{ tag.tagName }}
            </v-chip>
          </span>
      </div>
    </v-card>
  </v-hover>
</template>

<style scoped>

</style>