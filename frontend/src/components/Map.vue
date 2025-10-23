<script setup>
import { onMounted, watch, computed } from 'vue';
import { initMap } from '@/composables/useMap'; 
import { useFormStore } from '@/store/formStore';
import { newMarker, mapReady } from '@/composables/useMap';

const mapContainer = 'map-container';

const formStore = useFormStore();
const stops = formStore.currentFormState.stops


const allLocationCoords = computed(() => {
    const locations = [];
    
    stops.forEach((place) => {
        locations.push({
            lat: place.places.location.latitude, 
            lng: place.places.location.longitude
        })
    })
    console.log(locations)
    return locations;
});

watch(allLocationCoords, (newLocations) => {
    if (newLocations.length > 0) {
        newMarker(newLocations);
        console.log(`Map updated with ${newLocations.length} locations.`);
    } else {
        newMarker([]); 
    }
}, { deep: true }); 

onMounted(() => {
  initMap(mapContainer);
  mapReady.then(() => {
        console.log('Map is fully initialized and ready for commands.');
        newMarker(allLocationCoords.value);
    });
});


</script>

<template>
  <div :id="mapContainer" class="w-screen h-[100dvh]"></div>
</template>

<style scoped>
</style>