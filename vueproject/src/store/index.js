import {defineStore} from "pinia";

export const userStateStore = defineStore("user", {
    state: () => {
        return {
            user_id: 1,
            user_name: "admin",
            profile_photo: "src/assets/image/default-avatar.png",
            register_date: "default",
            isAuthentic: false,
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
        async login_store_info(accountInfo) {
            this.user_id = accountInfo.user_id
            this.user_name = accountInfo.user_name
            if (accountInfo.profile_photo.substring(0, 3) === "/9j") {
                this.profile_photo = 'data:image/jpg;base64,' + accountInfo.profile_photo
            } else if (accountInfo.profile_photo.substring(0, 3) === "iVB") {
                this.profile_photo = 'data:image/png;base64,' + accountInfo.profile_photo
            } else {
                this.profile_photo = "src/assets/image/default-avatar.png"
            }
            this.register_date = accountInfo.register_date
            this.isAuthentic = true
        },
        async reg_success_info(accountInfo) {
            this.user_name = accountInfo.user_name
            this.isAuthentic = true
        },
        async logout() {
            this.isAuthentic = false
        }
    }
})

export default userStateStore