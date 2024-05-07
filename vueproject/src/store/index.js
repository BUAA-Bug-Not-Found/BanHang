import {defineStore} from "pinia";
import mitt from "mitt" 

export const $bus = mitt();
export const isApp = false;
export const version = ['v0.0.1', 'alpha']
export const userStateStore = defineStore("user", {
    state: () => {
        if (isApp) {
            let perviousData = localStorage.getItem("userInfo")
            if (perviousData) {
                perviousData = JSON.parse(perviousData)
                return {
                    user_id: perviousData['user_id'],
                    user_name: perviousData['user_name'],
                    profile_photo: perviousData['profile_photo'],
                    register_date: perviousData['register_date'],
                    isAuthentic: perviousData['isAuthentic'],
                    email: perviousData['email'],
                    nickname: perviousData['nickname'],
                    headImage: perviousData['headImage'],
                    sign: perviousData['sign']
                }
            }
        }
        return {
            user_id: 0,
            user_name: "未登录",
            profile_photo: "src/assets/images/default-avatar.png",
            register_date: "default",
            isAuthentic: false,
            email: "",
            nickname: "",
            headImage: "",
            sign: ""
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
        getProfilePhoto: (state) => {
            return state.profile_photo
        },
        getRegisterDate: (state) => {
            return state.register_date
        },
        getIsAuthentic: (state) => {
            return state.isAuthentic
        }
    },

    actions: {
        async login_store_info(accountInfo, _email) {
            // this.user_id = accountInfo.user_id
            // this.user_name = accountInfo.user_name
            // if (accountInfo.profile_photo.substring(0, 3) === "/9j") {
            //     this.profile_photo = 'data:image/jpg;base64,' + accountInfo.profile_photo
            // } else if (accountInfo.profile_photo.substring(0, 3) === "iVB") {
            //     this.profile_photo = 'data:image/png;base64,' + accountInfo.profile_photo
            // } else {
            //     this.profile_photo = "src/assets/image/default-avatar.png"
            // }
            // this.register_date = accountInfo.register_date
            // this.isAuthentic = true
            // console.log("accountInfo")
            // console.log(accountInfo)
            
            this.email = _email;
            this.headImage = accountInfo.url;
            this.nickname = accountInfo.nickname;
            this.sign = accountInfo.sign;
            this.user_id = accountInfo.user_id;
            this.user_name = this.nickname;
            this.profile_photo = this.headImage;
            this.isAuthentic = true;
            $bus.emit("updateIndexData", {
                isLogin: true,
                user_name: this.user_name,
                avatar: this.headImage,
            })
            if (isApp) {
                localStorage.setItem("userInfo", JSON.stringify({
                    user_id: this.user_id,
                    user_name: this.user_name,
                    profile_photo: this.profile_photo,
                    register_date: this.register_date,
                    isAuthentic: this.isAuthentic,
                    email: this.email,
                    nickname: this.nickname,
                    headImage: this.headImage,
                    sign: this.sign
                }))
            }
        },
        async reg_success_info(accountInfo) {
            this.user_name = accountInfo.user_name
            this.isAuthentic = true
        },
        async logout() {
            this.isAuthentic = false
            $bus.emit("updateIndexData", {
                isLogin: false,
                user_name: '未登录',
                avatar: "src/assets/images/default-avatar.png",
            })
            localStorage.clear()
        },
        async resetUserInfo() {
            this.email = ""
            this.headImage = ""
            this.nickname = ""
            this.sign = ""
            this.user_id = 1
            localStorage.clear()
            $bus.emit("updateIndexData", {
                isLogin: false,
                user_name: '未登录',
                avatar: "src/assets/images/default-avatar.png",
            })
        }
    }
})
export default userStateStore