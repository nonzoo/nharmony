<template class='' >
  <div>
    <div class="bg-white border border-gray-200 rounded-lg">
      <div class="flex flex-col flex-grow ">
        <template v-for="user in activeConversation.users" :key="user.id">
          <span v-if="user.id !== userStore.user.id"
            class="text-black p-2 rounded-full flex justify-center mb-2 font-serif text-lg">
            {{ user.name }}
          </span>
        </template>
        <div class=" overflow-y-auto min-h-screen overflow-x-scroll w-auto h-64 p-4">
          <template v-for="message in activeConversation.messages" v-bind:key="message.id" class="item-bottom">
            <!-- Request.user -->
            <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
              v-if="message.created_by.id == userStore.user.id">
              <div>
                <div class="bg-purple-600 text-white p-3 rounded-l-lg rounded-br-lg">
                  <p class="text-sm">{{ message.body }}</p>
                </div>
                <span class="text-xs text-gray-500 leading-none">{{ message.created_at_formatted }}</span>
              </div>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full">
              </div>
            </div>

            <!-- User -->
            <div class="flex w-full mt-2 space-x-3 max-w-md" v-else>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full">
              </div>
              <div>
                <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                  <p class="text-sm">{{ message.body }}</p>
                </div>
                <span class="text-xs text-gray-500 leading-none">{{ message.created_at_formatted }}</span>
              </div>
            </div>
          </template>
        </div>


      </div>
    </div>

    <div class="bg-white border border-gray-200 rounded-lg">
      <form @submit.prevent="submitForm" class="bg-grey-lighter px-4 py-4 flex items-center">
        <div class="flex-1 mx-4">
          <textarea v-model="body" class="w-full border border-gray-600 rounded px-2 py-2" type="text"></textarea>
        </div>
        <button :disabled="!body.trim()">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
            class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
          </svg>
        </button>
      </form>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { ref, onMounted, watchEffect, onBeforeUnmount } from 'vue';

export default {
  data() {
    return {
      userStore: useUserStore(),
      activeConversation: {},
      body: '',
      pollInterval: null,
    };
  },

  mounted() {
    this.getMessages();
    this.startMessagePolling();
  },

  beforeDestroy() {
    this.stopMessagePolling();
  },

  beforeRouteLeave(to, from, next) {
    this.stopMessagePolling();
    next();
  },


  watch: {
    '$route.params.id': 'getMessages',
  },


  methods: {
    getMessages() {
      axios
        .get(`/api/chat/${this.$route.params.id}/`)
        .then((response) => {
          this.activeConversation = response.data;
        })
        .catch((error) => {
          console.log('Error fetching messages:', error);
        });
    },

    submitForm() {
      axios
        .post(`/api/chat/${this.$route.params.id}/send/`, {
          body: this.body,
        })
        .then((response) => {
          this.activeConversation.messages.push(response.data);
          this.body = '';
        })
        .catch((error) => {
          console.log('Error sending message:', error);
        });
    },

    startMessagePolling() {
      this.pollInterval = setInterval(() => {
        this.getMessages();
      }, 5000); // Poll every 5 seconds
    },

    stopMessagePolling() {
      clearInterval(this.pollInterval);
    },
  },
};


</script>