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
        params: {
            quesId: quesId
        },
        method: "get",
    }).then(response => {
        return response.data
    })
}

export function getTags() {
    return axios.request({
        url: '/getTags',
        method: 'get'
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

export function uploadFile(file) {
    return axios.post('/uploadfile', {
            file: file
        },
        {
            headers: {'Content-Type': 'multipart/form-data'}
        }).then(response => {
        return response.data
    })
}

export function uploadQues(content, imageList, quesTags) {
    return axios.post('/uploadQues', {
        quesContent: {
            content: content,
            imageList: imageList,
        },
        quesTags: quesTags
    }).then(response => {
        return response.data
    })
}

export function getQuestionsByTagId(pageNo, pageSize, tagId) {
    return axios.request({
        url: '/getQuestionsByTagId',
        params: {
            pageNo: pageNo,
            pageSize: pageSize,
            tagId: tagId
        },
        method: "get",
    }).then(response => {
        return response.data
    })
}