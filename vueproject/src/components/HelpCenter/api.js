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
    let form = new FormData
    form.append("file", file)
    return axios({
        method: "post",
        url: "https://banhang.lyhtool.com:8000/uploadfile/",
        data: form,
        headers: {'Content-Type': 'multipart/form-data'}
    }).then(response => {
        return response.data
    })
}

export function uploadQuesApi(content, imageList, quesTags) {
    return axios.request({
        url: 'uploadQues',
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        data: JSON.stringify({
            quesContent: {
                content: content,
                imageList: imageList,
            },
            quesTags: quesTags
        })
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
        headers: {'Content-Type': 'application/json'},
        data: JSON.stringify({
            ansId: ansId,
            setType: setType
        })
    }).then(response => {
        return response.data
    })
}

export function uploadAnsApi(quesId, content, imageList) {
    return axios.request(
        {
            url: '/answerQues',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                quesId: quesId,
                ansContent: {
                    content: content,
                    imageList: imageList
                },
            })
        }
    ).then(response => {
        return response.data
    })
}

export function getAnsById(ansId) {
    return axios.request(
        {
            url: '/getAnsById',
            params: {
                ansId: ansId
            },
            method: 'get',
        }
    ).then(response => {
        return response.data
    })
}

export function setAnsLikeAPI(ansId, ansType) {
    return axios.request(
        {
            url: '/setLikeAns',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                    ansId: ansId,
                    setType: ansType
                }
            )
        }
    ).then(response => {
        return response.data
    })
}

export function getInfoByUserIdAPI(userId) {
    return axios.request(
        {
            url: '/getInfoByUserId',
            params: {
                userId: userId
            },
            method: "get",
        }
    ).then(response => {
        return response.data
    })
}

export function delQuestionAPI(quesId) {
    return axios.request(
        {
            url: '/delQuestion',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                    quesId: quesId
                }
            )
        }
    ).then(response => {
        return response.data
    })
}

export function delAnswerAPI(ansId) {
    return axios.request(
        {
            url: '/delAnswer',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                    ansId: ansId
                }
            )
        }
    ).then(response => {
        return response.data
    })
}

export function solveQuesAPI(quesId) {
    return axios.request(
        {
            url: '/solveQuestion',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                    quesId: quesId
                }
            )
        }
    ).then(response => {
        return response.data
    })
}

export function acceptAnswer(ansId) {
    return axios.request(
        {
            url: '/acceptAnswer',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                    ansId: ansId
                }
            )
        }
    )
}

export function formatDate(time) {
    let date = new Date(Date.parse(time))
    let year = date.getFullYear();
    let month = ('0' + (date.getMonth() + 1)).slice(-2); // 月份从0开始，需要加1，并且保证两位数
    let day = ('0' + date.getDate()).slice(-2); // 保证两位数
    let hours = ('0' + date.getHours()).slice(-2); // 保证两位数
    let minutes = ('0' + date.getMinutes()).slice(-2); // 保证两位数

    return `${year}.${month}.${day} ${hours}:${minutes}`
}