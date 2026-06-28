<script setup>
import { watch } from 'vue';
import { useRoute } from 'vue-router'; 
import { useToast } from 'primevue/usetoast';
import { useToastStore } from '@/store/toastStore';
import Toast from 'primevue/toast';

const toast = useToast();
const toastStore = useToastStore();
const route = useRoute();

  watch(() => route.path, () => {
    const message = toastStore.consume(); 
    
    if (message) {
        toast.add(message);
    }
}, { immediate: true });
</script>

<template>
  <div id="app" class="h-dvh w-full relative overflow-hidden">
    <Toast />
    <router-view />
  </div>
    
</template>

<style scoped>

</style>
