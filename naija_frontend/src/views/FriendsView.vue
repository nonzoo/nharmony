<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <!-- Profile -->
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img :src="user.get_avatar" class="mb-6 rounded-full">

                <p><strong>{{user.name}}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500">{{user.friends_count}} friends</p>
                    <p class="text-xs text-gray-500">{{user.posts_count}} posts</p>
                </div>

            </div>
        </div>

        <!-- Friends Request -->
        <div class="main-center col-span-2 space-y-4">
            <div class="p-4 bg-white border border-gray-200 rounded-lg " v-if="friendRequests.length">
                <h2 class="mb-6 text-xl">Friend Requests</h2>
                <div v-for="friendRequest in friendRequests" v-bind:key="friendRequest.id" class="p-4 text-center bg-gray-100 rounded-lg">
                    <img :src="friendRequest.created_by.get_avatar" class="mb-6 mx-auto rounded-full">

                    <p>
                        <strong>
                            <RouterLink :to="{ name: 'profile', params: { 'id': friendRequest.created_by.id } }">{{ friendRequest.created_by.name }}</RouterLink>
                        </strong>
                    </p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{friendRequest.created_by.friends_count}} friends</p>
                        <p class="text-xs text-gray-500">{{friendRequest.created_by.posts_count}} posts</p>
                    </div>
                    <div class="mt-6 space-x-4">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg" @click="handleRequest('accepted', friendRequest.created_by.id)">Accept</button>
                        <button class="inline-block py-4 px-6 bg-red-600 text-white rounded-lg" @click="handleRequest('rejected',friendRequest.created_by.id)">Reject</button>
                    </div>
                </div>
                <hr>
            </div>

            
                        <!-- Friends -->
            <div class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-2 gap-4" v-if="friends.length">
               
                <div v-for="user in friends" v-bind:key="user.id" class="p-4 text-center bg-gray-100 rounded-lg">
                    <img :src="user.get_avatar" class="mb-6 rounded-full">

                    <p>
                        <strong>
                            <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }">{{ user.name }}</RouterLink>
                        </strong>
                    </p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{user.friends_count}} friends</p>
                        <p class="text-xs text-gray-500">{{user.posts_count}} posts</p>
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

import { useUserStore } from '@/stores/user';
export default {
    name: 'FriendsView',

    setup() {
        const userStore = useUserStore()
        return {
            userStore
        }
    },

    components: {
        PeopleYouMayKnow,
        Trends,
        
    },
    data() {
        return {
            user: {},
            friendRequests: [],
            friends: [],
        }
    },

    mounted() {
        this.getFriends()
    },


    methods: {
        getFriends() {
            axios
                .get(`/api/friends/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    this.friendRequests = response.data.requests
                    this.friends = response.data.friends
                    this.user = response.data.user

                })
                .catch(error => {
                    if (error.response.status === 401) {
                        window.location.href = '/login';

                    } else {
                        console.log('error', error);
                    }
                });
        },

        handleRequest(status, pk ){
            console.log('handleRequest', status)
            axios
                .post(`/api/friends/${pk}/${status}/`)

                .then(response=>{
                    console.log('data',response.data)
                    location.reload();
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}

</script>