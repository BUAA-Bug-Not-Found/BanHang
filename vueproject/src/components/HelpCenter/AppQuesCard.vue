<script>
import {ref, onMounted, onBeforeUnmount} from "vue";
import router from "@/router";
import {delQuestionAPI, formatDate, reportQuesAPI, setLikeQuesApi} from "@/components/HelpCenter/api";
import UserStateStore, {userStateStore} from "@/store";
import {ElMessage} from "element-plus";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";

export default {
  name: "AppQuesCard",
  methods: {userStateStore, formatDate},
  components: {UserAvatar},
  props: ["question", "disTags"],
  emits: ["editQues", 'delQues'],
  setup(props, context) {
    const truncate = (content) => {
      const strippedContent = String(content).replace(/<[^>]*>/g, "");
      if (strippedContent.length > 12) {
        return `${strippedContent.slice(0, 12)}...`;
      }
      return strippedContent;
    };

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

    const editQues = () => {
      router.push("/QuesInfo/" + props.question.quesId + "/1");
    }

    const isUser = ref(UserStateStore().getUserId === props.question.userId);

    const reportDialOpen = ref(false)

    const reportReason = ref('')

    const reportQues = () => {
      reportQuesAPI(props.question.quesId, reportReason.value).then(
          (res) => {
            if(res.isSuccess) {
              ElMessage.success("举报成功，请等待管理员审核举报结果")
              reportDialOpen.value = false
            } else {
              ElMessage.error("举报失败，请稍后再试")
            }
          }
      )
    }

    const userName = ref('')

    const getUserName = (nickName) => {
      userName.value = nickName
    }

    const state = userStateStore()

    return {
      truncate,
      menuClick,
      goto,
      userLike,
      likeSum,
      setLikeQues,
      delQues,
      delDialog,
      isUser,
      editQues,
      reportDialOpen,
      reportReason,
      getUserName,
      reportQues,
      userName,
      state
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
        <v-col offset="1" cols="2" style="min-width: 50px">
          <UserAvatar :userId="question.userId" @returnUserName="getUserName"></UserAvatar>
        </v-col>
        <v-col cols="5" style="text-align: left;" :class="`cursor-pointer`" @click="goto()">
          <div style="margin-top: 10px;">
            {{ truncate(question.quesContent.content) }}
          </div>
          <div style="font-size: 12px;color: grey">
            {{ question.userName }} {{ formatDate(question.quesTime) }}
          </div>
        </v-col>
        <v-col cols="4" style="text-align: right;margin-top: 3px">
          <v-btn :prepend-icon=" !userLike ?
                  'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text" size="x-small"
                 color="blue-grey-lighten-2" @click="setLikeQues">
            {{ likeSum }}
          </v-btn>
          <v-btn variant="text" prepend-icon="mdi-message-reply-text" size="x-small" color="blue-grey-lighten-2">
            {{ question.ansSum }}
          </v-btn>
          <v-menu v-if="userStateStore().email && (isHovering || menuClick)" :location="'bottom'">
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
              <v-list-item density="compact" v-if="isUser || userStateStore().isManager" @click="delDialog = !delDialog">
                <v-icon size="22" color="red-darken-1">mdi-delete-clock</v-icon> 删除
              </v-list-item>
              <v-list-item density="compact" v-if="isUser" color="primary" @click="editQues">
                <v-icon size="22" color="blue-darken-1">mdi-book-edit</v-icon> 修改
              </v-list-item>
              <v-list-item density="compact" color="primary" @click="reportDialOpen = true">
                <v-icon size="22" color="red-darken-1">mdi-shield-alert</v-icon> 举报
              </v-list-item>
            </v-list>
          </v-menu>
        </v-col>
      </v-row>
      <div style="margin-left: 30px;margin-bottom: 10px">
        <span style="margin-bottom: 10px">
            <v-chip v-for="tag in disTags" size="x-small" :key="question.quesId + '-' + tag.tagId"
                    :color="tag.tagColor">
              <v-icon>{{ tag.tagIcon }}</v-icon>
              {{ tag.tagName }}
            </v-chip>
          <v-chip v-if="disTags.length === 0" size="x-small" color="blue-grey-darken-1">
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;其他&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          </v-chip>
          </span>
      </div>
    </v-card>
  </v-hover>

  <v-dialog v-model="reportDialOpen" max-width="500">
    <template v-slot:default="{ isActive }">
      <v-card rounded="lg">
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="ps-2" style="color: darkred;align-content: center;font-size: 25px">
            <v-icon :size="35" style="margin-right: 5px">mdi-shield-alert</v-icon>举报
          </div>
          <v-btn
              icon="mdi-close"
              variant="text"
              @click="isActive.value = false"
          ></v-btn>
        </v-card-title>

        <v-divider class="mb-4"></v-divider>

        <v-card-text>
          <div class="mb-2">您正在检举用户{{userName}}的问题</div>
          <div class="mb-2" style="color: grey">{{ truncate(question.quesContent.content) }}</div>
          <div class="mb-2">举报原因 (optional)</div>

          <v-textarea
              :counter="300"
              class="mb-2"
              rows="2"
              variant="outlined"
              persistent-counter
              v-model="reportReason"
          ></v-textarea>
        </v-card-text>
        <v-divider class="mt-2"></v-divider>
        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn
              class="text-none"
              rounded="xl"
              text="Cancel"
              @click="isActive.value = false"
          ></v-btn>

          <v-btn
              class="text-none"
              color="primary"
              rounded="xl"
              text="Send"
              variant="flat"
              @click="reportQues"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>

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