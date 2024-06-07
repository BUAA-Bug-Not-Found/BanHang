<template>
  <v-dialog v-model="showDialog" max-width="500">
    <v-card>
      <v-card-title>日程创建</v-card-title>
      <v-card-text>
        <p>是否为博雅 "{{ curClass.name }}" 添加选课日程？</p>
        <p>使用手机日历打开下载文件来添加日程</p>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="showDialog = false">关闭</v-btn>
        <v-btn @click="showDialog = false; downloadICSFile()">添加</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <!--手机-->
  <div v-if="display.smAndDown.value">
    <div class="header">
      高级搜索：
      <v-chip v-for="(item, index) in chipList" :key="index" @click="handleChipClicked(item)" class="chip"
        :prepend-icon="item.clicked ? 'mdi-checkbox-marked-circle' : ''">
        {{ item.name }}
      </v-chip>
      <div v-if="isLogin">
        <p>我的委托：{{ myEntrust.campus.length == 0 || myEntrust.type.length == 0 ? '暂无委托' : ""}}</p>
        <div v-if="myEntrust.campus.length != 0 && myEntrust.type.length != 0">
          <p> 校区：{{ myEntrust.campus.join('、') }} </p>
          <p> 类型：{{ myEntrust.type.join('、') }} </p>
        </div>
        <v-btn @click="submitEntrust" variant="tonal" style="margin-top: 5px;margin-bottom: 5px;" color="primary">添加委托</v-btn>
        <v-btn @click="cancelEntrust" variant="tonal" style="margin-top: 5px;margin-bottom: 5px;margin-left: 5px;" color="primary">取消委托</v-btn>
        <p style="  font-size: 14px;color: grey;">当添加委托之后，如果有满足特定要求的博雅出现，会为您的北航邮箱发送邮件</p>
      </div>
    </div>

    <v-card v-for="(item, index) in getClassList()" :key="index"
      style="border-radius: 0px;margin-bottom: 1px;padding:0 20px 10px 20px;" variant="flat" @click="handleBoyaClicked(item)">
      <div style="height: 1px;  background-color: lightgrey; margin-bottom: 10px"></div>
      <div class="card-header">
        <div class="type">{{ item.type.slice(5) }}</div>
        <div class="name">{{ item.name }}</div>
        <div class="state" :style="getStateColor(item.state)">{{ item.state }}</div>
      </div>
      <div class="card-container">
        <div class="left-column">
          <div class="card-body">
            <div class="position">{{ item.position }}</div>
            <div class="teacher">{{ item.teacher }}</div>
            <div class="school">{{ item.school }}</div>
          </div>
        </div>
        <div class="right-column">
          <div>人数: {{ item.selected_number }}/{{ item.capacity_number }}</div>
          <div>选课时间: {{ item.select_start_time.slice(7) }} - {{ item.select_end_time.slice(7) }}</div>
          <div>上课时间: {{ item.start_time.slice(5) }} - {{ item.end_time.slice(5) }}</div>
        </div>
      </div>
    </v-card>
  </div>
  <!--电脑浏览器-->
  <v-container v-else style="width: 70%; margin-top: 10px;">
    <v-card style="text-align: left;padding: 25px">
      高级搜索：
      <v-chip v-for="(item, index) in chipList" :key="index" @click="handleChipClicked(item)" class="chip"
        :prepend-icon="item.clicked ? 'mdi-checkbox-marked-circle' : ''">
        {{ item.name }}
      </v-chip>
      <div v-if="isLogin">
        <p>我的委托：{{ myEntrust.campus.length == 0 || myEntrust.type.length == 0 ? '暂无委托' : ""}}</p>
        <div v-if="myEntrust.campus.length != 0 && myEntrust.type.length != 0">
          <p> 校区：{{ myEntrust.campus.join('、') }} </p>
          <p> 类型：{{ myEntrust.type.join('、') }} </p>
        </div>
        <v-btn @click="submitEntrust" variant="tonal" style="margin-top: 5px;margin-bottom: 5px;" color="primary">添加委托</v-btn>
        <v-btn @click="cancelEntrust" variant="tonal" style="margin-top: 5px;margin-bottom: 5px;margin-left: 5px;" color="primary">取消委托</v-btn>
        <p style="  font-size: 14px;color: grey;">当添加委托之后，如果有满足特定要求的博雅出现，会为您的北航邮箱发送邮件</p>
      </div>
    </v-card>
    <v-card v-for="(item, index) in getClassList()" :key="index" style="margin-top: 10px;padding:10px 20px 10px 20px;"
      @click="handleBoyaClicked(item)">
      <div class="card-header">
        <div class="type">{{ item.type.slice(5) }}</div>
        <div class="name">{{ item.name }}</div>
        <div class="state" :style="getStateColor(item.state)">{{ item.state }}</div>
      </div>
      <div class="card-container">
        <div class="left-column">
          <div class="card-body">
            <div class="position">{{ item.position }}</div>
            <div class="teacher">{{ item.teacher }}</div>
            <div class="school">{{ item.school }}</div>
          </div>
        </div>
        <div class="right-column">
          <div>人数: {{ item.selected_number }}/{{ item.capacity_number }}</div>
          <div>选课时间: {{ item.select_start_time.slice(7) }} - {{ item.select_end_time.slice(7) }}</div>
          <div>上课时间: {{ item.start_time.slice(5) }} - {{ item.end_time.slice(5) }}</div>
        </div>
      </div>
    </v-card>


  </v-container>
