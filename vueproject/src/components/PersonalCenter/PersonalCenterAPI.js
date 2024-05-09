import axios from "axios";
import { showTip } from "../AccountManagement/AccountManagementAPI";

export function queryStar(_a, _b) {
    // a b email
    return axios.request({
        url: "/queryStarById",
        method: "get",
        params: {
            "id1": _a,
            "id2": _b
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}

export function setStarState(_a, _b, _state) {
    return axios.request({
        url: "/setStarStateById",
        method: "post",
        data: {
            "id1": _a,
            "id2": _b,
            "state": _state
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {

    })
}

export function setNickname(_a, _id) {
    return axios.request({
        url: "/setNicknameById",
        method: "post",
        data: {
            "nickname": _a,
            "id": _id
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {

    })
}

export function setSign(_a, _id) {
    return axios.request({
        // 
        url: "/setSignById",
        method: "post",
        data: {
            "sign": _a,
            "id": _id
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}

export function setHeadImage(_id, _url) {
    // 
    return axios.request({
        // 
        url: "/setHeadImageById",
        method: "post",
        data: {
            "id": _id,
            "url": _url
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}

export function getHelpBlogs(_id) {
    return axios.request({
        url: "/getHelpBlogsById",
        method: "get",
        params: {
            "id": _id
        },
        withCredentials: true
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}

export function getWaterBlogs(_id) {
    return axios.request({
        url: "/getAnonyBlogsById",
        method: "get",
        params: {
            "id": _id
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}

export function getStars(_id) {
    // 
    return axios.request({
        url: "/getStarsById",
        method: "get",
        params: {
            "id": _id
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        showTip("网络异常", false)
    })
}

export function getFans(_id) {
    return axios.request({
        url: "/getFansById",
        method: "get",
        params: {
            "id": _id
        }
    }).then((reply) => {
        return reply.data
    }).catch(() => {
        
    })
}

export function getOtherInfos(_id) {
    return axios.request({
        url: "/getOtherInfosById",
        method: "get",
        params: { // 对于get类型的接口, 这里的变量值要用params
            "id": _id
        }
    }).then((reply) => {
        // 这个data是json格式的
        return reply.data
    }).catch(() => {
        // 错误处理 TODO
        return false
    })
}
