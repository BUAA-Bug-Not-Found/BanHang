<template>
    <v-container>
      
      <v-card>
        <v-tabs
          v-model="tab"
          color="blue"
          fixed-tabs
        >
          <v-tab value="one">我的关注</v-tab>
          <v-tab value="two">我的粉丝</v-tab>
        </v-tabs>
        
        <v-card-text>
          <v-window v-model="tab">
            <v-window-item value="one">
              <v-list>
                <UserShow
                  v-for="(post, index) in this.stars"
                  :key="index"
                  :nickname="post.nickname"
                  :sign="post.sign"
                  :id="post.id"
                  :headImage="post.headUrl"
                />
              </v-list>
            </v-window-item>
            
            <v-window-item value="two">
                <v-list>
                  <UserShow
                    v-for="(post, index) in this.fans"
                    :key="index"
                    :nickname="post.nickname"
                    :sign="post.sign"
                    :id="post.id"
                    :headImage="post.headUrl"
                  />
                </v-list>
            </v-window-item>
          </v-window>
        </v-card-text>
      </v-card>
    </v-container>
  </template>


<script>
import userStateStore from '../../store';

import router from '@/router';

import { getStars, getFans } from './PersonalCenterAPI';

import UserShow from "@/components/PersonalCenter/UserShow.vue";
import { checkLogin } from '../AccountManagement/AccountManagementAPI';

export default {
    components: {UserShow},
    created() {
      checkLogin();
        // 拿到stars和fans列表
        getStars(userStateStore().user_id).then((res) => {
            this.stars = res.stars
        })
        getFans(userStateStore().user_id).then((res) => {
            this.fans = res.fans
        })
    },
    data() {
        return {
            tab: 'one',
            stars: [
            ],
            fans: [
            ]
        }
    },
    methods: {
        clickOtherUser(_id) {
            // 展示_email对应的用户的首页
            // 传名的话, 就只有名, 而不要表示路径分隔的斜杠了
            router.push({name: "othersCenter", params: {"id": _id}})
        }
    }
}
</script>

<style scoped>


</style>