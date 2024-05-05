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
  getTagsApi,
  setLikeQuesApi, updateQuesApi,
  uploadAnsApi, uploadFileApi
} from "@/components/HelpCenter/api";
import {getQuesByIdApi} from "@/components/HelpCenter/api";
import {ElMessage} from "element-plus";
import router from "@/router";
import UserStateStore, {userStateStore} from "@/store";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";
import {api as viewerApi} from "v-viewer";

export default {
  name: "QuesInfo",
  components: {UserAvatar, AppAnsCard, AnsCard, RecQuesCard, Editor, Toolbar},
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
      let threshold = 60;

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
      getQuesByIdApi(qid.value).then(
          (res) => {
            question.value = res.question
            userLike.value = res.question.ifUserLike
            likeSum.value = res.question.likeSum
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

    const init = () => {
      let router = useRouter()
      qid.value = router.currentRoute.value.params.qid
      getQuesByIdApi(qid.value).then(
          (res) => {
            question.value = res.question
            userLike.value = res.question.ifUserLike
            likeSum.value = res.question.likeSum
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

    const toolbarConfig1 = {
      excludeKeys: ['undo', 'redo', 'todo', 'fontSize', 'fontFamily',
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

    const editorConfig = {placeholder: '请输入内容...'}

    onBeforeUnmount(() => {
      const editor1 = editorRef1.value
      if (editor1 == null) return
      editor1.destroy()

      const editor2 = editorRef2.value
      if (editor2 == null) return
      editor1.destroy()
    })

    const handleCreated1 = (editor) => {
      editorRef1.value = editor // 记录 editor 实例，重要！
    }

    const handleCreated2 = (editor) => {
      editorRef2.value = editor // 记录 editor 实例，重要！
    }

    const userLike = ref(false)

    const likeSum = ref(0)

    const replyHtml = ref("");

    const imageList = ref([])

    const uploadAnswer = () => {
      if(!userStateStore().isAuthentic) {
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
            if(res.isSuccess === true) {
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
      question.value.ansIdList.splice(index,1)
    }

    const editHtml = ref("")

    const editImgList = ref([])

    const editTagList = ref([])

    const sheet = ref(false)

    const toEdit = () => {
      sheet.value = !sheet.value
      editHtml.value = question.value.quesContent.content
      editImgList.value = []
      for(let i = 0;i < question.value.quesContent.imageList.length;i++) {
        editImgList.value.push(question.value.quesContent.imageList[i])
      }
      editTagList.value = []
      for(let i = 0;i < question.value.tagIdList.length;i++) {
        for(let j = 0;j < tags.value.length;j++) {
          if(question.value.tagIdList[i] === tags.value[j].tagId) {
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
        for(let i = 0;i < editTagList.value.length;i++) {
          for(let j =  0;j < tags.value.length; j++) {
            if(tags.value[j].tagName === editTagList.value[i]) {
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
                for(let i = 0;i < editImgList.value.length;i++) {
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
                editHtml.value= ""
                editImgList.value = []
                editTagList.value = []
                sheet.value = !sheet.value
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

    return {
      truncate,
      disTags,
      qid,
      question,
      tags,
      goAnchor,
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
      sheet,
      toEdit,
      updateQues,
      findTagColor,
      findTagIcon,
      handleChange,
      tagNamesArray,
      showPic,
      delPic,
      refresh
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
          <v-btn :icon="!userLike ?
              'mdi-thumb-up-outline' : 'mdi-thumb-up'"
                 color="light-blue-darken-1"
                 size="small" @click="setLikeQues"
                 v-if="likeSum === 0"
          />
          <v-badge v-else :content="likeSum" color="red-lighten-1" offset-x="5" offset-y="5">
            <v-btn :icon="!userLike ?
              'mdi-thumb-up-outline' : 'mdi-thumb-up'"
                   color="light-blue-darken-1"
                   size="small" @click="setLikeQues"
            />
          </v-badge>
        </div>
        <!-- 评论 -->
        <div style="margin-top: 25px">
          <a href="javascript:void(0)" @click="goAnchor('comment')" v-if="question.ansSum !== 0">
            <v-btn icon="mdi-message-reply-outline" size="small" color="light-blue-darken-1"/>
          </a>
          <v-badge v-else :content="question.ansSum" color="red-lighten-1" offset-x="5" offset-y="5">
            <a href="javascript:void(0)" @click="goAnchor('comment')">
              <v-btn icon="mdi-message-reply-outline" size="small" color="light-blue-darken-1"/>
            </a>
          </v-badge>
        </div>
      </div>
      <v-row>
        <v-col cols="8" offset="1">
          <v-card elevation="1" style="margin-top: 10px;text-align: left">
            <div style="display: flex; align-items: center;margin-left: 10px">
              <UserAvatar :userId="question.userId"></UserAvatar>
              <v-col cols="7">
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
            <div style="margin-left: 10px;margin-bottom: 10px;margin-top: 30px">
              <v-chip v-for="tag in disTags" size="small"
                      :key="question.quesId + '-' + tag.tagId" :color="tag.tagColor"
                      style="margin-left: 3px">
                <v-icon>{{ tag.tagIcon }}</v-icon>
                {{ tag.tagName }}
              </v-chip>
            </div>
          </v-card>

          <v-card elevation="1" style="margin-top: 10px;text-align: left">
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
            <div style="transform: translateX(3%);margin-top: 10px">
              <span style="font-weight: bold;font-size: 20px">全部评论 </span>
              <span style="color: gray">{{ question.ansIdList.length }}</span>
            </div>
            <AnsCard v-for="(ans,index) in question.ansIdList" :key="'ans1-' + index"
                     :ansId="ans" :index="index" @delAns="delAns"/>
            <div style="height: 100px"></div>
          </v-card>
        </v-col>
        <v-col cols="3">
          <v-card style="width: 250px;margin-bottom: 20px;margin-top: 10px">
            <div style="display: flex; align-items: center;justify-content: center">
              <UserAvatar :userId="userStateStore().getUserId"/>
              <v-col cols="7" style="text-align: left">
                <p style="font-size: 20px;margin-top: 10px">{{ userStateStore().getUserName }}</p>
              </v-col>
            </div>
            <div style="width: 75%;margin-top:3px;margin-bottom:10px;transform: translateX(12.5%)">
              <v-divider></v-divider>
            </div>
            <div style="margin-bottom: 10px">
              {{userStateStore().sign}}
            </div>
          </v-card>
          <v-card :style="top ?
          'position: fixed;top: 80px;width:250px;text-align:left' : 'width:250px;text-align:left'">
            <div style="display: flex; align-items: center; transform: translateX(5%); margin-top: 10px">
              <v-icon>mdi-hexagram-outline</v-icon>
              <span style="font-weight: bold; font-size: 15px">推荐问题 </span>
            </div>
            <v-divider></v-divider>
            <RecQuesCard v-for="ques in recommendQues" :key="'rec-' + ques.quesId" :tags="tags"
                         @refresh="refresh"
                         :question="ques"/>
          </v-card>
        </v-col>
      </v-row>
      <div style="height: 200px">

      </div>
    </div>
    <div v-else>
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
                      style="margin-left: 3px">
                <v-icon>{{ tag.tagIcon }}</v-icon>
                {{ tag.tagName }}
              </v-chip>
            </div>
          </v-card>

          <v-card elevation="1" style="margin-top: 10px;text-align: left">
            <div id="comment"
                 style="width:85%;transform: translateX(3%);margin-top: 10px;display: flex; justify-content: space-between;">
              <span style="font-weight: bold;font-size: 20px">评论 </span>
              <span><v-btn prepend-icon="mdi-message-reply-text" color="primary" @click="uploadAnswer">发送回复</v-btn></span>
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

  <v-bottom-sheet v-model="sheet" inset :persistent="true">
    <v-card
        class="text-center"
        height="800"
    >
      <v-card-text>
        <v-row align="center" style="margin-bottom: 5px">
          <v-col  cols="4" offset="4">
            编辑问题
          </v-col>
          <v-col cols="4">
            <v-btn variant="text" @click="updateQues">
              发布
            </v-btn>
            <v-btn variant="text" @click="sheet = !sheet">
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
                <v-btn @click="delPic(index)" density="compact" size="small" color="red-lighten-1" icon="mdi-close"></v-btn>
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
  top: 50%;
  left: 2%;
  transform: translateY(-50%);
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
</style>