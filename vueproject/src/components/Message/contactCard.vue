<template>
    <v-card class="box-card" shadow="never" @click="sendUserToParent">
            <div class="profile-wrapper">
                <img :src="profile_photo" alt="头像" class="profile-photo" />
                <p class="name">{{ user_name }}</p>
            </div>

    </v-card>
</template>
  
<script>
import axios from 'axios';
import { ElCard } from 'element-plus';
/* eslint-disable */
export default {
    name: "contactCard",
    props: {
        user_name: String,
        user_id: String
    },
    data() {
        return {
            profile_photo: '/src/assets/image/default-avatar.png',
        };
    },
    mounted() {
        this.getProfilePhoto();
    },
    components: {
        ElCard
    },
    methods: {
        getProfilePhoto() {
            return;
            axios.post('/', { user_name: this.user_name })
                .then(response => {
                    if (response.data.profile_photo) {
                        this.profile_photo = response.data.profile_photo;
                        this.profile_photo = this.profile_photo.startsWith('/9j') ? 'data:image/jpg;base64,' + this.profile_photo : 'data:image/png;base64,' + this.profile_photo
                    }
                })
                .catch(error => {
                    console.error(error);
                });
        },
        sendUserToParent() {
            this.$emit('open-message', this.user_id);
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
    border-radius: 0; /* 去除圆角 */
    height: 70px;
    box-shadow: none;
}

.box-card:hover {
    filter: brightness(95%);
}

.profile-wrapper {
  display: flex;
  align-items: center;
}

.name {
  margin-left: 10px; /* 可根据需要调整头像和名字之间的间距 */
  margin-top: 0;
  margin-bottom: 0;
  line-height: 1.3;
  text-align: left;
}
</style>