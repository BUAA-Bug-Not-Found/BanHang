<template>
    <v-card class="box-card"  @click="sendUserToParent">
        <img :src="avatar" class="profile-photo" />
        <p class="name">{{ user_name }}</p>
    </v-card>
</template>
  
<script>
import { ElCard } from 'element-plus';
/* eslint-disable */
export default {
    name: "contactCard",
    props: {
        user_name: String,
        user_id: Number,
        avatar: String
    },
    components: {
        ElCard
    },
    methods: {
        sendUserToParent() {
            this.$emit('open-message', this.user_id, this.user_name, this.avatar);
        },
    },
};
</script>
  
<style scoped>

.profile-photo {
    width: 30px;
    height: 30px;
    object-fit: cover;
    margin-right: 10px;
    border-radius: 50%;
}

.box-card {
    border-radius: 5; /* 去除圆角 */
    height: 70px;
    align-items: center;
    position: flex;
    display: flex;
    align-items: center;
    padding: 10px;
}

.box-card:hover {
    filter: brightness(95%);
}


.name {
  margin-left: 10px; /* 可根据需要调整头像和名字之间的间距 */
  margin-top: 0;
  margin-bottom: 0;
  line-height: 1.3;
  text-align: left;
}
</style>