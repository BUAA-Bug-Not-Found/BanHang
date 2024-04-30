import axios from "axios";
import {ElMessage} from "element-plus";

export function tryLogin(_email, _password) {
    // TODO 完善request中的数据
    console.log({
        "email": _email,
        "password": _password
    })
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

export function getUserInfos(_email) {
    return axios.request({
        url: "/getInfoByEmail",
        method: "get",
        params: { // 对于get类型的接口, 这里的变量值要用params
            "email": _email
        }
    }).then((reply) => {
        // 这个data是json格式的
        return reply.data
    }).catch(() => {
        // console.log("getInfo 失败")
        // 错误处理 TODO
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

export function showTip(content, isSuccess) {
    let t = 'error'
    if (isSuccess == true) {
        t = 'success'
    }
    ElMessage({
        message: content,
        showClose: true,
        type: t
    })
}


