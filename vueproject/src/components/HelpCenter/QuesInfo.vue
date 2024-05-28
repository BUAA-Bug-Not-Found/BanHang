<script>
import {onBeforeUnmount, ref, shallowRef} from "vue";
import {useRouter} from "vue-router";
import AnsCard from "@/components/HelpCenter/AnsCard.vue";
import {Editor, Toolbar} from "@wangeditor/editor-for-vue";
import RecQuesCard from "@/components/HelpCenter/RecQuesCard.vue";
import {useDisplay} from "vuetify";
import AppAnsCard from "@/components/HelpCenter/AppAnsCard.vue";
import {
  delQuestionAPI,
  formatDate,
  getQuestionsApi,
  getQuestionsByTagIdApi,
  getTagsApi, replyComment,
  setLikeQuesApi, updateQuesApi,
  uploadAnsApi, uploadFileApi
} from "@/components/HelpCenter/api";
import {getQuesByIdApi} from "@/components/HelpCenter/api";
import {ElMessage} from "element-plus";
import router from "@/router";
import UserStateStore, {userStateStore} from "@/store";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";
import {api as viewerApi} from "v-viewer";
import {Plus} from "@element-plus/icons-vue";

export default {
  name: "QuesInfo",
  components: {Plus, UserAvatar, AppAnsCard, AnsCard, RecQuesCard, Editor, Toolbar},
  data() {
    return {
      top: false,
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
  },
  methods: {
    formatDate,
    userStateStore,
    handleScroll() {
      // 假设 right-panel 初始时离顶部有200px的距离
      let scrollDistance = window.pageYOffset || document.documentElement.scrollTop;
      let threshold = 450;

      this.top = !(scrollDistance < threshold || scrollDistance === 0);
    }
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  setup() {
    const display = useDisplay()

    const truncate = (content) => {
      const strippedContent = content.replace(/<[^>]*>/g, "");
      if (strippedContent.length > 20) {
        return `${strippedContent.slice(0, 20)}...`;
      }
      return strippedContent;
    };

    const tags = ref([])

    const recommendQues = ref([])

    const disTags = ref([])
    const qid = ref(0)

    const question = ref(null)

    async function fetchAdvise() {
      for (let i = 0; i < question.value.tagIdList.length; i++) {
        let response = await getQuestionsByTagIdApi(1, 10, question.value.tagIdList[i])
        recommendQues.value = recommendQues.value.concat(response.questions);
        if (recommendQues.value.length > 5) {
          break
        }
      }
      if (recommendQues.value.length < 5) {
        let response = await getQuestionsApi(1, 5)
        recommendQues.value = recommendQues.value.concat(response.questions);
      }
      if (recommendQues.value.length > 5) {
        recommendQues.value.slice(0, 5)
      }
      for (let i = 0; i < recommendQues.value.length; i++) {
        if (recommendQues.value[i].quesId == qid.value) {
          recommendQues.value.splice(i, 1)
          break;
        }
      }
    }

    const tagNamesArray = ref([])

    const refresh = (index) => {
      qid.value = index
      question.value.ansIdList = []
      avatarShow.value = false
      getQuesByIdApi(qid.value).then(
          (res) => {
            question.value = res.question
            userLike.value = res.question.ifUserLike
            likeSum.value = res.question.likeSum
            recommendQues.value = []
            avatarShow.value = true
            try {
              fetchAdvise()
            } catch (e) {
              console.log(e)
            }
            isUser.value = UserStateStore().getUserId === question.value.userId
            disTags.value = []
            for (let i = 0; i < question.value.tagIdList.length; i++) {
              for (let j = 0; j < tags.value.length; j++) {
                if (tags.value[j].tagId === question.value.tagIdList[i]) {
                  disTags.value.push(tags.value[j])
                }
              }
            }
          }
      )
    }

    const avatarShow = ref(false)

    const init = () => {
      let router = useRouter()
      qid.value = router.currentRoute.value.params.qid
      let opId = router.currentRoute.value.params.opId
      getQuesByIdApi(qid.value).then(
          (res) => {
            question.value = res.question
            userLike.value = res.question.ifUserLike
            likeSum.value = res.question.likeSum
            avatarShow.value = true
            recommendQues.value = []
            try {
              fetchAdvise()
            } catch (e) {
              console.log(e)
            }
            isUser.value = UserStateStore().getUserId === question.value.userId
            getTagsApi().then(
                (data) => {
                  tags.value = data.tags
                  for (let i = 0; i < question.value.tagIdList.length; i++) {
                    for (let j = 0; j < tags.value.length; j++) {
                      if (tags.value[j].tagId === question.value.tagIdList[i]) {
                        disTags.value.push(tags.value[j])
                      }
                    }
                  }
                  for (let i = 0; i < tags.value.length; i++) {
                    tagNamesArray.value.push(tags.value[i].tagName)
                  }
                  if (opId == 1) {
                    toEdit()
                  }
                }
            )
          }
      )
    }

    init()

    const goAnchor = (id) => {
      let anchor = document.getElementById(id);
      anchor.scrollIntoView();
    }

    const editorRef1 = shallowRef()

    const editorRef2 = shallowRef()

    const editorRef3 = shallowRef()

    const toolbarConfig1 = {
      excludeKeys: ['undo', 'redo', 'fontSize', 'fontFamily',
        'lineHeight', 'group-justify', 'group-video',
        'group-indent', 'bgColor', 'bulletedList', 'italic', 'group-image',
        'fullScreen'
      ],
    }

    const toolbarConfig2 = {
      excludeKeys: [
        'fullScreen'
      ],
    }

    const editorConfig = {
      placeholder: '请输入内容...'
    }

    const replyAnsConfig = {
      placeholder: '回复某人'
    }

    onBeforeUnmount(() => {
      const editor1 = editorRef1.value
      if (editor1 == null) return
      editor1.destroy()

      const editor2 = editorRef2.value
      if (editor2 == null) return
      editor2.destroy()

      const editor3 = editorRef3.value
      if (editor3 == null) return
      editor3.destroy()
    })

    const handleCreated1 = (editor) => {
      editorRef1.value = editor // 记录 editor 实例，重要！
    }

    const handleCreated2 = (editor) => {
      editorRef2.value = editor // 记录 editor 实例，重要！
    }

    const handleCreated3 = (editor) => {
      editorRef3.value = editor // 记录 editor 实例，重要！
    }

    const userLike = ref(false)

    const likeSum = ref(0)

    const replyHtml = ref("");

    const imageList = ref([])

    const uploadAnswer = () => {
      if (!userStateStore().isAuthentic) {
        ElMessage.error("请先登录")
        router.push('/loginPage')
      } else {
        if (String(replyHtml.value).replace(/<[^>]*>/g, "") === '') {
          ElMessage.error("不能上传空白答案")
        } else {
          uploadAnsApi(qid.value, replyHtml.value, imageList.value).then(
              (res) => {
                if (res.isSuccess === true) {
                  ElMessage.success("回答已上传")
                  replyHtml.value = ''
                  imageList.value = []
                  sheet2.value = false
                  router.go(0)
                } else {
                  ElMessage.error("回答失败，请稍后再试")
                }
              }
          )
        }
      }
    }

    const delPic = (index) => {
      editImgList.value.splice(index, 1)
    }

    const setLikeQues = () => {
      const state = UserStateStore()
      if (!state.email) {
        ElMessage.error("请先登录")
      } else {
        setLikeQuesApi(qid.value, userLike.value ? 0 : 1).then(
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
      delQuestionAPI(qid.value).then(
          (res) => {
            if (res.isSuccess === true) {
              ElMessage.success('问题已删除')
              router.push('/HelpCenter')
              delDialog.value = false
            } else {
              ElMessage.error('删除失败，请稍后再试')
            }
          }
      )
    }

    const delDialog = ref(false)

    const isUser = ref(false);

    const delAns = (index) => {
      question.value.ansIdList.splice(index, 1)
    }

    const editHtml = ref("")

    const editImgList = ref([])

    const editTagList = ref([])

    const sheet1 = ref(false)

    const sheet2 = ref(false)

    const toEdit = () => {
      sheet1.value = !sheet1.value
      editHtml.value = question.value.quesContent.content
      editImgList.value = []
      for (let i = 0; i < question.value.quesContent.imageList.length; i++) {
        editImgList.value.push(question.value.quesContent.imageList[i])
      }
      editTagList.value = []
      for (let i = 0; i < question.value.tagIdList.length; i++) {
        for (let j = 0; j < tags.value.length; j++) {
          if (question.value.tagIdList[i] === tags.value[j].tagId) {
            editTagList.value.push(tags.value[j].tagName)
            break
          }
        }
      }
    }

    const updateQues = () => {
      if (String(editHtml.value).replace(/<[^>]*>/g, "") === '') {
        ElMessage.error('问题内容不得为空');
      } else {
        let uploadTags = []
        for (let i = 0; i < editTagList.value.length; i++) {
          for (let j = 0; j < tags.value.length; j++) {
            if (tags.value[j].tagName === editTagList.value[i]) {
              uploadTags.push(tags.value[j].tagId)
              break;
            }
          }
        }
        updateQuesApi(qid.value,
            editHtml.value, editImgList.value, uploadTags).then(
            (res) => {
              if (res.isSuccess === true) {
                ElMessage.success("成功修改问题")
                question.value.quesContent.content = editHtml.value
                question.value.quesContent.imageList = []
                for (let i = 0; i < editImgList.value.length; i++) {
                  question.value.quesContent.imageList.push(editImgList.value[i])
                }
                question.value.tagIdList = uploadTags
                disTags.value = []
                for (let i = 0; i < question.value.tagIdList.length; i++) {
                  for (let j = 0; j < tags.value.length; j++) {
                    if (tags.value[j].tagId === question.value.tagIdList[i]) {
                      disTags.value.push(tags.value[j])
                    }
                  }
                }
                editHtml.value = ""
                editImgList.value = []
                editTagList.value = []
                sheet1.value = !sheet1.value
              } else {
                ElMessage.error("上传修改失败，请稍后再试")
              }
            }
        )
      }
    }

    const handleChange = (file) => {
      if (file.raw.type !== "image/jpeg" && file.raw.type !== "image/png") {
        ElMessage.error('Avatar picture must be JPG format!');
        return false;
      }
      uploadFileApi(file.raw).then((res) => {
        if (res.response === 'success') {
          ElMessage.success("Avatar picture upload succeeded!")
          imageList.value.push(res.fileUrl)
        } else {
          ElMessage.error('Avatar picture upload failed!');
        }
      })
      return true;
    }

    const findTagColor = (index) => {
      return tags.value[index].tagColor
    }

    const findTagIcon = (index) => {
      return tags.value[index].tagIcon
    }

    const showPic = (imgList) => {
      viewerApi({images: imgList})
    }

    const tagClick = (index) => {
      router.push("/HelpCenter/" + index)
    }

    const dialShow = ref(false)

    const goTop = () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    const menuClick = ref(false);

    const openAns = ref(false)

    const replyIndex = ref(-1)

    const openComment = ref(false)

    const commentHtml = ref('')

    const commentUserName = ref('')

    const toReplyComment = (params) => {
      commentUserName.value = params.commentUserName
      replyIndex.value = params.index
      openComment.value = true
      openAns.value = false
    }

    const uploadComment = () => {
      if (!userStateStore().isAuthentic) {
        ElMessage.error("请先登录")
        router.push('/loginPage')
      } else {
        if (String(commentHtml.value).replace(/<[^>]*>/g, "") === '') {
          ElMessage.error("不能上传空白答案")
        } else {
          replyComment(replyIndex.value, commentHtml.value, imageList.value).then(
              (res) => {
                if (res.isSuccess === true) {
                  ElMessage.success("回答已上传")
                  commentHtml.value = ''
                  imageList.value = []
                  sheet2.value = false
                  router.go(0)
                } else {
                  ElMessage.error("回答失败，请稍后再试")
                }
              }
          )
        }
      }
    }

    return {
      replyIndex,
      menuClick,
      tagClick,
      truncate,
      disTags,
      qid,
      question,
      tags,
      goAnchor,
      replyAnsConfig,
      mode: 'default',
      replyHtml,
      handleCreated1,
      toolbarConfig1,
      editorRef1,
      editorConfig,
      recommendQues,
      display,
      userLike,
      likeSum,
      setLikeQues,
      uploadAnswer,
      init,
      delQues,
      delDialog,
      isUser,
      delAns,
      handleCreated2,
      toolbarConfig2,
      editorRef2,
      editHtml,
      editImgList,
      editTagList,
      sheet1,
      toEdit,
      updateQues,
      findTagColor,
      findTagIcon,
      handleChange,
      tagNamesArray,
      showPic,
      delPic,
      refresh,
      dialShow,
      sheet2,
      goTop,
      avatarShow,
      openAns,
      openComment,
      editorRef3,
      handleCreated3,
      commentHtml,
      uploadComment,
      toReplyComment,
      commentUserName
    };
  },
};
</script>

<template>
  <div v-if="question !== null">
    <div v-if="!display.smAndDown.value">
      <div class="left-buttons">
        <!-- 点赞 -->
        <div>
          <v-btn :icon="'mdi-chevron-up'"
                 color="light-blue-darken-1"
                 @click="goTop"
          />
        </div>
      </div>
      <v-row>
        <v-col cols="12">
          <v-card elevation="1" style="text-align: left">
            <v-row>
              <v-col cols="8" offset="1">
                <div style="margin-left: 10px;margin-bottom: 10px;margin-top: 30px">
                  <v-chip v-for="tag in disTags"
                          :key="question.quesId + '-' + tag.tagId" :color="tag.tagColor"
                          @click="tagClick(tag.tagId)"
                          :class="`cursor-pointer`"
                          style="margin-left: 3px">
                    <v-icon>{{ tag.tagIcon }}</v-icon>
                    {{ tag.tagName }}
                  </v-chip>
                </div>
                <div style="margin-left: 20px;margin-right: 20px;margin-top: 10px;font-weight: bold;font-size: 25px"
                     v-dompurify-html="question.quesContent.content"/>
                <v-row style="margin: 10px">
                  <v-col v-for="(image,index) in question.quesContent.imageList"
                         :key="'image' + index" :cols="display.smAndDown.value? 4 : 3"
                  >
                    <div class="avatar-wrapper">
                      <el-image
                          class="avatar"
                          :src="image"
                          :fit="'cover'"
                          @click="showPic(question.quesContent.imageList)"
                      />
                    </div>
                  </v-col>
                </v-row>
                <div style="display: flex; align-items: center;margin-left: 10px">
                  <UserAvatar v-if="avatarShow" :userId="question.userId"></UserAvatar>
                  <v-col cols="7">
                    <p style="font-size: 20px;margin-top: 10px">{{ question.userName }}</p>
                    <p style="font-size: 15px;color: gray">{{ formatDate(question.quesTime) }}</p>
                  </v-col>
                </div>
                <div style="margin-bottom: 20px">
                  <v-btn color="blue-lighten-1">关注问题</v-btn>
                  <v-btn v-if="!openAns" style="margin-left:15px" variant="outlined" color="blue-lighten-1"
                         prepend-icon="mdi-pen" @click="openAns = true;openComment = false">写回答
                  </v-btn>
                  <v-btn v-if="openAns" style="margin-left:15px" variant="outlined"
                         prepend-icon="mdi-window-close" @click="openAns = false">取消回答
                  </v-btn>
                  <v-btn :prepend-icon="!userLike ?
                  'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text"
                         @click="setLikeQues"
                         color="blue-grey-lighten-2">
                    好问题 {{ likeSum }}
                  </v-btn>
                  <v-btn variant="text" prepend-icon="mdi-message-reply-text" color="blue-grey-lighten-2">
                    {{ question.ansIdList.length }} 条回答
                  </v-btn>
                  <v-menu v-show="menuClick" :location="'bottom'">
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
                        <v-icon size="22" color="red-darken-1">mdi-delete-clock</v-icon>
                        删除
                      </v-list-item>
                      <v-list-item density="compact" v-if="isUser" color="primary" @click="toEdit">
                        <v-icon size="22" color="blue-darken-1">mdi-book-edit</v-icon>
                        修改
                      </v-list-item>
                      <v-list-item density="compact">
                        举报
                      </v-list-item>
                    </v-list>
                  </v-menu>
                </div>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="8" offset="1">
          <v-card elevation="1" style="text-align: left">
            <div v-if="openAns">
              <div id="comment"
                   style="width:85%;transform: translateX(3%);margin-top: 10px;display: flex; justify-content: space-between;">
                <span style="font-weight: bold;font-size: 20px">评论 </span>
                <span>
                <v-btn prepend-icon="mdi-message-reply-text" color="primary" @click="uploadAnswer">
                  发送回复
                </v-btn>
              </span>
              </div>
              <div style="width: 85%;transform: translateX(2%);border: 1px solid #ccc;margin: 10px">
                <Toolbar
                    style="border-bottom: 1px solid #ccc"
                    :editor="editorRef1"
                    :defaultConfig="toolbarConfig1"
                    :mode="mode"
                />
                <Editor
                    style="height: 250px; overflow-y: hidden;"
                    v-model="replyHtml"
                    :defaultConfig="editorConfig"
                    :mode="mode"
                    @onCreated="handleCreated1"
                />
              </div>
            </div>

            <div v-if="openComment">
              <div
                   style="width:85%;transform: translateX(3%);margin-top: 10px;display: flex; justify-content: space-between;">
                <span style="font-weight: bold;font-size: 20px">回复 </span> {{commentUserName}}
                <span>
                <v-btn prepend-icon="mdi-message-reply-text" color="primary" @click="uploadComment">
                  发送回复
                </v-btn>
              </span>
              </div>
              <div style="width: 85%;transform: translateX(2%);border: 1px solid #ccc;margin: 10px">
                <Toolbar
                    style="border-bottom: 1px solid #ccc"
                    :editor="editorRef3"
                    :defaultConfig="toolbarConfig1"
                    :mode="mode"
                />
                <Editor
                    style="height: 250px; overflow-y: hidden;"
                    v-model="commentHtml"
                    :defaultConfig="replyAnsConfig"
                    :mode="mode"
                    @onCreated="handleCreated3"
                />
              </div>
            </div>

            <div style="transform: translateX(3%);margin-top: 10px">
              <span style="font-weight: bold;font-size: 20px">全部评论 </span>
              <span style="color: gray">{{ question.ansIdList.length }}</span>
            </div>
            <AnsCard v-for="(ans,index) in question.ansIdList" :key="'ans1-' + index"
                     @replyAnswer="toReplyComment"
                     :ansId="ans" :index="index" @delAns="delAns"/>
            <div style="height: 100px"></div>
          </v-card>
        </v-col>
        <v-col cols="3">
          <div>
            <v-card
                :style="top ? 'position: fixed;top: 80px;width:250px;text-align:left;max-height:550px;overflow-y:scroll'
                      : 'width:250px;text-align:left;max-height:550px;overflow-y:scroll'"
            >
              <div style="display: flex; align-items: center; transform: translateX(5%); margin-top: 10px">
                <v-icon>mdi-hexagram-outline</v-icon>
                <span style="font-weight: bold; font-size: 15px">推荐问题 </span>
              </div>
              <v-divider></v-divider>
              <RecQuesCard v-for="ques in recommendQues" :key="'rec-' + ques.quesId" :tags="tags"
                           @refresh="refresh"
                           :question="ques"/>
            </v-card>
          </div>

        </v-col>
      </v-row>
      <div style="height: 200px">

      </div>
    </div>
    <div v-else>

      <div class="dials" v-if="dialShow">
        <!-- 点赞 -->
        <div style="margin-bottom: 10px">
          <v-btn :icon="'mdi-minus'"
                 color="grey-lighten-5"
                 @click="dialShow = !dialShow"
          />
        </div>
        <div style="margin-bottom: 10px">
          <v-btn :icon="!userLike ?
              'mdi-thumb-up-outline' : 'mdi-thumb-up'"
                 color="grey-lighten-5"
                 size="small" @click="setLikeQues"
                 v-if="likeSum === 0"
          />
          <v-badge v-else :content="likeSum" color="red-lighten-1" offset-x="5" offset-y="5">
            <v-btn :icon="!userLike ?
              'mdi-thumb-up-outline' : 'mdi-thumb-up'"
                   color="grey-lighten-5"
                   size="small" @click="setLikeQues"
            />
          </v-badge>
        </div>
        <div style="margin-bottom: 10px">
          <v-btn :icon="'mdi-message-reply-text'"
                 color="grey-lighten-5"
                 size="small"
                 @click="sheet2 = !sheet2"
          />
        </div>
      </div>
      <div class="dials" v-else>
        <div>
          <v-btn :icon="'mdi-plus'"
                 color="grey-lighten-5"
                 @click="dialShow = !dialShow"
          />
        </div>
      </div>
      <v-row style="margin-left: 12px;margin-right: 12px">
        <v-col cols="12">
          <v-card elevation="1" style="margin-top: 10px;text-align: left">
            <div style="display: flex; align-items: center;">
              <v-col cols="2" style="justify-content: end;margin-right: 5px">
                <UserAvatar :userId="question.userId"/>
              </v-col>
              <v-col cols="6">
                <p style="font-size: 20px;margin-top: 10px">{{ question.userName }}</p>
                <p style="font-size: 15px;color: gray">{{ formatDate(question.quesTime) }}</p>
              </v-col>
              <v-col cols="3" v-if="isUser" offset="1" style="display: flex; justify-content: space-around;">
                <v-btn variant="text" icon="mdi-delete-clock" size="large" @click="delDialog = !delDialog"></v-btn>
                <v-btn variant="text" icon="mdi-book-edit" size="large" @click="toEdit"></v-btn>
              </v-col>
            </div>
            <div style="margin-left: 20px;margin-right: 20px;margin-bottom: 15px"
                 v-dompurify-html="question.quesContent.content"/>
            <v-row>
              <v-col v-for="(image,index) in question.quesContent.imageList"
                     :key="'image' + index" :cols="display.smAndDown.value? 4 : 3"
              >
                <div class="avatar-wrapper">
                  <el-image
                      class="avatar-app"
                      :src="image"
                      :fit="'cover'"
                      @click="showPic(question.quesContent.imageList)"
                  />
                </div>
              </v-col>
            </v-row>
            <div style="margin-left: 10px;margin-bottom: 10px;margin-top: 10px">
              <v-btn :prepend-icon=" !userLike ?
                  'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text" size="small"
                     color="blue-grey-lighten-2" @click="setLikeQues">
                {{ likeSum }}
              </v-btn>
              <v-btn variant="text" prepend-icon="mdi-message-reply-text" size="small" color="blue-grey-lighten-2">
                {{ question.ansSum }}
              </v-btn>
              <v-chip v-for="tag in disTags" size="small"
                      :key="question.quesId + '-' + tag.tagId" :color="tag.tagColor"
                      @click="tagClick(tag.tagId)"
                      style="margin-left: 3px;cursor: pointer">
                <v-icon>{{ tag.tagIcon }}</v-icon>
                {{ tag.tagName }}
              </v-chip>
            </div>
          </v-card>

          <v-card elevation="1" style="margin-top: 10px;text-align: left">
            <div style="transform: translateX(3%);margin-top: 10px">
              <span style="font-weight: bold;font-size: 20px">全部评论 </span>
              <span style="color: gray">{{ question.ansIdList.length }}</span>
            </div>
            <div v-for="(ans,index) in question.ansIdList" :key="'ans2-' + index">
              <AppAnsCard :ansId="ans" :index="index" @delAns="delAns"/>
            </div>
          </v-card>
        </v-col>
      </v-row>
      <div style="height: 200px"></div>
    </div>
  </div>

  <v-bottom-sheet v-model="sheet1" inset>
    <v-card
        class="text-center"
        height="800"
    >
      <v-card-text>
        <v-row align="center" style="margin-bottom: 5px">
          <v-col cols="4" offset="4">
            编辑问题
          </v-col>
          <v-col cols="4">
            <v-btn variant="text" @click="updateQues">
              发布
            </v-btn>
            <v-btn variant="text" @click="sheet1 = !sheet1">
              close
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col v-for="(image,index) in editImgList"
                 :key="'image' + index" :cols="display.smAndDown.value? 4 : 3"
          >
            <div class="avatar-wrapper">
              <div class="right-top">
                <v-btn @click="delPic(index)" density="compact" size="small" color="red-lighten-1"
                       icon="mdi-close"></v-btn>
              </div>
              <el-image
                  class="avatar"
                  :src="image"
                  :fit="'cover'"
                  @click="showPic(editImgList)"
              />
            </div>
          </v-col>
          <v-col :cols="display.smAndDown.value? 4 : 3">
            <el-form style="width: 100%">
              <el-upload
                  class="avatar-uploader"
                  action="#"
                  :show-file-list="false"
                  :auto-upload="false"
                  :on-change="handleChange"
                  accept=".jpg,.png"
              >
                <el-icon class="avatar-uploader-icon">
                  <Plus/>
                </el-icon>
              </el-upload>
            </el-form>
          </v-col>
        </v-row>

        <div>
          <v-select
              v-model="editTagList"
              :items="tagNamesArray.length  === 0 ? [] : tagNamesArray"
              multiple
              label="添加标签"
              density="default"
          >
            <template v-slot:selection="{item, index}">
              <v-chip size="x-small" :color="findTagColor(index)">
                <v-icon>{{ findTagIcon(index) }}</v-icon>
                {{ item.title }}
              </v-chip>
            </template>
          </v-select>
        </div>

        <div style="border: 1px solid #ccc">
          <Editor
              style="height: 350px; overflow-y: hidden;"
              v-model="editHtml"
              :defaultConfig="editorConfig"
              :mode="mode"
              @onCreated="handleCreated2"
          />
          <Toolbar
              style="border-bottom: 1px solid #ccc"
              :editor="editorRef2"
              :defaultConfig="toolbarConfig2"
              :mode="mode"
          />
        </div>
      </v-card-text>
    </v-card>
  </v-bottom-sheet>
  <v-bottom-sheet v-model="sheet2" inset>
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
                   color="primary" @click="uploadAnswer">
              回复
            </v-btn>
          </v-col>
        </v-row>
        <div style="border: 1px solid #ccc;overflow-y: scroll;margin: 0">
          <Toolbar
              style="border-bottom: 1px solid #ccc;"
              :editor="editorRef1"
              :defaultConfig="toolbarConfig1"
              :mode="mode"
          />
          <Editor
              style="height: 300px;"
              v-model="replyHtml"
              :defaultConfig="editorConfig"
              :mode="mode"
              @onCreated="handleCreated1"
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
.left-buttons {
  position: fixed;
  z-index: 888;
  top: 90%;
  left: 2%;
  transform: translateY(-90%);
}

.dials {
  position: fixed;
  z-index: 888;
  top: 85%;
  right: 2%;
  transform: translateY(-85%);
}
</style>

<style>
.avatar-wrapper {
  position: relative;
  width: 100%;
  height: 0;
  padding: 0;
  padding-bottom: 100%;
  z-index: 1000;
}

.avatar {
  position: absolute !important;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  cursor: pointer;

  overflow: hidden;
}

.avatar-app {
  position: absolute !important;
  top: 5px;
  right: 0;
  bottom: 0;
  left: 5px;
  overflow: hidden;
}

.height-restrict {
  max-height: 550px;
  overflow: scroll;
}
</style>