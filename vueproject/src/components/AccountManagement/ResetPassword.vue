<template>
    <v-container>
            <v-card>
                <v-card-title class="headline">找回密码</v-card-title>
                    <v-card-text>
                        <!-- <v-text-field v-model="password1" label="新密码" type="password"  style="width: 100%"></v-text-field>
                        <v-text-field v-model="password2" label="确认密码" type="password" style="width: 100%"></v-text-field>
                        <v-text-field v-model="email" label="邮箱" style="width: 100%"></v-text-field>
                        <v-text-field v-model="checkCode" label="验证码" style="width: 100%"></v-text-field>
                        <v-btn color="primary" block type="submit" @click.prevent="sendCheckCode" v-bind="props">发送验证码</v-btn> <br/>
                        <v-btn color="#42a300" block type="submit" @click.prevent="resetPassword1" v-bind="props">重置密码</v-btn> -->


                        <v-text-field v-model="password1" label="新密码" type="password" style="width: 100%"></v-text-field>
                        <v-text-field v-model="password2" label="确认密码" type="password" style="width: 100%"></v-text-field>
                        <v-text-field v-model="email" label="邮箱" style="width: 100%"></v-text-field>
                        <div style="display: flex;">
                            <v-text-field v-model="checkCode" label="验证码" style="width: 60%; margin-right: 16px;"></v-text-field>
                            <v-btn color="primary" type="submit" @click.prevent="sendCheckCode" style="height: 56px;">发送验证码</v-btn>
                        </div>
                        <v-btn color="#42a300" block type="submit" @click.prevent="resetPassword1" v-bind="props">重置密码</v-btn>


                        <!-- <v-row>
                            <v-col cols="12">
                                <v-text-field v-model="password1" label="新密码" type="password" style="width: 100%"></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field v-model="password2" label="确认密码" type="password" style="width: 100%"></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field v-model="email" label="邮箱" style="width: 100%; padding-bottom: 0px;"></v-text-field>
                            </v-col>
                            <v-col cols="9">
                                <v-text-field v-model="checkCode" label="验证码" style="width: 100%; margin-bottom: 0px;"></v-text-field>
                            </v-col>
                            <v-col cols="3">
                                <v-btn color="primary" block type="submit" @click.prevent="sendCheckCode" v-bind="props" class="mt-0">发送验证码</v-btn>
                            </v-col>
                            <v-col cols="12">
                                <v-btn color="#42a300" block type="submit" @click.prevent="resetPassword1" v-bind="props">重置密码</v-btn>
                            </v-col>
                        </v-row> -->
                    </v-card-text>
            </v-card>
    </v-container>
</template>

<script>
import router from '@/router';
import { tryResetPassword, trySendCheckCode, showTip, hashPassword, isPasswordFormatOk, PASSWORD_FORMAT_TIP } from './AccountManagementAPI';
export default {
    data() {
        return {
            password1: "",
            password2: "",
            email: "",
            checkCode: ""
        };
    },
    methods: {
        sendCheckCode() {
            const buaaEmailPattern = /^[a-zA-Z0-9_-]+@(?:buaa\.edu\.cn)$/
            if (!this.email) {
                showTip("邮箱不可为空", false)
            } else if (!buaaEmailPattern.test(this.email)) {// 格式校验
                showTip("请保证邮箱符合北航邮箱格式", false)
            } else {
                trySendCheckCode(this.email).then((res) => {
                    if (res.isSuccess) {
                        showTip("发送成功 !", true)
                    } else {
                        showTip("发送失败 !", false)
                    }
                })
            }
            // 调函数
        },
        resetPassword1() {
            if (!this.password1) {
                showTip("请输入密码", false)
            } else if (!this.password2) {
                showTip("请确认密码", false)
            } else if (this.password1 !== this.password2) {
                showTip("两次输入的密码不一致, 请重新输入", false)
            } else if (!isPasswordFormatOk(this.password1)) {
                showTip(PASSWORD_FORMAT_TIP, false, 5000)
            } else if (!this.checkCode) {
                showTip("请输入验证码", false)
            } else {
                // 调用后端函数进行验证码验证
                tryResetPassword(this.email, hashPassword(this.password1), this.checkCode)
                    .then((res) => {
                        if (res.isSuccess) {
                            showTip("重置成功 !!", true)
                            router.push({path : '/loginPage'})
                        } else {
                            showTip("重置密码失败, 请检查各项信息", false)
                        }
                    })
            }
        }
    }
}
</script>
<style scoped>
.v-card {
    justify-content: center;
}

.v-text-field {
    width: 400px;
}

.v-input__details {
    /* height: 0px; */
    display: none;
}

</style>