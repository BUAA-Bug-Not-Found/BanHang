<template>
    <v-container>
        <v-dialog v-model="showDialog" max-width="400px">
            <v-card>
            <v-card-title class="headline" style="text-align:center;">头像操作</v-card-title>
            <v-divider></v-divider>
            <div style="margin-top: 20px; margin-bottom: 10px;">
                <v-card style="padding-top:10px; padding-bottom:10px; margin-left: 10px; margin-right: 10px;" @click="clickLocalHeadImage">
                    <v-text style="margin-left: 12px;">从本地选择头像</v-text>
                </v-card>

                <v-card v-if="this.isMobileDevice" style="padding-top:10px; padding-bottom:10px; margin-left: 10px; margin-right: 10px; margin-top: 10px;" @click="clickCameraHeadImage">
                    <v-text style="margin-left: 12px;">拍照上传头像</v-text>
                </v-card>

                <!-- <v-card style="padding-top:10px; padding-bottom:10px; margin-left: 10px; margin-right: 10px; margin-top: 10px;">
                    <v-text style="margin-left: 12px;">从相册选择头像</v-text>
                </v-card> -->
            </div>
            <div style="text-align: center; margin-top: 30px;">
                <v-btn color="blue darken-1" @click="showDialog = false" style="margin-bottom: 10px; max-width: 50%;">取消</v-btn>
            </div>
            <!-- <v-card-text>
                确定要退出登录吗？
            </v-card-text> 
            <v-card-actions>
                <v-btn color="error" @click="clickQuitLogin">确认</v-btn>
                <v-btn color="blue darken-1" @click="showDialog = false">取消</v-btn>
            </v-card-actions> -->
            </v-card>
        </v-dialog>


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
                    @click="showDialog = true">
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
    </v-container>
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
        this.isMobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    },
    data() {
        return {
            nickname: "默认",
            sign: "默认签名",
            headImage1: "https://banhang.oss-cn-beijing.aliyuncs.com/927eb856063e45368c424a4d22b6fffa.jpg",
            exchangeImage: '',
            showDialog: false,
            isMobileDevice: false
        }
    },
    methods: {
        clickLocalHeadImage() {
            this.$refs.fileInput.click(); // 控制input组件点一下
            this.showDialog = false
        },
        handleFileUpload(event) {
            // 当用户点击了新的图片之后才会触发这个函数
            const file = event.target.files[0];
            if (file) {
                let form = new FormData();
                form.append("file", file);
                axios({
                    method: "post",
                    url: "https://banhang.lyhtool.com:8000/uploadAvatar/",
                    data: form,
                    headers: {'Content-Type': 'multipart/form-data'}
                }).then((res) => {
                    const data = res.data
                    if (data.response == 'success') {
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
            router.push({path: "/personalCenter"});
        },
        clickCameraHeadImage() {
            // const isMobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
            // if (!isMobileDevice) {
            //     showTip("pc端不支持")
            //     return
            // }
            const constraints = {
                video: true
            };
            navigator.mediaDevices.getUserMedia(constraints)
            .then((stream) => {
                // 将拍摄的视频流设置为视频元素的源
                const videoElement = document.createElement('video');
                videoElement.srcObject = stream;
                videoElement.autoplay = true;

                // 在页面上显示视频元素
                document.body.appendChild(videoElement);

                // 当用户点击视频元素时，将当前帧作为图片上传
                videoElement.addEventListener('click', () => {
                const canvasElement = document.createElement('canvas');
                canvasElement.width = videoElement.videoWidth;
                canvasElement.height = videoElement.videoHeight;
                const canvasContext = canvasElement.getContext('2d');
                canvasContext.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

                // 将 Canvas 中的图像转换为 Blob 对象
                canvasElement.toBlob((blob) => {
                    // 创建 FormData 对象
                    const formData = new FormData();
                    formData.append('photo', blob, 'photo.png');

                    // 关闭视频流
                    stream.getTracks().forEach(track => track.stop());
                    videoElement.remove();

                    // 将 FormData 发送到服务器
                    // 此处可以使用你喜欢的方式发送 FormData
                    axios({
                        method: "post",
                        url: "https://banhang.lyhtool.com:8000/uploadAvatar/",
                        data: formData,
                        headers: {'Content-Type': 'multipart/form-data'}
                    }).then((res) => {
                        const data = res.data
                        if (data.response == 'success') {
                            this.headImage1 = data.fileUrl; // 回显
                        } else {
                            // 图片上传失败给一个弹窗
                            showTip("图片上传失败, 请重新尝试!", false)
                        }
                    }).catch(() => {
                        showTip("图片上传失败, 请重新尝试!", false)
                    })
                });
                });
            }).catch((error) => {
                console.error('getUserMedia error:', error);
            });
        }
    },
};
</script>

<style scoped>

</style>
