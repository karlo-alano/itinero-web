<script setup>
import ProgressBar from 'primevue/progressbar';
</script>

<template>
<div class="h-screen w-screen">
    
    <div class="w-full h-full flex justify-center items-center flex-col">
        <p class="text-3xl font-extrabold mb-5 text-primary-500">Generating your itinerary...</p>
        <ProgressBar mode="indeterminate" style="height: 10px" class="grid-row-2 w-[50%]"></ProgressBar>
    </div>
    
</div>
</template>