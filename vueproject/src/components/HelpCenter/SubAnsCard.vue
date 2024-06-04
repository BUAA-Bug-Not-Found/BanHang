<script>
import {onBeforeUnmount, ref, shallowRef} from "vue";
import {delAnswerAPI, formatDate, getAnsById, replyComment, setAnsLikeAPI} from "@/components/HelpCenter/api";
import UserStateStore, {userStateStore} from "@/store";
import {ElMessage} from "element-plus";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";
import {Editor, Toolbar} from "@wangeditor/editor-for-vue";
import router from "@/router";

export default {
  name: "SubAnsCard",
  methods: {formatDate},
  components: {Editor, Toolbar, UserAvatar},
  props: ["ansId", "index"],
  emits: ["delComment", "editComment", "replyComment"],
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
            if(res.isSuccess === true) {
              ElMessage.success("删除成功")
              context.emit("delAns", {index: props.index})
              delDialog.value = false
            } else {
              ElMessage.error("删除失败，请稍后再试")
            }
          }
      )
    }

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
      if (!userStateStore().isAuthentic) {
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

    const openEditor = ref(false)

    return {
      ans,
      ansIdRef,
      setAnsLike,
      userLike,
      likeSum,
      delDialog,
      isUser,
      delAnswer,
      openEditor,
      uploadComment,
      editorRef,
      toolbarConfig,
      replyAnsConfig,
      commentHtml,
      mode: 'default',
      handleCreated
    };
  },
};
</script>

<template>
  <div v-if="ans !== null">
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
<!--        <v-col cols="1" style="display: flex;justify-content: end;">-->
<!--          <UserAvatar :userId="ans.userId"/>-->
<!--        </v-col>-->
<!--        <v-col cols="11">-->
<!--          <div style="display: flex; justify-content: space-between;margin-top: 10px">-->
<!--            <span style="font-size: 15px">{{ ans.userName }}-->
<!--              <span v-if="ans.replyAnsId != -1">-->
<!--                <v-icon>mdi-menu-right</v-icon> {{ans.replyAnsUserName}}-->
<!--              </span>-->
<!--            </span>-->
<!--            <span style="font-size: 12px;color: gray">回答于{{ formatDate(ans.ansTime) }}</span>-->
<!--          </div>-->
<!--          <div style="margin-top: 3px" v-dompurify-html="ans.ansContent"/>-->
<!--          <div style="margin-bottom: 5px">-->
<!--            <v-btn-->
<!--                :prepend-icon=" !userLike ?-->
<!--              'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text" size="small"-->
<!--                color="blue-grey-lighten-2"-->
<!--                @click="setAnsLike"-->
<!--            >-->
<!--              {{ likeSum }}-->
<!--            </v-btn>-->
<!--            <v-btn-->
<!--                :prepend-icon="'mdi-message-reply-text'" variant="text" size="small"-->
<!--                @click="openEditor = !openEditor"-->
<!--                color="blue-grey-lighten-2">-->
<!--            </v-btn>-->
<!--            <v-btn v-if="isUser"-->
<!--                   :icon="'mdi-delete-circle'" variant="text" size="small"-->
<!--                   color="blue-grey-lighten-2"-->
<!--                   @click="delDialog = !delDialog">-->
<!--            </v-btn>-->
<!--            &lt;!&ndash;            <v-btn v-if="isUser"&ndash;&gt;-->
<!--            &lt;!&ndash;                   :icon="'mdi-file-edit'" variant="text" size="small"&ndash;&gt;-->
<!--            &lt;!&ndash;                   color="blue-grey-lighten-2">&ndash;&gt;-->
<!--            &lt;!&ndash;            </v-btn>&ndash;&gt;-->
<!--          </div>-->
<!--        </v-col>-->


      </v-row>
      <div style="display: flex;width: 100%;margin-top: 20px">
        <div style="flex: 1; display: flex; justify-content: flex-end;margin-right: 10px">
          <UserAvatar :userId="ans.userId"/>
        </div>
        <div style="flex: 10;">
          <div style="display: flex; justify-content: space-between;margin-top: 10px">
            <span style="font-size: 15px">{{ ans.userName }}
              <span v-if="ans.replyAnsId != -1">
                <v-icon>mdi-menu-right</v-icon> {{ans.replyAnsUserName}}
              </span>
            </span>
            <span style="font-size: 12px;color: gray">回答于{{ formatDate(ans.ansTime) }}</span>
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
                @click="openEditor = !openEditor"
                color="blue-grey-lighten-2">
            </v-btn>
            <v-btn v-if="isUser"
                   :icon="'mdi-delete-circle'" variant="text" size="small"
                   color="blue-grey-lighten-2"
                   @click="delDialog = !delDialog">
            </v-btn>
          </div>
        </div>
      </div>
      <v-row v-if="openEditor">
        <div style="width: 90%;transform: translateX(3%);border: 1px solid #ccc;margin: 10px">
          <Toolbar
              style="border-bottom: 1px solid #ccc"
              :editor="editorRef"
              :defaultConfig="toolbarConfig"
              :mode="mode"
          />
          <Editor
              style="height: 80px; overflow-y: hidden;"
              v-model="commentHtml"
              :defaultConfig="replyAnsConfig"
              :mode="mode"
              @onCreated="handleCreated"
          />
        </div>
        <div style="display: flex;justify-content: end;width: 95%">
          <v-btn size="small" style="margin-top: 10px;margin-bottom: 10px" prepend-icon="mdi-message-reply-text" color="primary" @click="uploadComment">
            回复
          </v-btn>
        </div>
        <div style="height: 80px"></div>
      </v-row>
    </v-card>
  </div>
  <v-dialog
      v-model="delDialog"
      width="auto"
  >
    <v-card
        max-width="400"
        min-width="200"
        prepend-icon="mdi-delete-clock"
        text="你的评论将会被删除，确认嘛？"
        title="删除评论"
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
</template>

<style scoped>

</style>