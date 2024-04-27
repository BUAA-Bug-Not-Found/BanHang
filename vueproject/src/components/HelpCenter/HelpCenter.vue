<script>
import {getQuestions} from "@/components/HelpCenter/api";
import '@wangeditor/editor/dist/css/style.css'
import {onBeforeUnmount, ref, shallowRef} from "vue";
import QuesCard from "@/components/HelpCenter/QuesCard.vue";
import {Editor, Toolbar} from "@wangeditor/editor-for-vue";
import {useDisplay} from "vuetify";
import AppQuesCard from "@/components/HelpCenter/AppQuesCard.vue";

export default {
  name: "HelpCenter",
  components: {AppQuesCard, Editor, Toolbar, QuesCard},
  setup() {
    const page = ref(1)
    const pageSize = ref(10)
    const quesSum = ref(4)
    const valueHtml = ref('')
    const editorRef = shallowRef()
    const sheet = ref(false)

    const toolbarConfig = {}
    const editorConfig = {placeholder: '请输入内容...'}

    const selectTags = ref([])

    const tags = ref([
      {
        tagId: 1,
        tagName: "学业生活",
        tagIcon: 'mdi-clock',
        tagColor: 'blue-darken-1',
      },
      {
        tagId: 2,
        tagName: "日常事务",
        tagIcon: 'mdi-account',
        tagColor: 'cyan-darken-1',
      },
      {
        tagId: 3,
        tagName: "情感交流",
        tagIcon: 'mdi-flag',
        tagColor: 'red-darken-1',
      }
    ])

    const tagNamesArray = ref(['学习生活', '日常生活', '情感交流'])

    const questions = ref(
        [
          {
            quesId: 1,
            userId: 1,
            userName: "test_user",
            quesContent: "test_question1",
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
            quesContent: "test_question2",
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
            quesContent: "test_question3",
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
            quesContent: "test_question4",
            quesState: 3,
            quesTime: "2024/4/22 14:03",
            ifUserLike: 0,
            ansSum: 2,
            likeSum: 10,
            tagIdList: [1]
          }
        ]
    )
    const init = () => {
      getQuestions(1, pageSize.value).then(
          (data) => {
            quesSum.value = data.ques_sum
            questions.value = data.questions
            console.log(data.ques_sum)
          }
      )
    }
    init()
    const updatePage = () => {
      console.log(page.value)
      console.log(questions)
      // getQuestions(page.value, pageSize).then(
      //     (data) => {
      //       quesSum.value = data.ques_sum
      //       questions.value = data.questions
      //     }
      // )
    }
    const getMore = () => {
      page.value = page.value + 1
      // getQuestions(page.value, pageSize).then(
      //     (data) => {
      //       quesSum.value = data.ques_sum
      //       questions.value.concat(data.questions)
      //     }
      // )
    }

    onBeforeUnmount(() => {
      const editor = editorRef.value
      if (editor == null) return
      editor.destroy()
    })

    const handleCreated = (editor) => {
      editorRef.value = editor // 记录 editor 实例，重要！
    }

    const findTagColor = (index) => {
      return tags.value[index].tagColor
    }

    const findTagIcon = (index) => {
      return tags.value[index].tagIcon
    }

    const display = useDisplay()
    return {
      editorConfig,
      mode: 'default',
      toolbarConfig,
      editorRef,
      page,
      tags,
      questions,
      quesSum,
      pageSize,
      getMore,
      updatePage,
      valueHtml,
      handleCreated,
      sheet,
      selectTags,
      tagNamesArray,
      findTagColor,
      findTagIcon,
      display
    }
  }
}
</script>

<template>

  <div v-if="!display.smAndDown.value">
    <v-row justify="center" style="margin-top: 10px">
      <v-col cols="2" style="margin-right: 10px">
        <v-list density="compact">
          <v-btn @click="sheet = !sheet" color="blue-darken-1" class="w-100" style="margin-bottom: 15px">
            发起问题
          </v-btn>
          <v-list-subheader>分区</v-list-subheader>
          <v-list-item
              v-for="(item, i) in tags"
              :key="i"
              :value="item"
              color="primary"
              style="text-align: left;"
          >
            <v-icon :icon="item.tagIcon" size="20" :color="item.tagColor"></v-icon>
            <span style="font-size: 13px;margin-left: 5px">
            {{ item.tagName }}
          </span>
          </v-list-item>
        </v-list>
      </v-col>

      <v-col cols="8" style="margin-bottom: 25px">
        <QuesCard style="margin-bottom: 5px" v-for="(ques, index) in questions" :key="ques.quesId"
                  :question="questions[index]" :tags="tags"/>
        <!--      <v-pagination-->
        <!--          v-model="page"-->
        <!--          :length="Math.floor(quesSum / pageSize) + 2"-->
        <!--          class="my-4"-->
        <!--          @update:modelValue="updatePage"-->
        <!--      ></v-pagination>-->
        <v-btn v-if="questions.length < quesSum" color="light-blue-darken-1" style="margin-top: 5px" @click="getMore">
          加载更多
        </v-btn>
      </v-col>
      <v-col cols="2">

      </v-col>
    </v-row>
  </div>
  <div v-else>
    <div class="left-buttons">
      <!-- 点赞 -->
      <div>
          <v-btn :icon="'mdi-plus'"
                 color="light-blue-darken-1"
                 size="small" @click="sheet = !sheet"
          />
      </div>
      <!-- 评论 -->
    </div>
    <v-row>
      <v-col cols="12" style="margin-bottom: 25px">
        <AppQuesCard style="margin-bottom: 5px" v-for="(ques, index) in questions" :key="ques.quesId"
                  :question="questions[index]" :tags="tags"/>
        <v-btn v-if="questions.length < quesSum" color="light-blue-darken-1" style="margin-top: 5px" @click="getMore">
          加载更多
        </v-btn>
      </v-col>
    </v-row>
  </div>
  <v-bottom-sheet v-model="sheet" inset>
    <v-card
        class="text-center"
        height="600"
    >
      <v-card-text>
        <v-row align="center" style="margin-bottom: 5px">
          <v-col cols="4" offset="4">
            发布问题
          </v-col>
          <v-col cols="4">
            <v-btn variant="text" @click="sheet = !sheet">
              close
            </v-btn>
          </v-col>
        </v-row>

        <div>
          <v-select
              v-model="selectTags"
              :items="tagNamesArray"
              multiple
              label="添加标签"
              density="default"
          >
            <template v-slot:selection="{item, index}">
              <v-chip size="x-small" :color="findTagColor(index)">
                <v-icon>{{findTagIcon(index)}}</v-icon>
                {{item.title}}
              </v-chip>
            </template>
          </v-select>
        </div>
        <div style="border: 1px solid #ccc">
          <Toolbar
              style="border-bottom: 1px solid #ccc"
              :editor="editorRef"
              :defaultConfig="toolbarConfig"
              :mode="mode"
          />
          <Editor
              style="height: 350px; overflow-y: hidden;"
              v-model="valueHtml"
              :defaultConfig="editorConfig"
              :mode="mode"
              @onCreated="handleCreated"
          />
        </div>
      </v-card-text>
    </v-card>
  </v-bottom-sheet>

</template>

<style scoped>
.left-buttons {
  position: fixed;
  z-index: 888;
  top: 86%;
  right: 2%;
  transform: translateY(-86%);
}
</style>