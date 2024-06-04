<script>
import {onBeforeUnmount, ref, shallowRef} from "vue";
import {delAnswerAPI, formatDate, getAnsById, replyComment, setAnsLikeAPI} from "@/components/HelpCenter/api";
import UserStateStore, {userStateStore} from "@/store";
import {ElMessage} from "element-plus";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";
import SubAnsCard from "@/components/HelpCenter/SubAnsCard.vue";
import router from "@/router";
import {Editor, Toolbar} from "@wangeditor/editor-for-vue";

export default {
  name: "AnsCard",
  methods: {formatDate},
  components: {Toolbar, Editor, SubAnsCard, UserAvatar},
  props: ["ansId", "index"],
  emits: ["delAns", "editAns"],
  setup(props, context) {

    const init = () => {
      getAnsById(props.ansId).then(
          (res) => {
            ans.value = res.answer
            userLike.value = res.answer.ifUserLike
            likeSum.value = res.answer.likeSum
            isUser.value = UserStateStore().getUserId === ans.value.userId
            if ('subAnsIdList' in res && Array.isArray(res.subAnsIdList)) {
              subAnsIdList.value = res.subAnsIdList
            } else {
              subAnsIdList.value = []
            }
          }
      )
    }

    init()

    const subAnsIdList = ref()

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

    const openSubAns = ref(false)

    const delComment = (params) => {
      subAnsIdList.value.splice(params.index, 1)
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

    return {
      ans,
      ansIdRef,
      setAnsLike,
      userLike,
      likeSum,
      delDialog,
      isUser,
      delAnswer,
      subAnsIdList,
      openSubAns,
      delComment,
      handleCreated,
      replyAnsConfig,
      editorRef,
      mode: 'default',
      toolbarConfig,
      uploadComment,
      commentHtml
    };
  },
};
</script>

<template>
  <div v-if="ans !== null">
    <v-card
        class="mx-auto"
        width="w-75"
        elevation="0"
    >
      <v-row>
        <v-col cols="1" style="display: flex;margin-left: 10px;justify-content: end;">
          <UserAvatar :userId="ans.userId"/>
        </v-col>
        <v-col cols="10">
          <div style="display: flex; justify-content: space-between;margin-top: 10px">
            <span style="font-size: 15px">{{ ans.userName }}</span>
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
                @click="openSubAns = !openSubAns"
                color="blue-grey-lighten-2">
              <span v-if="openSubAns">收起评论</span>
              <span v-else-if="subAnsIdList.length !== 0">{{ subAnsIdList.length }}条评论</span>
              <span v-else>快来评论吧~</span>
            </v-btn>
            <v-btn v-if="isUser"
                   :icon="'mdi-delete-circle'" variant="text" size="small"
                   color="blue-grey-lighten-2"
                   @click="delDialog = !delDialog">
            </v-btn>
            <!--            <v-btn v-if="isUser"-->
            <!--                   :icon="'mdi-file-edit'" variant="text" size="small"-->
            <!--                   color="blue-grey-lighten-2">-->
            <!--            </v-btn>-->
          </div>
          <div v-if="openSubAns">
            <div style="width: 100%;;border: 1px solid #ccc;margin: 10px">
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
            <v-row justify="end">
              <v-btn style="margin-top: 10px;margin-bottom: 10px" prepend-icon="mdi-message-reply-text" color="primary" @click="uploadComment">
                发送回复
              </v-btn>
            </v-row>
            <SubAnsCard v-for="(ansId, index) in subAnsIdList"
                        :index="index" :ansId="ansId"
                        :key="ansId + '-ans'"
                        @delComment="delComment"
            ></SubAnsCard>
          </div>
        </v-col>
      </v-row>
    </v-card>
    <v-divider
        color="light-blue-darken-3"
        style="margin-top: 5px;margin-bottom: 5px"
    ></v-divider>
  </div>
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
</template>

<style scoped>

</style>