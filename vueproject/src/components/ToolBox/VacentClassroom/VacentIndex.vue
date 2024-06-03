<template>
  <div>
    <div class="header">
      {{ compus == '' ? '校区：' : '教学楼：' }}
      <v-chip v-for="(item, index) in (compus == '' ? compusList : buildingList)" :key="index"
        @click="handleClickChip(item)" class="chip">
        {{ item }}
      </v-chip>
    </div>
    <div v-if="classroomList != null" style="padding-bottom: 50px">
      <v-card v-for="(item, index) in classroomList" :key="index">
        <v-card-title primary-title class="text-left">{{ item.name }}</v-card-title>
        <v-card-text class="text-left">
          空闲时间直到{{ item.vacent_time_end }}
        </v-card-text>
      </v-card>
    </div>
    <div v-else>
      请首先选择教学楼
    </div>
  </div>
</template>
<script>
import axios from 'axios';
import { processVacantClassrooms } from './ProcessData.js'
import { ref } from "vue";
/* eslint-disable */
export default {
  name: "VacentIndex",
  setup() {
    const data = ref(null);
    const compus = ref('');
    const compusList = ref(['学院路', '沙河'])
    const buildings = ref('');
    const buildingList = ref([])
    const classroomList = ref(null);


    const fetchData = () => {
      axios.get('/getVacantClassroom').then(res => {
        data.value = processVacantClassrooms(res.data)
        console.log(data.value)
      }).catch(error => {
        console.error(error)
      })
    }

    const handleClickChip = (label) => {
      if (compus.value == '') {
        compus.value = label == '学院路' ? 'xueyuanlu' : 'shahe'
        buildingList.value = data.value[compus.value]['buildings'].map(x => x.name)
        buildingList.value.push('返回')
      } else {
        if (label == '返回') {
          compus.value = ''
          classroomList.value = null
        } else {
          buildings.value = label
          classroomList.value = data.value[compus.value]['buildings'].filter(x => x.name == buildings.value)[0]['vacantClassroomInfo']
        }
      }
    }

    fetchData()
    return {
      compusList,
      buildingList,
      classroomList,
      handleClickChip,
      compus,
    }
  },
}
</script>

<style scoped>
.header {
  margin: 10px;
  text-align: left;
}

.chip {
  margin:5px
}
</style>