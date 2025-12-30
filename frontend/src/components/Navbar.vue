<script setup>
import { useFormStore } from '@/store/formStore';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/userStore';
const formStore = useFormStore();
const router = useRouter();
const userStore = useUserStore();

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

</script>
<template>
      <nav class="p-4 flex justify-center items-center h-screen">
        <div class="navbarContainer">
           <router-link to="/" class="flex items-center gap-3 hover:opacity-80 transition duration-150">
               <img src="@/assets/imgs/ItineroLogo.svg" alt="Logo" class="h-15 w-15"/>
               <h1 class="label text-3xl font-bold text-primary-500 font-[Inter]">Itinero</h1>
           </router-link>
           <hr class="mb-2 mt-2">
           <div class="flex flex-col justify-between items-center h-full">
             <div class="top-item-container flex flex-col gap-2 h-full items-center">
              <div class="nav-item hover:bg-slate-200 transition-all duration-250 ease-in-out cursor-pointer rounded-xl" :class="{ 'nav-item-active': isActive('/Create') }" @click="createAndRefresh">
                <Button icon="pi pi-plus" rounded class="icon-class bg-transparent border-0 text-black hover:bg-transparent transition-all duration-550 ease-in-out"/>
                <span class="label">Create</span>
              </div>
              <div class="nav-item hover:bg-slate-200 transition-all duration-250 ease-in-out cursor-pointer rounded-xl" :class="{ 'nav-item-active': isActive('/Explore') }" @click="router.push('/Explore')">
                <Button icon="pi pi-compass" rounded class="icon-class bg-transparent border-0 text-black hover:bg-transparent transition-all duration-550 ease-in-out" />
                <span class="label">Explore</span>
              </div>
              <div class="nav-item hover:bg-slate-200 transition-all duration-250 ease-in-out cursor-pointer rounded-xl">
                <Button icon="pi pi-cog" rounded class="icon-class bg-transparent border-0 text-black hover:bg-transparent transition-all duration-550 ease-in-out hover:rotate-45"/>
                <span class="label">Settings</span>
              </div>
             </div>
             <div class="nav-item hover:bg-slate-200 transition-all duration-250 ease-in-out cursor-pointer rounded-xl" :class="{ 'nav-item-active': isActive('/Registration') || isActive('/Account')}" @click="registration">
              <Button icon="pi pi-user" rounded class="icon-class bg-transparent border-0 text-black hover:bg-transparent transition-all duration-550 ease-in-out hover:rotate-45"/>
              <span class="label">Account</span>
             </div>
           </div>
          </div>
      </nav>

</template>

<style scoped>
  @import '@/assets/styles.css';

  .navbarContainer {
    @apply bg-white w-18 h-full drop-shadow-2xl flex flex-col p-2 rounded-xl border-1 border-slate-300  hover:w-55;
    transition: all 0.3s ease-in-out !important;
  }

  .label {
    transition: opacity 0.2s ease-in-out, transform 0.2s ease-in-out, max-width 0.3s ease-in-out;
    opacity: 0;
    max-width: 0;
    transform: translateX(30px);
  }

  .top-item-container .nav-item, .nav-item {
    @apply flex items-center min-w-10 h-12  p-2;
    transition: min-width 0.3s ease-in-out !important;
  }

  .navbarContainer:hover .label {
    display: flex;
    transform: translateX(0);
    opacity: 100;
    max-width:50px;
  }

  .navbarContainer:hover .nav-item, .navbarContainer:hover .top-item-container .nav-item {
    @apply min-w-50;
    transition-delay: 0.3s;
    transition: background-color 0.2s ease-in-out;
  }

  .nav-item:hover .icon-class {
    @apply rotate-20
  }

  .nav-item-active {
    @apply bg-slate-300
  }




</style>