<script>
import {ref} from "vue";
import {getAnsById, setAnsLikeAPI} from "@/components/HelpCenter/api";
import UserStateStore from "@/store";
import {ElMessage} from "element-plus";

export default {
  name: "AnsCard",
  props: ["ansId", "index"],
  setup(props) {

    const init = () => {
      getAnsById(props.ansId).then(
          (res) => {
            ans.value = res.answer
            userLike.value = res.answer.ifUserLike
            likeSum.value = res.answer.likeSum
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

    return {
      ans,
      ansIdRef,
      setAnsLike,
      userLike,
      likeSum
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
        <v-col cols="1">
          <v-avatar color="surface-variant" style="margin: 10px;" size="40"/>
        </v-col>
        <v-col cols="10">
          <div style="display: flex; justify-content: space-between;margin-top: 10px">
            <span style="font-size: 15px">{{ ans.userName }}</span>
            <span style="font-size: 12px;color: gray">回答于{{ ans.ansTime }}</span>
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
                :prepend-icon="'mdi-reply'" variant="text" size="small"
                color="blue-grey-lighten-2">
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-card>
  </div>

</template>

<style scoped>

</style>