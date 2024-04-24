<script>
import {ref} from "vue";
// import {getAnsById} from "@/components/HelpCenter/api";

export default {
  name: "AppAnsCard",
  props: ["ansId", "index"],
  setup(props) {

    const init = () => {
      // getAnsById(props.ansId).then((res) => {
      //   ans.value = res.ans
      // })
    }

    const ansIdRef = ref(props.ansId)

    const ans = ref(
        {
          userId: 1,
          userName: 'testuser_ans',
          ansContent: "<h3>Lorem ipsum dolor sit amet consectetur adipisicing elit.</h3> \" +\n" +
              "          \"Commodi, ratione debitis quis est labore voluptatibus! Eaque cupiditate minima, \" +\n" +
              "          \"at placeat totam, magni doloremque veniam neque porro libero rerum unde voluptatem!\"",
          ansState: '1',
          ansTime: '2024-4-24 13:42',
          ifUserLike: 0,
          likeSum: '10'
        })
    init()

    return {ans, ansIdRef};
  },
};
</script>

<template>
  <v-divider
      v-if="index !== 0"
      color="light-blue-darken-3"
      style="margin-top: 5px;margin-bottom: 5px"
  ></v-divider>
  <v-card
      class="mx-auto"
      width="w-75"
      elevation="0"
  >
    <v-row style="height: 55px">
      <v-col cols="1" style="margin-right: 15px">
        <v-avatar color="surface-variant" style="margin: 10px;" size="40"/>
      </v-col>
      <v-col cols="10">
        <div style="display: flex; justify-content: space-between;margin-top: 10px">
          <span style="font-size: 15px">{{ ans.userName }}</span>
          <span style="font-size: 12px;color: gray">回答于{{ ans.ansTime }}</span>
        </div>
        <div style="margin-bottom: 5px">
          <v-btn
              :prepend-icon="ans.ifUserLike === 1 ?
              'mdi-thumb-up-outline' : 'mdi-thumb-up'" variant="text" size="small"
              color="blue-grey-lighten-2">
            {{ ans.likeSum }}
          </v-btn>
          <v-btn
              :prepend-icon="'mdi-reply'" variant="text" size="small"
              color="blue-grey-lighten-2">
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <v-row :justify="'center'" style="margin-bottom: 10px">
      <v-col cols="11" style="margin-top: 3px" v-html="ans.ansContent"/>
    </v-row>
  </v-card>
</template>

<style scoped>

</style>