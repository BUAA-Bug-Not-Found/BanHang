import axios from "axios";

export function getQuestions(pageNo, pageSize) {
    return axios.request({
        url: '/getQuestions',
        params: {
            pageNo: pageNo,
            pageSize: pageSize,
        },
        method: "get",
    }).then(response => {
        return response.data
    })
}

export function getQuesById(quesId) {
    return axios.request({
        url: '/getQuesById',
        method: "post",
        data: JSON.stringify({
            quesId: quesId
        })
    }).then(response => {
        return response.data
    })
}

export function getAnsById(ansId) {
    return axios.request({
        url: '/getAnsById',
        method: "post",
        data: JSON.stringify({
            ansId: ansId
        })
    }).then(response => {
        return response.data
    })
}