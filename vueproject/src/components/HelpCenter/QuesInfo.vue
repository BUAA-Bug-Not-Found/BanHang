<script>
import {onBeforeUnmount, ref, shallowRef} from "vue";
import {useRouter} from "vue-router";
import AnsCard from "@/components/HelpCenter/AnsCard.vue";
import {Editor, Toolbar} from "@wangeditor/editor-for-vue";
import RecQuesCard from "@/components/HelpCenter/RecQuesCard.vue";
import {useDisplay} from "vuetify";
import AppAnsCard from "@/components/HelpCenter/AppAnsCard.vue";
import {getTagsApi, setLikeQuesApi} from "@/components/HelpCenter/api";
import {getQuesByIdApi} from "@/components/HelpCenter/api";

export default {
  name: "QuesInfo",
  components: {AppAnsCard, RecQuesCard, Editor, Toolbar, AnsCard},
  data() {
    return {
      top: false,
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
  },
  methods: {
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

    const selectTags = ref([])

    const tags = ref([])

    const recommendQues = ref([
      {
        quesId: 1,
        userId: 1,
        userName: "test_user",
        quesContent: {
          content: "test_question1"
        },
        quesState: 1,
        quesTime: "2024/4/22 14:03",
        ifUserLike: 1,
        ansSum: 20,
        likeSum: 10,
        tagIdList: [1, 2]
      },
      {
        quesId: 2,
        userId: 1,
        userName: "test_user",
        quesContent: {
          content: "test_question2"
        },
        quesState: 2,
        quesTime: "2024/4/22 14:03",
        ifUserLike: 0,
        ansSum: 20,
        likeSum: 10,
        tagIdList: [3]
      },
      {
        quesId: 3,
        userId: 1,
        userName: "test_user",
        quesContent: {
          content: "test_question3"
        },
        quesState: 3,
        quesTime: "2024/4/22 14:03",
        ifUserLike: 0,
        ansSum: 2,
        likeSum: 10,
        tagIdList: [3]
      },
      {
        quesId: 4,
        userId: 1,
        userName: "test_user",
        quesContent: {
          content: "test_question4"
        },
        quesState: 3,
        quesTime: "2024/4/22 14:03",
        ifUserLike: 0,
        ansSum: 2,
        likeSum: 10,
        tagIdList: [1]
      }
    ])

    const disTags = ref([])
    const qid = ref(0)

    const replyHtml = ref("");

    const question = ref(null)

    const answers = ref()

    const init = () => {
      let router = useRouter()
      qid.value = router.currentRoute.value.params.qid
      console.log(qid.value)
      getQuesByIdApi(qid.value).then(
          (res) => {
            question.value = res.question
            userLike.value = res.question.ifUserLike
            likeSum.value = res.question.likeSum
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

    const editorRef = shallowRef()

    const toolbarConfig = {
      excludeKeys: ['undo', 'redo', 'todo', 'fontSize', 'fontFamily',
        'lineHeight', 'group-justify', 'group-video',
        'group-indent', 'bgColor', 'bulletedList', 'italic', 'group-image'
      ],
    }
    const editorConfig = {placeholder: '请输入内容...'}

    onBeforeUnmount(() => {
      const editor = editorRef.value
      if (editor == null) return
      editor.destroy()
    })

    const handleCreated = (editor) => {
      editorRef.value = editor // 记录 editor 实例，重要！
      console.log(editor.getAllMenuKeys())
    }

    const userLike = ref(false)

    const likeSum = ref(0)

    const setLikeQues = () => {
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

    return {
      truncate,
      disTags,
      qid,
      question,
      selectTags,
      tags,
      goAnchor,
      mode: 'default',
      answers,
      replyHtml,
      handleCreated,
      toolbarConfig,
      editorRef,
      editorConfig,
      recommendQues,
      display,
      userLike,
      likeSum,
      setLikeQues
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
            <div style="display: flex; align-items: center;">
              <v-avatar color="surface-variant" style="margin-left: 10px;margin-top: 10px" size="48"/>
              <v-col cols="7">
                <p style="font-size: 20px;margin-top: 10px">{{ question.userName }}</p>
                <p style="font-size: 15px;color: gray">{{ question.quesTime }}</p>
              </v-col>
              <v-col style="margin-left: 10px;">
              </v-col>
            </div>
            <div style="margin-left: 20px;margin-right: 20px;margin-bottom: 15px"
                 v-dompurify-html="question.quesContent.content"/>
            <div style="margin-left: 10px;margin-bottom: 10px">
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
              <span><v-btn prepend-icon="mdi-reply" color="primary">发送回复</v-btn></span>
            </div>
            <div style="width: 85%;transform: translateX(2%);border: 1px solid #ccc;margin: 10px">
              <Toolbar
                  style="border-bottom: 1px solid #ccc"
                  :editor="editorRef"
                  :defaultConfig="toolbarConfig"
                  :mode="mode"
              />
              <Editor
                  style="height: 250px; overflow-y: hidden;"
                  v-model="replyHtml"
                  :defaultConfig="editorConfig"
                  :mode="mode"
                  @onCreated="handleCreated"
              />
            </div>
            <div style="transform: translateX(3%);margin-top: 10px">
              <span style="font-weight: bold;font-size: 20px">全部评论 </span>
              <span style="color: gray">{{ question.ansIdList.length }}</span>
            </div>
            <AnsCard v-for="(ans,index) in question.ansIdList" :key="'ans-' + ans" :index="index"/>
          </v-card>
        </v-col>
        <v-col cols="3">
          <v-card style="width: 250px;margin-bottom: 20px;margin-top: 10px">
            <div style="display: flex; align-items: center;">
              <v-avatar color="surface-variant" style="margin-left: 10px;margin-top: 10px" size="35"/>
              <v-col cols="7" style="text-align: left">
                <p style="font-size: 20px;margin-top: 10px">{{ question.userName }}</p>
              </v-col>
            </div>
            <div style="width: 75%;margin-top:3px;margin-bottom:10px;transform: translateX(12.5%)">
              <v-divider></v-divider>
            </div>
            <div style="margin-bottom: 10px">
              statistic info
            </div>
          </v-card>
          <v-card :style="top ?
          'position: fixed; z-index: 888;top: 80px;width:250px;text-align:left' : 'width:250px;text-align:left'">
            <div style="display: flex; align-items: center; transform: translateX(5%); margin-top: 10px">
              <v-icon>mdi-hexagram-outline</v-icon>
              <span style="font-weight: bold; font-size: 15px">推荐问题 </span>
            </div>
            <v-divider></v-divider>
            <RecQuesCard v-for="ques in recommendQues" :key="'rec-' + ques.quesId" :tags="tags" :question="ques"/>
          </v-card>
        </v-col>
      </v-row>
      <div style="height: 200px">

      </div>
    </div>
    <div v-else>
      <v-row>
        <v-col cols="12">
          <v-card elevation="1" style="margin-top: 10px;text-align: left">
            <div style="display: flex; align-items: center;">
              <v-avatar color="surface-variant" style="margin-left: 10px;margin-top: 10px" size="48"/>
              <v-col cols="7">
                <p style="font-size: 20px;margin-top: 10px">{{ question.userName }}</p>
                <p style="font-size: 15px;color: gray">{{ question.quesTime }}</p>
              </v-col>
              <v-col style="margin-left: 10px;">
              </v-col>
            </div>
            <div style="margin-left: 20px;margin-right: 20px;margin-bottom: 15px"
                 v-dompurify-html="question.quesContent.content"/>
            <div style="margin-left: 10px;margin-bottom: 10px">
              <v-btn :prepend-icon=" !userLike ?
                  'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text" size="small"
                     color="blue-grey-lighten-2" @click="setLikeQues">
                {{ likeSum }}
              </v-btn>
              <v-btn variant="text" prepend-icon="mdi-reply" size="small" color="blue-grey-lighten-2">
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
              <span><v-btn prepend-icon="mdi-reply" color="primary">发送回复</v-btn></span>
            </div>
            <div style="width: 85%;transform: translateX(2%);border: 1px solid #ccc;margin: 10px">
              <Toolbar
                  style="border-bottom: 1px solid #ccc"
                  :editor="editorRef"
                  :defaultConfig="toolbarConfig"
                  :mode="mode"
              />
              <Editor
                  style="height: 250px; overflow-y: hidden;"
                  v-model="replyHtml"
                  :defaultConfig="editorConfig"
                  :mode="mode"
                  @onCreated="handleCreated"
              />
            </div>
            <div style="transform: translateX(3%);margin-top: 10px">
              <span style="font-weight: bold;font-size: 20px">全部评论 </span>
              <span style="color: gray">{{ question.ansIdList.length }}</span>
            </div>
            <AppAnsCard v-for="(ans,index) in question.ansIdList" :key="'ans-' + ans" :index="index"/>
          </v-card>
        </v-col>
      </v-row>
      <div style="height: 200px">

      </div>
    </div>
  </div>
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