<script setup>
//System
import { ref,computed,onMounted } from 'vue';
import { useFormStore } from '@/store/formStore.js';
import { useRouter } from 'vue-router'
import { useAutocomplete } from '@/composables/autocomplete';


//PrimeVue
import FloatLabel from 'primevue/floatlabel';
import InputText from 'primevue/inputtext';
import Stepper from 'primevue/stepper';
import StepList from 'primevue/steplist';
import StepPanels from 'primevue/steppanels';
import Step from 'primevue/step';
import StepPanel from 'primevue/steppanel';
import Message from 'primevue/message';
import DatePicker from 'primevue/datepicker';
import Chip  from 'primevue/chip';
import Dialog from 'primevue/dialog';


//Form Store and Router
const formStore = useFormStore();
const router = useRouter()

//My Variables
const timeallocated = ref('')
const selectedTagIds = ref([]);
const selectedTagTypes = ref([])
const incomplete = ref(false);    
const noTime1 = ref(false);
const noTime2 = ref(false);
const shortTime = ref(false);
let warning = ref(false);
let simpleTime = '';
let noInterests = ref(false);
let limitedInterests = ref(false);

//Autocomplete Import
const { startingLocation, endingLocation, startingLocationPlaceName,
    endingLocationPlaceName, startPlaceData, endPlaceData, initAutocomplete } = useAutocomplete(); 



/////BUTTON FUNCTION FOR ADVANCING PAGE/////
const nextStep1 = (tabNumber, callbackFunction) => {
  if (startingLocationPlaceName.value && endingLocationPlaceName.value) {
    console.log(startingLocationPlaceName.value)
    callbackFunction(tabNumber)
  } else {
    incomplete.value = true;
    setTimeout(() => {
        incomplete.value = false;
    }, 5000)
  }
};

const nextStep2 = (tabNumber, callbackFunction) => {
    const rawDateValue = timeallocated.value;
    if (timeallocated.value) {
        const hours = rawDateValue.getHours();
        const minutes = rawDateValue.getMinutes();
        simpleTime = (hours * 60) + minutes;
    if (simpleTime != 0) {
        if (simpleTime > 60) {
            callbackFunction(tabNumber)
        } else {
            if (warning.value) {
                callbackFunction(tabNumber);

            } else  {
                shortTime.value = true;
                setTimeout(() => {
                shortTime.value = false;
                }, 5000)
                warning.value = true;
            }
        }
    } else {
        noTime2.value = true;
        setTimeout(() => {
            noTime2.value = false;
        }, 5000)
    }
  } else {
    noTime1.value = true;
    setTimeout(() => {
        noTime1.value = false;
    }, 5000)
  }
};

////MAX TIME LIMIT SETTING////
const maxTimeLimit = computed(() => {
    const today = new Date();
    const maxDate = new Date(today);
    maxDate.setHours(6);
    maxDate.setMinutes(0);
    maxDate.setSeconds(0);
    maxDate.setMilliseconds(0);
    return maxDate;
});

// Available Tags
const availableTags = ref([
    { id: 1, name: 'Restaurants', icon:'restaurant', type: 'restaurant'},
    { id: 2, name: 'Cafes', icon:'local_cafe', type: 'cafe'},
    { id: 3, name: 'Museums', icon:'museum', type: 'museum'},
    { id: 4, name: 'Churches', icon:'church', type: 'church'},
    { id: 5, name: 'Parks', icon:'park', type: 'park'},
    { id: 6, name: 'Cool Buildings', icon:'attractions', type: 'tourist_attraction'},
]);

////SE


const selectedTags = computed(() => {
    return availableTags.value.filter(tag => selectedTagIds.value.includes(tag.id));
});
const toggleTag = (tagId) => {
    const index = selectedTagIds.value.indexOf(tagId);
    if (index > -1) {
        selectedTagIds.value.splice(index, 1);
        selectedTagTypes.value.splice(index, 1);
    } else {
        const tag = availableTags.value.find(t => t.id === tagId);
        selectedTagIds.value.push(tagId);
        selectedTagTypes.value.push(tag.type)
    }
};

