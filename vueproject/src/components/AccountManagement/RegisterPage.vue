<template>
    <v-container>
        <v-card>
            <v-card-title class="headline">注册</v-card-title>
                <v-card-text>
                        <v-text-field v-model="username" label="昵称" style="width: 100%"></v-text-field>
                        <v-text-field v-model="password1" label="密码" type="password" style="width: 100%"></v-text-field>
                        <v-text-field v-model="password2" label="确认密码" type="password" style="width: 100%"></v-text-field>
                        <v-text-field v-model="email" label="邮箱" style="width: 100%"></v-text-field>
                        <v-text-field v-model="checkCode" label="验证码" style="width: 100%"></v-text-field>
                        <v-btn color="primary" block type="submit" @click.prevent="sendCheckCode" v-bind="props">发送验证码</v-btn> <br/>
                        <v-btn color="#42a300" block type="submit" @click.prevent="register" v-bind="props">注册</v-btn>
                </v-card-text>
        </v-card>
    </v-container>
</template>

<script>
import router from '@/router';
import { trySendCheckCode, tryRegister, showTip, hashPassword, isNicknameFormatOk, isPasswordFormatOk, PASSWORD_FORMAT_TIP, NICKNAME_FORMAT_TIP } from './AccountManagementAPI';

export default {
    name : "RegisterPage", 
    data() {
        return {
            username: "",
            password1: "",
            password2: "",
            email: "",
            checkCode: ""
        };
        // show: false
    },
    
    methods: {
        sendCheckCode() {
            // 调用后端函数, 向this.email发送验证码
            // 将验证码记录到const checkCode中
            const buaaEmailPattern = /^[a-zA-Z0-9_-]+@(?:buaa\.edu\.cn)$/
            if (!this.email) {
                showTip("邮箱不可为空", false);
            } else if (!buaaEmailPattern.test(this.email)) {// 格式校验
                showTip("请保证邮箱符合北航邮箱格式", false)
            } else {
                trySendCheckCode(this.email).then((res) => {
                    if (res.isSuccess) {
                        showTip("发送成功", true)     
                    } else {
                        showTip("发送失败", false)
                    }
                })
                
            }
            // 注意错误处理, 有可能是一个错误的邮箱号 TODO
        },
        register() {
            const infos = {
                "name": this.username,
                pass1: this.password1,
                pass2: this.password2,
                toEmail: this.email,
                inputCheckCode: this.checkCode
            }
            if (!infos.name) {
                showTip("昵称不可为空", false)
            } else if (!infos.pass1) {
                showTip("密码不可为空", false)
            } else if (!infos.pass2) {
                showTip("请确认密码", false)
            } else if (infos.pass1 !== infos.pass2) {
                showTip("两次输入的密码不相等, 请重新输入", false)
            } else if (!isNicknameFormatOk(infos.name)) {
                showTip(NICKNAME_FORMAT_TIP, false)
            } else if (!isPasswordFormatOk(infos.pass1)) {
                showTip(PASSWORD_FORMAT_TIP, false)
            } else {
                // 注册账户
                tryRegister(infos.name, infos.toEmail, hashPassword(infos.pass1), infos.inputCheckCode)
                    .then((res) => {
                        if (res.isSuccess) {
                            showTip("注册成功", true)
                            router.push({path: "/loginPage"})
                        } else {
                            showTip("注册失败", false)
                        }
                    })
            }
        }
    }
}
</script>

<style scoped>
    .v-text-field {
        width: 400px;
    }
</style>