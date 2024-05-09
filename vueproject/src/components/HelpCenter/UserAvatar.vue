<template>
    <v-menu rounded>
      <template v-slot:activator="{ props }">
          <v-avatar v-bind="props" style="margin-top:8px">
            <v-img :src="url"></v-img>
          </v-avatar>
      </template>
      <v-card>
        <v-card-text>
          <div class="mx-auto text-center">
            <v-avatar>
              <v-img :src="url"></v-img>
            </v-avatar>
            <h3>{{ nickname }}</h3>
            <p class="text-caption mt-1">
              {{ sign }}
            </p>
            <v-divider class="my-3"></v-divider>
            <v-btn
                variant="text"
                rounded
                density="compact"
                @click="goHomePage"
            >
              前往主页
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-menu>
</template>

<script>

import {getInfoByUserIdAPI} from "@/components/HelpCenter/api";
import {ref} from "vue";
import UserStateStore from "@/store";
import router from "@/router";

export default {
  name: "UserAvatar",
  props: ["userId"],
  setup(props) {
    const nickname = ref('')

    const sign = ref('')

    const url = ref('')

    const email = ref('')

    const goHomePage = () => {
      if(props.userId !== UserStateStore.getUserId) {
        // router.push('/othersCenter/' + email.value)
        router.push('/othersCenter/' + props.userId)
      } else {
        router.push("/personalCenter")
      }
    }

    const init = () => {
      getInfoByUserIdAPI(props.userId).then(
          (res) => {
            email.value = res.email
            nickname.value = res.nickname
            url.value = res.url
            sign.value = res.sign
          }
      )
    }
    init()

    return {
      nickname,
      sign,
      url,
      goHomePage
    }
  }
}
</script>

<style scoped>

</style>