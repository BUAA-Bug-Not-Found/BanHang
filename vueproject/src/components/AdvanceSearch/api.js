import axios from "axios";

export function searchBlogAPage(searchContent, pageno, pagesize, nowSortMethod) {
    return axios.request({
        url: '/search/searchBlogAPage',
        method: "post",
        headers: {'Content-Type': 'application/json'},
        data: JSON.stringify({
            searchContent: searchContent,
            pageno: pageno,
            pagesize: pagesize,
            nowSortMethod: nowSortMethod,
        })
    }).then(response => {
        return response.data
    })
}

export function searchQuesAPage(searchContent, pageno, pagesize, nowSortMethod) {
    return axios.request({
        url: '/searchQuesAPage',
        method: "post",
        headers: {'Content-Type': 'application/json'},
        data: JSON.stringify({
            searchContent: searchContent,
            pageno: pageno,
            pagesize: pagesize,
            nowSortMethod: nowSortMethod,
        })
    }).then(response => {
        return response.data
    })
}

export function searchUserAPage(searchContent, pageno, pagesize, nowSortMethod) {
    return axios.request({
        url: '/searchUserAPage',
        method: "post",
        headers: {'Content-Type': 'application/json'},
        data: JSON.stringify({
            searchContent: searchContent,
            pageno: pageno,
            pagesize: pagesize,
            nowSortMethod: nowSortMethod,
        })
    }).then(response => {
        return response.data
    })
}
