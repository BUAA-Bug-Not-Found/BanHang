<template>
    <!-- <p>dddddddddddddd</p> -->

    <div>
        <v-card> 
        <v-toolbar density="compact" style="background-color:aliceblue;">
            <v-btn icon @click="clickGoBack">
                <v-icon color="grey">mdi-arrow-left</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
        </v-toolbar>
        <div style="margin-top: 10px;">
            <v-card-text>
                <div style="text-align: center;">
                    <input v-show="false" id="fileInput" type="file" @change="handleFileUpload" ref="fileInput" accept="image/*" multiple>
                    <v-avatar color="surface-variant"
                    style="margin-top: 15px;margin-left: 10px; cursor: pointer;"
                    size="80"
                    :image="headImage1"
                    @click="clickHeadImage">
                    </v-avatar>
                </div>
                <v-card style="margin-top: 18px;">
                    <div style="margin-top: 10px;">
                        <div style="text-align: left; vertical-align: center; margin-left: 10px; margin-bottom: 10px; margin-top: 10px; padding-right: 10px;">
                            <v-text-field label="输入新昵称" v-model="nickname"></v-text-field>
                        </div>
                        <v-divider></v-divider>
                        <div style="text-align: left; vertical-align: center; margin-left: 10px; margin-bottom: 10px; margin-top: 10px; padding-right: 10px;">
                            <v-text-field label="输入新签名" v-model="sign"></v-text-field>
                        </div>
                    </div>
                </v-card>
            </v-card-text>
        </div>

        <v-btn style="vertical-align: center; background-color: azure; margin-top: 25px; margin-bottom: 60px;" @click="save">
            <span>保存</span>
            <v-icon style="color: #4caf50;">mdi-checkbox-marked-circle</v-icon>
        </v-btn>
    </v-card>
    </div>
</template>

<script>
import axios from "axios";
import userStateStore from '../../store';
import {setSign, setNickname, setHeadImage} from "@/components/PersonalCenter/PersonalCenterAPI";
import router from "@/router";
import { isNicknameFormatOk, isSignFormatOk, NICKNAME_FORMAT_TIP, showTip, SIGN_FORMAT_TIP } from "../AccountManagement/AccountManagementAPI";

export default {
    name: "EditPersonalInfo",
    created() {
        // 加载数据
        this.nickname = userStateStore().nickname
        this.sign = userStateStore().sign
        this.headImage1 = userStateStore().headImage
        if (!userStateStore().email) {
            showTip("请首先登陆", false)
            router.replace({path: "loginPage"})
        }
    },
    data() {
        return {
            nickname: "默认",
            sign: "默认签名",
            headImage1: "https://banhang.oss-cn-beijing.aliyuncs.com/927eb856063e45368c424a4d22b6fffa.jpg",
            exchangeImage: ''
        }
    },
    methods: {
        clickHeadImage() {
            this.$refs.fileInput.click(); // 控制input组件点一下
        },
        handleFileUpload(event) {
            // 当用户点击了新的图片之后才会触发这个函数
            const file = event.target.files[0];
            if (file) {
                let form = new FormData();
                form.append("file", file);
                axios({
                    method: "post",
                    url: "https://banhang.lyhtool.com:8000/uploadfile/",
                    data: form,
                    headers: {'Content-Type': 'multipart/form-data'}
                }).then((res) => {
                    const data = res.data
                    if (data.response == 'success') {
                        console.log("成功上传图片: " + data.fileUrl)
                        this.headImage1 = data.fileUrl; // 回显
                    } else {
                        // 图片上传失败给一个弹窗
                        showTip("图片上传失败, 请重新尝试!", false)
                    }
                }).catch(() => {
                    showTip("图片上传失败, 请重新尝试!", false)
                })
            }
        },
        save() {
            if (!this.nickname || !this.sign) {
                showTip("昵称或个性签名不可为空!", false)
            } else if (!isSignFormatOk(this.sign)) {
                showTip(SIGN_FORMAT_TIP, false)
            } else if (!isNicknameFormatOk(this.nickname)) {
                showTip(NICKNAME_FORMAT_TIP, false)
            } else {
                setSign(this.sign, userStateStore().email)
                .then((res) => {
                    if (res.isSuccess) {
                        userStateStore().sign = this.sign
                    }
                })
                setNickname(this.nickname, userStateStore().email)
                    .then((res) => {
                        if (res.isSuccess) {
                            userStateStore().nickname = this.nickname;
                        }
                    })
                // 保存头像
                setHeadImage(userStateStore().email, this.headImage1)
                    .then((res) => {
                        if (res.isSuccess) {
                            userStateStore().headImage = this.headImage1;
                            router.push({path: "/personalCenter"});
                        }
                    })
            }
        },
        clickGoBack() {
            // console.log("尝试返回")
            router.push({path: "/personalCenter"});
        }
    },
};
</script>

<style scoped>

</style>
