<template>
    <div class="max-w-7xl mx-auto gap-4">
        <div class="main-center">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <div class="space-y-4" v-if="conversations.length>0">
                    <router-link v-for="conversation in conversations" :key="conversation.id"
                        :to="{ name: 'chatdetail', params: { id: conversation.id } }">
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex items-center space-x-2">
                                
                                <template v-for="user in conversation.users" :key="user.id">
                                    <i v-if="user.id !== userStore.user.id">
                                    <img :src="user.get_avatar" class="w-[40px] rounded-full" /></i>
                                    <span v-if="user.id !== userStore.user.id" class="text-xs font-bold">{{ user.name
                                    }}</span>
                                </template>
                            </div>
                            <span class="text-xs text-gray-500">{{ conversation.modified_at_formatted }}</span>
                        </div>
                    </router-link>
                </div>
                <div v-else>
                <div class="flex items-center justify-center h-40">
                    <div class="bg-gray-200 p-6 rounded-lg shadow-md">
                        <h1 class="text-2xl font-bold text-gray-700">No message here</h1>
                    </div>
                </div>
            </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user';

export default {
    name: 'chat',
    setup() {
        const userStore = useUserStore();
        return {
            userStore,
        };
    },
    data() {
        return {
            conversations: [],

        };
    },
    mounted() {
        this.getConversations();
    },
    methods: {

        getConversations() {
            axios
                .get('/api/chat/')
                .then((response) => {
                    console.log(response.data);
                    this.conversations = response.data;
                })
                .catch((error) => {
                    if (error.response.status === 401) {
                        window.location.href = '/login';

                    } else {
                        console.log('error', error);
                    }
                });
        },


    },
};
</script>
  