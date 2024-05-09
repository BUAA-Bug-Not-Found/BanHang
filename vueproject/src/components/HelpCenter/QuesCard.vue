<script>
import {ref, onMounted, onBeforeUnmount} from "vue";
import router from "@/router";
import {delQuestionAPI, formatDate, setLikeQuesApi} from "@/components/HelpCenter/api";
import UserStateStore from "@/store"
import {ElMessage} from "element-plus";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";

export default {
  name: "QuesCard",
  methods: {formatDate},
  components: {UserAvatar},
  props: ["question", "tags", "index", "disTags"],
  emits: ["editQues", 'delQues'],
  setup(props, context) {
    const truncate = (content) => {
      const strippedContent = String(content).replace(/<[^>]*>/g, "")
      if (strippedContent.length > 20) {
        return `${strippedContent.slice(0, 20)}...`;
      }
      return strippedContent;
    };


    const userLike = ref(props.question.ifUserLike)
    const likeSum = ref(props.question.likeSum)

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
      router.push("/QuesInfo/" + props.question.quesId + "/0");
    }

    const setLikeQues = () => {
      const state = UserStateStore()
      if(!state.email) {
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
              } else {
                ElMessage.error("点赞失败，请稍后再试")
              }
            }
        )
      }
    }

    const editQues = () => {
      router.push("/QuesInfo/" + props.question.quesId + "/1");
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
      goto,
      setLikeQues,
      userLike,
      likeSum,
      delQues,
      editQues,
      delDialog,
      isUser,
    };
  },
};
</script>

<template>
  <v-hover v-slot="{ isHovering, props }">
    <v-card
        class="mx-auto"
        style="width: 90%"
        :color="isHovering ? 'cyan-lighten-5' : undefined"
        v-bind="props"
    >
      <v-row>
        <v-col cols="2">
          <div style="display:flex; justify-content: end;align-content: center">
            <UserAvatar :userId="question.userId"></UserAvatar>
          </div>
        </v-col>
        <v-col cols="7" style="text-align: left;" :class="`cursor-pointer`" @click="goto()">
          <div style="margin-top: 10px;">
            {{ truncate(question.quesContent.content) }}
          </div>
          <div style="font-size: 12px;color: grey;margin-bottom: 5px">
            {{ question.userName }}发表于{{ formatDate(question.quesTime) }}
          </div>
        </v-col>
        <v-col cols="3" style="text-align: left;margin-top: 3px">
          <div>
            <v-btn :prepend-icon=" !userLike ?
                  'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text" size="small"
                   color="blue-grey-lighten-2" @click="setLikeQues">
              {{ likeSum }}
            </v-btn>
            <v-btn variant="text" prepend-icon="mdi-message-reply-text" size="small" color="blue-grey-lighten-2">
              {{ question.ansSum }}
            </v-btn>
            <v-menu v-show="isHovering || menuClick" :location="'bottom'">
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
                  <v-icon size="22" color="red-darken-1">mdi-delete-clock</v-icon> 删除
                </v-list-item>
                <v-list-item density="compact" v-if="isUser" color="primary" @click="editQues">
                  <v-icon size="22" color="blue-darken-1">mdi-book-edit</v-icon> 修改
                </v-list-item>
<!--                <v-list-item density="compact">-->
<!--                  举报-->
<!--                </v-list-item>-->
              </v-list>
            </v-menu>
          </div>
          <div style="margin-bottom: 10px">
            <v-chip v-for="tag in disTags" size="x-small" :key="question.quesId + '-' + tag.tagId"
                    :color="tag.tagColor">
              <v-icon>{{ tag.tagIcon }}</v-icon>
              {{ tag.tagName }}
            </v-chip>
          </div>
        </v-col>
      </v-row>
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
            density="compact"
            @click="delDialog = false"
        ></v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>

<style scoped>

</style>