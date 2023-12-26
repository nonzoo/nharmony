<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">

                <form v-on:submit.prevent="submitForm" v-if="userStore.user.isAuthenticated" method="post">
                    <div class="p-4">
                        <textarea class="p-4 w-full bg-gray-100 rounded-lg" v-model="body"
                            placeholder="What are you thinking about?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg"
                            :disabled="!body.trim()">Attach image</button>

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
                        <p class="text-gray-500 mt-2">Add more friends to get started</p>
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

export default {
    name: 'FeedView',
    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem
    },


    setup() {
        const userStore = useUserStore()
        return {
            userStore
        }
    },

    data() {
        return {
            posts: [],
            body: ''
        }
    },


    mounted() {
        this.getFeed()
    },


    methods: {
        getFeed() {
            axios
                .get('/api/posts/')
                .then(response => {
                    this.posts = response.data

                })

                .catch(error => {
                    if (error.response.status === 401) {
                        window.location.href = '/login';

                    } else {
                        console.log('error', error);
                    }
                });
        },

        submitForm() {
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
        }
    }
}

</script>