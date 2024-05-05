<script>
import {ref} from "vue";
import {delAnswerAPI, formatDate, getAnsById, setAnsLikeAPI} from "@/components/HelpCenter/api";
import UserStateStore from "@/store";
import {ElMessage} from "element-plus";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";

export default {
  name: "AnsCard",
  methods: {formatDate},
  components: {UserAvatar},
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

    return {
      ans,
      ansIdRef,
      setAnsLike,
      userLike,
      likeSum,
      delDialog,
      isUser,
      delAnswer
    };
  },
};
</script>

<template>
  <div v-if="ans !== null">
    <v-divider
        v-if="index !== 0"
        color="light-blue-darken-3"
        style="margin-top: 5px;margin-bottom: 5px"
    ></v-divider>
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
<!--            <v-btn-->
<!--                :prepend-icon="'mdi-reply'" variant="text" size="small"-->
<!--                color="blue-grey-lighten-2">-->
<!--            </v-btn>-->
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
        </v-col>
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