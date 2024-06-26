import {defineStore} from "pinia";
import mitt from "mitt" 

export const $bus = mitt();
export const isApp = false;
export const version = ['v0.1.1', 'beta']
export const userStateStore = defineStore("user", {
    state: () => {
        // if (isApp) {
            let perviousData = localStorage.getItem("userInfo")
            if (perviousData) {
                perviousData = JSON.parse(perviousData)
                return {
                    user_id: perviousData['user_id'],
                    user_name: perviousData['user_name'],
                    register_date: perviousData['register_date'],
                    isAuthentic: perviousData['isAuthentic'],
                    email: perviousData['email'],
                    isManager: perviousData['isManager'],
                    nickname: perviousData['nickname'],
                    headImage: perviousData['headImage'],
                    hashPassword: perviousData['hashPassword'],
                    sign: perviousData['sign'],
                    coins: perviousData['coins']
                }
            }
        // }
        return { // 这一个return在正常情况下是没有用的
            user_id: 0,
            user_name: "未登录",
            register_date: "default",
            isAuthentic: false,
            email: "",
            hashPassword: "",
            nickname: "",
            headImage: "",
            sign: "",
            coins: 0
        }
    },

    persist: {
        enabled: true,
        key: "demo",
        storage: sessionStorage,
    },

    getters: {
        getUserName: (state) => {
            return state.user_name
        },
        getUserId: (state) => {
            return state.user_id
        },
        getRegisterDate: (state) => {
            return state.register_date
        },
        getIsAuthentic: (state) => {
            return state.isAuthentic
        }
    },

    actions: {
        async login_store_info(accountInfo, _email, _id, hashPassword) {
            this.email = _email;
            this.headImage = accountInfo.url;
            this.nickname = accountInfo.nickname;
            this.sign = accountInfo.sign;
            this.isManager = accountInfo.isManager;
            this.hashPassword = hashPassword
            this.user_id = _id;
            this.user_name = this.nickname;
            this.isAuthentic = true;
            $bus.emit("updateIndexData", {
                isLogin: true,
                user_name: this.user_name,
                avatar: this.headImage,
            })
            localStorage.setItem("userInfo", JSON.stringify({
                user_id: this.user_id,
                user_name: this.user_name,
                register_date: this.register_date,
                isAuthentic: this.isAuthentic,
                email: this.email,
                hashPassword: this.hashPassword,
                isManager: this.isManager,
                nickname: this.nickname,
                headImage: this.headImage,
                sign: this.sign,
                coins: 0
            }))
        },
        async coins_info(coins) {
            this.coins = coins
            localStorage.setItem("userInfo", JSON.stringify({
                user_id: this.user_id,
                user_name: this.user_name,
                register_date: this.register_date,
                isAuthentic: this.isAuthentic,
                email: this.email,
                hashPassword: this.hashPassword,
                isManager: this.isManager,
                nickname: this.nickname,
                headImage: this.headImage,
                sign: this.sign,
                coins: this.coins
            }))
        },
        async resetUserInfo() {
            this.email = ""
            this.headImage = ""
            this.nickname = ""
            this.user_name = ""
            this.register_date = ""
            this.isAuthentic = false
            this.sign = ""
            this.user_id = 1
            this.isManager = false
            this.hashPassword = ''
            this.coins = 0
            localStorage.clear()
            $bus.emit("updateIndexData", {
                isLogin: false,
                user_name: '未登录',
                avatar: "src/assets/images/default-avatar.png",
            })
        },
        async updateNewInfo(_nickname, _sign, _url) {
            // if (isApp) {
                localStorage.setItem("userInfo", JSON.stringify({
                    user_id: this.user_id,
                    user_name: _nickname,
                    register_date: this.register_date,
                    isAuthentic: this.isAuthentic,
                    email: this.email,
                    hashPassword: this.hashPassword,
                    isManager: this.isManager,
                    nickname: _nickname,
                    headImage: _url,
                    sign: _sign,
                    coins: this.coins
                }))
            // }
        },
        async updateCoins(coins) {
            this.coins = coins
            localStorage.setItem("userInfo", JSON.stringify({
                user_id: this.user_id,
                user_name: this.user_name,
                register_date: this.register_date,
                isAuthentic: this.isAuthentic,
                email: this.email,
                hashPassword: this.hashPassword,
                isManager: this.isManager,
                nickname: this.nickname,
                headImage: this.headImage,
                sign: this.sign,
                coins: coins
            }))
        }
    }
})
export default userStateStore