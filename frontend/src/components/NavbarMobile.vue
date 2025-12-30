<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

import { useUserStore } from '@/store/userStore';
const userStore = useUserStore();

import { useFormStore } from '@/store/formStore';
const formStore = useFormStore();

const createAndRefresh = () => {
    formStore.resetState()
    router.push('/Create'); 
};

const registration = () => {
  const isLoggedIn = userStore.hasProfile;
  if (!isLoggedIn) {
    router.push('/Registration')
  } else {
    router.push('/Account')
  }
}

const isActive = (navPath) => {
  const path = router.currentRoute.value.path;
  return path === navPath;
};


const isLoggedIn = false;
</script>

<template>
    <nav class="h-2rem w-screen z-10">
        <div class="flex justify-center p-2 bg-white shadow-2xl">
            <div class="nav-item" :class="{ 'nav-item-active': isActive('/Create') }">
                <Button class="w-25 h-15 bg-white border-0 text-slate-500" severity="secondary" icon="pi pi-plus" @click="createAndRefresh" label="Create" icon-pos="top"/>
            </div>
            <div class="nav-item" :class="{ 'nav-item-active': isActive('/Explore') }">
                <Button class="w-25 h-15 bg-white border-0 text-slate-500" severity="secondary" icon="pi pi-compass" @click="router.push('/Explore')" label="Explore" icon-pos="top"/>
            </div>
            <div class="nav-item" :class="{ 'nav-item-active': isActive('/Registration') || isActive('/Account')}">
                <Button class="w-25 h-15 bg-white border-0 text-slate-500" severity="secondary" icon="pi pi-user" @click="registration" label="User" icon-pos="top"/>
            </div>
        </div>
    </nav>
</template>

<style scoped>
    @import '@/assets/styles.css';

    .nav-item-active Button{
    @apply bg-slate-200 font-extrabold text-slate-700
  }

</style>

