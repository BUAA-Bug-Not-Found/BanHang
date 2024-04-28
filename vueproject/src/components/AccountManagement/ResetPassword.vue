<template>
    <v-container>
        <v-layout style="justify-content:center">
            <v-flex>
                <v-card>
                    <v-card-title class="headline">找回密码</v-card-title>
                        <v-card-text>
                            <v-form>
                                <v-text-field v-model="password1" label="新密码" type="password"></v-text-field>
                                <v-text-field v-model="password2" label="确认密码" type="password"></v-text-field>
                                <v-text-field v-model="email" label="邮箱"></v-text-field>
                                <v-text-field v-model="checkCode" label="验证码"></v-text-field>
                                <v-snackbar :timeout="2000" :color="barColor">
                                    <template v-slot:activator="{ props }">
                                        <!-- <v-btn class="ma-2" v-bind="props">open</v-btn> -->
                                        <!-- <v-btn color="primary" block type="submit" @click.prevent="sendCheckCode" v-bind="props">发送验证码</v-btn> <br/>
                                        <v-btn color="#42a300" block type="submit" @click.prevent="register" v-bind="props">注册</v-btn> -->
                                        <v-btn color="primary" block type="submit" @click.prevent="sendCheckCode" v-bind="props">发送验证码</v-btn> <br/>
                                        <v-btn color="#42a300" block type="submit" @click.prevent="resetPassword1" v-bind="props">重置密码</v-btn>
                                    </template>
                                    {{ mes }}
                                </v-snackbar>
                            </v-form>
                        </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
import router from '@/router';
import { tryResetPassword, trySendCheckCode } from './AccountManagementAPI';
export default {
    data() {
        return {
            mes: "",
            barColor: "",
            password1: "",
            password2: "",
            email: "",
            checkCode: ""
        };
    },
    methods: {
        setFailBarInfo(_m) {
            this.mes = _m
            this.barColor = "#FF0000"
        },
        setSuccessBarInfo(_m) {
            this.mes = _m
            this.barColor = "#42a300"
        },
        sendCheckCode() {
            const buaaEmailPattern = /^[a-zA-Z0-9_-]+@(?:buaa\.edu\.cn)$/
            if (!this.email) {
                this.mes = '邮箱不可为空'
                this.barColor = '#FF0000'
            } else if (!buaaEmailPattern.test(this.email)) {// 格式校验
                this.mes = '请保证邮箱符合北航邮箱格式'
                this.barColor = '#FF0000'
            } else {
                trySendCheckCode(this.email).then((res) => {
                    if (res.value) {
                        this.mes = '发送成功 !'
                        this.barColor = '#42a300'
                    } else {
                        this.mes = '发送失败 !'
                        this.barColor = '#FF0000'
                    }
                })
            }
            // 调函数
        },
        resetPassword1() {
            if (!this.password1) {
                this.setFailBarInfo("请输入密码")
            } else if (!this.password2) {
                this.setFailBarInfo("请确认密码")
            } else if (this.password1 !== this.password2) {
                this.setFailBarInfo("两次输入的密码不一致, 请重新输入")
            } else if (!this.checkCode) {
                this.setFailBarInfo("请输入验证码")
            } else {
                // 调用后端函数进行验证码验证
                tryResetPassword(this.email, this.password1, this.checkCode)
                    .then((res) => {
                        if (res.value) {
                            this.setSuccessBarInfo("重置成功 !!")
                            router.push({path : '/loginPage'})
                        } else {
                            this.setFailBarInfo("重置密码失败, 请检查各项信息")
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
</style>