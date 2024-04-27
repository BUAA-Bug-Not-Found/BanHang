<!-- 本文件是关注列表页面 -->

<!-- <template>
    <v-container>
        <v-card>
            <v-tabs v-model="tab" color="red darken-4" fixed-tabs>
                <v-tab value="one">我的关注</v-tab>
                <v-tab value="two">我的粉丝</v-tab>
            </v-tabs>
            <v-card-text>
                <v-window v-model="tab">
                        <v-window-item value="one">
                            <v-list>
                                    <v-list-item v-for="(star, index) in stars" :key="index">
                                            <div style="text-align: left;">
                                                <v-avatar size="30" style="margin-top: 10px;">
                                                    <img src='../../assets/nr/headImage.jpg' alt="Avatar">
                                                </v-avatar>
                                            </div>
                                            <span>12312</span>
                                            <divider></divider>
                                    </v-list-item>
                            </v-list>
                        </v-window-item>
                </v-window>
            </v-card-text>
        </v-card>

        <v-window v-model="tab">
            <v-window-item value="two">
            </v-window-item>
        </v-window>

    </v-container>

</template> -->
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
                <v-list-item v-for="(content, index) in stars" :key="index" @click="clickItem">
                  <div style="text-align: left; vertical-align: middle; margin-top: 10px; margin-left: 10px;">
                    <v-avatar size="30">
                        <img src="../../assets/nr/headImage.jpg" alt="Avatar">
                    </v-avatar>
                    <span style="font-weight: bold; margin-left: 10px;">{{ content.nickname }}</span>
                    <v-spacer></v-spacer>
                </div>
                  <v-divider style="margin-top: 10px;"></v-divider>
                </v-list-item>
              </v-list>
            </v-window-item>
            
            <v-window-item value="two">
                <v-list>
                    <v-list-item v-for="(content, index) in fans" :key="index" @click="clickItem">
                    <div style="text-align: left; vertical-align: middle; margin-top: 10px; margin-left: 10px;">
                        <v-avatar size="30">
                            <img src="../../assets/nr/headImage.jpg" alt="Avatar">
                        </v-avatar>
                        <span style="font-weight: bold; margin-left: 10px;">{{ content.nickname }}</span>
                        <v-spacer></v-spacer>
                    </div>
                    <v-divider style="margin-top: 10px;"></v-divider>
                    </v-list-item>
                </v-list>
            </v-window-item>
          </v-window>
        </v-card-text>


      </v-card>

      
      

    </v-container>
  </template>


<script>

export default {
    data() {
        return {
            tab: 'one',
            stars: [
                {
                    'headImage': '../../assets/nr/headImage.jpg',
                    'nickname': 'Goths'
                },
                {
                    'headImage': '../../assets/nr/headImage.jpg',
                    'nickname': 'Goths'
                },
                {
                    'headImage': '../../assets/nr/headImage.jpg',
                    'nickname': 'Goths'
                }

            ],
            fans: [
                {
                    'headImage': '',
                    'nickname': 'Goths'
                }
            ]
        }
    },
    methods: {

    }
}
</script>

<style scoped>



</style>