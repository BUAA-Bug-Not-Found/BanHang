<template>
  <v-container>
    <v-dialog v-model="showDialog" max-width="300px">
      <v-card>
        <v-card-title class="headline">确认操作</v-card-title>
        <v-card-text>
          确定要退出登录吗？
        </v-card-text>
        <v-card-actions>
          <v-btn color="error" @click="clickQuitLogin">确认</v-btn>
          <v-btn color="blue darken-1" @click="showDialog = false">取消</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="isShowBadgeDesc" max-width="300px">
      <v-card style="padding-bottom:12px;">
        <v-card-title class="d-flex justify-space-between align-center" style="padding-bottom:0; padding-top:0;">
            <span style="color: #2a9af3;font-size: 15px">
              徽章描述
            </span>
          <v-btn
              icon="mdi-close"
              variant="text"
              @click="isShowBadgeDesc = false"
          ></v-btn>
        </v-card-title>

        <v-divider></v-divider>
        <span style="margin-left:14px; color:grey; margin-top:8px;">
            {{ curDesc }}
          </span>
          <div style="justify-content:center; align-items:center; text-align:center;">
            <v-btn @click="clickDelBadge" style="width:50%; background-color:#2a9af3; color:aliceblue; margin-top:16px; width:auto; height:30px;">删除本徽章</v-btn>
          </div>
          <!-- <v-card-actions>
          <v-btn color="error" @click="clickQuitLogin">确认</v-btn>
          <v-btn color="blue darken-1" @click="showDialog = false">取消</v-btn>
        </v-card-actions> -->
      </v-card>
    </v-dialog>

    <v-dialog
        v-model="buyBadgeDialog"
        max-width="480"
    >
      <v-card title="购买勋章">
        <template v-slot:text>
          <v-row>
            <v-col cols="8" offset="2">
              <div style="margin: 10px" elevation="1">
                <v-row justify="center" style="margin-top: 10px">
                  <v-avatar color="surface-variant"
                            style="margin-top: 5px; margin-bottom: 10px;"
                            size="200"
                            :image="currentBuyBadge.badgeUrl">
                  </v-avatar>
                </v-row>
                <div style="width: 100%;display: flex;justify-content: center;">
                  <v-tooltip :text="currentBuyBadge.badgeDesc">
                    <template v-slot:activator="{ props }">
                      <v-chip
                          class="ma-2"
                          :style="{ color: currentBuyBadge.badgeColor }"
                          v-bind="props"
                          label
                      >
                        {{ currentBuyBadge.badgeName }}
                      </v-chip>
                    </template>
                  </v-tooltip>
                </div>
              </div>
            </v-col>
          </v-row>
        </template>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
              text="确定购买"
              variant="text"
              @click="uploadBuyBadge()"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="badgeDialog" max-width="500px">
      <template v-slot:default="{ isActive }">
        <v-card rounded="lg" height="800">
          <v-card-title class="d-flex justify-space-between align-center">
            <div class="ps-2" style="color: deepskyblue;align-content: center;font-size: 20px">
              <v-icon :size="30" style="margin-right: 5px">mdi-square-rounded-badge-outline</v-icon>
              获取徽章
            </div>
            <v-btn
                icon="mdi-close"
                variant="text"
                @click="isActive.value = false"
            ></v-btn>
          </v-card-title>

          <v-divider class="mb-4"></v-divider>
          <v-card-text>
            <v-tabs
                v-model="tab2"
                align-tabs="center"
                color="deep-purple-accent-4"
                style="margin-bottom: 10px"
            >
              <v-tab :value="1">勋章商城</v-tab>
              <v-tab :value="2">自定义勋章</v-tab>
            </v-tabs>

            <v-window v-model="tab2" height="700" class="overflow-y-auto">
              <v-window-item
                  :value="1"
              >
                <v-row>
                  <v-col :cols="useDisplay().smAndDown.value? 6 : 4" v-for="badge in mall_badges" :key="badge.badgeId">
                    <v-card style="margin: 10px" elevation="1">
                      <v-row justify="center" style="margin-top: 10px">
                        <v-avatar color="surface-variant"
                                  style="margin-top: 5px; margin-bottom: 10px;"
                                  size="100"
                                  :image="badge.badgeUrl">
                        </v-avatar>
                      </v-row>
                      <div style="width: 100%;display: flex;justify-content: center;">
                        <v-tooltip :text="badge.badgeDesc">
                          <template v-slot:activator="{ props }">
                            <v-chip
                                size="small"
                                class="ma-2"
                                :style="{ color: badge.badgeColor }"
                                v-bind="props"
                                label
                            >
                              {{ badge.badgeName }}
                            </v-chip>
                          </template>
                        </v-tooltip>
                      </div>
                    </v-card>
                    <div style="width: 100%;display: flex;justify-content: center;">
                      <v-btn prepend-icon="mdi-star-four-points-circle-outline" size="small" color="primary"
                             @click="buyBadge(badge)">
                        <span v-if="badge.badgeCost != 0">
                          {{ badge.badgeCost }}
                        </span>
                        <span v-else>
                          免费获取
                        </span>
                      </v-btn>
                    </div>
                  </v-col>
                </v-row>
                <div style="height: 100px"></div>
              </v-window-item>

              <v-window-item
                  :value="2"
              >
                <div class="mb-2"
                     style="width: 100%;display: flex;font-weight: bold;
                   font-size: 18px;margin-bottom: 3px"
                >
                  预览效果：
                </div>
                <v-row>
                  <v-col :cols="useDisplay().smAndDown.value? 6 : 4" :offset="useDisplay().smAndDown.value? 3 : 4">
                    <el-form :style="'width: 100%'">
                      <el-upload
                          class="avatar-uploader1"
                          action="#"
                          :show-file-list="false"
                          :auto-upload="false"
                          :on-change="handleChange"
                          accept=".jpg,.png"
                      >
                        <el-icon v-if="badgeSrc === ''" class="avatar-uploader-icon1">
                          <Plus/>
                        </el-icon>
                        <el-image
                            v-else
                            class="avatar1"
                            :src="badgeSrc"
                            :fit="'cover'"
                        />
                      </el-upload>
                    </el-form>
                  </v-col>
                </v-row>
                <div style="width: 100%;display: flex;justify-content: center;">
                  <v-tooltip :text="badgeDescription">
                    <template v-slot:activator="{ props }">
                      <v-chip
                          class="ma-2"
                          :style="{ color: badgeColor }"
                          v-bind="props"
                          label
                      >
                        {{ badgeName }}
                      </v-chip>
                    </template>
                  </v-tooltip>
                </div>
                <v-color-picker v-model="badgeColor" hide-inputs hide-canvas
                                style="margin: 10px;margin-left: 5px;"></v-color-picker>
                <div class="mb-2">
                  徽章名：
                  <el-input v-model="badgeName" style="width: 150px" maxlength="4"
                            placeholder="请输入徽章名" show-word-limit/>
                </div>
                <div class="mb-2">徽章描述：
                  <el-input v-model="badgeDescription" style="width: 250px" maxlength="10"
                            placeholder="请输入徽章介绍" show-word-limit/>
                </div>

                <v-divider class="mt-2"></v-divider>
                <v-card-actions class="my-2 d-flex justify-end">
                  <v-btn
                      class="text-none"
                      rounded="xl"
                      text="取消"
                      @click="isActive.value = false"
                  ></v-btn>

                  <v-btn
                      class="text-none"
                      color="primary"
                      :prepend-icon="'mdi-star-four-points-circle-outline'"
                      text="1000 创建"
                      variant="flat"
                      @click="uploadBadge"
                  ></v-btn>
                </v-card-actions>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </template>
    </v-dialog>

    <div>
      <v-card style="margin-bottom: 20px; height: auto;">
        <!-- div好像是行内的 -->
        <div style="text-align: center;">
          <v-toolbar density="compact" style="background-color:aliceblue;">
            <v-btn v-if="this.isManager"
                   style="height: 28px; padding-left: 6px; padding-right: 6px; vertical-align: center; background-color: #2a9af3;"
                   @click="clickComplain">
              <div style="display: flex;">
                <span style="color:white; font-size: 12px;">待处理 </span>
                <span v-if="complainAmount !== '0'"
                      style="font-weight: bold; color:aquamarine; font-size: 14px;"> {{ complainAmount }}</span>
                <span v-if="complainAmount !== '0'" style="color:white; font-size: 12px;"> 项</span>
              </div>
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
                :color="'success'"
                :prepend-icon="'mdi-square-rounded-badge-outline'"
                :text="'获取徽章'"
                @click="badgeDialog=true"
                class="text-none"
                size="small"
                variant="flat"
                flat
            ></v-btn>

            <v-btn icon @click="clickMyInterest">
              <v-icon color="red">mdi-heart</v-icon>
            </v-btn>

            <v-btn icon @click="clickUpdateInfo">
              <v-icon color="blue">mdi-pencil</v-icon>
            </v-btn>

            <v-btn icon @click="showDialog = true">
              <v-icon color="grey">mdi-logout</v-icon>
            </v-btn>
          </v-toolbar>
        </div>

        <div style="text-align: center;">
          <v-menu rounded>
            <template v-slot:activator="{ props }">
              <v-avatar v-bind="props" color="surface-variant"
                        style="margin-top: 15px;margin-left: 10px; cursor: pointer;"
                        size="80"
                        :image="headUrl">
              </v-avatar>
            </template>

            <!-- <v-card style="width: 330px;"> -->
            <v-card style="width: auto;">
              <v-card-text>
                <div style="display: flex; align-items: center;">
                  <span style="font-weight: bold; color:red;">Lv.{{ level }}</span>
                  <v-progress-linear style="margin-left: 10px; margin-right: 10px;"
                                     :model-value="100.0 * (currentExperience / (currentExperience + experienceNeeded))"
                                     color="success" height="5"></v-progress-linear>
                  <span style="font-weight: bold; color:grey;">Lv.{{ level + 1 }}</span>
                </div>
                <span style="font-size: 13px; color: grey; margin-top: 10px;">您已经获得{{ currentExperience }}经验, 距离下一级还需{{
                    experienceNeeded
                  }}经验</span>
              </v-card-text>
            </v-card>
          </v-menu>

        </div>
        <div style="margin-top: 10px;">
          <div style="display: flex; align-items: center; text-align: center; justify-content: center;">
            <span class="nickname"> {{ nickname }}</span>
            <span
                style="padding-left: 3px; padding-right: 3px; border-radius: 3px; margin-left: 5px; background-color:bisque; font-weight:bold; color:#2a9af3; font-size: 12px;">Lv.{{
                level
              }}</span>
          </div>

        </div>
        <div style="margin-bottom: 10px; font-size: 10px; text-align: center;">
          <span class="signature">{{ sign }}</span>
        </div>

        <v-container v-if="badges" style="display:flex; justify-content:center; padding-top:0px;">
          <v-slide-group show-arrows>
            <v-slide-item
                v-for="(content, index) in badges"
                :key="content.badgeId"
                :style="'padding:4px;'"
            >
              <v-card outlined @click="clickBadge(index)" style="cursor:pointer">
                <div style="align-items: center; display: flex; flex-direction: column; margin:10px;">
                  <v-avatar color="surface-variant"
                            style="margin-top: 5px; margin-bottom: 10px;"
                            size="70"
                            :image="content.badgeUrl">
                  </v-avatar>
                  <v-chip
                      :style="{ color: content.badgeColor, fontSize:'10px', height: '20px', paddingTop: '2px', paddingLeft: '6px', paddingRight: '6px', verticalAlign: 'middle' }"
                      label>
                    {{ content.badgeName }}
                  </v-chip>

                  <!-- <div style="display:flex; align-items:center;">
                    <span style="font-size:12px; color:grey;">{{ content.badgeDesc }}</span>
                  </div> -->
                </div>
              </v-card>
            </v-slide-item>
          </v-slide-group>
        </v-container>
      </v-card>
    </div>
    <!-- 个人动态区域 -->
    <v-card>
      <v-tabs
          v-model="tab"
          color="blue"
          fixed-tabs
      >
        <v-tab value="one">匿名贴</v-tab>
        <v-tab value="two">互助贴</v-tab>
        <!-- <v-tab value="three">我的徽章</v-tab> -->
      </v-tabs>

      <v-card-text>
        <v-window v-model="tab">
          <!-- 该window展示匿名贴的内容 -->
          <v-window-item value="one">
            <v-list>
              <v-list-item v-for="(content, index) in waterBlogs.slice().reverse()" :key="index"
                           @click="clickWaterItem(content.blogId)" style="cursor: pointer;">
                <div style="text-align: left;">
                  <v-text style="vertical-align: middle; font-size: 18px; font-weight: bold;">{{
                      content.blogTitle
                    }}
                  </v-text>
                </div>
                <div style="text-align: left; margin-top: 10px;">
                  <v-text style="vertical-align: middle; font-size: 12px; color: grey;">{{ content.blogText }}</v-text>
                </div>
                <div style="text-align: right; margin-top: 10px;">
                  <v-text class="time" style=" margin-right: 5px;">{{ this.formatDateTime(content.time) }}</v-text>
                </div>
                <!-- 分隔线 -->
                <v-divider style="margin-top: 0px;"></v-divider>
              </v-list-item>
            </v-list>
          </v-window-item>
          <!-- 该window展示互助贴的内容 -->
          <v-window-item value="two">
            <v-list>
              <v-list-item v-for="(content, index) in helpBlogs.slice().reverse()" :key="index"
                           @click="clickHelpItem(content.blogId)" style="cursor: pointer;">
                <div style="text-align: left;">{{ truncate(content.blogTitle) }}</div>
                <div style="text-align: right; margin-top: 10px;">
                  <v-text class="time" style=" margin-right: 5px;">{{ this.formatDateTime(content.time) }}</v-text>
                </div>
                <v-divider style="margin-top: 0px;"></v-divider>
              </v-list-item>
            </v-list>
          </v-window-item>
          <!-- 该window展示徽章的详细信息 -->
          <!-- <v-window-item value="three">
            <v-list>
              <v-list-item v-for="(content, index) in badges" :key="index">
                <div style="align-items: center; display: flex; flex-direction: column;">
                  <v-chip
                    class="ma-2"
                    :style="{ color: content.badgeColor }"
                    label
                  >
                    {{ content.badgeName }}
                  </v-chip>
                  <v-avatar color="surface-variant"
                    style="margin-top: 0px;"
                    size="100"
                    :image="content.badgeUrl">
                  </v-avatar>
                  <div style="display:flex; align-items:center;">
                    <span style="font-size:12px; color:grey;">{{ content.badgeDesc }}</span>
                  </div>
              </div>
                <v-divider style="margin-top: 10px;"></v-divider>
              </v-list-item>
            </v-list>
          </v-window-item> -->
        </v-window>
      </v-card-text>

    </v-card>
  </v-container>
