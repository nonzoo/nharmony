<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img :src="user.get_avatar" class=" w-30 mb-6 rounded-full">

                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around" v-if="user.id">
                    <RouterLink :to="{ name: 'friends', params: { id: user.id } }" class="text-xs text-gray-500">
                        {{ user.friends_count }} friends</RouterLink>
                    <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                </div>
                <div class="mt-6 space-x-4">
                    <button class="inline-block py-4 px-3 text-xs bg-purple-600 text-white rounded-lg"
                        @click="sendFriendRequest"
                        v-if="userStore.user.isAuthenticated && userStore.user.id !== user.id">Send Friend Request</button>

                    <RouterLink to="/profile/edit"
                        class="inline-block py-4 px-3 text-xs bg-purple-600 mr-4 text-white rounded-lg"
                        v-if="userStore.user.id === user.id">Edit</RouterLink>

                    <button class="inline-block py-4 px-3 text-xs bg-red-600 text-white rounded-lg" @click="logout"
                        v-if="userStore.user.id === user.id">Logout</button>


                    <button class="inline-block py-4 px-3 text-xs bg-purple-600 text-white rounded-lg mt-5"
                        @click="sendDirectmessage"
                        v-if="userStore.user.isAuthenticated && userStore.user.id !== user.id">Message</button>
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

                    <div id="preview" v-if="url" class="p-4">
                        <img :src="url" class="w-[100px] rounded-xl  mt-2">
                    </div>


                    <div class="p-4 border-t border-gray-100 flex justify-between">

                        <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                            <input type="file" ref="file" @change="onFileChange">
                            Attach image
                        </label>

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
            <div v-if="userStore.user.isAuthenticated">
                <PeopleYouMayKnow />
            </div>


            <Trends />
        </div>
    </div>
</template>

<style>
input[type="file"] {
    display: none;
}

.custom-file-upload {
    border: 1px solid #ccc;
    display: inline-block;
    padding: 6px 12px;
    cursor: pointer;
}
</style>

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
            user: { id: '' },
            body: '',
            url: null
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

        onFileChange(e){
            const file = e.target.files[0]
            this.url = URL.createObjectURL(file)
        },

        sendFriendRequest() {
            axios
                .post(`/api/friends/${this.$route.params.id}/request/`)
                .then(response => {
                    console.log('data', response.data)

                    if (response.data.message == 'request already sent') {
                        this.toastStore.showToast(5000, 'Request already sent', 'bg-red-300')
                    } else {
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

                    // console.log('http://127.0.0.1:8000' + this.user.avatar)

                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        submitForm() {
            console.log('submitForm', this.body)
            let formData = new FormData()

            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)

            axios
                .post('/api/posts/create/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    console.log('data', response.data)

                    this.posts.unshift(response.data)
                    this.body = ''
                    this.$refs.file.files= null
                    this.url = null
                    this.user.posts_count += 1
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        logout() {
            this.userStore.removeToken()
            window.location.href = "/login"
            // this.toastStore.showToast(5000, 'Logout Successfully!', 'bg-emerald-300')


        },

        sendDirectmessage() {
            axios
                .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
                .then(response => {
                    this.$router.push(`/chat/${response.data.id}/`)
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}

</script>