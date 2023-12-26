import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import SignupView from '../views/SignupView.vue';
import LoginView from '../views/LoginView.vue';
import FeedView from '../views/FeedView.vue';
import ChatDetailView from '../views/ChatDetailView.vue';
import SearchView from '../views/SearchView.vue';
import ProfileView from '../views/ProfileView.vue';
import FriendsView from '../views/FriendsView.vue';
import PostView from '../views/PostView.vue';
import ChatView from '../views/ChatView.vue';
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView,
    },
    {
      path:'/search',
      name:'search',
      component: SearchView,
    },
    {
      path:'/profile/:id',
      name:'profile',
      component: ProfileView,
    },
    { 
      path:'/profile/:id/friends',
      name:'friends',
      component: FriendsView,
    },
    {
      path:'/:id',
      name:'postdetail',
      component:PostView
    },
    {
      path:'/chat',
      name:'chat',
      component:ChatView
      
    },
    {
      path:'/chat/:id',
      name:'chatdetail',
      component: ChatDetailView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
  ],
  
});


export default router;