////STYLER OF CHIPS////
const getChipPT = (tagId) => {
    const isSelected = selectedTagIds.value.includes(tagId);
    let baseClasses = 'px-4 py-2 h-16 md:h-full text-sm font-medium rounded-full transition-all duration-200';
    if (isSelected) {
        baseClasses += 'shadow-md bg-primary-500 text-white ';
    } else {
        baseClasses += 'bg-slate-100 text-gray-700 hover:border-slate-300 hover:bg-primary-50';
    }

    return {
        root: baseClasses, 
        label: 'select-none'
    };
};


////FORM AND DATA HANDLER////
const submitHandler = () => {
    if (selectedTagIds.value.length) {
        if (simpleTime > 60) {
            formStore.updateFormData( {
                startingLocation: startPlaceData,
                endingLocation: endPlaceData,
                timeAllotted: simpleTime,
                interests: selectedTagTypes.value
            });
            router.push('/Loading');
            console.log('Starting Locations: ', formStore.currentFormState.startingLocation.name)
            console.log('Lat: ', formStore.currentFormState.startingLocation.lat)
            console.log('Address: ', formStore.currentFormState.startingLocation.address)
            console.log('PlaceID: ', formStore.currentFormState.startingLocation.place_id)
            console.log('Ending Location: ', formStore.currentFormState.endingLocation.name)
            console.log('Address: ', formStore.currentFormState.endingLocation.address)
            console.log('Place ID: ', formStore.currentFormState.endingLocation.place_id)
            console.log('Time: ', formStore.currentFormState.timeAllotted)
            console.log('Interests chosen: ', formStore.currentFormState.interests)
        } else if (selectedTagIds.value.length == 1 && simpleTime < 60) {
            formStore.updateFormData( {
                startingLocation: startPlaceData,
                endingLocation: endPlaceData,
                timeAllotted: simpleTime,
                interests: selectedTagTypes.value
            });
            router.push('/Loading');
            
        } else {
                limitedInterests.value = true;
                setTimeout(() => {
                limitedInterests.value = false;
                }, 5000)
            }

    } else {
        noInterests.value = true;
        setTimeout(() => {
        noInterests.value = false;
        }, 5000)
    }
}


onMounted(() => {
    if (typeof google !== 'undefined') {
        initAutocomplete();
    } else {
        console.error("Google Maps API script not loaded. Check your index.html.");
    }
});

</script>

