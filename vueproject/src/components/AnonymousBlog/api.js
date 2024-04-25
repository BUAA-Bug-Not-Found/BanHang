import axios from "axios";

export function uploadfile(file) {
    return axios.post('/uploadfile', file,
        {
            headers: {'Content-Type': 'multipart/form-data'}
        }).then(response => {
        return response.data
    })
}

export function getBlogs(pageno, pagesize, nowtag) {
    return axios.request({
        url: '/blog/getBlogs',
        method: "post",
        data: JSON.stringify({
            pageno: pageno,
            pagesize: pagesize,
            nowtag: nowtag
        })
    }).then(response => {
        return response.data
    })
}

// export function getUserByBlogId(blogId) {
//     return axios.request({
//         url: '/blog/getUserByBlogId',
//         method: "post",
//         data: JSON.stringify({
//             blogId: blogId
//         })
//     }).then(response => {
//         return response.data
//     })
// }

export function getBlogByBlogId(blogId) {
    return axios.request({
        url: '/blog/getBlogByBlogId',
        method: "post",
        data: JSON.stringify({
            blogId: blogId
        })
    }).then(response => {
        return response.data
    })
}

export function getCommentsByBlogId(blogId) {
    return axios.request({
        url: '/blog/getCommentsByBlogId',
        method: "post",
        data: JSON.stringify({
            blogId: blogId
        })
    }).then(response => {
        return response.data
    })
}

// export function getUserByCommentId(commentId) {
//     return axios.request({
//         url: '/blog/getUserByCommentId',
//         method: "post",
//         data: JSON.stringify({
//             commentId: commentId
//         })
//     }).then(response => {
//         return response.data
//     })
// }

export function uploadBlog(blogData) {
    return axios.post('/blog/uploadBlog', blogData,
        {
            headers: {'Content-Type': 'multipart/form-data'}
        }).then(response => {
        return response.data
    })
}

export function uploadComment(commentData) {
    return axios.post('/blog/uploadComment', commentData,
        {
            headers: {'Content-Type': 'multipart/form-data'}
        }).then(response => {
        return response.data
    })
}