</template>
<script>
import axios from 'axios';
import { ref } from "vue";
import { useDisplay } from 'vuetify'
import { isApp } from '@/store';
import userStateStore from '@/store';
import { showTip } from '@/components/AccountManagement/AccountManagementAPI';

/* eslint-disable */
export default {
  name: "BoyaIndex",
  setup() {
    const data = ref([]);
    const showDialog = ref(false);
    const curClass = ref({});
    const isLogin = userStateStore().isAuthentic
    const myEntrust = ref({campus:[], type:[]})
    const chipList = ref(isApp && localStorage.getItem('boyaChips') ? JSON.parse(localStorage.getItem('boyaChips')) : [
      {
        name: '学院路',
        clicked: true,
      },
      {
        name: '沙河',
        clicked: true
      },
      {
        name: '劳动教育',
        clicked: true
      },
      {
        name: '美育',
        clicked: true
      },
      {
        name: '德育',
        clicked: true
      },
      {
        name: '安全健康',
        clicked: true
      },
      {
        name: '其他方面',
        clicked: true
      },
    ])
    const display = useDisplay()

    const handleBoyaClicked = (item) => {
      showDialog.value = true
      curClass.value = item
    }
    const fetchData = () => {
      axios.get('/getBoyaInfo').then(res => {
        data.value = res.data
      }).catch(error => {
        console.error(error)
      })
      axios.post('/getBoyaEntrust', {}).then(res => {
        myEntrust.value = res.data
      }).catch(error => {
        console.error(error)
      })
    }
    const handleChipClicked = (item) => {
      item.clicked = !item.clicked
      if (isApp) {
        localStorage.setItem('boyaChips', JSON.stringify(chipList.value))
      }
    }
    const submitEntrust = () => {
      let requestData = {
        campus:[], 
        type:[]
      }
      if (chipList.value[0].clicked) {
        requestData.campus.push('学院路')
      }
      if (chipList.value[1].clicked) {
        requestData.campus.push('沙河')
      }
      for (let i = 2; i <= 6; i++) {
        if (chipList.value[i].clicked) {
          requestData.type.push(chipList.value[i].name)
        }
      }
      if (requestData.campus.length == 0) {
        showTip('请选择至少一个校区', false);
        return;
      }
      if (requestData.type.length == 0) {
        showTip('请选择至少一个类别', false);
        return;
      }
      axios.post('/createBoyaEntrust', requestData).then(res => {
        myEntrust.value = requestData;
        showTip('成功创建委托', true);
      }).catch(error => {
        console.error(error)
      })
    }
    const cancelEntrust = () => {
      if (myEntrust.value.campus.length == 0 || myEntrust.value.type.length == 0) {
        showTip('当前没有委托', false);
        return;
      }
      axios.post('/deleteBoyaEntrust').then(res => {
        myEntrust.value = {campus:[], type:[]}
        showTip('委托已取消', true);
      }).catch(error => {
        console.error(error)
      })
    }

    fetchData()

    const getClassList = () => {
      const ret = data.value.filter(cls => {
        if (!chipList.value[0].clicked && cls.position.includes('学院路')) {
          return false;
        }
        if (!chipList.value[1].clicked && cls.position.includes('沙河')) {
          return false;
        }
        let deleted = false
        chipList.value.forEach(e => {
          if (!e.clicked && cls.type.slice(5) == e.name) {
            deleted = true
          }
        })
        return !deleted;
      })
      //console.log(ret)
      return ret;
    }
    return {
      display,
      chipList,
      handleChipClicked,
      getClassList,
      handleBoyaClicked,
      submitEntrust,
      cancelEntrust,
      showDialog,
      curClass, 
      isLogin,
      myEntrust,
    }
  },
  methods: {
    getStateColor(state) {
      let backgroundColor = 'transparent'
      switch (state) {
        case '已开课':
        case '选课结束':
          backgroundColor = 'grey';
          break;
        case '可选':
          backgroundColor = 'green';
          break;
        case '预告':
          backgroundColor = '#658dd1';
          break;
        default:
          backgroundColor = 'transparent';
      }
      return {
        backgroundColor: backgroundColor,
      };

    },
    downloadICSFile() {
      // Parse the provided time string and calculate start and end times
      let name = this.curClass.name
      let time = '20' + this.curClass.select_start_time.slice(7)
      console.log(time)
      const endTime = new Date(time.replace(/-/g, '/')); // Replace '-' with '/' for compatibility
      const startTime = new Date(endTime.getTime() - 10 * 60 * 1000); // Subtract 10 minutes
      if (startTime < new Date()) {
        showTip('该课程已经开始选课', false)
        return;
      }
      // Format the dates to the required format for .ics file
      const formatDate = (date) => {
        return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
      };

      const icsContent = `
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Your App//EN
BEGIN:VEVENT
UID:${new Date().toISOString()}
DTSTAMP:${new Date().toISOString().replace(/[-:]/g, '').split('.')[0]}Z
DTSTART:${formatDate(startTime)}
DTEND:${formatDate(endTime)}
SUMMARY:${name}
DESCRIPTION:博雅选课提醒
LOCATION:Sample Location
END:VEVENT
END:VCALENDAR
      `.trim();

      const blob = new Blob([icsContent], { type: 'text/calendar' });
      const url = URL.createObjectURL(blob);

      // Create a temporary link element
      const a = document.createElement('a');
      a.href = url;
      a.download = 'event.ics';

      // Append link to the body
      document.body.appendChild(a);

      // Trigger the download by simulating a click
      a.click();

      // Remove the link after downloading
      document.body.removeChild(a);

      // Revoke the object URL
      URL.revokeObjectURL(url);
    }
  },
}
</script>

