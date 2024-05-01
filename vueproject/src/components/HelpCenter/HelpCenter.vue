<script>
import {
  getQuestionsApi,
  getQuestionsByTagIdApi,
  getTagsApi,
  uploadFileApi,
  uploadQuesApi
} from "@/components/HelpCenter/api";
import '@wangeditor/editor/dist/css/style.css'
import {onBeforeUnmount, ref, shallowRef} from "vue";
import QuesCard from "@/components/HelpCenter/QuesCard.vue";
import {Editor, Toolbar} from "@wangeditor/editor-for-vue";
import {useDisplay} from "vuetify";
import AppQuesCard from "@/components/HelpCenter/AppQuesCard.vue";
import {ElMessage} from "element-plus";
import router from "@/router";
import {Plus} from "@element-plus/icons-vue";

export default {
  name: "HelpCenter",
  components: {Plus, AppQuesCard, Editor, Toolbar, QuesCard},
  setup() {
    const page = ref(0)
    const pageSize = ref(10)
    const quesSum = ref(4)
    const valueHtml = ref('')
    const editorRef = shallowRef()
    const sheet = ref(false)

    const toolbarConfig = {}
    const editorConfig = {placeholder: '请输入内容...'}

    const imageList = ref([])

    const selectTags = ref([])

    const tags = ref([])

    const tagNamesArray = ref([])

    const lastIndex = ref(0)

    const questions = ref([])

    const getMore = () => {
      page.value = page.value + 1
      if (lastIndex.value !== 0) {
        getQuestionsByTagIdApi(page.value, pageSize.value, tags.value[lastIndex.value].tagId).then(
            (data) => {
              quesSum.value = data.quesSum
              questions.value = questions.value.concat(data.questions)
              console.log(questions.value)
              console.log(quesSum.value)
            }
        )
      } else {
        getQuestionsApi(page.value, pageSize.value).then(
            (data) => {
              quesSum.value = data.quesSum
              questions.value = questions.value.concat(data.questions)
            }
        )
      }
    }

    const init = () => {
      getMore()
      getTagsApi().then(
          (data) => {
            tags.value = data.tags
            tags.value.unshift({
              tagId: 0,
              tagName: "全部",
              tagIcon: 'mdi-home-circle',
              tagColor: 'indigo-lighten-4',
            })
            for (let i = 0; i < tags.value.length; i++) {
              tagNamesArray.value.push(tags.value[i].tagName)
            }
          }
      )
    }

    init()

    const shiftIndex = (index) => {
      if (index !== lastIndex.value) {
        page.value = 0
        lastIndex.value = index
        questions.value = []
        getMore()
      }
    }

    onBeforeUnmount(() => {
      const editor = editorRef.value
      if (editor == null) return
      editor.destroy()
    })

    const handleCreated = (editor) => {
      editorRef.value = editor // 记录 editor 实例，重要！
    }

    const handleChange = (file) => {
      if (file.raw.type !== "image/jpeg" && file.raw.type !== "image/png") {
        ElMessage.error('Avatar picture must be JPG format!');
        return false;
      }
      uploadFileApi(file).then((res) => {
        if (res.response === 'success') {
          ElMessage.success("Avatar picture upload succeeded!")
          imageList.value.push(res.fileUrl)
        } else {
          ElMessage.error('Avatar picture upload failed!');
        }
      })
      return true;
    }

    const deleteImage = (index) => {
      imageList.value.splice(index, 1);
    }

    const uploadQuestion = () => {
      if (String(valueHtml.value).replace(/<[^>]*>/g, "") === '') {
        ElMessage.error('问题内容不得为空');
      } else {
        uploadQuesApi(valueHtml.value, imageList.value, selectTags.value).then(
            (res) => {
              console.log(res.isSuccess)
              if (res.isSuccess === true) {
                ElMessage.success('问题发布成功');
                router.go(0)
              } else {
                ElMessage.error('发布失败，请重新尝试');
              }
            }
        )
      }
    }

    const display = useDisplay()

    const findTagColor = (index) => {
      return tags.value[index + 1].tagColor
    }

    const findTagIcon = (index) => {
      return tags.value[index + 1].tagIcon
    }

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
      valueHtml,
      handleCreated,
      sheet,
      selectTags,
      tagNamesArray,
      display,
      imageList,
      handleChange,
      deleteImage,
      uploadQuestion,
      shiftIndex,
      findTagColor,
      findTagIcon
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
              @click="shiftIndex(i)"
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
    <v-col cols="12" style="margin-bottom: 25px">
      <AppQuesCard style="margin-bottom: 5px" v-for="(ques, index) in questions" :key="ques.quesId"
                   :question="questions[index]" :tags="tags"/>
      <v-btn v-if="questions.length < quesSum" color="light-blue-darken-1" style="margin-top: 5px" @click="getMore">
        加载更多
      </v-btn>
    </v-col>
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
            <v-btn variant="text" @click="uploadQuestion">
              发布
            </v-btn>
            <v-btn variant="text" @click="sheet = !sheet">
              close
            </v-btn>
          </v-col>
        </v-row>
        <v-row justify="space-around">
          <v-col v-for="(image,index) in imageList" :key="'image' + index" :cols="3" style="margin-right: 15px">
            <img :src="image" class="avatar">
          </v-col>
          <v-col>
            <el-form>
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
              v-model="selectTags"
              :items="tagNamesArray.length  === 0 ? [] : tagNamesArray.slice(1, tagNamesArray.length)"
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
              v-model="valueHtml"
              :defaultConfig="editorConfig"
              :mode="mode"
              @onCreated="handleCreated"
          />
          <Toolbar
              style="border-bottom: 1px solid #ccc"
              :editor="editorRef"
              :defaultConfig="toolbarConfig"
              :mode="mode"
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

.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>