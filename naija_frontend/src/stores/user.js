import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore({
    id: 'user',

    state: () => ({
        user: {
            isAuthenticated: false,
            id: null,
            name: null,
            email: null,
            age:null,
            gender:null,
            access: null,
            refresh: null,
            avatar: null,
            bio:null,
            locations:null
        }
    }),

    actions: {
        initStore() {
            console.log('initStore', localStorage.getItem('user.access'))

            if (localStorage.getItem('user.access')) {
                console.log('User has access!')

                this.user.access = localStorage.getItem('user.access')
                this.user.refresh = localStorage.getItem('user.refresh')
                this.user.id = localStorage.getItem('user.id')
                this.user.name = localStorage.getItem('user.name')
                this.user.age = localStorage.getItem('user.age')
                this.user.email = localStorage.getItem('user.email')
                this.user.gender = localStorage.getItem('user.gender')
                this.user.avatar = localStorage.getItem('user.avatar')
                this.user.bio = localStorage.getItem('user.bio')
                this.user.locations = localStorage.getItem('user.locations')
                this.user.isAuthenticated = true

                this.refreshToken()

                console.log('Initialized user:', this.user)
            }
        },

        //login
        setToken(data) {
            console.log('setToken', data)

            this.user.access = data.access
            this.user.refresh = data.refresh
            this.user.isAuthenticated = true

            localStorage.setItem('user.access', data.access)
            localStorage.setItem('user.refresh', data.refresh)

            console.log('user.access: ', localStorage.getItem('user.access'))
        },

        //logout
        removeToken() {
            console.log('removeToken')

            this.user.refresh = null
            this.user.access = null
            this.user.isAuthenticated = false
            this.user.id = null
            this.user.name = null
            this.user.email = null
            this.user.gender = null
            this.user.avatar = null
            this.user.age = null
            this.user.locations = null
            this.user.bio = null

            localStorage.setItem('user.access', '')
            localStorage.setItem('user.refresh', '')
            localStorage.setItem('user.id', '')
            localStorage.setItem('user.name', '')
            localStorage.setItem('user.age', '')
            localStorage.setItem('user.email', '')
            localStorage.setItem('user.gender', '')
            localStorage.setItem('user.bio', '')
            localStorage.setItem('user.locations', '')
            localStorage.setItem('user.avatar', '')

        },

        setUserInfo(user) {
            console.log('setUserInfo', user)

            this.user.id = user.id
            this.user.name = user.name
            this.user.email = user.email
            this.user.gender = user.gender
            this.user.avatar = user.avatar
            this.user.locations = user.locations
            this.user.age = user.age
            this.user.bio = user.bio

            localStorage.setItem('user.id', this.user.id)
            localStorage.setItem('user.name', this.user.name)
            localStorage.setItem('user.email', this.user.email)
            localStorage.setItem('user.gender', this.user.gender)
            localStorage.setItem('user.bio', this.user.bio)
            localStorage.setItem('user.age', this.user.age)
            localStorage.setItem('user.locations', this.user.locations)
            localStorage.setItem('user.avatar', this.user.avatar)

            console.log('User', this.user)
        },

        refreshToken() {
            axios.post('/api/refresh/', {
                refresh: this.user.refresh
            })
                .then((response) => {
                    this.user.access = response.data.access

                    localStorage.setItem('user.access', response.data.access)

                    axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
                })
                .catch((error) => {
                    console.log(error)

                    this.removeToken()
                })
        },
    }
})