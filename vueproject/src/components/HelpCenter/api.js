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
        console.log(response.data)
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
    }).catch(error => {
        // 错误处理
        const { response } = error;
        if (response && response.status === 400) {
            return response.data
        } else {
            // 其他错误按原样抛出
            throw error;
        }
    })
}

export function updateQuesApi(quesId, content, imageList, quesTags) {
    return axios.request({
        url: 'updateQues',
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        data: JSON.stringify({
            quesId: quesId,
            quesContent: {
                content: content,
                imageList: imageList,
            },
            quesTags: quesTags
        })
    }).then(response => {
        return response.data
    }).catch(error => {
        // 错误处理
        const { response } = error;
        if (response && response.status === 400) {
            return response.data
        } else {
            // 其他错误按原样抛出
            throw error;
        }
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
    }).catch(error => {
        // 错误处理
        const { response } = error;
        if (response && response.status === 400) {
            return response.data
        } else {
            // 其他错误按原样抛出
            throw error;
        }
    });
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

export function replyComment(replyCommentId, content, imageList) {
    return axios.request(
        {
            url: '/replyComment',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                replyCommentId: replyCommentId,
                ansContent: {
                    content: content,
                    imageList: imageList
                },
            })
        }
    ).then(response => {
        return response.data
    }).catch(error => {
        // 错误处理
        const { response } = error;
        if (response && response.status === 400) {
            return response.data
        } else {
            // 其他错误按原样抛出
            throw error;
        }
    })
}

export function setFocusQues(quesId, ifFocus) {
    return axios.request(
        {
            url: '/setFocusQues',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                quesId: quesId,
                ifFocus: ifFocus == true ? 1: 0
            })
        }
    ).then(response => {
        return response.data
    })
}

export function reportQuesAPI(quesId, reportReason) {
    return axios.request(
        {
            url: '/reportQues',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                quesId: quesId,
                reportReason: reportReason
            })
        }
    ).then(response => {
        return response.data
    })
}

export function reportAnswerAPI(quesId, ansId, reportReason) {
    return axios.request(
        {
            url: '/reportAnswer',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                quesId: quesId,
                ansId: ansId,
                reportReason: reportReason
            })
        }
    ).then(response => {
        return response.data
    })
}

export function isShutUpByUserIdAPI(userId) {
    return axios.request(
        {
            url: '/isShutUpByUserId',
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            data: JSON.stringify({
                id: userId,
            })
        }
    ).then(response => {
        return response.data
    })
}
