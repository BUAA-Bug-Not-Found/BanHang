<script>
import {ref, onMounted, onBeforeUnmount} from "vue";
import router from "@/router";
import {setLikeQuesApi} from "@/components/HelpCenter/api";
import UserStateStore from "@/store"
import {ElMessage} from "element-plus";
import UserAvatar from "@/components/HelpCenter/UserAvatar.vue";

export default {
  name: "QuesCard",
  components: {UserAvatar},
  props: ["question", "tags"],
  emits: ["editQues"],
  setup(props) {
    const truncate = (content) => {
      console.log(content)
      const strippedContent = String(content).replace(/<[^>]*>/g, "")
      if (strippedContent.length > 20) {
        return `${strippedContent.slice(0, 20)}...`;
      }
      return strippedContent;
    };

    const disTags = ref([])

    const userLike = ref(props.question.ifUserLike)
    const likeSum = ref(props.question.likeSum)

    const init = () => {
      for (let i = 0; i < props.question.tagIdList.length; i++) {
        for (let j = 0; j < props.tags.length; j++) {
          if (props.tags[j].tagId === props.question.tagIdList[i]) {
            disTags.value.push(props.tags[j])
          }
        }
      }
      console.log(userLike.value)
    }

    init()

    const menuClick = ref(false);

    function handleClickOutside(event) {
      if (!event.composedPath().includes(this.$el)) {
        menuClick.value = false;
      }
    }

    onMounted(() => {
      document.addEventListener("click", handleClickOutside);
    });

    onBeforeUnmount(() => {
      document.removeEventListener("click", handleClickOutside);
    });

    const goto = () => {
      router.push("/QuesInfo/" + props.question.quesId);
    }

    const setLikeQues = () => {
      const state = UserStateStore()
      if(!state.email) {
        ElMessage.error("请先登录")
      } else {
        setLikeQuesApi(props.question.quesId, userLike.value ? 0 : 1).then(
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

    const editQues = () => {

    }

    const delQues = () => {

    }


    return {
      truncate,
      menuClick,
      disTags,
      goto,
      setLikeQues,
      userLike,
      likeSum,
      delQues,
      editQues
    };
  },
};
</script>

<template>
  <v-hover v-slot="{ isHovering, props }">
    <v-card
        class="mx-auto"
        style="width: 90%"
        :color="isHovering ? 'cyan-lighten-5' : undefined"
        v-bind="props"
    >
      <v-row>
        <v-col cols="2">
          <div style="display:flex; justify-content: end;align-content: center">
            <UserAvatar :userId="question.userId"></UserAvatar>
          </div>
        </v-col>
        <v-col cols="7" style="text-align: left;" :class="`cursor-pointer`" @click="goto()">
          <div style="margin-top: 10px;">
            {{ truncate(question.quesContent.content) }}
          </div>
          <div style="font-size: 12px;color: grey;margin-bottom: 5px">
            {{ question.userName }}发表于{{ question.quesTime }}
          </div>
        </v-col>
        <v-col cols="3" style="text-align: left;margin-top: 3px">
          <div>
            <v-btn :prepend-icon=" !userLike ?
                  'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text" size="small"
                   color="blue-grey-lighten-2" @click="setLikeQues">
              {{ likeSum }}
            </v-btn>
            <v-btn variant="text" prepend-icon="mdi-reply" size="small" color="blue-grey-lighten-2">
              {{ question.ansSum }}
            </v-btn>
            <v-menu v-show="isHovering || menuClick" :location="'bottom'">
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
                <v-list-item density="compact" @click="delQues">
                  删除
                </v-list-item>
                <v-list-item @click="editQues">
                  修改
                </v-list-item>
                <v-list-item>
                  举报
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
          <div style="margin-bottom: 10px">
            <v-chip v-for="tag in disTags" size="x-small" :key="question.quesId + '-' + tag.tagId"
                    :color="tag.tagColor">
              <v-icon>{{ tag.tagIcon }}</v-icon>
              {{ tag.tagName }}
            </v-chip>
          </div>
        </v-col>
      </v-row>
    </v-card>
  </v-hover>

  <v-dialog>

  </v-dialog>
</template>

<style scoped>

</style>