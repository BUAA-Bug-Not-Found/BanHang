<template>
    <v-container>
      <v-dialog v-model="showShutUpDialog" style="max-width: 400px;">
        <v-card>
            <v-card-title class="headline" style="text-align: center;">禁言时间</v-card-title>
            <v-divider></v-divider>
            <div style="margin-top: 20px; padding-left: 10px; padding-right: 10px;">
                <v-autocomplete
                    v-model="selectedDays"
                    :items="days"
                    label="选择天数"
                    outlined
                ></v-autocomplete>
                <v-autocomplete
                    v-model="selectedHours"
                    :items="hours"
                    label="选择小时数"
                    outlined
                ></v-autocomplete>
                <v-autocomplete
                    v-model="selectedMinutes"
                    :items="minutes"
                    label="选择分钟数"
                    outlined
                ></v-autocomplete>
            </div>
            <div style="text-align: center; margin-top: 10px;">
                <v-btn color="blue darken-1" @click="clickCertainShutUp" style="margin-bottom: 10px; max-width: 50%;">确定</v-btn>
                <v-btn color="blue darken-1" @click="showShutUpDialog = false" style="margin-left: 7px; margin-bottom: 10px; max-width: 50%;">取消</v-btn>
            </div>
        </v-card>
      </v-dialog>

      <v-card>
        <v-tabs
          v-model="tab"
          color="blue"
          fixed-tabs
        >
          <v-tab value="one">待处理举报项详情</v-tab>
          <!-- <v-tab value="two">匿名区举报</v-tab> -->
        </v-tabs>
        
        <v-card-text>
          <v-window v-model="tab">
            <v-window-item value="one">
              <v-list>
                <v-list-item v-for="(content, index) in helpInfos" :key="index" @click="clickItem(content.blogId, content.isAno)" style="cursor: pointer; margin-bottom: 10px;">
                    <div style="text-align: left; margin-bottom: 5px;">
                        <div v-if="content.isComment" style="display: inline-block; margin-right: 5px; width: 50px; background-color: #a4ffa1; text-align: center; margin-bottom: 7px; border-radius: 3px;">
                            <span style="font-size: 10px;  color: black; padding: 2px;">评论举报</span>
                        </div>
                        <div v-else style="display: inline-block; margin-right: 5px; width: 50px; background-color: #9ae5ff; text-align: center; margin-bottom: 7px; border-radius: 3px;">
                            <span style="font-size: 10px;  color: black; padding: 2px;">帖子举报</span>
                        </div>

                        <div v-if="content.isAno" style="display: inline-block; width: 60px; background-color: #efff8d; text-align: center; margin-bottom: 7px; border-radius: 3px;">
                            <span style="font-size: 10px;  color: black; padding: 2px;">匿名区举报</span>
                        </div>
                        <div v-else style="display: inline-block; width: 60px; background-color: #ffb9f4; text-align: center; margin-bottom: 7px; border-radius: 3px;">
                            <span style="font-size: 10px;  color: black; padding: 2px;">互助区举报</span>
                        </div>
                        <v-space></v-space>
                        <!-- <div style="display: inline-block; text-align: right; vertical-align: center;">
                            <span>222</span>
                        </div> -->
                    </div>
                    <div v-if="content.isAno" style="text-align: left; margin-bottom: 8px;">
                        <v-text style="vertical-align: middle; font-size: 18px; font-weight: bold;">{{ content.blogTitle }}</v-text>
                    </div>
                    <div style="text-align: left; font-size: 15px;">{{ truncate(content.blogContent) }}</div>
                    <div v-if="content.isComment">
                        <div style="height: 1px; background-color: #e7ecff; width: 60px; margin-top: 10px; margin-bottom: 5px;"></div>
                        <div style="text-align: left;">
                            <span style="font-weight:bold">评论内容：</span>
                            <span>{{ content.comment }}</span>
                        </div>
                    </div>
                    <div style="height: 1px; background-color: #e7ecff; width: 60px; margin-top: 10px; margin-bottom: 5px;"></div>
                    <div style="text-align: left;">
                        <span style="font-weight:bold">举报理由：</span>
                        <span>{{ content.cause }}</span>
                    </div>
                    
                    <div style="text-align: right; margin-top: 10px; margin-bottom: 5px;">
                        <v-text class="time" style="color: grey; margin-right: 5px;">{{ this.formatDateTime(content.time) }}</v-text>
                    </div>
                    <div style="margin-bottom: 10px; text-align: left;">
                        <v-btn style="vertical-align: center; background-color: #f6f6f6;" @click.stop="clickDeleteComplain(index)">
                            <div>
                                <span>已处理本项</span>
                                <span style="color:red"> {{ complainAmount }}</span>
                            </div>
                        </v-btn>
                        <v-btn v-if="content.isComment" style="margin-left: 5px; vertical-align: center; background-color: #f6f6f6;" @click.stop="clickDeleteComment(content.commentId, content.isAno)">
                            <div>
                                <span>删除此评</span>
                                <span style="color:red"> {{ complainAmount }}</span>
                            </div>
                        </v-btn>
                        <v-btn v-else style="margin-left: 5px; vertical-align: center; background-color: #f6f6f6;" @click.stop="clickDeleteBlog(content.blogId, content.isAno)">
                            <div>
                                <span>删除此帖</span>
                                <span style="color:red"> {{ complainAmount }}</span>
                            </div>
                        </v-btn>
                        <v-btn v-if="content.isComment" style="margin-left: 5px; vertical-align: center; background-color: #f6f6f6;" @click.stop="clickTryShutUp(content.commentAuthorId)">
                            <div>
                                <span>禁言发评人</span>
                                <span style="color:red"> {{ complainAmount }}</span>
                            </div>
                        </v-btn>
                        <v-btn v-else style="margin-left: 5px; vertical-align: center; background-color: #f6f6f6;" @click.stop="clickTryShutUp(content.blogAuthorId)">
                            <div>
                                <span>禁言发贴人</span>
                                <span style="color:red"> {{ complainAmount }}</span>
                            </div>
                        </v-btn>
                    </div>
                    <v-divider></v-divider>
                </v-list-item>
              </v-list>
            </v-window-item>
          </v-window>
        </v-card-text>
      </v-card>
    </v-container>
  </template>

