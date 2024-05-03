<script>
import {ref, onMounted, onBeforeUnmount} from "vue";
import router from "@/router";
import {delQuestionAPI, setLikeQuesApi} from "@/components/HelpCenter/api";
import UserStateStore from "@/store";
import {ElMessage} from "element-plus";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";

export default {
  name: "AppQuesCard",
  components: {UserAvatar},
  props: ["question", "tags"],
  emits: ["editQues", 'delQues'],
  setup(props, context) {
    const truncate = (content) => {
      const strippedContent = String(content).replace(/<[^>]*>/g, "");
      if (strippedContent.length > 15) {
        return `${strippedContent.slice(0, 15)}...`;
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

    const userLike = ref(props.question.ifUserLike)

    const likeSum = ref(props.question.likeSum)

    const setLikeQues = () => {
      const state = UserStateStore()
      if (!state.email) {
        ElMessage.error("请先登录")
      } else {
        setLikeQuesApi(props.question.quesId, userLike.value ? 0 : 1).then(
            (res) => {
              if (res.isSuccess === true) {
                if (userLike.value) {
                  likeSum.value--
                } else {
                  likeSum.value++
                }
                userLike.value = !userLike.value;
              }
            }
        )
      }
    }

    const delQues = () => {
      delQuestionAPI(props.question.quesId).then(
          (res) => {
            if(res.isSuccess === true) {
              ElMessage.success('问题已删除')
              context.emit("delQues", {index: props.index})
              delDialog.value = false
            } else {
              ElMessage.error('删除失败，请稍后再试')
            }
          }
      )
    }

    const delDialog = ref(false)

    const isUser = ref(UserStateStore().getUserId === props.question.userId);

    return {
      truncate,
      menuClick,
      disTags,
      goto,
      userLike,
      likeSum,
      setLikeQues,
      delQues,
      delDialog,
      isUser
    };
  },
};
</script>

<template>
  <v-hover v-slot="{ isHovering, props }">
    <v-card
        class="mx-auto"
        width="w-75"
        style="text-align: left"
        :color="isHovering ? 'cyan-lighten-5' : undefined"
        v-bind="props"
    >
      <v-row>
        <v-col cols="1" style="min-width: 50px">
          <UserAvatar :userId="question.userId"></UserAvatar>
        </v-col>
        <v-col cols="5" style="text-align: left;" :class="`cursor-pointer`" @click="goto()">
          <div style="margin-top: 10px;">
            {{ truncate(question.quesContent.content) }}
          </div>
          <div style="font-size: 12px;color: grey">
            {{ question.userName }} {{ question.quesTime }}
          </div>
        </v-col>
        <v-col cols="4" style="text-align: right;margin-top: 3px">
          <v-btn :prepend-icon=" !userLike ?
                  'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text" size="x-small"
                 color="blue-grey-lighten-2" @click="setLikeQues">
            {{ likeSum }}
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
              <v-list-item density="compact" v-if="isUser" @click="delDialog = !delDialog">
                删除
              </v-list-item>
              <v-list-item density="compact" v-if="isUser">
                修改
              </v-list-item>
              <v-list-item density="compact">
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

  <v-dialog
      v-model="delDialog"
      width="auto"
  >
    <v-card
        max-width="400"
        min-width="200"
        prepend-icon="mdi-delete-clock"
        text="你的问题将会被删除，确认嘛？"
        title="删除问题"
    >
      <template v-slot:actions>
        <v-btn
            variant="flat"
            density="compact"
            text="确认"
            color="red-darken-1"
            @click="delQues"
        ></v-btn>

        <v-btn
            text="取消"
            @click="delDialog = false"
        ></v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>

<style scoped>

</style>