<template>
    <v-container>
        <v-layout style="justify-content:center;">
            <v-flex>
                <v-card>
                    <v-card-title class="headline">注册</v-card-title>
                        <v-card-text>
                            <v-form>
                                <v-text-field v-model="username" label="昵称"></v-text-field>
                                <v-text-field v-model="password1" label="密码" type="password"></v-text-field>
                                <v-text-field v-model="password2" label="确认密码" type="password"></v-text-field>
                                <v-text-field v-model="email" label="邮箱"></v-text-field>
                                <v-text-field v-model="checkCode" label="验证码"></v-text-field>
                                <v-snackbar :timeout="2000" :color="barColor">
                                    <template v-slot:activator="{ props }">
                                        <!-- <v-btn class="ma-2" v-bind="props">open</v-btn> -->
                                        <v-btn color="primary" block type="submit" @click.prevent="sendCheckCode" v-bind="props">发送验证码</v-btn> <br/>
                                        <v-btn color="#42a300" block type="submit" @click.prevent="register" v-bind="props">注册</v-btn>
                                    </template>
                                    {{ mes }}
                                </v-snackbar>
                                <!-- <v-btn color="#42a300" block type="submit" @click.prevent="register" v-bind="props">注册</v-btn> -->
                                
                            </v-form>
                        </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>

</template>

<script>
// import { info } from 'console';
// import ElMessage from 'element-plus';
// import { ref } from 'vue';
// const checkCode = ref('')
import { trySendCheckCode, tryRegister } from './AccountManagementAPI';

export default {
    name : "RegisterPage", 
    data() {
        return {
            mes: "注册成功！",
            barColor: "#42a300",
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
            // const buaaEmailPattern = /^[a-zA-Z0-9_-]+@(?:buaa\.edu\.cn)$/

            if (!this.email) {
                this.mes = '邮箱不可为空'
                this.barColor = '#FF0000'
            // } else if (!buaaEmailPattern.test(this.email)) {// 格式校验
            //     this.mes = '请保证邮箱符合北航邮箱格式'
            //     this.barColor = '#FF0000'
            } else {
                // console.log('debug-> ' + this.email);
                trySendCheckCode(this.email).then((res) => {
                    if (res.isSuccess) {
                        // 发送成功
                        this.mes = '发送成功 !'
                        this.barColor = '#42a300'        
                    } else {
                        this.mes = '发送失败 !'
                        this.barColor = '#FF0000'
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
            // console.log(infos)
            if (!infos.name) {
                this.mes = '昵称不可为空'
                this.barColor = '#FF0000'
            } else if (!infos.pass1) {
                this.mes = '密码不可为空'
                this.barColor = '#FF0000'
            } else if (!infos.pass2) {
                this.mes = '请确认密码'
                this.barColor = '#FF0000'
            } else if (infos.pass1 !== infos.pass2) {
                this.mes = '两次输入的密码不相等, 请重新输入'
                this.barColor = '#FF0000'
            } else {
                // 注册账户
                // console.log("准备注册 !")
                tryRegister(infos.name, infos.toEmail, infos.pass1, infos.inputCheckCode)
                    .then((res) => {
                        if (res.isSuccess) {
                            this.mes = '注册成功 !'
                            this.barColor = '#42a300'
                        } else {
                            this.mes = '注册失败 !'
                            this.barColor = '#FF0000'
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