<script setup>
import InputText from 'primevue/inputtext';
import Chip from 'primevue/chip';

import { supabase } from '@/lib/supabase';
import { ref, onMounted, computed } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import ToggleSwitch from 'primevue/toggleswitch';
import { useToast } from 'primevue/usetoast';
import { useUserStore } from '@/store/userStore';

const catalog = 2

const search = null;

const publicItineraries = ref([]);

let isLoading = ref(false);

const userStore = useUserStore();
const toast = useToast();
const saving = ref(false);

let visible = ref(false);
const selectedItinerary = ref(null);
let stopsArray = ref(null);
let isPublic = ref(null);

// Typing animation
const displayedTitle = ref("");
const fullTitleText = "Pocket Journals";

const selectItinerary = (itinerary) => {
    selectedItinerary.value = itinerary;
    visible.value = true;

    stopsArray.value = selectedItinerary.value.itinerary_stops?.[0]?.full_trip_data?.stops;
    isPublic.value = selectedItinerary.value.is_public;
    
    // Ensure tags is always an array of strings
    if (Array.isArray(selectedItinerary.value.tags)) {
        selectedItinerary.value.parsedTags = selectedItinerary.value.tags;
    } else if (typeof selectedItinerary.value.tags === 'string') {
        let tagString = selectedItinerary.value.tags;
        tagString = tagString.replace(/^{|}$|^\[|\]$/g, ''); 
        selectedItinerary.value.parsedTags = tagString ? tagString.split(',').map(tag => tag.trim().replace(/^"|"$/g, '')) : [];
    } else {
        selectedItinerary.value.parsedTags = [];
    }

    console.log('selected:', stopsArray.value);
    console.log('public', isPublic.value);
    console.log('tags:', selectedItinerary.value.parsedTags);
};

async function saveItinerary() {
    if (!selectedItinerary.value || !userStore.profile) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'No itinerary selected or user profile not loaded', life: 3000 });
        return;
    }

    saving.value = true;
    try {
        // 1. Prepare data for the new itinerary
        const newTitle = selectedItinerary.value.title + ' (Copy)';
        const newDescription = selectedItinerary.value.description;
        const newTags = selectedItinerary.value.parsedTags; // Use the parsed tags
        const newIsPublic = false; // Always set to false for copied itineraries
        const ownerId = userStore.profile.id;

        // 2. Insert the new itinerary header
        const { data: newItineraryData, error: itineraryError } = await supabase
            .from('itineraries')
            .insert({
                owner_id: ownerId,
                title: newTitle,
                description: newDescription,
                is_public: newIsPublic,
                tags: newTags,
                created_at: new Date().toISOString() // Add created_at timestamp
            })
            .select('id')
            .single();

        if (itineraryError) throw itineraryError;

        const newItineraryId = newItineraryData.id;

        // 3. Insert itinerary stops
        console.log('Selected Itinerary Stops before insert:', selectedItinerary.value.itinerary_stops); // Added log

        if (selectedItinerary.value.itinerary_stops && selectedItinerary.value.itinerary_stops.length > 0) {
            const stopsToInsert = selectedItinerary.value.itinerary_stops.map(stop => ({
                itinerary_id: newItineraryId,
                full_trip_data: selectedItinerary.value.itinerary_stops?.[0]?.full_trip_data // Copy the entire full_trip_data object
            }));
            
            const { error: stopsError } = await supabase
                .from('itinerary_stops')
                .insert(stopsToInsert);

            if (stopsError) throw stopsError;
        }

        toast.add({ severity: 'success', summary: 'Success', detail: 'Itinerary copied successfully to your saved itineraries!', life: 3000 });
        visible.value = false; // Close dialog on success
    } catch (error) {
        console.error('Error saving itinerary:', error);
        toast.add({ severity: 'error', summary: 'Error', detail: `Failed to copy itinerary: ${error.message || error}`, life: 3000 });
    } finally {
        saving.value = false;
    }
}

async function fetchPublicItineraries() {
    isLoading.value = true; // Set loading to true at the start
    try {
        const { data, error } = await supabase
            .from('itineraries')
            .select('*, itinerary_stops(*), users(user_name)') // Join with users table to get user_name
            .eq('is_public', true);

        if (error) {
            console.error('Error fetching public itineraries:', error);
            // Optionally, clear publicItineraries on error
            publicItineraries.value = [];
        } else {
            publicItineraries.value = data.map(itinerary => ({
                ...itinerary,
                parsedTags: parseTags(itinerary.tags)
            }));
        }
    } catch (e) {
        console.error('Unhandled error in fetchPublicItineraries:', e);
        publicItineraries.value = []; // Clear on unhandled error as well
    } finally {
        isLoading.value = false; // Always set to false when done
    }
}

function parseTags(tagsData) {
    if (Array.isArray(tagsData)) {
        return tagsData;
    } else if (typeof tagsData === 'string') {
        let tagString = tagsData;
        tagString = tagString.replace(/^{|}$|^\[|\]$/g, ''); 
        return tagString ? tagString.split(',').map(tag => tag.trim().replace(/^"|"$/g, '')) : [];
    } else {
        return [];
    }
}

