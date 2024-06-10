import axios from "axios";
import {showTip} from "../AccountManagement/AccountManagementAPI";

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

// 以下几条有关举报
export function getComplainAmount() {
    return axios.request({
        url: "/getComplainAmount",
        method: "get",
        params: {}
    }).then((reply) => {
        return reply.data // 返回一个整数
    }).catch(() => {
        return false
    })
}

export function isShutUpByUserId(_id) {
    return axios.request({
        url: "/isShutUpByUserId",
        method: "post",
        data: {
            id: _id
        }
    }).then((r) => {
        console.log("r.data")
        console.log(r.data)
        console.log(r.data.isShutUp)
        return r.data.isShutUp;
    }).catch(() => {

    })
}

// export function isShutUpByUserId(_id) {
//     isShutUpByUserId1(_id).then((r) => {
//         return r
//     })
// }

export function shutUpUser(_id, _d, _h, _m) {
    return axios.request({
        url: "/shutUpUser",
        method: "post",
        data: {
            id: _id,
            day: _d,
            hour: _h,
            min: _m
        }
    }).then((r) => {
        return r.data.isSuccess
    }).catch(() => {

    })
}

export function deleteComplainItem(_id) {
    return axios.request({
        url: '/deleteComplainItem',
        method: "post",
        data: {
            id: _id
        }
    }).then((r) => {
        return r.data
    })
}

export function getComplainList() {
    // 本函数直接返回js列表
    return axios.request({
        url: "/getComplainList",
        method: "get",
        params: {}
    }).then((r) => {
        return r.data
    }).catch(() => {
        return false
    })
}

export function getCurrentLevelById(_id) {
    return axios.request({
        url: "getCurrentLevelById",
        method: "get",
        params: {
            "id": _id
        }
    }).then((r) => {
        return r.data.exp
    }).catch(() => {
        return false
    })
}

export function getCurrentExpById(_id) {
    return axios.request({
        url: "getCurrentExpById",
        method: "get",
        params: {
            "id": _id
        }
    }).then((r) => {
        return r.data.level
    }).catch(() => {
        return false
    })
}

export function uploadBadgeAPI(badgeName, badgeDescription, badgeUrl, color, cost) {
    return axios.request(
        {
            url: '/uploadBadge',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                badgeName: badgeName,
                badgeDesc: badgeDescription,
                badgeUrl: badgeUrl,
                badgeColor: color,
                badgeCost: cost,
            })
        }
    ).then(response2 => {
        return response2.data
    })
}

// export function getBadgesByUserId(userId, isOnlyShow) {
export function getBadgesByUserId(userId) {
    return axios.request({
        url: "getBadgesByUserId",
        method: "post",
        data: {
            "user_id": userId,
        }
    }).then((r) => {
        if (r.data.response == 'success')
            return r.data.badges // 表示成功
        else
            return false
    }).catch(() => {
        return false
    })
}

export function setBadgeShowState(userId, badgeId, state) {
    return axios({
        url: '/setBadgeShowState',
        method: "post",
        data: {
            "userId": userId,
            "badgeId": badgeId,
            "state": state
        }
    }).then(r => {
        if (r.data.response == 'success') return true
        else return false
    }).catch(() => {
        return false
    })
}

export function getBadges() {
    return axios.request(
        {
            url: '/getBadges',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({})
        }
    ).then(response => {
        return response.data
    })
}

export function uploadBuyBadge(userId, badgeId) {
    return axios.request(
        {
            url: '/buyBadge',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                badgeId: badgeId
            })
        }
    ).then(response => {
        return response.data
    })
}
