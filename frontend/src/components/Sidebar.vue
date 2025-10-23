<script setup>
import { ref } from 'vue';
import Chip from 'primevue/chip';

import { useFormStore } from '@/store/formStore.js';

import { togglePan, isPanned, activeStopTitle } from '@/composables/useMap';


const formStore = useFormStore();
const destinationsArray = formStore.currentFormState.stops
const durations = formStore.currentFormState.durations
const distances = formStore.currentFormState.distances
const totalDurationData = formStore.currentFormState.totalDuration
const totalDuration = Math.ceil(totalDurationData / 60)


const totalDistanceData = formStore.currentFormState.totalDistance
const totalDistance = Number(totalDistanceData / 1000).toFixed(1)
const stops = []

destinationsArray.forEach((place,index) => {
    const stop = {
        tag: place.interestType,
        title: place.places.displayName.text,
        address: place.places.formattedAddress,
        distance: distances[index],
        duration: durations[index],
        lat: place.places.location.latitude,
        lng: place.places.location.longitude,
        arrivalTime: place.arrival_time,
        departureTime: place.leave_time
    }
    stops.push(stop)    
 })



const startTime = ref('3:30')
const endTime = ref('4:45')
console.log("sidebar", destinationsArray)
console.log("Stops:", stops)
</script>


<template>
    <div id="sideBarContainer" class="bg-transparent z-5 p-4 h-full w-full">
        <div class="w-full h-full bg-white rounded-xl shadow-[0_0_10px_rgba(0,0,0,0.5)] flex flex-col p-2">
            <div class="flex p-2 gap-2 justify-between">
                <div class="flex items-center font-bold ">Total Metrics </div>
                <div class="flex gap-2">
                    <Chip class="rounded-full bg-primary-400 text-white font-bold text-sm pr-2 w-25">
                        <i class="material-icons">straighten</i>
                        {{ totalDistance }} km
                    </Chip>
                    <Chip icon="" class="rounded-full bg-primary-400 text-white font-bold text-sm w-25">
                        <i class="material-icons">directions_walk</i>
                        {{ totalDuration }} min
                    </Chip>
                </div>
            </div>
            <div id="lowerBox" class="h-full bg-slate-100 rounded-xl flex flex-col p-2 gap-2 overflow-y-auto">
                <div v-for="stop in stops" :key="stop.title" @click="togglePan(stop.lat, stop.lng, stop.title)" 
                :class="{
                'w-full min-h-55 rounded-xl shadow-[0_0_10px_rgba(0,0,0,0.2)] p-4 grid grid-cols-4 grid-rows-5 border-b-8 cursor-pointer transition-all ease-in': true,
                
                'border-primary-200': activeStopTitle !== stop.title,
                'border-primary-400 scale-101 bg-white': activeStopTitle === stop.title
                }">      
                    <div class="col-start-1 row-start-1 col-span-3 overflow-hidden row-span-2 min-h-10 flex justify-baseline">
                        <p class="font-bold text-xl">{{ stop.title }}</p>
                    </div>
                    <div class="p-2 h-10 text-xs bg-primary-200 rounded-full col-start-4 row-span-1 flex justify-center items-center">
                        <p class="font-bold text-white">{{ stop.tag.charAt(0).toUpperCase() + stop.tag.slice(1) }}</p>
                    </div>
                    <p class="row-start-3 col-span-4 row-span-2 text-slate-700 italic text-md overflow-hidden">{{stop.address}}</p>
                    <p class="row-start-5 text-slate-700 w-5">{{ stop.arrivalTime }}</p>
                    <p class="row-start-5 text-slate-700 w-5">{{ stop.departureTime }}</p>
                    <p class="row-start-5 col-start-3 col-span-2">{{ stop.distance }} meters from last stop</p>
                    
                </div>
            </div>

        </div>
    </div>
</template>