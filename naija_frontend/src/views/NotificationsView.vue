<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-center col-span-3 space-y-4">

            <div v-if="notifications.length > 0">
                <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="notification in notifications"
                    v-bind:key="notification.id">
                    {{ notification.body }}


                        <button class="underline" @click="readNotification(notification)">Go to page</button>
                    
                </div>
            </div>

            <div v-else>
                <div class="flex items-center justify-center h-40">
                    <div class="bg-gray-200 p-6 rounded-lg shadow-md">
                        <h1 class="text-2xl font-bold text-gray-700">No notifications</h1>
                        <p class="text-gray-500 mt-2">new notifications will appear here when recieved</p>
                    </div>
                </div>
            </div>


        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'notifications',

    data() {
        return {
            notifications: []
        }
    },

    mounted() {
        this.getNotifications()
    },

    methods: {
        getNotifications() {
            axios
                .get('/api/notifications/')
                .then(response => {
                    console.log(response.data)
                    this.notifications = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        async readNotification(notification) {
            console.log('readNotification', notification.id)
            await axios

                .post(`/api/notifications/read/${notification.id}/`)
                .then(response => {
                    console.log(response.data)
                    if (notification.type_of_notification == 'post_like' || notification.type_of_notification == 'post_comment') {
                        this.$router.push({name:"postdetail", params:{id: notification.post_id}})
                    }
                    else if(notification.type_of_notification == 'new_friendrequest') {
                        this.$router.push({name:'friends', params:{id:notification.created_for_id}})
                    }
                    else{
                        this.$router.push({name:'profile', params:{id:notification.created_by_id}})
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })

        }
    }
}
</script>