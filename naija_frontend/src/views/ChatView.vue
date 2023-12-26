<template>
    <div class="max-w-7xl mx-auto gap-4">
        <div class="main-center">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <div class="space-y-4">
                    <router-link v-for="conversation in conversations" :key="conversation.id"
                        :to="{ name: 'chatdetail', params: { id: conversation.id } }">
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex items-center space-x-2">
                                <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full" />
                                <template v-for="user in conversation.users" :key="user.id">
                                    <span v-if="user.id !== userStore.user.id" class="text-xs font-bold">{{ user.name
                                    }}</span>
                                </template>
                            </div>
                            <span class="text-xs text-gray-500">{{ conversation.modified_at_formatted }}</span>
                        </div>
                    </router-link>
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
                    console.log(error);
                });
        },


    },
};
</script>
  