// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

//layouts
import NavbarLayout from '@/layouts/NavbarLayout.vue'
import SidebarLayout from '@/layouts/SidebarLayout.vue'


//views
import Home from '@/views/Home.vue'
import Dashboard from '@/views/Dashboard.vue'
import Create from '@/views/Create.vue'
import LoadingScreen from '@/views/LoadingScreen.vue'
import Explore from '@/views/Explore.vue'
import Registration from '@/views/Registration.vue'
import Blog from '@/views/Blog.vue'

const routes = [
    {
        path: '/',
        component: NavbarLayout,
        children: [
            {path: '', name: 'Home', component: Home},
            {path: '/Create', name: 'Create', component: Create},
            {path: '/Loading', name: 'Loading', component: LoadingScreen},
            {path: '/Explore', name: 'Explore', component: Explore},
            {path: '/Blog', name: 'Blog', component: Blog},
            {path: 'Registration', name: 'Registration', component: Registration}
        ]
    },
    {
        path: '/Dashboard',
        component: SidebarLayout,
        children: [
            {path: '', name: 'Dashboard', component: Dashboard}
        ]
    }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export let routerInstance = router
export default router