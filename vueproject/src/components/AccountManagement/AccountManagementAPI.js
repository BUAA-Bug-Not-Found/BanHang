import axios from "axios";


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
    })
}

export function getUserInfos(_email) {
    return axios.request({
        // TODO
        url: "/getInfoByEmail",
        method: "get",
        data: {
            "email": _email
        }
    }).then((reply) => {
        // 这个data是json格式的
        return reply.data
    }).catch(() => {
        // 错误处理 TODO
    })
}

export function trySendCheckCode(_email) {
    return axios.request({
        url: "/sendCheckCode",
        method: "post",
        data: {
            email: _email
        }
    }).then(reply => {
        return reply.data
    }).catch(() => {
        // 错误处理
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
        // 错误处理 TODO
    })
}
