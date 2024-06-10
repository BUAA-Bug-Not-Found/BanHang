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
            <v-row style="margin: 1px">
              <v-tooltip v-for="badge in badges" :key="badge.badgeId" :text="badge.badgeDesc">
                <template v-slot:activator="{ props }">
                  <v-chip
                      size="x-small"
                      class="ma-2"
                      :style="{ color: badge.badgeColor }"
                      label
                      v-bind="props"
                  >
                    {{ badge.badgeName }}
                  </v-chip>
                </template>
              </v-tooltip>
            </v-row>

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
import {getBadgesByUserId} from "@/components/PersonalCenter/PersonalCenterAPI";

export default {
  name: "UserAvatar",
  emits: ['returnUserName'],
  props: ["userId", "size"],
  setup(props, context) {
    const nickname = ref('')

    const sign = ref('')

    const url = ref('')

    // const email = ref('')

    const goHomePage = () => {
      if(props.userId !== UserStateStore.getUserId) {
        // router.push('/othersCenter/' + email.value)
        router.push('/othersCenter/' + props.userId)
      } else {
        router.push("/personalCenter")
      }
    }

    const badges = ref([])
    const init = () => {
      getInfoByUserIdAPI(props.userId).then(
          (res) => {
            // email.value = res.email
            nickname.value = res.nickname
            url.value = res.url
            sign.value = res.sign
            context.emit('returnUserName', nickname.value)
          }
      )
      getBadgesByUserId(props.userId).then(
          (res) => {
            if(res) {
              badges.value = res
            }
          }
      )
    }

    init()

    return {
      nickname,
      sign,
      url,
      goHomePage,
      badges
    }
  }
}
</script>

<style scoped>

</style>