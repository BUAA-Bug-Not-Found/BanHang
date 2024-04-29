const { defineConfig } = require('@vue/cli-service')

//const isLocal = false
//const targetUrl = isLocal ? "http://0.0.0.0:8000 " : "http://lyhtool.tpddns.cn:8000"
//
//module.exports = defineConfig({
//  transpileDependencies: true,
//  devServer: {
//    host: '0.0.0.0',
//    port: 8080,
//    open: true,// vue项目启动时自动打开浏览器
//    proxy: {
//      '/api': { // '/api'是代理标识，用于告诉node，url前面是/api的就是使用代理的
//        target: targetUrl, //目标地址，一般是指后台服务器地址
//        changeOrigin: true, //是否跨域
//        pathRewrite: { // pathRewrite 的作用是把实际Request Url中的'/api'用""代替
//          '^/api': ""
//        }
//      }
//    }
//  }
//})
