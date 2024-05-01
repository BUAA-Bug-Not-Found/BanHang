import axios from "axios";

export function queryStar(_a, _b) {
    // a b email
    console.log("query参数: ")
    console.log(_a)
    console.log(_b)
    return axios.request({
        url: "/queryStar",
        method: "get",
        params: {
            "email1": _a,
            "email2": _b
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}

export function setStarState(_a, _b, _state) {
    return axios.request({
        url: "/setStarState",
        method: "post",
        data: {
            "email1": _a,
            "email2": _b,
            "state": _state
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {

    })
}

export function setNickname(_a, _email) {
    return axios.request({
        url: "/setNicknameByEmail",
        method: "post",
        data: {
            "nickname": _a,
            "email": _email
        }
    }).then((reply) => {
        // 
        console.log("reply")
        console.log(reply.data)
        return reply.data
    }).catch(() => {

    })
}

export function setSign(_a, _email) {
    return axios.request({
        // 
        url: "/setSignByEmail",
        method: "post",
        data: {
            "sign": _a,
            "email": _email
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}

export function getHelpBlogs(_email) {
    return axios.request({
        url: "/getHelpBlogsByEmail",
        method: "get",
        params: {
            "email": _email
        },
        withCredentials: true
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}

export function getWaterBlogs(_email) {
    return axios.request({
        url: "/getAnonyBlogsByEmail",
        method: "get",
        params: {
            "email": _email
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}

export function getStars(_email) {
    // 
    return axios.request({
        url: "/getStarsByEmail",
        method: "get",
        params: {
            "email": _email
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}

export function getFans(_email) {
    return axios.request({
        url: "/getFansByEmail",
        method: "get",
        params: {
            "email": _email
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}

export function setHeadImage(_email, _url) {
    // 
    return axios.request({
        // 
        url: "/setHeadImageByEmail",
        method: "post",
        data: {
            "email": _email,
            "url": _url
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}