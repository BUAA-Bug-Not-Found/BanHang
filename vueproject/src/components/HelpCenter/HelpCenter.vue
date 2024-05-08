<script>
import {
  getQuestionsApi,
  getQuestionsByTagIdApi,
  getTagsApi,
  uploadFileApi,
  uploadQuesApi,
  updateQuesApi
} from "@/components/HelpCenter/api";
import '@wangeditor/editor/dist/css/style.css'
import {onBeforeUnmount, ref, shallowRef} from "vue";
import QuesCard from "@/components/HelpCenter/QuesCard.vue";
import {Editor, Toolbar} from "@wangeditor/editor-for-vue";
import {useDisplay} from "vuetify";
import AppQuesCard from "@/components/HelpCenter/AppQuesCard.vue";
import {ElMessage} from "element-plus";
import {Plus} from "@element-plus/icons-vue";
import userStateStore from "../../store";
import router from "@/router";
import {api as viewerApi} from 'v-viewer'
import {useRouter} from "vue-router";

export default {
  name: "HelpCenter",
  methods: {userStateStore},
  components: {Plus, AppQuesCard, Editor, Toolbar, QuesCard},
  setup() {
    const page = ref(0)
    const pageSize = ref(10)
    const quesSum = ref(4)
    const valueHtml = ref('')
    const editorRef = shallowRef()
    const sheet = ref(false)

    const toolbarConfig = {
      excludeKeys: [
        'fullScreen', 'group-image', 'group-video'
      ],
    }

    const editorConfig = {placeholder: '请输入问题内容...'}

    const imageList = ref([])

    const selectTags = ref([])

    const tags = ref([])

    const tagNamesArray = ref([])

    const lastIndex = ref(0)

    const questions = ref([])

    const reviseMode = ref(false)

    const reviseHtml = ref('')

    const reviseImgList = ref([])

    const reviseTagList = ref([])

    const lockMore = ref(false)

    const getMore = () => {
      if(lockMore.value === false) {
        lockMore.value = true
        page.value = page.value + 1
        if (lastIndex.value != 0) {
          getQuestionsByTagIdApi(page.value, pageSize.value, tags.value[lastIndex.value].tagId).then(
              (data) => {
                let ori_len = questions.value.length
                quesSum.value = data.quesSum
                questions.value = questions.value.concat(data.questions)
                for (let i = ori_len; i < questions.value.length; i++) {
                  disTags.value.push([])
                  calTags(i)
                }
              }
          )
        } else {
          getQuestionsApi(page.value, pageSize.value).then(
              (data) => {
                let ori_len = questions.value.length
                quesSum.value = data.quesSum
                questions.value = questions.value.concat(data.questions)
                for (let i = ori_len; i < questions.value.length; i++) {
                  disTags.value.push([])
                  calTags(i)
                }
              }
          )
        }
        lockMore.value = false
      }
    }

    const init = () => {
      let router = useRouter()
      lastIndex.value = router.currentRoute.value.params.tagId
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
            getMore()
          }
      )
    }

    init()

    const shiftIndex = (index) => {
      if (index !== lastIndex.value) {
        page.value = 0
        lastIndex.value = index
        questions.value = []
        disTags.value = []
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
      console.log(editor.getAllMenuKeys())
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

    const deleteImage = (index) => {
      imageList.value.splice(index, 1);
    }

    const uploadQuestion = () => {
      if (String(valueHtml.value).replace(/<[^>]*>/g, "") === '') {
        ElMessage.error('问题内容不得为空');
      } else {
        let uploadTags = []
        for (let i = 0; i < selectTags.value.length; i++) {
          for (let j = 0; j < tags.value.length; j++) {
            if (tags.value[j].tagName === selectTags.value[i]) {
              uploadTags.push(tags.value[j].tagId)
              break;
            }
          }
        }
        uploadQuesApi(valueHtml.value, imageList.value, uploadTags).then(
            (res) => {
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

    const findTagColor = (tagName) => {
      for(let i = 0;i < tags.value.length;i++) {
        if(tags.value[i].tagName === tagName) {
          return tags.value[i].tagColor
        }
      }
    }

    const findTagIcon = (tagName) => {
      for(let i = 0;i < tags.value.length;i++) {
        if(tags.value[i].tagName === tagName) {
          return tags.value[i].tagIcon
        }
      }
    }

    const recommendQues = ref([])

    const delQuestion = (id) => {
      questions.value.splice(id, 1)
    }

    const uploadHtml = ref("")
    const uploadImageList = ref([])
    const uploadTags = ref([])

    const editMode = ref(false)

    const editQuesIndex = ref()

    const toEditQues = (data) => {
      editMode.value = true
      editQuesIndex.value = data.index
      valueHtml.value = questions.value[data.index].quesContent.content
      imageList.value = questions.value[data.index].quesContent.imageList
      selectTags.value = []
      for (let i = 0; i < questions.value[data.index].tagIdList.length; i++) {
        for (let j = 0; j < tags.value.length; j++) {
          if (questions.value[data.index].tagIdList[i] === tags.value[j].tagId) {
            selectTags.value.push(tags.value[j].tagName)
            break
          }
        }
      }
      sheet.value = !sheet.value
    }

    const toUploadQues = () => {
      valueHtml.value = uploadHtml.value
      imageList.value = uploadImageList.value
      selectTags.value = uploadTags.value
      editMode.value = false
      sheet.value = !sheet.value
    }

    const editDialog = ref(false)

    const undoEdit = () => {
      valueHtml.value = ""
      imageList.value = []
      selectTags.value = []
      sheet.value = !sheet.value
      editDialog.value = false
    }

    const updateQuestion = () => {
      if (String(valueHtml.value).replace(/<[^>]*>/g, "") === '') {
        ElMessage.error('问题内容不得为空');
      } else {
        let uploadTags = []
        for (let i = 0; i < selectTags.value.length; i++) {
          for (let j = 0; j < tags.value.length; j++) {
            if (tags.value[j].tagName === selectTags.value[i]) {
              uploadTags.push(tags.value[j].tagId)
              break;
            }
          }
        }
        updateQuesApi(questions.value[editQuesIndex.value].quesId,
            valueHtml.value, imageList.value, uploadTags).then(
            (res) => {
              if (res.isSuccess === true) {
                ElMessage.success("成功修改问题")
                questions.value[editQuesIndex.value].quesContent.content = valueHtml.value
                questions.value[editQuesIndex.value].quesContent.imageList = imageList.value
                questions.value[editQuesIndex.value].tagIdList = uploadTags
                valueHtml.value = ""
                imageList.value = []
                selectTags.value = []
                sheet.value = !sheet.value
                calTags(editQuesIndex.value)
              } else {
                ElMessage.error("上传修改失败，请稍后再试")
              }
            }
        )
      }
    }

    const disTags = ref([])

    const calTags = (index) => {
      disTags.value[index] = []
      for (let i = 0; i < questions.value[index].tagIdList.length; i++) {
        for (let j = 0; j < tags.value.length; j++) {
          if (tags.value[j].tagId === questions.value[index].tagIdList[i]) {
            disTags.value[index].push(tags.value[j])
            break
          }
        }
      }
      disTags.value[index] = disTags.value[index].splice(0, 2)
    }

    const saveUpload = () => {
      sheet.value = !sheet.value
      uploadHtml.value = valueHtml.value
      uploadTags.value = selectTags.value
      uploadImageList.value = imageList.value
    }

    const showPic = (imgList) => {
      viewerApi({images: imgList})
    }

    const delPic = (index) => {
      imageList.value.splice(index, 1)
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
      findTagIcon,
      reviseMode,
      reviseHtml,
      reviseImgList,
      reviseTagList,
      recommendQues,
      delQuestion,
      toEditQues,
      toUploadQues,
      uploadTags,
      uploadHtml,
      uploadImageList,
      editMode,
      editDialog,
      undoEdit,
      saveUpload,
      updateQuestion,
      disTags,
      showPic,
      delPic
    }
  }
}
</script>

<template>
  <div v-if="!display.smAndDown.value">
    <v-row justify="center" style="margin-top: 10px">
      <v-col cols="2" style="margin-right: 10px">
        <v-list density="compact"
                :style="'position: fixed;top: 80px;width:200px;text-align:left'"
          >
          <v-btn @click="toUploadQues" color="blue-darken-1" class="w-100" :style="'margin-bottom: 15px'">
            发起问题
          </v-btn>
          <v-list-subheader>分区</v-list-subheader>
          <v-list-item
              v-for="(item, i) in tags"
              :key="i"
              :value="item"
              color="primary"
              :style="'text-align: left;'"
              @click="shiftIndex(i)"
          >
            <v-icon :icon="item.tagIcon" size="20" :color="item.tagColor"></v-icon>
            <span style="font-size: 13px;margin-left: 5px">
              {{ item.tagName }}
            </span>
          </v-list-item>
        </v-list>
      </v-col>
      <v-col cols="8" :style="'margin-bottom: 25px'">
        <QuesCard :style="'margin-bottom: 5px'" v-for="(ques, index) in questions" :key="ques.quesId"
                  :index="index"
                  @delQues="delQuestion"
                  @editQues="toEditQues"
                  :disTags="disTags[index]"
                  :question="questions[index]"/>
        <v-btn v-if="questions.length < quesSum" color="light-blue-darken-1" :style="'margin-top: 5px'" @click="getMore">
          加载更多
        </v-btn>
      </v-col>
      <v-col cols="2"></v-col>
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
      <AppQuesCard :style="'margin-bottom: 5px'" v-for="(ques, index) in questions" :key="ques.quesId"
                   :index="index"
                   :disTags="disTags[index]"
                   @delQues="delQuestion"
                   :question="questions[index]"
      />
      <v-btn v-if="questions.length < quesSum" color="light-blue-darken-1" :style="'margin-top: 5px'" @click="getMore">
        加载更多
      </v-btn>
      <div style="height: 200px;"></div>
  </div>
  <v-bottom-sheet v-model="sheet" inset :persistent="true">
    <v-card
        class="text-center"
        height="800"
    >
      <v-card-text>
        <v-row v-if="editMode === false" align="center" :style="'margin-bottom: 5px'">
          <v-col cols="4" offset="4">
            发布问题
          </v-col>
          <v-col cols="4">
            <v-btn variant="text" @click="uploadQuestion">
              发布
            </v-btn>
            <v-btn variant="text" @click="saveUpload">
              close
            </v-btn>
          </v-col>
        </v-row>
        <v-row v-else align="center" :style="'margin-bottom: 5px'">
          <v-col cols="4" offset="4">
            编辑问题
          </v-col>
          <v-col cols="4">
            <v-btn variant="text" @click="updateQuestion">
              发布
            </v-btn>
            <v-btn variant="text" @click="editDialog = !editDialog">
              close
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col v-for="(image, index) in imageList" :key="image" :cols="display.smAndDown.value? 4 : 3">
            <div class="avatar-wrapper">
              <div class="right-top">
                <v-btn @click="delPic(index)" density="compact" size="small" color="red-lighten-1" icon="mdi-close"></v-btn>
              </div>
              <el-image
                  class="avatar"
                  :src="image"
                  :fit="'cover'"
                  @click="showPic(imageList)"
              />
            </div>
          </v-col>
          <v-col :cols="display.smAndDown.value? 4 : 3">
            <el-form :style="'width: 100%'">
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
            <template v-slot:selection="{item}">
              <v-chip size="x-small" :color="findTagColor(item.title)">
                <v-icon>{{ findTagIcon(item.title) }}</v-icon>
                {{ item.title }}
              </v-chip>
            </template>
          </v-select>
        </div>

        <div style="border: 1px solid #ccc">
          <Toolbar
              :style="'border-bottom: 1px solid #ccc'"
              :editor="editorRef"
              :defaultConfig="toolbarConfig"
              :mode="mode"
          />
          <Editor
              :style="'height: 350px; overflow-y: hidden;'"
              v-model="valueHtml"
              :defaultConfig="editorConfig"
              :mode="mode"
              @onCreated="handleCreated"
          />
        </div>
        <div style="height: 50px"></div>
      </v-card-text>
    </v-card>
  </v-bottom-sheet>

  <v-dialog
      v-model="editDialog"
      width="auto"
  >
    <v-card
        max-width="400"
        min-width="200"
        prepend-icon="mdi-delete-clock"
        text="如若关闭，你的修改将不会被保存，你确认嘛？"
        title="修改问题"
    >
      <template v-slot:actions>
        <v-btn
            variant="flat"
            density="compact"
            text="确认"
            color="red-darken-1"
            @click="undoEdit"
        ></v-btn>
        <v-btn
            text="取消"
            density="compact"
            @click="editDialog = false"
        ></v-btn>
      </template>
    </v-card>
  </v-dialog>

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

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;

  overflow: hidden;
  height: 0;
  padding: 0;
  padding-bottom: 100%;
  width: 100%;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.avatar-wrapper {
  position: relative;
  width: 100%;
  height: 0;
  padding: 0;
  padding-bottom: 100%;
}

.right-top {
  position: absolute; /* 使用绝对定位 */
  top: -5%;
  right: -5%;
  z-index: 88888;
}

.avatar {
  position: absolute !important;
  top: 0;
  left: 0;
  cursor: pointer;

  overflow: hidden;
}

.el-icon.avatar-uploader-icon {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  font-size: 28px;
  color: #8c939d;
  width: 100%;
  height: 100%;
  text-align: center;
}
</style>