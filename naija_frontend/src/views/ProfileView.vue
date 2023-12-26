<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">

                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{ name: 'friends', params: { id: user.id } }" class="text-xs text-gray-500">
                        {{ user.friends_count }} friends</RouterLink>
                    <p class="text-xs text-gray-500">120 posts</p>
                </div>
                <div class="mt-6" >
                    <button class="inline-block py-4 px-3 text-xs bg-purple-600 text-white rounded-lg" 
                        @click="sendFriendRequest" v-if="userStore.user.isAuthenticated && userStore.user.id !== user.id">Send Friend Request</button>

                    <button class="inline-block py-4 px-3 text-xs bg-red-600 text-white rounded-lg" 
                        @click="logout" v-if="userStore.user.id === user.id">Logout</button>


                    <button class="inline-block py-4 px-3 text-xs bg-purple-600 text-white rounded-lg mt-5" 
                        @click="sendDirectmessage" v-if="userStore.user.isAuthenticated && userStore.user.id !== user.id">Message</button>
                </div>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg" v-if="userStore.user.id === user.id">

                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">
                        <textarea class="p-4 w-full bg-gray-100 rounded-lg" v-model="body"
                            placeholder="What are you thinking about?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</button>

                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
                            :disabled="!body.trim()">Post</button>
                    </div>
                </form>
            </div>

            <div v-if="posts.length > 0">
                <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                    <FeedItem v-bind:post="post" />
                </div>
            </div>

            <div v-else>
                <div class="flex items-center justify-center h-40">
                    <div class="bg-gray-200 p-6 rounded-lg shadow-md">
                        <h1 class="text-2xl font-bold text-gray-700">No feed</h1>
                        <p class="text-gray-500 mt-2">Start sharing your thoughts with the world!</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />

            <Trends />
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import Trends from '../components/Trends.vue';
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue';
import FeedItem from '../components/FeedItem.vue';
import { useUserStore } from '@/stores/user';
import { RouterLink } from 'vue-router';
import { useToastStore } from '@/stores/toast'

export default {
    name: 'ProfileView',

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()
        return {
            userStore,
            toastStore
        }
    },

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
        RouterLink
    },
    data() {
        return {
            posts: [],
            user: {},
            body: ''
        }
    },

    mounted() {
        this.getFeed()
    },
    //when i click my profile in another persons profile it refreshes and takes me to my profile
    watch: {
        '$route.params.id': {
            handler: function () {
                this.getFeed()
            },
            deep: true,
            immediate: true
        }
    },

    methods: {
        sendFriendRequest() {
            axios
                .post(`/api/friends/${this.$route.params.id}/request/`)
                .then(response => {
                    console.log('data', response.data)

                    if (response.data.message == 'request already sent') {
                        this.toastStore.showToast(5000, 'Request already sent', 'bg-red-300')
                    }else{
                        this.toastStore.showToast(5000, 'Request sent', 'bg-emerald-300')
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },


        getFeed() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    this.posts = response.data.posts
                    this.user = response.data.user

                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        submitForm() {
            console.log('submitForm', this.body)
            axios
                .post('/api/posts/create/', {
                    'body': this.body
                })
                .then(response => {
                    console.log('data', response.data)

                    this.posts.unshift(response.data)
                    this.body = ''
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        logout(){
            this.userStore.removeToken()
            this.$router.push('/login')
            this.toastStore.showToast(5000, 'Logout Successfully!', 'bg-emerald-300')
            
        },

        sendDirectmessage(){
            axios
                .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
                .then(response => {
                    this.$router.push(`/chat/${response.data.id}/`)
                })
                .catch(error =>{
                    console.log('error', error)
                })
        }
    }
}

</script>