<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

const createAndRefresh = () => {
    router.push('/Create'); 
    setTimeout(() => {
        window.location.reload(); 
    }, 50); 
};

const isLoggedIn = false;

</script>

<template>
      <!-- <nav id="topNavContainerDesktop" class="bg-transparent hidden md:flex justify-between items-center p-2 z-10">
        <div class="h-3rem w-screen flex">
          <router-link to="/" class="h-12 flex items-center px-4 hover:opacity-80 transition duration-150">
              <img src="@/assets/imgs/Itinero_Standalone.svg" alt="Logo" class="w-10 h-10"/>
              <p class="text-4xl font-bold text-primary-200">Itinero</p>
          </router-link>

          <Button label="Create" rounded raised class="mr-2 w-30 pointer-events-auto" severity="secondary" icon="pi pi-plus" @click="createAndRefresh"/>
          <Button label="Explore" rounded raised class="mr-2 w-30 pointer-events-auto" severity="secondary" icon="pi pi-compass" @click="router.push('/Explore')"/>
          <Button label="Settings" rounded raised class="mr-2 w-30 pointer-events-auto" severity="secondary" icon="pi pi-cog" />
          <Button label="About" rounded raised class="mr-2 w-30 pointer-events-auto" severity="secondary" icon="pi pi-question"/>
        </div>

        <div>
          <Avatar v-if="isLoggedIn" label="K" class="mr-4 shadow-xl" size="large" style="background-color: #9954DD; color: white" shape="circle" severity="secondary"/>
          <Button v-else label="Sign In" rounded raised class="mr-4 w-30 pointer-events-auto" @click="router.push('/Register')"/>
        </div>
      </nav>

       -->
      <nav class="py-4 pl-6 pr-4 ml-3 flex justify-center items-center h-screen">
        <div class="bg-white w-16 h-full drop-shadow-2xl flex flex-col p-3 rounded-xl">
           <router-link to="/" class="flex flex-col items-center gap-3 py-4 hover:opacity-80 transition duration-150">
               <img src="@/assets/imgs/Itinero_standalone.svg" alt="Logo" class="h-10 w-10"/>
           </router-link>
           <hr class="mb-2 mt-4">
           <div class="flex flex-col justify-between items-center h-full">
             <div class="flex flex-col gap-2">
              <Button icon="pi pi-plus" rounded class="bg-transparent border-0 text-black font-bold hover:bg-slate-300 transition-all duration-250 ease-in-out hover:rotate-45" @click="createAndRefresh"/>
              <Button icon="pi pi-compass" rounded class="bg-transparent border-0 text-black hover:bg-slate-300 transition-all duration-250 ease-in-out hover:rotate-45" @click="router.push('/Explore')"/>
              <Button icon="pi pi-book" rounded class="bg-transparent border-0 text-black hover:bg-slate-300 transition-all duration-250 ease-in-out hover:rotate-45" @click="router.push('/Blog')"/>
              <Button icon="pi pi-cog" rounded class="bg-transparent border-0 text-black hover:bg-slate-300 transition-all duration-250 ease-in-out hover:rotate-45"/>
             </div>
             <div>
              <Button icon="pi pi-user" rounded class="bg-transparent border-0 text-black hover:bg-slate-300 transition-all duration-250 ease-in-out hover:rotate-45" @click="router.push('/Registration')"/>
             </div>
           </div>
          </div>
      </nav>

</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Ubuntu:wght@500;600;700&display=swap");

.itineroword {
  font-family: "Ubuntu", sans-serif;
}
</style>