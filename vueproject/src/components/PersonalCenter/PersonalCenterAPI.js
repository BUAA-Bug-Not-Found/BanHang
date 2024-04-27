import axios from "axios";

export function queryStar(_a, _b) {
    // a b email
    return axios.request({
        url: "/queryStar",
        method: "post",
        data: {
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
