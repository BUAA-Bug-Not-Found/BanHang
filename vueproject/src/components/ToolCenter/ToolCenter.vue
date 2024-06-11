<template>
    <!--电脑-->
    <v-container style="width: 70%;margin-top: 10px;" v-if="!display.smAndDown.valueOf()">
        <v-dialog v-model="showAddCourseDialog" style="max-width: 400px;">
            <v-card>
                <v-card-title class="headline" style="text-align: center;">申请加课</v-card-title>
                <div style="text-align:center;">
                    <span style="color:grey; font-size: 12px;">描述清楚课程以下三方面特性, 管理员审核通过后会加上该课程</span>
                </div>
                <v-divider></v-divider>
                <div style="margin-top: 20px; padding-left: 10px; padding-right: 10px;">
                    <v-text-field
                        v-model="addCourseSchool"
                        label="开课院系"
                        outlined
                    ></v-text-field>
                    <v-text-field
                        v-model="addCourseType"
                        label="课程类型"
                        outlined
                    ></v-text-field>
                    <v-text-field
                        v-model="addCourseName"
                        label="课程名称"
                        outlined
                    ></v-text-field>
                </div>
                <div style="text-align: center; margin-top: 10px;">
                    <v-btn color="blue darken-1" @click="clickCertainAddCourse" style="margin-bottom: 10px; max-width: 50%;">提交</v-btn>
                    <v-btn color="blue darken-1" @click="showAddCourseDialog = false" style="margin-left: 7px; margin-bottom: 10px; max-width: 50%;">取消</v-btn>
                </div>
            </v-card>
        </v-dialog>

        <v-card v-for="(post, index) in this.toolList" :key="index" @click="clickToolItem(index)" style="
         height: 70px;
         margin-top: 10px;
         margin-left: 10px;
         margin-right: 10px;">
            <v-row>
                <img :src="post.toolLogo"
                    style="width:45px; height: 45px; margin-top: 20px; margin-left: 25px; cursor: pointer;">
                <v-col style="text-align: left; margin-top: 10px;">
                    <span style="font-weight: bold; margin-left: 0px; font-size: 15px;">{{ post.toolName }}</span><br />
                    <span style="color: grey; margin-left: 0px; font-size: 12px;">{{ post.toolDesc }}</span>
                </v-col>
                <v-col v-if="index === 2" style="display: flex; align-items: center; justify-content: end;">
                    <v-btn style="color:deepskyblue; margin-right: 10px;" icon="mdi-plus" variant="text" @click.stop="clickAddCourse"></v-btn>
                </v-col>
            </v-row>
        </v-card>
    </v-container>
    <!--手机-->
    <div v-else>

        <v-dialog v-model="showAddCourseDialog" style="max-width: 400px;">
            <v-card>
                <v-card-title class="headline" style="text-align: center;">申请加课</v-card-title>
                <div style="text-align:center;">
                    <span style="color:grey; font-size: 12px;">描述清楚课程以下三方面信息, 管理员审核通过后会加上该课程</span>
                </div>
                <v-divider></v-divider>
                <div style="margin-top: 20px; padding-left: 10px; padding-right: 10px;">
                    <v-text-field
                        v-model="addCourseSchool"
                        label="开课院系"
                        outlined
                    ></v-text-field>
                    <v-text-field
                        v-model="addCourseType"
                        label="课程类型"
                        outlined
                    ></v-text-field>
                    <v-text-field
                        v-model="addCourseName"
                        label="课程名称"
                        outlined
                    ></v-text-field>
                </div>
                <div style="text-align: center; margin-top: 10px;">
                    <v-btn color="blue darken-1" @click="clickCertainAddCourse" style="margin-bottom: 10px; max-width: 50%;">提交</v-btn>
                    <v-btn color="blue darken-1" @click="showAddCourseDialog = false" style="margin-left: 7px; margin-bottom: 10px; max-width: 50%;">取消</v-btn>
                </div>
            </v-card>
        </v-dialog>
        <v-card v-for="(post, index) in this.toolList" :key="index" @click="clickToolItem(index)" style="
         /* height: 70px; */
         min-height: 70px;
         border-top: 10px;
         border-radius: 0px;
         margin-bottom: 1px;"
         variant="flat">
         <div style="height: 1px;  background-color: lightgrey"></div>
            <v-row>
                <img :src="post.toolLogo"
                    style="width:45px; height: 45px; margin-top: 20px; margin-left: 25px; cursor: pointer;">
                <v-col style="text-align: left; margin-top: 10px;">
                    <span style="font-weight: bold; margin-left: 0px; font-size: 15px;">{{ post.toolName }}</span><br />
                    <span style="color: grey; margin-left: 0px; font-size: 12px;">{{ post.toolDesc }}</span>
                </v-col>
                <v-col v-if="index === 2" style="display: flex; align-items: center; justify-content: end;">
                    <v-btn style="color:deepskyblue; margin-right: 10px;" icon="mdi-plus" variant="text" @click.stop="clickAddCourse"></v-btn>
                </v-col>
            </v-row>
        </v-card>
        <div style="height: 1px;  background-color: lightgrey"></div>
    </div>
</template>

<script>
import router from '@/router';
import { useDisplay } from 'vuetify'
import { showTip } from '../AccountManagement/AccountManagementAPI';

export default {
    name: 'ToolCenter',
    created() {
        console.log("我的ToolItem呢?")
    },
    data() {
        return {
            showAddCourseDialog: false,
            addCourseName: "",
            addCourseSchool: "",
            addCourseType: "",
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
                    toolRouteName: "boya"
                },
                {
                   toolName: "课程评价宝典",
                   toolDesc: "为您的选课质量保驾护航",
                   toolLogo: "https://banhang.oss.chlience.com/14/avatar/eb8fe133911442848e4c169e94ef3c2d.png",
                   toolRouteName: ["HelpCenter/11", 11]
                },
                {
                    toolName: "自习教室查询",
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
            if (i == 2)
                router.push("/HelpCenter/11")
            else router.push({ name: this.toolList[i].toolRouteName })
        },
        clickAddCourse() {
            this.showAddCourseDialog = true
            this.addCourseName = ""
            this.addCourseSchool = ""
            this.addCourseType = ""
        },
        clickCertainAddCourse() {
            if (this.addCourseName === "" || this.addCourseSchool === "" || this.addCourseType === "") {
                showTip("请保证信息填写完整", false)
                this.showAddCourseDialog = false
            } else {
                showTip("提交成功, 请等待审核", true)
                this.showAddCourseDialog = false
            }
        }
    },
};
</script>

<style scoped></style>
