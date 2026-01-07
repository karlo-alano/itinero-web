<script setup>
    import { ref, computed, onBeforeMount } from 'vue'; // Added onBeforeMount
    import Chip from 'primevue/chip';
    import Button from 'primevue/button';
    import { useFormStore } from '@/store/formStore.js';
    import { togglePan, activeStopTitle } from '@/composables/useMap';
    import { useRouter } from 'vue-router';
    import { useUserStore } from '@/store/userStore.js';
    
    const userStore = useUserStore();
    const isLoggedIn = userStore.hasProfile;
    
    const router = useRouter();
    const formStore = useFormStore();
    
    // --- 1. COMPUTED PROPERTIES (The Fix) ---
    // This prevents the "Cannot read properties of null" error
    const stops = computed(() => {
        // Safety Check: Return empty array if data is missing
        if (!formStore.tripData || !formStore.tripData.stops) return [];
    
        const destinationsArray = formStore.tripData.stops;
        const durations = formStore.tripData.durations || [];
        const distances = formStore.tripData.distances || [];
    
        return destinationsArray.map((place, index) => ({
            tag: place.interestType,
            title: place.places.displayName.text,
            address: place.places.formattedAddress,
            distance: distances[index] || 0,
            duration: durations[index] || 0,
            lat: place.places.location.latitude,
            lng: place.places.location.longitude,
            arrivalTime: place.arrival_time,
            departureTime: place.leave_time
        }));
    });
    
    const totalDuration = computed(() => {
        if (!formStore.tripData) return 0;
        return Math.ceil(formStore.tripData.totalDuration / 60);
    });
    
    const totalDistance = computed(() => {
        if (!formStore.tripData) return 0;
        return Number(formStore.tripData.totalDistance / 1000).toFixed(1);
    });
    
    // --- 2. LOGIC ---
    async function saveItinerary() {
        const result = await formStore.saveTripPlan();
        if (result.success) {
            console.log('Successfully saved');
            // Optional: You could add a toast notification here
        } else {
            alert(`Failed to save trip: ${result.error}`);
        }
    }
    
    // Drawer Logic
    const isOpen = ref(true);
    
    const toggleButton = () => {
        isOpen.value = !isOpen.value;
    };
    
    const positionClass = computed(() => {
        return isOpen.value ? 'translate-x-0' : '-translate-x-[100%]';
    });
    
    const regenerateItinerary = () => {
        router.push('/Loading');
        formStore.regenerateItinerary();
    }
    
    // --- 3. SAFETY REDIRECT ---
    onBeforeMount(() => {
        if (!formStore.tripData || !formStore.tripData.stops) {
            console.warn("Mobile Sidebar: No trip data found, redirecting...");
            router.push('/Create');
        }
    });
    </script>
    
    <template>
        <div id="sideBarContainer"
            class="fixed h-[calc(100%-5rem)] max-w-[90vw] z-50 pointer-events-auto flex flex-col transition-transform duration-300 ease-in-out p-2 pr-0 justify-center"
            :class="positionClass">
    
            <div class="absolute right-[-40px] top-60 z-50">
                <Button 
                    @click="toggleButton"
                    :icon="isOpen ? 'pi pi-chevron-left' : 'pi pi-chevron-right'"
                    class="!w-10 !h-10 !rounded-r-xl !rounded-l-none !bg-white !text-slate-700 !border-l-0 !border-slate-300 shadow-lg"
                    aria-label="Toggle Drawer" 
                />
            </div>
    
            <div class="w-full top-6 h-[93%] bg-white rounded-xl shadow-2xl flex flex-col p-2 gap-2 overflow-hidden relative card">
                
                <div class="flex p-2 gap-2 justify-between items-center border-b border-slate-100 pb-4">
                    <div class="flex items-center font-bold text-md text-slate-800">Total Metrics</div>
                    <div class="flex gap-2">
                        <Chip class="!bg-slate-700 !text-white !font-bold !text-xs">
                            <i class="pi pi-compass mr-1"></i>
                            {{ totalDistance }} km
                        </Chip>
                        <Chip class="!bg-slate-700 !text-white !font-bold !text-xs">
                            <i class="pi pi-clock mr-1"></i>
                            {{ totalDuration }} min
                        </Chip>
                    </div>
                </div>
    
                <div id="lowerBox" class="flex-1 bg-slate-50 rounded-lg flex flex-col p-2 gap-3 overflow-y-auto">
                    <div v-for="stop in stops" :key="stop.title" @click="togglePan(stop.lat, stop.lng, stop.title)"
                        class="relative w-full rounded-xl p-4 cursor-pointer transition-all duration-200 shadow-sm hover:shadow-md card"
                        :class="activeStopTitle === stop.title ? 'bg-white' : 'bg-slate-100'">
                        
                        <div class="flex justify-between items-start mb-2">
                            <h3 class="font-bold text-slate-800 leading-tight pr-2">{{ stop.title }}</h3>
                            <span class="text-[10px] font-bold uppercase tracking-wider px-2 py-1 text-xs bg-slate-200 border-1 border-slate-300 rounded-full shrink-0">
                                {{ stop.tag }}
                            </span>
                        </div>
    
                        <p class="text-xs text-slate-500 mb-3 line-clamp-2">{{ stop.address }}</p>
    
                        <div class="flex justify-between items-end text-xs text-slate-600 font-medium">
                            <div class="flex gap-3">
                                <span class="flex items-center"><i class="pi pi-arrow-down-right mr-1 text-slate-400"></i>{{ stop.arrivalTime }}</span>
                                <span class="flex items-center"><i class="pi pi-arrow-up-right mr-1 text-primary-500"></i>{{ stop.departureTime }}</span>
                            </div>
                            <span v-if="stop.distance" class="text-slate-400 italic text-[10px]">{{ stop.distance }}m away</span>
                        </div>
                    </div>
                </div>
    
                <div class="flex justify-between pt-2 px-1">
                    <Button icon="pi pi-pencil" rounded text severity="secondary" aria-label="Edit" @click="router.push('/Edit')" class="!w-10 !h-10" />
                    <Button icon="pi pi-save" rounded text severity="secondary" :disabled="!isLoggedIn" aria-label="Save" class="!w-10 !h-10" @click="saveItinerary"/>
                    <Button icon="pi pi-refresh" rounded text severity="secondary" aria-label="Regenerate" @click="regenerateItinerary" class="!w-10 !h-10" />
                </div>
            </div>
        </div>
    </template>