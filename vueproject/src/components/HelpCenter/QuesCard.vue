<script>
import { ref, onMounted, onBeforeUnmount } from "vue";
import router from "@/router";

export default {
  name: "QuesCard",
  props: ["question", "tags"],
  setup(props) {
    const truncate = (content) => {
      console.log(content)
      const strippedContent = String(content).replace(/<[^>]*>/g, "")
      if (strippedContent.length > 20) {
        return `${strippedContent.slice(0, 20)}...`;
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
      router.push("/QuesInfo/" + props.question.quesId);
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
        <v-col cols="1">
          <v-avatar color="surface-variant" style="margin: 10px" size="40"></v-avatar>
        </v-col>
        <v-col cols="7" style="text-align: left;">
          <div style="margin-top: 10px;">
            {{ truncate(question.quesContent.content) }}
          </div>
          <div style="font-size: 12px;color: grey">
            {{ question.userName }}发表于{{ question.quesTime }}
          </div>
        </v-col>
        <v-col cols="3" style="text-align: left;margin-top: 3px">
          <div>
            <v-btn :prepend-icon="question.ifUserLike === 1 ?
                  'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text" size="small"
                   color="blue-grey-lighten-2">
              {{ question.likeSum }}
            </v-btn>
            <v-btn variant="text" prepend-icon="mdi-reply" size="small" color="blue-grey-lighten-2">
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
          </div>
          <div style="margin-bottom: 10px">
            <v-chip v-for="tag in disTags" size="x-small" :key="question.quesId + '-' + tag.tagId" :color="tag.tagColor">
              <v-icon>{{tag.tagIcon}}</v-icon>
              {{tag.tagName}}
            </v-chip>
          </div>
        </v-col>
      </v-row>
    </v-card>
  </v-hover>
</template>

<style scoped>

</style>