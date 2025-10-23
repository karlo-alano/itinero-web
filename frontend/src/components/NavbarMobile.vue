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
    <div class="h-[100dvh] w-screen pointer-events-none ">
        <nav id="topNav" class="bg-transparent p-2 z-10 fixed">
                <div class="h-3rem w-screen flex justify-between items-center">
                    <router-link to="/" class="h-12 flex items-center px-4">
                        <img src="@/assets/imgs/Itinero_Standalone.svg" alt="Logo" class="w-10 h-10"/>
                    </router-link>
                    <div>
                        <Avatar v-if="isLoggedIn" label="K" class="mr-3 shadow-xl" size="large" style="background-color: #9954DD; color: white" shape="circle" severity="secondary"/>
                        <Button label="Sign In" rounded raised class="mr-4 w-25 pointer-events-auto"></Button>                        
                    </div>
                </div>
            </nav>

        <nav class="h-2rem w-screen z-10 fixed bottom-0">
            <div class="flex justify-between p-2 bg-white">
                <Button label="Create" class="w-1/3 bg-white border-0 pointer-events-auto" severity="secondary" icon="pi pi-plus" icon-pos="top" @click="createAndRefresh" />
                <Button label="Explore" class=" w-1/3 bg-white border-0 pointer-events-auto" severity="secondary" icon="pi pi-compass" icon-pos="top"/>
                <Button label="Settings" class=" w-1/3 bg-white border-0 pointer-events-auto" severity="secondary" icon="pi pi-cog" icon-pos="top"/>
            </div>
            </nav>

    </div>

    
</template>

