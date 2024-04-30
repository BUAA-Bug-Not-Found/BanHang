<template>
    <div>
        <img :src="headImage">
        <span>{{ nickname }}</span>
        <span>{{ email }}</span>
        <span style="size:100px;">ddddddddddd:{{ sign }}</span>
    </div>
</template>


<script>
//   该文件是用户列表中的一个表项视图
export default {
    name: "UserShow",
    data() {
        return {
            nickname: "",
            email: "",
            headImage: "",
            sign: ""
        };
    },

    methods: {
    }
};
</script>
  
<style scoped>

</style>
  