<script setup>
    //System
    import { ref, computed, onMounted } from 'vue';
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
    import SelectButton from 'primevue/selectbutton';
    import Button from 'primevue/button';
    
    //Form Store and Router
    const formStore = useFormStore();
    const router = useRouter()
    
    //My Variables
    const timeallocated = ref(null);
    const selectedTagIds = ref([]);
    const selectedTagTypes = ref([])
    const simpleTime = ref(0);
    
    // Error States
    const incomplete = ref(false);    
    const invalidGoogleLocation = ref(false);
    const noTime1 = ref(false);
    const noTime2 = ref(false);
    const timeTooShort = ref(false);
    const timeTooLong = ref(false);
    const shortTimeWarning = ref(false);
    const warningAcknowledged = ref(false); 
    const noInterests = ref(false);
    const limitedInterests = ref(false);
    const limitMessage = ref('');
    
    // --- NEW VARIABLES FOR LATE NIGHT WARNING ---
    const lateTimeWarning = ref(false);
    const lateTimeAcknowledged = ref(false);

    // --- NEW VARIABLES FOR LONG TIME SINGLE INTEREST WARNING ---
    const longTimeSingleInterestWarning = ref(false);
    const longTimeWarningAcknowledged = ref(false);
    
    //Autocomplete Import
    const { startingLocation, endingLocation, startingLocationPlaceName,
        endingLocationPlaceName, startPlaceData, endPlaceData, initAutocomplete } = useAutocomplete(); 
    
    
    ///// STEP 1: LOCATION VALIDATION /////
    const nextStep1 = (tabNumber, callbackFunction) => {
      incomplete.value = false;
      invalidGoogleLocation.value = false;
    
      if (!startingLocationPlaceName.value || !endingLocationPlaceName.value) {
        incomplete.value = true;
        setTimeout(() => incomplete.value = false, 5000);
        return;
      }
    
      if (!startPlaceData.value || !endPlaceData.value) {
        invalidGoogleLocation.value = true;
        setTimeout(() => invalidGoogleLocation.value = false, 5000);
        return;
      }
    
      callbackFunction(tabNumber);
    };
    
    ///// STEP 2: TIME VALIDATION /////
    const nextStep2 = (tabNumber, callbackFunction) => {
        noTime1.value = false;
        noTime2.value = false;
        timeTooShort.value = false;
        timeTooLong.value = false;
        shortTimeWarning.value = false;
    
        if (!timeallocated.value) {
            noTime1.value = true;
            setTimeout(() => noTime1.value = false, 5000);
            return;
        }
    
        const rawDateValue = timeallocated.value;
        const hours = rawDateValue.getHours();
        const minutes = rawDateValue.getMinutes();
        const totalMinutes = (hours * 60) + minutes;
        
        simpleTime.value = totalMinutes;
    
        if (totalMinutes === 0) {
            noTime2.value = true;
            setTimeout(() => noTime2.value = false, 5000);
            return;
        }
    
        if (totalMinutes < 30) {
            timeTooShort.value = true;
            setTimeout(() => timeTooShort.value = false, 5000);
            return;
        }
    
        if (totalMinutes > 360) {
            timeTooLong.value = true;
            setTimeout(() => timeTooLong.value = false, 5000);
            return;
        }
    
        if (totalMinutes <= 60) {
            if (warningAcknowledged.value) {
                callbackFunction(tabNumber);
            } else {
                shortTimeWarning.value = true;
                warningAcknowledged.value = true; 
                setTimeout(() => {
                    shortTimeWarning.value = false;
                }, 5000);
            }
            return;
        }
    
        callbackFunction(tabNumber);
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
        { id: 6, name: 'Attractions', icon:'attractions', type: 'tourist_attraction'},
    ]);
    
    const interestLimit = computed(() => {
        const minutes = simpleTime.value;
        
        if (minutes <= 60) return 1;
        
        if (minutes <= 150) return 2;
        
        if (minutes <= 270) return 3;
        
        return availableTags.value.length; 
    });

    const toggleTag = (tagId) => {
        const index = selectedTagIds.value.indexOf(tagId);
        
        if (index > -1) {
            selectedTagIds.value.splice(index, 1);
            selectedTagTypes.value.splice(index, 1);
            return;
        } 
        
        if (selectedTagIds.value.length >= interestLimit.value) {
            const limit = interestLimit.value;
            
            if (limit === 1) {
                limitMessage.value = "With 1 hour or less, you can only pick 1 interest.";
            } else if (limit === 2) {
                limitMessage.value = "With this short duration, you are limited to 2 interests.";
            } else if (limit === 3) {
                limitMessage.value = "For trips under 4.5 hours, you are limited to 3 interests.";
            }
            
            limitedInterests.value = true;
            setTimeout(() => limitedInterests.value = false, 4000);
            return; 
        }
    
        const tag = availableTags.value.find(t => t.id === tagId);
        selectedTagIds.value.push(tagId);
        selectedTagTypes.value.push(tag.type)
    };
    
    ////STYLER OF CHIPS////
    const getChipPT = (tagId) => {
        const isSelected = selectedTagIds.value.includes(tagId);
        let baseClasses = 'px-4 py-2 h-16 md:h-full text-sm font-medium rounded-full transition-all duration-200';
        if (isSelected) {
            baseClasses += 'shadow-md bg-primary-500 text-white border-1 border-transparent';
        } else {
            baseClasses += 'bg-slate-100 text-gray-700 hover:border-slate-300 hover:bg-primary-50 border-1 border-slate-300';
        }
    
        return {
            root: baseClasses, 
            label: 'select-none'
        };
    };
    
    const rankingPreference = ref('DISTANCE');
    const rankingLabels = ref(['DISTANCE', 'POPULARITY']);
    
    
    ////FORM AND DATA HANDLER////
    const submitHandler = () => {
        if (selectedTagIds.value.length === 0) {
            noInterests.value = true;
            setTimeout(() => noInterests.value = false, 5000);
            return;
        }

        // Check for long time with single interest warning
        if (!longTimeWarningAcknowledged.value && simpleTime.value >= 240 && selectedTagTypes.value.length === 1) {
            longTimeSingleInterestWarning.value = true;
            longTimeWarningAcknowledged.value = true; // Set flag so NEXT click goes through

            // Hide the message after 5 seconds, but keep the flag true
            setTimeout(() => longTimeSingleInterestWarning.value = false, 5000);
            return; // STOP submission here
        }

        if (!lateTimeAcknowledged.value) {
            const now = new Date();
            const currentHour = now.getHours();

            // 20 is 8PM, 5 is 5AM
            if (currentHour >= 20 || currentHour < 5) {
                lateTimeWarning.value = true;
                lateTimeAcknowledged.value = true; // Set flag so NEXT click goes through

                // Hide the message after 5 seconds, but keep the flag true
                setTimeout(() => lateTimeWarning.value = false, 5000);
                return; // STOP submission here
            }
        }
    
        // 3. SUBMIT
        formStore.updateFormData( {
            startingLocation: startPlaceData,
            endingLocation: endPlaceData,
            timeAllotted: simpleTime.value, 
            interests: selectedTagTypes.value,
            rankingPreference: rankingPreference.value
        });
        
        router.push('/Loading');
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
    
      <div class="h-full w-full p-4 md:p-20 md:pl-25 flex flex-col justify-center items-center overflow-hidden gradient-5">
        <Stepper value="1" linear class="md:w-[70%] h-full mt-15 md:mt-10 !z-1 animate-enter text-sm" style="--delay: 0s">
            <StepList class="text-xs max-w-90%">
                <Step value="1" >Location</Step>
                <Step value="2">Time</Step>
                <Step value="3">Interests</Step>
            </StepList>
            <StepPanels class="h-[80%] bg-transparent">
                
                <StepPanel v-slot="{ activateCallback }" value="1" class="flex flex-col h-full bg-transparent">
                    <div class="md:mb-0 w-full md:w-[60%]">
                        <h1 class="text-2xl md: 4xl font-bold font-[Poppins] text-center md:text-left animate-enter" style="--delay:0s">
                            Where are you starting and where do you want to end your journey?
                        </h1>
                    </div>
                    
                     <div class="md:h-15 h-20">
                        <Transition name="fade">
                            <div v-show="incomplete || invalidGoogleLocation" class="flex justify-center items-center pointer-events-none m-2">
                                <Message severity="error" v-show="incomplete">Please fill in both text fields.</Message>
                                <Message severity="error" v-show="invalidGoogleLocation">Please select a valid location from the dropdown suggestions.</Message>
                            </div>
                        </Transition>
                     </div>
    
                    <div class="flex flex-col justify-start md:justify-center items-center md:items-start md:flex-row gap-8 md:gap-8 flex-1 md:mt-10 w-full">
                        <FloatLabel>
                            <InputText id="startingLocation" class="w-full field-input animate-enter" style="--delay:0.1s" ref="startingLocation" v-model="startingLocationPlaceName"
                            :ref="(el) => startingLocation.value = el" />
                            <label for="startingLocation">Starting location</label>
                        </FloatLabel>
                        <FloatLabel>
                            <InputText id="endingLocation"  class="w-full field-input animate-enter" style="--delay:0.2s" ref="endingLocation" v-model="endingLocationPlaceName"
                            :ref="(el) => endingLocation.value = el" />
                            <label for="endingLocation">Ending location</label>
                        </FloatLabel>
                    </div>
                    <div class="flex pt-6 justify-end">
                        <Button label="Next" icon="pi pi-arrow-right" iconPos="right" class="w-45 interactive-btn-primary animate-enter" style="--delay:0.3s" rounded @click="nextStep1('2', activateCallback)" />
                    </div>
                </StepPanel>
    
                <StepPanel v-slot="{ activateCallback }" value="2" class="flex flex-col h-full bg-transparent animate-enter" style="--delay:0s">
                    <div class="md:mb-0 w-full md:w-[60%]">
                        <h1 class="text-2xl md: 4xl font-bold font-[Poppins] w-full text-center md:text-left">
                            How much time do you have available for your trip?
                        </h1>
                    </div>
                    <div class="md:h-15 h-20">
                        <Transition name="fade">
                            <div v-show="noTime1 || noTime2 || shortTimeWarning || timeTooShort || timeTooLong" class="flex justify-center items-center pointer-events-none m-2 flex-col">
                                <Message severity="error" v-show="noTime1">Please select a time.</Message>
                                <Message severity="error" v-show="noTime2">Zero minutes is not enough for a trip!</Message>
                                <Message severity="error" v-show="timeTooShort">Minimum time required is 30 minutes.</Message>
                                <Message severity="error" v-show="timeTooLong">Maximum time allowed is 6 hours.</Message>
                                <Message severity="warn" v-show="shortTimeWarning">Warning: 1 hour or less limits you to 1 Interest. Click Next again to confirm.</Message>
                            </div>
                        </Transition>
                     </div>
    
                    <div class="flex justify-center items-start md:flex-row gap-8 md:gap-4 flex-1 animate-enter" style="--delay:0.1s">
                        <DatePicker id="datepicker-timeonly" v-model="timeallocated" timeOnly fluid :maxDate="maxTimeLimit" :manualInput="false" :stepMinute="15" dateFormat="HH:mm"/>
                    </div>
                    <div class="flex pt-6 justify-between animate-enter p-4 gap-2" style="--delay:0.2s">
                        <Button label="Back" severity="secondary" icon="pi pi-arrow-left" class="w-40 interactive-btn-secondary" rounded @click="activateCallback('1')" />
                        <Button label="Next" icon="pi pi-arrow-right" iconPos="right" class="w-40 interactive-btn-primary" rounded @click="nextStep2('3', activateCallback)" />
                    </div>
                </StepPanel>
    
                <StepPanel v-slot="{ activateCallback }" value="3" class="flex flex-col h-full bg-transparent overflow-y-scroll">
                    <div class="md:mb-0 w-full md:w-[60%] mb-15">
                        <h1 class="text-2xl md: 4xl font-bold font-[Poppins] w-full text-center md:text-left animate-enter px-4" style="--delay:0s">
                            What are the places you would like to see?
                        </h1>
                    </div>
                    
                    <div class="md:h-15 h-20">
                        <Transition name="fade">
                            <div v-show="noInterests || limitedInterests || lateTimeWarning || longTimeSingleInterestWarning" class="flex justify-center items-center pointer-events-none m-2 flex-col">
                                <Message severity="error" v-show="noInterests">Select at least 1 interest.</Message>
                                <Message severity="warn" v-show="limitedInterests">{{ limitMessage }}</Message>
                                <Message severity="warn" v-show="lateTimeWarning">It is late (8PM-5AM). Limited establishments may be open. Click Generate again to proceed.</Message>
                                <Message severity="warn" class="text-center" v-show="longTimeSingleInterestWarning">With 4+ hours and only one interest, your itinerary may feel repetitive. Consider adding more interests. Click Generate again to proceed.</Message>
                            </div>
                        </Transition>
                     </div>
    
                    <div class="flex flex-col items-center justify-center gap-8 md:gap-4 flex-1">
                        <div class="grid grid-cols-2 md:grid-cols-3 gap-3 animate-enter" style="--delay:0.1s">
                            <Chip v-for="tag in availableTags" :key="tag.id" :label="tag.name" class="cursor-pointer" :pt="getChipPT(tag.id)" @click="toggleTag(tag.id)">
                                <template #icon>
                                    <i class="material-icons text-lg mr-2">{{ tag.icon }}</i> 
                                </template>
                            </Chip>
                        </div>
                        <!-- <div class="flex justify-center flex-col items-center px-4">
                            <SelectButton v-model="rankingPreference" fluid :options="rankingLabels" class="border border-slate-300 mt-4 animate-enter mb-2" style="--delay:0.2s"/>
                            <div v-if="rankingPreference === 'DISTANCE'" class="animate-enter text-slate-500 text-center" style="--delay:0.1s">Selects establishments that are close but not necessarily highest rated.</div>
                            <div v-else-if="rankingPreference === 'POPULARITY'" class="animate-enter text-slate-500  text-center" style="--delay:0.1s">Selects establishments that are highest rated but not necessarily close.</div>
                        </div> -->
    
                    </div>
                    <div class="flex pt-6 justify-between gap-2 p-4 animate-enter" style="--delay:0.3s">
                        <Button label="Back" severity="secondary" icon="pi pi-arrow-left" class="w-40 interactive-btn-secondary" rounded @click="activateCallback('2')" />
                        <Button label="Generate" class="w-40 interactive-btn-primary" rounded type="submit" @click="submitHandler"/>
                    </div>
                </StepPanel>
            </StepPanels>
        </Stepper>
        <div class="flex justify-end w-full">
            <Button icon="pi pi-question" class="interactive-btn-primary rounded-full! w-12 h-12"/>
        </div>
      </div>
    </template>
    
    <style scoped>
    .fade-enter-active,
    .fade-leave-active {
      transition: opacity 0.5s ease;
    }
    
    .fade-enter-from,
    .fade-leave-to {
      opacity: 0;
    }
    </style>