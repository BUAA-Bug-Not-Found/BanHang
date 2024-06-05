<script>
import {onBeforeUnmount, ref, shallowRef} from "vue";
import {
  delAnswerAPI,
  formatDate,
  getAnsById,
  replyComment,
  reportAnswerAPI,
  setAnsLikeAPI
} from "@/components/HelpCenter/api";
import UserStateStore, {userStateStore} from "@/store";
import {ElMessage} from "element-plus";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";
import router from "@/router";
import {Editor, Toolbar} from "@wangeditor/editor-for-vue";

export default {
  name: "SubAppAnsCard",
  methods: {userStateStore, formatDate},
  components: {Editor, Toolbar, UserAvatar},
  props: ["quesId", "ansId", "index"],
  emits: ["delAns"],
  setup(props, context) {

    const init = () => {
      getAnsById(props.ansId).then(
          (res) => {
            ans.value = res.answer
            userLike.value = res.answer.ifUserLike
            likeSum.value = res.answer.likeSum
            isUser.value = UserStateStore().getUserId === ans.value.userId
          }
      )
    }

    init()

    const ansIdRef = ref(props.ansId)

    const ans = ref(null)

    const userLike = ref(false)
    const likeSum = ref(0)

    const setAnsLike = () => {
      const state = UserStateStore()
      if (!state.email) {
        ElMessage.error("请先登录")
      } else {
        setAnsLikeAPI(props.ansId, userLike.value ? 0 : 1).then(
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

    const delDialog = ref(false)

    const isUser = ref(false)

    const delAnswer = () => {
      delAnswerAPI(props.ansId).then(
          (res) => {
            if (res.isSuccess === true) {
              ElMessage.success("删除成功")
              context.emit("delAns", {index: props.index})
              delDialog.value = false
            } else {
              ElMessage.error("删除失败，请稍后再试")
            }
          }
      )
    }

    const sheet = ref(false)

    const replyAnsConfig = {
      placeholder: '回复'
    }

    const editorRef = shallowRef()

    const toolbarConfig = {
      excludeKeys: ['undo', 'redo', 'fontSize', 'fontFamily',
        'lineHeight', 'group-justify', 'group-video',
        'group-indent', 'bgColor', 'bulletedList', 'italic', 'group-image',
        'fullScreen'
      ],
    }

    const handleCreated = (editor) => {
      editorRef.value = editor // 记录 editor 实例，重要！
    }

    onBeforeUnmount(() => {
      const editor = editorRef.value
      if (editor == null) return
      editor.destroy()
    })

    const imageList = ref([])

    const uploadComment = () => {
      if (!userStateStore().email) {
        ElMessage.error("请先登录")
        router.push('/loginPage')
      } else {
        if (String(commentHtml.value).replace(/<[^>]*>/g, "") === '') {
          ElMessage.error("不能上传空白答案")
        } else {
          replyComment(props.ansId, commentHtml.value, imageList.value).then(
              (res) => {
                if (res.isSuccess === true) {
                  ElMessage.success("回答已上传")
                  commentHtml.value = ''
                  imageList.value = []
                  router.go(0)
                } else {
                  ElMessage.error("回答失败，请稍后再试")
                }
              }
          )
        }
      }
    }

    const commentHtml = ref('')

    const reportDialOpen = ref(false)

    const reportReason = ref('')

    const reportAnswer = () => {
      reportAnswerAPI(props.quesId, props.ansId, reportReason.value).then(
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

    const truncate = (content) => {
      const strippedContent = String(content).replace(/<[^>]*>/g, "")
      if (strippedContent.length > 20) {
        return `${strippedContent.slice(0, 20)}...`;
      }
      return strippedContent;
    };

    return {
      ans,
      ansIdRef,
      setAnsLike,
      userLike,
      likeSum,
      delDialog,
      isUser,
      delAnswer,
      sheet,
      commentHtml,
      handleCreated,
      uploadComment,
      toolbarConfig,
      editorRef,
      replyAnsConfig,
      mode: 'default',
      reportDialOpen,
      reportAnswer,
      userName,
      getUserName,
      reportReason,
      truncate
    };
  },
};
</script>

<template>
  <div v-if="ans !== null" style="width: 100%">
    <v-divider
        color="light-blue-darken-3"
        style="margin-top: 5px;margin-bottom: 5px"
    ></v-divider>
    <v-card
        class="mx-auto"
        width="w-100"
        elevation="0"
    >
      <v-row>
        <v-col cols="1" style="margin-right: 10px">
          <UserAvatar :userId="ans.userId" @returnUserName="getUserName"/>
        </v-col>
        <v-col cols="10">
          <div style="margin-top: 10px">
            <div style="font-size: 15px">
              <span style="font-size: 15px">{{ ans.userName }}
              <span v-if="ans.replyAnsId != -1">
                <v-icon>mdi-menu-right</v-icon> {{ ans.replyAnsUserName }}
              </span>
            </span>
            </div>
            <div style="font-size: 12px;color: gray">回答于{{ formatDate(ans.ansTime) }}</div>
          </div>
          <div style="margin-top: 3px" v-dompurify-html="ans.ansContent"/>
          <div style="margin-bottom: 5px">
            <v-btn
                :prepend-icon=" !userLike ?
              'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text" size="small"
                color="blue-grey-lighten-2"
                @click="setAnsLike"
            >
              {{ likeSum }}
            </v-btn>
            <v-btn
                :prepend-icon="'mdi-message-reply-text'" variant="text" size="small"
                @click="sheet = !sheet"
                color="blue-grey-lighten-2">
            </v-btn>
            <v-btn v-if="isUser"
                   :icon="'mdi-delete-circle'" variant="text" size="small"
                   color="blue-grey-lighten-2"
                   @click="delDialog = !delDialog">
            </v-btn>
            <v-btn v-if="userStateStore().email"
                   :prepend-icon="'mdi-shield-alert'" variant="text" size="small"
                   color="red-darken-2"
                   @click="reportDialOpen = !reportDialOpen">
              举报
            </v-btn>
            <!--            <v-btn v-if="isUser"-->
            <!--                :icon="'mdi-file-edit'" variant="text" size="small"-->
            <!--                color="blue-grey-lighten-2">-->
            <!--            </v-btn>-->
          </div>
        </v-col>
      </v-row>
    </v-card>
  </div>
  <v-bottom-sheet v-model="sheet">
    <v-card
        class="text-center"
        height="500"
    >
      <v-card-text>
        <v-row align="center" style="margin-bottom: 5px">
          <v-col cols="4" offset="4">
            发布评论
          </v-col>
          <v-col cols="4">
            <v-btn prepend-icon="mdi-message-reply-text"
                   color="primary" @click="uploadComment">
              回复
            </v-btn>
          </v-col>
        </v-row>
        <div style="border: 1px solid #ccc;overflow-y: scroll;margin: 0">
          <Toolbar
              style="border-bottom: 1px solid #ccc"
              :editor="editorRef"
              :defaultConfig="toolbarConfig"
              :mode="mode"
          />
          <Editor
              style="height: 250px; overflow-y: hidden;"
              v-model="commentHtml"
              :defaultConfig="replyAnsConfig"
              :mode="mode"
              @onCreated="handleCreated"
          />
        </div>
      </v-card-text>
    </v-card>
  </v-bottom-sheet>
  <v-dialog
      v-model="delDialog"
      width="auto"
  >
    <v-card
        max-width="400"
        min-width="200"
        prepend-icon="mdi-delete-clock"
        text="你的回答将会被删除，确认嘛？"
        title="删除回答"
    >
      <template v-slot:actions>
        <v-btn
            variant="flat"
            density="compact"
            text="确认"
            color="red-darken-1"
            @click="delAnswer"
        ></v-btn>

        <v-btn
            text="取消"
            density="compact"
            @click="delDialog = false"
        ></v-btn>
      </template>
    </v-card>
  </v-dialog>
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
          <div class="mb-2">您正在检举用户{{userName}}的回答</div>
          <div class="mb-2" style="color: grey">{{ truncate(ans.ansContent) }}</div>
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
              @click="reportAnswer"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<style scoped>

</style>