<style scoped>
.header {
  margin: 20px;
  text-align: left;
  z-index: 1000000000;
}

.pc-container {
  width: 70%;
  margin-left: 15%;
  margin-top: 10px;
}

/* CSS part */
.card-container {
  display: flex;
}

.left-column {
  flex: 1;
}

.right-column {
  max-width: 50%;
}

.card-header {
  display: flex;
}

.type,
.state {
  background-color: #658dd1;
  color: white;
  padding: 3px 6px;
  border-radius: 3px;
  /* Add margin between elements */
  font-size: 14px;
  white-space: nowrap;
  max-height: 27px;
}

.name {
  text-align: left;
  font-weight: bold;
  color: black;
  font-size: 18px;
  margin: 0px 5px 0px 5px;
}

.card-body,
.card-footer {
  margin-top: 10px;
  text-align: left;
  /* Left align the text in card body */
}

.card-footer {
  color: grey;
}

.position,
.teacher,
.school,
.start-time,
.end-time {
  margin-top: 5px;
}

.right-column div {
  margin-top: 10px;
  text-align: right;
  /* Right align the text in right column */
  font-size: 12px;
  /* Make text smaller in right column */
  color: grey;
  /* Set text color to grey in right column */
}

.chip {
  margin: 5px
}
</style>