</template>

<script>
import router from '@/router';
import userStateStore from '../../store';
import {
  delUserBadge,
  getBadges,
  getBadgesByUserId,
  getComplainAmount,
  getCurrentExpById,
  getCurrentLevelById,
  getHelpBlogs,
  getWaterBlogs,
  uploadBadgeAPI, uploadBuyBadge
} from "./PersonalCenterAPI";
import {showTip} from '../AccountManagement/AccountManagementAPI';
import {api as viewerApi} from "v-viewer";
import {ElMessage} from "element-plus";
import {Plus} from "@element-plus/icons-vue";
import {uploadFileApi} from "@/components/HelpCenter/api";
import {useDisplay} from "vuetify";

export default {
  components: {Plus},
  created() {
    // 这里放置需要延迟执行的代码
    this.headUrl = userStateStore().headImage;
    this.nickname = userStateStore().nickname;
    this.email = userStateStore().email;
    this.sign = userStateStore().sign;
    this.isManager = userStateStore().isManager;
    if (!this.email) {
      showTip("请首先登录", false)
      router.replace({path: "loginPage"})
    }
    if (this.sign === "" || !this.sign) {
      this.sign = "快介绍一下自己吧~"
    }
    // 加载一下匿名贴和互助贴

    getBadges().then(
        (res) => {
          this.mall_badges = res.badges
        }
    )


    getHelpBlogs(userStateStore().user_id).then((res) => {
      this.helpBlogs = res
    })

    getWaterBlogs(userStateStore().user_id).then((res) => {
      this.waterBlogs = res
    })

    // getBadgesByUserId(userStateStore().user_id, false).then((res) => {
    getBadgesByUserId(userStateStore().user_id).then(
        (res) => {
          if (res) {// 出现错误那就是空数组就可以了
            this.badges = res
          }
        }
    )

    Promise.all([
      getCurrentLevelById(userStateStore().user_id),
      getCurrentExpById(userStateStore().user_id)
    ]).then(rets => {
      if (rets[0] === false) this.level = 0
      else this.level = rets[0]
      if (rets[1] === false) this.currentExperience = 0
      else this.currentExperience = rets[1]
      let exps = [0, 100, 500, 1500, 3000, 6000, 10500, 18000, 30000, 54000, 54000] // 经验阈值
      this.experienceNeeded = exps[this.level + 1] - this.currentExperience
    }).catch(() => {
      showTip("出现异常！", false)
    })

    // 加载待处理举报信息条数
    if (this.isManager) {
      getComplainAmount().then((res) => {
        if (res.count == 0)
          this.complainAmount = "0" // 0条的话就不显示了
        else if (res.count <= 99)
          this.complainAmount = res.count;
        else
          this.complainAmount = "99+"
      })
    }
  },
  data() {
    return {
      tab: 'one', // 这里指定一个默认值, 上面点了才会有效果
      headUrl: "",
      nickname: "",
      email: "",
      sign: "",
      level: 4, // 当前等级
      currentExperience: 8685, // 当前经验值
      experienceNeeded: 2115, // 升级所需的经验值
      // expPercent: ,
      isManager: false,
      complainAmount: "", // 待处理的举报信息数量, 显示
      showDialog: false,
      badgeDialog: false,
      badgeImage: "",
      badgeSrc: "",
      isShowBadgeDesc: false,
      curDesc: "",
      curBadgeId: 0,
      curBadgeIndex: -1,
      posts: [
        {content: "这是第一条动态"},
      ],
      helpBlogs: [],
      waterBlogs: [],
      badges: [],
      mall_badges: [],
      images: [
        'https://via.placeholder.com/150',
        // 添加更多图片链接...
      ],
      badgeDescription: '',
      badgeName: '',
      badgeColor: '#ff4500',
      badgeCost: 1000,
      tab2: 1,
      buyBadgeDialog: false,
      currentBuyBadge: ''
    };
  },
  methods: {
    useDisplay,
    clickDelBadge() {
      // 删除掉curBadgeId
      delUserBadge(this.curBadgeId).then((r) => {
        if (r == false) {
          this.isShowBadgeDesc = false
          showTip("出现异常，操作失败！", false)
        } else {
          // 维护前端显示
          this.badges.splice(this.curIndex, 1);
          this.isShowBadgeDesc = false
          showTip("操作成功！", true)
        }
      })
    },
    clickBadge(index) {
      this.curDesc = this.badges[index].badgeDesc
      this.curBadgeId = this.badges[index].badgeId
      this.curBadgeIndex = index
      this.isShowBadgeDesc = true
    },
    // 可以添加其他方法
    clickUpdateInfo() {
      router.push({path: '/editPersonalInfo', ps: {id: '123'}})
    },
    clickMyInterest() {
      router.push({path: "/interestList"})
    },
    handleChange(file) {
      if (file.raw.type !== "image/jpeg" && file.raw.type !== "image/png") {
        ElMessage.error('Avatar picture must be JPG format!');
        return false;
      }
      const reader = new FileReader();
      reader.onload = (e) => {
        this.badgeSrc = e.target.result;
      };
      this.badgeImage = file.raw
      reader.readAsDataURL(file.raw);
      return true;
    },
    uploadBadge() {
      uploadFileApi(this.badgeImage).then(
          (res) => {
            uploadBadgeAPI(this.badgeName, this.badgeDescription,
                res.fileUrl, this.badgeColor, this.badgeCost).then(
                (res) => {
                  if (res.response == 'success') {
                    ElMessage.success("徽章创建成功")
                    this.badgeDialog = false
                  } else {
                    // 图片上传失败给一个弹窗
                    ElMessage.success("徽章创建失败，请稍后再试")
                  }
                }
            )
          }
      )
    },
    clickQuitLogin() {
      // 注销登录信息
      userStateStore().resetUserInfo()
      router.replace({path: "/loginPage"})
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
    clickWaterItem(_blogId) {
      router.push({name: 'blogView', params: {id: _blogId}});
    },
    clickHelpItem(_blogId) {
      router.push('/QuesInfo/' + _blogId + "/0");
    },
    showPic(image) {
      viewerApi({images: [image]})
    },
    clickComplain() {
      // 直接跳转到举报信息页面而不需要传参
      router.push("/complainInfos");
    },
    buyBadge(badge) {
      this.buyBadgeDialog = true
      this.currentBuyBadge = badge
    },
    uploadBuyBadge() {
      uploadBuyBadge(userStateStore().user_id, this.currentBuyBadge.badgeId).then(
          (res) => {
            if (res.response == 'success') {
              ElMessage.success("购买勋章成功")
              this.buyBadgeDialog = false
              router.go(0)
            } else {
              this.badgeDialog = false
              this.buyBadgeDialog = false
              ElMessage.error(res.description)
            }
          }
      )
    }
    // setBadgeState(index, state) {
    //   setBadgeShowState(userStateStore().user_id, this.badges[index].badgeId, state).then((r) => {
    //     if (r != false) {
    //       this.badges[index].isShow = state
    //     } else showTip("设置失败", false)
    //   })
    // }
  },
};
</script>

<style scoped>

.nickname {
  font-size: 20px;
  font-weight: bold;
}

.signature {
  font-size: 12px;
  color: gray;
}

.time {
  font-size: 10px;
  color: gray;
}

.redHeart {
  color: red;
}

.greyHeart {
  color: grey;
}
</style>

<style>
.avatar-uploader1 .el-upload {
  border: 1px dashed grey;
  border-radius: 50% !important;
  cursor: pointer;
  position: relative;

  overflow: hidden;
  height: 0;
  padding: 0;
  padding-bottom: 100%;
  width: 100%;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader1 .el-upload:hover {
  border-radius: 50% !important;
  border-color: var(--el-color-primary);
}

.avatar-wrapper1 {
  position: relative;
  width: 100%;
  border-radius: 50% !important;
  height: 0;
  padding: 0;
  padding-bottom: 100%;
}

.right-top1 {
  position: absolute; /* 使用绝对定位 */
  top: -5%;
  right: -5%;
  z-index: 88888;
}

.avatar1 {
  position: absolute !important;
  top: 0;
  left: 0;
  border-radius: 50% !important;
  cursor: pointer;

  overflow: hidden;
}

.el-icon.avatar-uploader-icon1 {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  font-size: 28px;
  color: #8c939d;
  width: 100%;
  height: 100%;
  text-align: center;
}
</style>
