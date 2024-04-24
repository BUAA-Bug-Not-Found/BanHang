<template>
    <v-card>
        <v-card-title primary-title class="text-left">{{ title }}</v-card-title>
        <v-card-text class="text-left">
            {{ startTime }} - {{ endTime }}
            <div class="progress-container">
                <div class="progress-info text-left">
                    <span>剩余时间: {{ remainingHours }}小时</span>
                </div>
                <div style="width: 30%;">
                    <dProgress :percentage="calculateProgress()" 
                    :pcolor="getRank" 
                    :text-inside="true" 
                    strokeHeight="20" />
                </div>
            </div>
        </v-card-text>
        <v-expand-transition>
            <v-card-text :class="{ 'content': !showContent }" class="text-left">
                <div v-html="content"></div>
            </v-card-text>
        </v-expand-transition>

        <v-btn text @click="toggleContent" class="btn-expand">
            <v-icon>{{ showContent ? 'mdi-arrow-up' : 'mdi-arrow-down' }}</v-icon>
        </v-btn>
    </v-card>
</template>

<script>
import dProgress from './dProgress.vue';
export default {
    name: "TaskItem",
    props: {
        title: String,
        content: String,
        startTime: String,
        endTime: String
    },
    data() {
        return {
            showContent: false
        };
    },
    components: {
        dProgress
    },
    methods: {
        toggleContent() {
            this.showContent = !this.showContent;
        },
        calculateProgress() {
            const currentTime = new Date().getTime();
            const startTime = new Date(this.startTime).getTime();
            const endTime = new Date(this.endTime).getTime();
            return Math.min((((currentTime - startTime) / (endTime - startTime)) * 100).toFixed(1), 100);
        },
    },
    computed: {
        remainingHours() {
            const currentTime = new Date().getTime();
            const endTime = new Date(this.endTime).getTime();
            const remainingMilliseconds = endTime - currentTime;
            const remainingHours = Math.floor(remainingMilliseconds / (1000 * 60 * 60));
            return remainingHours;
        },
        getRank() {
            const remainingTime = this.remainingHours;
            if (remainingTime > 72) {
                return "green";
            } else if (remainingTime > 24) {
                return "orange";
            } else if (remainingTime > 0) {
                return "red";
            } else {
                return "grey"
            }
        }
    }
};
</script>

<style scoped>
.progress-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.progress-info {
    color: gray;
}

.text-left {
    text-align: left;
}

.content {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-height: 1.2em;
}

.btn-expand {
    width: 100%;
    border: none;
}
</style>/
