<template>
    <v-container>
        <div>
        <!-- <v-layout style="justify-content:center;"> -->
            <!-- <v-flex> -->
                <v-card>
                    <v-card-title class="headline">登录</v-card-title>
                        <v-card-text>
                            <v-form>
                                <v-text-field v-model="email" label="邮箱" style="width: 100%"></v-text-field>
                                <v-text-field v-model="password" label="密码" type="password" style="width: 100%"></v-text-field>
                                <div style="display: flex; justify-content: flex-end; align-items: center;">
                                    <span @click="findPassword" style="color: #4a8bee; cursor: pointer;">找回密码</span>
                                </div>
                                <v-btn color="primary" block type="submit" @click.prevent="login" style="margin-top: 10px;">登录</v-btn> <br/>
                                <v-btn color="#42a300" block type="submit" @click.prevent="register">注册</v-btn>
                            </v-form>
                        </v-card-text>
                </v-card>
            <!-- </v-flex> -->
        <!-- </v-layout> -->
        </div>
    </v-container>
</template>

<script>
import router from '@/router';
import { getUserInfos, showTip, tryLogin, hashPassword} from "./AccountManagementAPI.js";
import {userStateStore} from "../../store/index";
import "element-plus/dist/index.css";

export default {
    name: "LoginPage",
    data() {
        return {
            email: "",
            password: ""
        };
    },
    methods: {
        login() {
            if (!this.email) {
                showTip("请输入邮箱", false)
            } else if (!this.password) {
                showTip("请输入密码", false)
            } else {
                // // 和数据库发送请求拿到密文密码, 然后拿用户输入的明文和密文进行比对
                // getPasswordByEmail(this.email).then((res) => {
                //     if (res === false) {
                //         showTip("登录异常", false)
                //     } else {
                //         const darkPass = res.password
                //         // 明暗文进行比对
                //         if (hashTool.compareSync(this.password, darkPass)) {
                //             getUserInfos(this.email).then((ret) => {
                //                 const st = userStateStore();
                //                 // 存储用户信息
                //                 st.login_store_info(ret, this.email);
                //                 showTip("登录成功 !", true)
                //                 router.push({path: "/HelpCenter"});
                                
                //             })
                //         } else {
                //             showTip("信息验证失败, 请重新输入!!", false)
                //         }
                //     }
                // })
                
                tryLogin(this.email, hashPassword(this.password)).then((res) => {
                    if (res.isSuccess) { // 用户信息验证成功
                        getUserInfos(this.email).then((ret) => {
                            const st = userStateStore();
                            // 存储用户信息
                            st.login_store_info(ret, this.email);
                            showTip("登录成功 !", true)
                            router.push({path: "/blogList", params: {tagId: -1}});
                        })
                    } else { // 验证失败
                        showTip("信息验证失败, 请重新输入!!", false)
                    }
                })        
            }
        },
        register() {
            // 直接跳转到注册界面
            router.push({path: "/registerPage"});
        },
        findPassword() {
            router.push({path: "/resetPassword"});
        },
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
  