onMounted(() => {
    // Typewriter effect for title
    const typeWriter = () => {
        let i = 0;
        const speed = 80;
        const type = () => {
            if (i < fullTitleText.length) {
                displayedTitle.value += fullTitleText.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        };
        setTimeout(type, 200);
    };
    typeWriter();

    fetchPublicItineraries();
});
</script>

<template>
    <section class="min-h-dvh w-full gradient-5 p-4 pl-25 animate-enter" style="--delay:0s">
        <div class="mb-8">
            <h1 class="text-5xl font-extrabold mb-2">
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-700 via-purple-600 to-indigo-600">{{ displayedTitle }}</span><span class="blinking-cursor text-purple-700">|</span>
            </h1>
            <p class="text-lg text-slate-600 subtext-animate">Your saved itineraries and discoveries.</p>
        </div>
        <div v-if="isLoading" class="flex justify-center items-center text-xl">Loading...</div>
        <div class="grid grid-cols-3 gap-2">
            <div v-for="itinerary in publicItineraries" :key="itinerary.id" class="card bg-white hover:bg-slate-100 cursor-pointer animate-enter" style="--delay:0s" @click="selectItinerary(itinerary)">
                <h1 class="text-xl text-slate-800 font-bold">{{ itinerary.title }}</h1>
                <p class="font-italic text-slate-700 mb-5">Author: {{ itinerary.users?.user_name || 'Unknown' }}</p>
                <p class="text-slate-700">{{ itinerary.description }}</p>
                <hr class="text-black text-xl p-2 mt-8">
                <div class="flex gap-2">
                    <Chip v-for="tag in itinerary.parsedTags" :key="tag" :label="tag" class="border-1 border-slate-300 flex justify-center p-1 text-sm w-15"/>
                </div>
                <p class="mt-10 text-xs text-slate-500">Created: {{ new Date(itinerary.created_at).toLocaleDateString() }}</p>

            </div>
        </div>


        <Dialog v-model:visible="visible" modal :header="'Itinerary Details'" :style="{ width: '60rem'}" class="card gradient-5 h-150">
            <div class="h-full flex flex-col justify-between" v-if="selectedItinerary">
                <div class="flex-1">
                    <div class="flex">
                        <div class="w-[50%]">
                            <div class="flex items-center gap-4 mb-4">
                                <h1 class="font-bold text-xl">{{ selectedItinerary.title }}</h1>
                            </div>
                            
                            <div class="flex items-center gap-4 mb-4">
                                <p class="text-slate-700">{{ selectedItinerary.description }}</p>                          
                            </div>

                            <div class="flex flex-col gap-4 mb-8">
                                <label for="tags" class="font-semibold w-24">Tags</label>
                                <div class="flex flex-wrap gap-1 w-full">
                                    <Chip 
                                        v-for="tag in selectedItinerary.parsedTags" 
                                        :key="tag" 
                                        :label="tag" 
                                        class="text-sm bg-white border border-slate-300"
                                    />
                                </div>
                            </div>

            
                            <p class="text-sm">Created: {{ selectedItinerary.created_at }}</p>
                            <p class="text-sm">Author: {{ selectedItinerary.users?.user_name || 'Unknown' }}</p>
                            <p class="text-sm">Total Stops: {{ stopsArray?.length || 0 }}</p>
                        </div>
                        <div class="flex flex-col gap-2 overflow-y-scroll p-4">
                            <h1 class="font-bold text-xl">Stops:</h1>
                            <div v-for="stop in stopsArray" class="card bg-slate-100 w-full p-2">
                                <h1>{{ stop.places.displayName.text }}</h1>
                            </div>
                        </div>
                    </div>
                </div>    
                
                <div class="flex justify-between gap-2 pt-20">
                    <div>
                        <Button type="button" label="Edit in Itinerary Viewer" severity="secondary" @click="visible = false" class="interactive-btn-secondary w-55 h-full"></Button>
                    </div>
                    <div class="flex gap-2">
                        <Button type="button" label="Close" severity="secondary" @click="visible = false" class="interactive-btn-secondary w-25 h-full"></Button>
                        <Button type="button" label="Save Itinerary" @click="saveItinerary" class="interactive-btn-primary w-40" :loading="saving" :disabled="saving || !userStore.profile || selectedItinerary.owner_id === userStore.profile.id" v-if="selectedItinerary.owner_id !== userStore.profile?.id"></Button>
                    </div>
                </div>
            </div>

         </Dialog>

    </section>
</template>

<style>
.blinking-cursor {
    font-weight: 100;
    animation: blink 1s step-end infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

.subtext-animate {
    opacity: 0;
    transform: translateY(10px);
    animation: subtextFadeIn 0.8s ease-out forwards;
    animation-delay: 0.4s;
}

@keyframes subtextFadeIn {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
}
</style>
