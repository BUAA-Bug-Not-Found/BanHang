<template>
    <v-container>
      
      <v-card>
        <v-tabs
          v-model="tab"
          color="red darken-4"
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
                  :email="post.email"
                  :headImage="post.headUrl"
                />
                <!-- <v-list-item v-for="(content, index) in stars" :key="index">
                  <div style="text-align: left; vertical-align: middle; margin-top: 10px; margin-left: 10px;">
                    <v-avatar size="30" @click="clickOtherUser(content.email)" style="cursor: pointer;">
                        <img :src="content.headUrl" alt="Avatar">
                    </v-avatar>
                    <span style="font-weight: bold; margin-left: 10px;">{{ content.nickname }}</span>
                    <v-spacer></v-spacer>
                </div>
                  <v-divider style="margin-top: 10px;"></v-divider>
                </v-list-item> -->
              </v-list>
            </v-window-item>
            
            <v-window-item value="two">
                <v-list>
                  <UserShow
                    v-for="(post, index) in this.fans"
                    :key="index"
                    :nickname="post.nickname"
                    :sign="post.sign"
                    :email="post.email"
                    :headImage="post.headUrl"
                  />

                    <!-- <v-list-item v-for="(content, index) in fans" :key="index">
                    <div style="text-align: left; vertical-align: middle; margin-top: 10px; margin-left: 10px;">
                        <v-avatar size="30" @click="clickOtherUser(content.email)" style="cursor: pointer;">
                            <img :src="content.headUrl" alt="Avatar">
                        </v-avatar>
                        <span style="font-weight: bold; margin-left: 10px;">{{ content.nickname }}</span>
                        <v-spacer></v-spacer>
                    </div>
                    <v-divider style="margin-top: 10px;"></v-divider>
                    </v-list-item> -->
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
        getStars(userStateStore().email).then((res) => {
            // this.stars.concat(res.stars)
            this.stars = res.stars
            console.log("res.stars -> ")
            console.log(res.stars)
            // this.stars = this.stars.concat(res.map(star => ({
            //   headUrl: star.headUrl,
            //   nickname: star.nickname,
            //   email: star.email,
            //   sign: "这是写死的签名, 等待后端返回"
            // })));
        })

        // this.stars.concat([
        //   {
        //     'headUrl': '../../assets/nr/headImage.jpg',
        //     'nickname': 'Goths',
        //     'email': "123"
        //   },
        //   {
        //     'headUrl': '../../assets/nr/headImage.jpg',
        //     'nickname': 'Goths',
        //     'email': "123"
        //   }
        // ])
        getFans(userStateStore().email).then((res) => {
            this.fans = res
        })
        // this.fans.concat([
        //   {
        //     'headUrl': '../../assets/nr/headImage.jpg',
        //     'nickname': 'Goths',
        //     'email': "123"
        //   },
        //   {
        //     'headUrl': '../../assets/nr/headImage.jpg',
        //     'nickname': 'Goths',
        //     'email': "123"
        //   },
        //   {
        //     'headUrl': '../../assets/nr/headImage.jpg',
        //     'nickname': 'Goths',
        //     'email': "123"
        //   }
        // ])
    },
    data() {
        return {
            tab: 'one',
            stars: [
                // {
                //     'headUrl': '../../assets/nr/headImage.jpg',
                //     'nickname': 'Goths',
                //     'email': "123"
                // }

                // {
                //     'headUrl': '',
                //     'nickname': 'Goths',
                //     "email": "232323",
                //     "sign": "签名"
                // },
                // {
                //   'headUrl': '../../assets/nr/headImage.jpg',
                //   'nickname': 'Goths',
                //   'email': "123",
                //   "sign": "签名"
                // }
            ],
            fans: [
                // {
                //     'headUrl': '',
                //     'nickname': 'Goths',
                //     "email": "232323",
                //   "sign": "签名"

                // },
                // {
                //   'headUrl': '../../assets/nr/headImage.jpg',
                //   'nickname': 'Goths',
                //   'email': "123",
                //   "sign": "签名"

                // }
            ]
        }
    },
    methods: {
        clickOtherUser(_email) {
            // 展示_email对应的用户的首页
            // console.log("跳转-> ")
            // 传名的话, 就只有名, 而不要表示路径分隔的斜杠了
            router.push({name: "othersCenter", params: {"e": _email}})
        }
    }
}
</script>

<style scoped>



</style>