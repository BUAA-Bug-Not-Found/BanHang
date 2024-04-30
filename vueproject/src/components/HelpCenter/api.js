import axios from "axios";

export function getQuestionsApi(pageNo, pageSize) {
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

export function getQuesByIdApi(quesId) {
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

export function getTagsApi() {
    return axios.request({
        url: '/getTags',
        method: 'get'
    }).then(response => {
        return response.data
    })
}

export function getAnsByIdApi(ansId) {
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

export function uploadFileApi(file) {
    return axios.post('/uploadfile', {
            file: file
        },
        {
            headers: {'Content-Type': 'multipart/form-data'}
        }).then(response => {
        return response.data
    })
}

export function uploadQuesApi(content, imageList, quesTags) {
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

export function getQuestionsByTagIdApi(pageNo, pageSize, tagId) {
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

export function setLikeQuesApi(quesId, setType) {
    return axios.request({
        url: '/setLikeQues',
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        data: JSON.stringify({
            quesId: quesId,
            setType: setType
        })
    }).then(response => {
        return response.data
    })
}

export function setLikeAnsApi(ansId, setType) {
    return axios.request({
        url: '/setLikeAns',
        method: 'post',
        data: JSON.stringify({
            ansId: ansId,
            setType: setType
        })
    }).then(response => {
        return response.data
    })
}
