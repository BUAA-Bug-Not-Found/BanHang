<template>
    <!--电脑-->
    <v-container style="width: 70%;margin-top: 10px;" v-if="!display.smAndDown.valueOf()">
        <v-card v-for="(post, index) in this.toolList" :key="index" @click="clickToolItem(index)" style="
         /* background-color: #c7e3b2; */
         height: 70px;
         margin-top: 10px;
         margin-left: 10px;
         margin-right: 10px;">
            <v-row>
                <!-- <v-avatar color="surface-variant"
                        style="margin-top: 20px;margin-left: 25px; cursor: pointer;"
                        size="50"
                        :image=post.toolLogo
                        @click="clickToolItem(index)">
                    </v-avatar> -->
                <img :src="post.toolLogo"
                    style="width:45px; height: 45px; margin-top: 20px; margin-left: 25px; cursor: pointer;">
                <v-col style="text-align: left; margin-top: 10px;">
                    <span style="font-weight: bold; margin-left: 0px; font-size: 15px;">{{ post.toolName }}</span><br />
                    <span style="color: grey; margin-left: 0px; font-size: 12px;">{{ post.toolDesc }}</span>
                </v-col>
            </v-row>
        </v-card>
    </v-container>
    <!--手机-->
    <div v-else>
        <v-card v-for="(post, index) in this.toolList" :key="index" @click="clickToolItem(index)" style="
         /* background-color: #c7e3b2; */
         height: 70px;
         border-top: 10px;
         border-radius: 0px;
         margin-bottom: 1px;"
         variant="flat">
         <div style="height: 1px;  background-color: lightgrey"></div>

            <v-row>
                <!-- <v-avatar color="surface-variant"
                        style="margin-top: 20px;margin-left: 25px; cursor: pointer;"
                        size="50"
                        :image=post.toolLogo
                        @click="clickToolItem(index)">
                    </v-avatar> -->
                <img :src="post.toolLogo"
                    style="width:45px; height: 45px; margin-top: 20px; margin-left: 25px; cursor: pointer;">
                <v-col style="text-align: left; margin-top: 10px;">
                    <span style="font-weight: bold; margin-left: 0px; font-size: 15px;">{{ post.toolName }}</span><br />
                    <span style="color: grey; margin-left: 0px; font-size: 12px;">{{ post.toolDesc }}</span>
                </v-col>
            </v-row>
        </v-card>
        <div style="height: 1px;  background-color: lightgrey"></div>

    </div>
</template>

<script>
import router from '@/router';
import { useDisplay } from 'vuetify'

export default {
    name: 'ToolCenter',
    // components: {ToolItem},
    created() {
        console.log("我的ToolItem呢?")
    },
    data() {
        return {
            toolList: [
                {
                    toolName: "SPOC作业提醒",
                    toolDesc: "妈妈再也不用担心我忘记作业ddl了!!",
                    toolLogo: "https://banhang.oss.chlience.com/14/avatar/4ed4688f2ba74049a0f986936b10e67b.png",
                    toolRouteName: "spoc"
                },
                {
                    toolName: "博雅课程提醒",
                    toolDesc: "让您设置个性化博雅提醒~",
                    toolLogo: "https://banhang.oss.chlience.com/14/avatar/9d35aaa0948f49f08cf69d675c5acce1.png",
                    toolRouteName: ""
                },
                {
                    toolName: "通识课宝典",
                    toolDesc: "为您的选课质量保驾护航",
                    toolLogo: "https://banhang.oss.chlience.com/14/avatar/eb8fe133911442848e4c169e94ef3c2d.png",
                    toolRouteName: ""
                },
                {
                    toolName: "空教室查询(魔改版)",
                    toolDesc: "横扫苦苦寻找的烦恼！",
                    toolLogo: "https://banhang.oss.chlience.com/14/avatar/3e902d793655453d9289e676cc9842dd.png",
                    toolRouteName: "vacentClassroom"
                }
            ],
            display:useDisplay()
        };
    },
    methods: {
        clickToolItem(i) {
            router.push({ name: this.toolList[i].toolRouteName })
        }
    },
};
</script>

<style scoped></style>
