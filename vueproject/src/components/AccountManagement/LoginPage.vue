<template>
    <v-container>
        <v-layout style="justify-content:center;">
            <v-flex>
                <v-card>
                    <v-card-title class="headline">登录</v-card-title>
                        <v-card-text>
                            <v-form>
                                <v-text-field v-model="email" label="邮箱"></v-text-field>
                                <v-text-field v-model="password" label="密码" type="password"></v-text-field>
                                <div @click="findPassword" style="display: flex; justify-content: flex-end; align-items: center;">
                                    <span style="color: #4a8bee; cursor: pointer;">找回密码</span>
                                </div>
                                <v-snackbar :timeout="2000" :color="barColor">
                                    <template v-slot:activator="{props}"> 
                                        <v-btn color="primary" block type="submit" @click.prevent="login" style="margin-top: 10px;" v-bind="props">登录</v-btn> <br/>
                                    </template>
                                    {{ mes }}
                                </v-snackbar>
                                <v-btn color="#42a300" block type="submit" @click.prevent="register">注册</v-btn>
                            </v-form>
                        </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
import router from '@/router';
import {tryLogin, getUserInfos} from "./AccountManagementAPI.js";
import { ref } from 'vue';
import {userStateStore} from "../../store/index";

export default {
    name: "LoginPage",
    data() {
        return {
            mes: "",
            barColor: "",
            email: "",
            password: ""
        };
    },
    methods: {
        setFailBarInfo(_m) {
            this.mes = _m;
            this.barColor = "#FF0000";
        },
        setSuccessBarInfo(_m) {
            this.mes = _m;
            this.barColor = "#42a300";
        },
        login() {
            if (!this.email) {
                this.setFailBarInfo("请输入邮箱")
            } else if (!this.password) {
                this.setFailBarInfo("请输入密码")
            }
            const match = ref(false);
            // 和数据库发送请求进行信息验证
            tryLogin(this.email, this.password).then((res) => {
                match.value = Boolean(res.match === "true");
            }).then(() => {
                if (match.value) { // 用户信息验证成功
                    getUserInfos(this.email).then((ret) => {
                        const st = userStateStore();
                        // 存储用户信息
                        st.login_store_info(ret);
                        // 跳转
                        router.push({path: "/helpCenter"});
                        this.setSuccessBarInfo("登录成功!!")
                    })
                } else { // 验证失败
                    this.setFailBarInfo("信息验证失败, 请重新输入!!")
                }
            })
            // 切换界面
        },
        register() {
            // 直接跳转到注册界面
            router.push({path: "/registerPage"});
        },
        findPassword() {
            router.push({path: "/resetPassword"});
        }
    }
}
</script>

<style scoped>
    .v-container {
        height: 100vh;
        margin: auto;
    }

    .v-layout {
        height: 100%;
    }

    .v-text-field {
        width: 400px;
    }

    .v-flex {
        margin: auto;
    }
</style>
  