<template>

  <div class="h-screen w-screen p-4 md:p-15 flex flex-col justify-center items-center">
    <Stepper value=1 linear class="md:w-[70%] h-full mt-25 md:mt-10 !z-1">
        <StepList>
            <Step value="1">Location</Step>
            <Step value="2">Time</Step>
            <Step value="3">Interests</Step>
        </StepList>
        <StepPanels class="h-[80%]">
            <StepPanel v-slot="{ activateCallback }" value="1" class="flex flex-col h-full ">
                <div class="md:mb-0 w-full md:w-[60%]">
                    <h1 class="text-2xl md: 4xl font-bold font-[Poppins] text-center md:text-left">
                        Where are you starting and where do you want to end your journey?
                    </h1>
                    
                </div>
                <!-- <Message v-if="incomplete" severity="error" class="mt-2">Complete all inputs to proceed</Message> -->
                 <div class="md:h-15 h-20">
                    <Transition name="fade">
                        <div v-show="incomplete" class="flex justify-center items-center pointer-events-none m-2">
                            <Message severity="error">Complete all inputs to proceed</Message>
                        </div>
                    </Transition>
                 </div>

                
                <div class="flex flex-col justify-start md:justify-center items-center md:items-start md:flex-row gap-8 md:gap-8 flex-1 md:mt-10 w-full">
                    <FloatLabel>
                        <InputText id="startingLocation" class="w-full" ref="startingLocation" v-model="startingLocationPlaceName"
                        :ref="(el) => startingLocation.value = el" />
                        <label for="startingLocation">Starting location</label>
                    </FloatLabel>
                    <FloatLabel>
                        <InputText id="endingLocation"  class="w-full" ref="endingLocation" v-model="endingLocationPlaceName"
                        :ref="(el) => endingLocation.value = el" />
                        <label for="endingLocation">Ending location</label>
                    </FloatLabel>
                    
                </div>
                <div class="flex pt-6 justify-end">
                    <Button label="Next" icon="pi pi-arrow-right" iconPos="right" class="w-45" rounded @click="nextStep1('2', activateCallback)" />
                </div>
            </StepPanel>

            <StepPanel v-slot="{ activateCallback }" value="2" class="flex flex-col h-full">
                <div class="md:mb-0 w-full md:w-[60%]">
                    <h1 class="text-2xl md: 4xl font-bold font-[Poppins] w-full text-center md:text-left">
                        How much time do you have available for your trip?
                    </h1>
                </div>
                <div class="md:h-15 h-20">
                    <Transition name="fade">
                        <div v-show="noTime1 || noTime2 || shortTime" class="flex justify-center items-center pointer-events-none m-2">
                            <Message severity="error" v-show="noTime1">Complete all inputs to proceed</Message>
                            <Message severity="error" v-show="noTime2">Are you really going with no time at all? XD</Message>
                            <Message severity="warn" v-show="shortTime">Setting your time less than an hour greatly reduces the effectiveness of your itinerary. Are you sure you want to proceed?</Message>
                        </div>
                    </Transition>
                 </div>

                <div class="flex justify-center items-start md:flex-row gap-8 md:gap-4 flex-1">
                    <DatePicker id="datepicker-timeonly" v-model="timeallocated" timeOnly fluid :maxDate="maxTimeLimit" :manualInput="false" :stepMinute="15" dateFormat="HH:mm"/>

                </div>
                <div class="flex pt-6 justify-between">
                    <Button label="Back" severity="secondary" icon="pi pi-arrow-left" class="w-45" rounded @click="activateCallback('1')" />
                    <Button label="Next" icon="pi pi-arrow-right" iconPos="right" class="w-45" rounded @click="nextStep2('3', activateCallback)" />
                </div>

            </StepPanel>
            <StepPanel v-slot="{ activateCallback }" value="3" class="flex flex-col h-full">
                <div class="md:mb-0 w-full md:w-[60%] mb-15">
                    <h1 class="text-2xl md: 4xl font-bold font-[Poppins] w-full text-center md:text-left">
                        What are the stuff you would like to see?
                    </h1>
                </div>
                <div class="md:h-15 h-20">
                    <Transition name="fade">
                        <div v-show="noInterests || limitedInterests" class="flex justify-center items-center pointer-events-none m-2">
                            <Message severity="error" v-show="noInterests">Select at least 1 interest</Message>
                            <Message severity="error" v-show="limitedInterests">Because of your short time, you are unfortunately limited to 1 interest</Message>
                        </div>
                    </Transition>
                 </div>
                <div class="flex justify-center items-start md:flex-row gap-8 md:gap-4 flex-1">
                    <div>
                        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                            <Chip v-for="tag in availableTags" :key="tag.id" :label="tag.name" class="cursor-pointer" :pt="getChipPT(tag.id)" @click="toggleTag(tag.id)">
                                <template #icon>
                                    <i class="material-icons text-lg mr-2">{{ tag.icon }}</i> 
                                </template>
                            </Chip>
                        </div>
                    </div>

                </div>
                <div class="flex pt-6 justify-between">
                    <Button label="Back" severity="secondary" icon="pi pi-arrow-left" class="w-45" rounded @click="activateCallback('2')" />
                    <Button label="Generate" class="w-45" rounded type="submit" @click="submitHandler"/>
                </div>
            </StepPanel>
        </StepPanels>
    </Stepper>
  </div>
</template>
