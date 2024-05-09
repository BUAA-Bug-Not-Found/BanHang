import axios from "axios";
// import {getInfoByUserId} from "@/components/AccountManagement/AccountManagementAPI";

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
        headers: {'Content-Type': 'application/json'},
        data: JSON.stringify({
            pageno: pageno,
            pagesize: pagesize,
            nowTag: nowtag
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
        headers: {'Content-Type': 'application/json'},
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
        headers: {'Content-Type': 'application/json'},
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
            headers: {'Content-Type': 'application/json'},
        }).then(response => {
        return response.data
    })
}

export function uploadComment(commentData) {
    return axios.post('/blog/uploadComment', commentData,
        {
            headers: {'Content-Type': 'application/json'},
        }).then(response => {
        return response.data
    })
}

export function deleteBlogByBlogId(blogId) {
    return axios.request({
        url: '/blog/deleteBlogByBlogId',
        method: "post",
        headers: {'Content-Type': 'application/json'},
        data: JSON.stringify({
            blogId: blogId
        })
    }).then(response => {
        return response.data
    })
}

export function getALlBlogTags() {
    return axios.request({
        url: '/blog/getAllBlogTags',
        method: "post",
        headers: {'Content-Type': 'application/json'},
    }).then(response => {
        return response.data
    })
}

export function goToOtherUser(otherUserId) {
    // let otherUserEmail = null
    // getInfoByUserId(otherUserId).then((info) => {
    //     if (info == "false") {
    //         otherUserEmail = null
    //     } else {
    //         otherUserEmail = info.email
    //         this.$router.push({name: 'othersCenter', params: {"e": otherUserEmail}})
    //     }
    // })
    this.$router.push({name: 'othersCenter', params: {"id": otherUserId}})
}

export async function getTags() {
    try {
        const data = await getALlBlogTags();
        const tags = data.map(tag => ({
            tagId: tag.tagId,
            tagName: tag.tagName,
            tagColor: tag.tagColor,
            tagIcon: tag.tagIcon
        }));
        return tags;
    } catch (error) {
        // 处理错误
        console.error("Failed to get tags:", error);
        throw error;
    }
}
