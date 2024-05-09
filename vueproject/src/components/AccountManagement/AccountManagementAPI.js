import axios from "axios";
import {ElMessage} from "element-plus";
import CryptoJS from "crypto-js";
import userStateStore from "@/store";
import router from "@/router";

export const NICKNAME_FORMAT_TIP = "昵称必须由1-15个字符组成, 只可包含汉字,字母,数字,下划线,连字符";
export const PASSWORD_FORMAT_TIP = "密码必须至少含8个字符, 最多32个字符, 且不可仅包含数字或仅包含大写字母或仅包含小写字母";
export const SIGN_FORMAT_TIP = "个性签名最多包含30个字符"
export const hashTool = require("bcryptjs")


export function tryLogin(_email, _password) {
    // TODO 完善request中的数据
    return axios.request({
        url: "/login",
        method: "put",
        data: {
            "email": _email,
            "password": _password
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        // 错误处理 TODO
        return {"isSuccess": false}
    })
}

export function tryResetPassword(_email, _password, _checkCode) {
    return axios.request({
        url: "/resetPassword",
        method: "post",
        data: {
            "email": _email,
            "password": _password,
            "checkCode": _checkCode
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        // 错误处理
        return {"isSuccess": false}
    })
}

// export function getUserInfos(_email) {
//     return axios.request({
//         url: "/getInfoByEmail",
//         method: "get",
//         params: { // 对于get类型的接口, 这里的变量值要用params
//             "email": _email
//         }
//     }).then((reply) => {
//         // 这个data是json格式的
//         return reply.data
//     }).catch(() => {
//         // 错误处理 TODO
//         return false
//     })
// }

export function getInfoByUserId(_id) {
    return axios.request({
        url: "/getInfoByUserId",
        method: "get",
        params: { // 对于get类型的接口, 这里的变量值要用params
            "userId": _id
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        return false
    })
}

export function trySendCheckCode(_email) {
    return axios.request({
        url: "/sendCheckCode",
        method: "post",
        data: {
            "email": _email
        }
    }).then(reply => {
        return reply.data
    }).catch(() => {
        return {"isSuccess": false}
    })
}

export function tryRegister(_username, _email, _password, _checkCode) {
    return axios.request({
        url: "/registerUser",
        method: "post",
        data: {
            "username": _username,
            "password": _password,
            "email": _email,
            "checkCode": _checkCode
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        return {"isSuccess": false}
    })
}

export function showTip(content, isSuccess, time=2000) {
    let t = 'error'
    if (isSuccess == true) {
        t = 'success'
    }
    ElMessage({
        message: content,
        showClose: true,
        type: t,
        duration: time
    })
}

export function hashPassword(password) {
    return hashSHA256(password)
}

export function hashBcryptjs(password) {
    const salt = hashTool.genSaltSync(10);
    return hashTool.hashSync(password, salt)
}

export function hashSHA256(password) {
    return CryptoJS.SHA256(password).toString();
}

export function isNicknameFormatOk(nickname) {
    const regex = /^[a-zA-Z0-9_\-\u4e00-\u9fa5]{1,15}$/;
    return regex.test(nickname)
}

export function isPasswordFormatOk(password) {
    // const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
    const regex1 = /^[0-9]+$/
    const regex2 = /^[a-z]+$/
    const regex3 = /^[A-Z]+$/
    const len = password.length
    return !regex1.test(password) && !regex2.test(password) && !regex3.test(password) && len <= 32 && len >= 8
    // const regex2 = /[a-zA-Z]/
    // return regex1.test(password) && regex2.test(password) && len <= 32 && len >= 8
}

export function isSignFormatOk(sign) {
    return sign.length <= 30 && sign.length >= 1
}

export function checkLogin() {
    if (!userStateStore().email) {
          showTip("请首先登录", false)
          router.replace({path: "/loginPage"})
    }
}

