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
    <div class="max-h-[100dvh] w-screen pointer-events-none">
        <nav id="topNav" class="bg-transparent p-2 z-10 fixed top-0">
                <div class="h-3rem w-screen flex justify-between items-center hover:opacity-80 pointer-cursor">
                    <router-link to="/" class="h-12 w-12 flex items-center px-4 bg-red-500">
                        <img src="@/assets/imgs/Itinero_standalone.svg" alt="Logo" class="w-12 h-12 scale-200"/>
                    </router-link>
                    <div>
                        <Avatar v-if="isLoggedIn" label="K" class="mr-3 shadow-xl" size="large" style="background-color: #9954DD; color: white" shape="circle" severity="secondary"/>
                        <Button label="Sign In" rounded raised class="mr-4 w-25 pointer-events-auto"></Button>                        
                    </div>
                </div>
            </nav>

        <nav class="h-2rem w-screen z-10 fixed bottom-0">
            <div class="flex justify-around p-2 gap-3 bg-white shadow-2xl">
                <Button class="w-15 h-15 bg-white border-0 pointer-events-auto" severity="secondary" icon="pi pi-plus" @click="createAndRefresh" />
                <Button class="w-15 h-15 bg-white border-0 pointer-events-auto" severity="secondary" icon="pi pi-compass" @click="router.push('/Explore')"/>
                <Button class="w-15 h-15 bg-white border-0 pointer-events-auto" severity="secondary" icon="pi pi-book"/>
                <Button class="w-15 h-15 bg-white border-0 pointer-events-auto" severity="secondary" icon="pi pi-user" />
            </div>
            </nav>

    </div>

    
</template>

