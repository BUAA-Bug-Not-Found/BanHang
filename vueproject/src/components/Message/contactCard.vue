<template>
    <v-card class="box-card"  @click="sendUserToParent">
        <img :src="avatar" class="profile-photo" />
        <div style="flex:1;max-width: calc(100% - 50px);text-align: left;">
            <b class="name">{{ user_name }}</b>
            <div class="last-message">{{ last_message }}</div>
        </div>
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
        avatar: String,
        last_message:String,
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
    width: 100%;
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

.last-message {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-height: 1.2em;
    padding-left: 10px;
    color: #999;
    font-size:12px;
}
</style>