<script>
import { showTip } from '../AccountManagement/AccountManagementAPI';
// import userStateStore from '@/store';
import router from '@/router';
import { checkLogin } from '../AccountManagement/AccountManagementAPI';
import { delAnswerAPI, delQuestionAPI } from '../HelpCenter/api';
import { deleteComplainItem, getComplainList, shutUpUser } from './PersonalCenterAPI';
import { deleteBlogByBlogId, deleteCommentByCommentId } from '../AnonymousBlog/api';

export default {
    components: { },
    created() {
      // 检查是否是管理员
      checkLogin(true);
      // 加载两类举报消息列表：互助/匿名 + 帖子/评论
      getComplainList().then((r) => {
        if (r === false) 
            showTip("您不是管理员或出现异常！", false)
        else {
            this.helpInfos = r
        }
      })
    },
    data() {
        return {
            tab: 'one',
            showShutUpDialog: false,
            days: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29], // 0, 1, 2, 3, 4, 5,6,7,8,9,10,11,12
            hours: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
            minutes: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59],
            selectedDays: 0,
            selectedHours: 0,
            selectedMinutes: 0,
            currentShutUpId: 0,
            helpInfos: [
                {
                    "complainId": 0,
                    "blogTitle": "", // 如果是匿名区举报，匿名贴有title要返回
                    "blogId": 7, // 举报对应的帖子id
                    "blogContent": "捞人教教python", // 帖子的内容
                    "commentId": 0, // 评论id, 如果不是举报评论则随便返回一个值即可(不会用到这个值)
                    "comment": "滚!", // 评论内容
                    "blogAuthorId": 0, // 发帖人的id, 非举报帖子则值随便取
                    "commentAuthorId": 0, // 评论人的id, 非举报评论则值随便取
                    "cause": "他连python都不会", // 举报的原因
                    "time": "", // 发起举报的时间
                    "isComment": false, // 是否是对评论的举报
                    "isAno": false // 是否是匿名区举报
                },
                {
                    "complainId": 0, // 加id, 便于删除
                    "blogTitle": "", // 如果是匿名区举报，匿名贴有title要返回
                    "blogId": 7, // 举报对应的帖子id
                    "blogContent": "捞人教教python", // 帖子的内容
                    "commentId": 0, // 评论id, 如果不是举报评论则随便返回一个值即可(不会用到这个值)
                    "comment": "滚!", // 评论内容
                    "blogAuthorId": 0, // 发帖人的id, 非举报帖子则值随便取
                    "commentAuthorId": 0, // 评论人的id, 非举报评论则值随便取 "cause": "乱说脏话", // 举报的原因
                    "cause": "说脏话",
                    "time": "", // 发起举报的时间
                    "isComment": true, // 是否是对评论的举报
                    "isAno": false // 是否是匿名区举报
                },
                {
                    "complainId": 0, // 加id, 便于删除
                    "blogTitle": "匿名举报！！", // 如果是匿名区举报，匿名贴有title要返回
                    "blogId": 7, // 举报对应的帖子id
                    "blogContent": "捞人教教python", // 帖子的内容
                    "commentId": 0, // 评论id, 如果不是举报评论则随便返回一个值即可(不会用到这个值)
                    "comment": "滚!", // 评论内容
                    "blogAuthorId": 0, // 发帖人的id, 非举报帖子则值随便取
                    "commentAuthorId": 0, // 评论人的id, 非举报评论则值随便取 "cause": "乱说脏话", // 举报的原因
                    "cause": "说脏话",
                    "time": "", // 发起举报的时间
                    "isComment": true, // 是否是对评论的举报
                    "isAno": true // 是否是匿名区举报
                },
                {
                    "complainId": 0, // 加id, 便于删除
                    "blogTitle": "匿名举报xxx！！", // 如果是匿名区举报，匿名贴有title要返回
                    "blogId": 7, // 举报对应的帖子id
                    "blogContent": "把猫猫的头割下来何尝不是一种乐趣呢", // 帖子的内容
                    "commentId": 0, // 评论id, 如果不是举报评论则随便返回一个值即可(不会用到这个值)
                    "comment": "滚!", // 评论内容
                    "blogAuthorId": 0, // 发帖人的id, 非举报帖子则值随便取
                    "commentAuthorId": 0, // 评论人的id, 非举报评论则值随便取 "cause": "乱说脏话", // 举报的原因
                    "cause": "他这条帖子在虐待猫！",
                    "time": "", // 发起举报的时间
                    "isComment": false, // 是否是对评论的举报
                    "isAno": true // 是否是匿名区举报
                },
            ],
        }
    },
    methods: {
        clickCertainShutUp() {
            if (this.selectedDays == 0 && this.selectedHours == 0 && this.selectedMinutes == 0) {
                showTip("禁言时长不能为0！", false)
                this.showShutUpDialog = false
            } else {
                this.showShutUpDialog = false
                // 开始调后端
                shutUpUser(this.currentShutUpId,
                this.selectedDays,
                this.selectedHours,
                this.selectedMinutes).then((r) => {
                    if (r === true)
                        showTip("禁言成功！", true)
                    else 
                        showTip("出现异常，禁言失败！", false)
                }).catch(() => { showTip("出现异常，禁言失败！", false) })
            }
        },
        clickItem(_blogId, isAno) { // 可能是匿名贴
            if (isAno)
                router.push({name: 'blogView', params: {id: _blogId}});
            else
                router.push('/QuesInfo/' + _blogId + "/0");
        },
        clickDeleteComplain(index) {
            // 删除index对应的项
            deleteComplainItem(this.helpInfos[index].complainId).then((r) => {
                if (r.isSuccess) {
                    // 前端也删了
                    this.helpInfos.splice(index, 1);
                    showTip("删除成功！", true);
                }
                else
                    showTip("出现异常，删除失败！", false)
            }).catch(() => { showTip("出现异常，删除失败！", false) })
        },
        clickDeleteComment(commentId, isAno) {
            if (isAno) {
                deleteCommentByCommentId(commentId).then((res) => {
                    if (res.response == 'success')
                        showTip("删除回复成功！", true)
                    else 
                        showTip("出现异常，删除失败！", false)
                }).catch(() => {
                    showTip("出现异常，删除失败！", false)
                })
            } else {
                delAnswerAPI(commentId).then((res) => {
                    if (res.isSuccess)
                        showTip("删除回复成功！", true)
                    else 
                        showTip("出现异常，删除失败!", false)
                }).catch(() => {
                    showTip("出现异常，删除失败!", false)
                })
            }
        },
        clickDeleteBlog(blogId, isAno) {
            if (isAno) {
                deleteBlogByBlogId(blogId).then((r) => {
                    if (r.response == 'success')
                        showTip('删除成功！', true)
                    else 
                        showTip("出现异常，删除失败！", false)
                }).catch(() => {
                    showTip("出现异常，删除失败！", false)
                })
            } else {
                delQuestionAPI(blogId).then((res) => {
                    if (res.isSuccess)
                        showTip("删除成功！", true)
                    else 
                        showTip("出现异常，删除失败！", false)
                }).catch(() => {
                    showTip("出现异常，删除失败！", false)
                })
            }
        },
        clickTryShutUp(userId) {
            // 弹出弹窗
            this.showShutUpDialog = true
            this.currentShutUpId = userId
        },
        truncate(content) {
            const strippedContent = String(content).replace(/<[^>]*>/g, "")
            if (strippedContent.length > 20) {
            return `${strippedContent.slice(0, 20)}...`;
            }
            return strippedContent;
        },
        formatDateTime(dateTimeStr) {
            // 创建 Date 对象
            const dateTime = new Date(dateTimeStr);
            
            // 提取年月日时分秒
            const year = dateTime.getFullYear();
            const month = String(dateTime.getMonth() + 1).padStart(2, '0');
            const date = String(dateTime.getDate()).padStart(2, '0');
            const hours = String(dateTime.getHours()).padStart(2, '0');
            const minutes = String(dateTime.getMinutes()).padStart(2, '0');
            const seconds = String(dateTime.getSeconds()).padStart(2, '0');
            
            // 拼接成目标格式的字符串
            const formattedDateTime = `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`;
            
            return formattedDateTime;
        },
    }
}
</script>

<style scoped>


</style>