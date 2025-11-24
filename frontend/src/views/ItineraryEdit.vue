<script setup>
import { useFormStore } from '@/store/formStore.js';

const formStore = useFormStore();

const destinationsArray = formStore.tripData.stops
const durations = formStore.tripData.durations
const distances = formStore.tripData.distances
const totalDurationData = formStore.tripData.totalDuration
const totalDuration = Math.ceil(totalDurationData / 60)
const totalDistanceData = formStore.tripData.totalDistance
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

const otherDestinationsArray = formStore.tripData.otherResults
const otherStops = []

otherDestinationsArray.forEach((type) => {
    type.places.forEach((place) => {
        const otherStop = {
            tag: type.interestType,
            title: place.displayName.text,
            address: place.formattedAddress,
            id: place.id,
            lat: place.location.latitude,
            lng: place.location.longitude,
        }
        otherStops.push(otherStop)
    })
})

const numbers = 5;
const numbers2 = 9;
</script>

<template>
    <section class="h-[100dvh] w-screen bg-slate-50 flex md:flex-row">
        <section class="w-[30%] h-full bg-transparent md:ml-20 p-4 ">
            <div class="w-full h-full bg-white rounded-xl shadow-2xl flex flex-col p-2  ">
                <div id="lowerBox" class="h-full bg-slate-100 rounded-xl flex flex-col p-2 gap-2 overflow-y-scroll">

                    <div v-for="stop in stops" :key="stop.title" class="w-full min-h-55 rounded-xl shadow-[0_0_10px_rgba(0,0,0,0.2)] p-4 grid grid-cols-4 grid-rows-5 cursor-pointer transition-all ease-in">
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


        </section>
        <section class="w-[70%] h-[100dvh] p-4 flex flex-col">
            <div class="text-7xl font-bold h-[10%]">Edit</div>
            <div class="grid grid-rows-4 grid-cols-3 gap-4 p-4 h-full overflow-y-scroll">
                <div v-for="stop in otherStops" :key="stop.title" class="h-full w-full rounded-xl bg-white drop-shadow-2xl p-2">
                    {{ stop.title }}
                </div>
            </div>
            
        </section>
    </section>
</template>