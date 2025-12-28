<script setup>
import { useRouter } from 'vue-router';
const router = useRouter();

const isLoggedIn = false;
</script>

<template>
    <nav id="topNav" class="bg-transparent p-2 z-10 fixed top-0 w-screen">
        <div class="h-3rem w-screen flex justify-between items-center hover:opacity-80 pointer-cursor">
            <router-link to="/" class="h-12 w-12 flex items-center px-4 bg-transparent">
                <img src="@/assets/imgs/ItineroLogo.svg" alt="Logo" class="w-12 h-12 scale-200"/>
            </router-link>
        </div>
    </nav>
</template>















