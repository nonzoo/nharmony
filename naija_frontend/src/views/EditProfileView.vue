<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-2">
        <div class="main-left col-span-2">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Edit Profile</h1>

                <p class="mb-6 text-gray-500">
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                </p>
                <RouterLink to="/profile/edit/password" class="underline">Edit Password</RouterLink>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div class="flex justify-center items-center h-full">
                        <label class="inline-block py-4 px-6 bg-gray-200 text-white rounded-lg">
                            <input type="file" ref="file" class="hidden">
                            <svg xmlns="http://www.w3.org/2000/svg" height="16" width="16" viewBox="0 0 512 512">
                                <path
                                    d="M149.1 64.8L138.7 96H64C28.7 96 0 124.7 0 160V416c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V160c0-35.3-28.7-64-64-64H373.3L362.9 64.8C356.4 45.2 338.1 32 317.4 32H194.6c-20.7 0-39 13.2-45.5 32.8zM256 192a96 96 0 1 1 0 192 96 96 0 1 1 0-192z" />
                            </svg>
                        </label>
                    </div>

                    <div>
                        <label>Name</label><br>
                        <input type="text" v-model="form.name" placeholder="Your full name"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>
                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>
                    <div>
                        <label>Gender</label><br>
                        <select v-model="form.gender" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                        </select>
                    </div>



                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Save Chages</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>



<script>

import axios from 'axios'
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';

export default {
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()
        return {
            toastStore,
            userStore
        }
    },
    data() {
        return {
            form: {
                email: this.userStore.user.email,
                name: this.userStore.user.name,
                gender: this.userStore.user.gender,
            },
            errors: [],
        }

    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.name === '') {
                this.errors.push('Your name is missing')
            }
            if (this.form.gender === '') {
                this.errors.push('Your gender is missing')
            }
            if (this.errors.length === 0) {
                let formData = new FormData()

                formData.append('avatar', this.$refs.file.files[0])
                formData.append('name', this.form.name)
                formData.append('email', this.form.email)
                formData.append('gender', this.form.gender)

                axios
                    .post('/api/editprofile/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'Information Updated') {
                            this.toastStore.showToast(5000, `${response.data.message}`, 'bg-emerald-300')

                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                email: this.form.email,
                                gender: this.form.gender,
                                avatar: response.data.user.get_avatar
                            })
                            this.$router.back()
                        } else {
                            this.toastStore.showToast(5000, `${response.data.message}. Please try again`, 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    }
}


</script>