<script setup>
import { onMounted, onUnmounted, ref } from "vue";

import { useFormStore } from '@/store/formStore';
const formStore = useFormStore();

import { useRouter } from 'vue-router';
const router = useRouter();

const stepCards = ref(null);
const howItWorks = ref(null);
const heroSection = ref(null);
const heroTitle = ref(null);
const heroSubtitle = ref(null);
const heroButton = ref(null);
const heroOverlay = ref(null);
const howItWorksTitle = ref(null);
const historySection = ref(null);
const historyTitle = ref(null);
const historyText = ref(null);
const historyImage = ref(null);
const mapPath = ref(null);
const mapMarkers = ref(null);
const mapElements = ref(null);
const maximizeSection = ref(null);
const maximizeTitle = ref(null);
const maximizeText = ref(null);
const maximizeImage = ref(null);
const communitySection = ref(null);
const communityTitle = ref(null);
const communityText = ref(null);
const communityImage = ref(null);
const communityCardsBg = ref(null);
const communityMainCard = ref(null);
const displayedTitle = ref("");
const fullTitleText = "Plan Your Intramuros Trip in a Minute";
const hourHandRotation = ref(0);
const minuteHandRotation = ref(0);
const secondHandRotation = ref(0);
const currentTimeString = ref("");

let clockInterval;
let observer;

const createAndRefresh = () => {
    formStore.resetState()
    router.push('/Create'); 
};

onMounted(() => {
  // Typewriter effect for hero title
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

  // Clock update
  const updateClock = () => {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const seconds = now.getSeconds();

    const secondAngle = seconds * 6; 
    const minuteAngle = minutes * 6 + seconds * 0.1; 
    const hourAngle = (hours % 12) * 30 + minutes * 0.5; 

    secondHandRotation.value = secondAngle;
    minuteHandRotation.value = minuteAngle;
    hourHandRotation.value = hourAngle;

    let hours12 = hours % 12;
    hours12 = hours12 ? hours12 : 12; 
    const ampm = hours >= 12 ? 'PM' : 'AM';
    currentTimeString.value = `${hours12}:${minutes.toString().padStart(2, '0')} ${ampm}`;
  };

  updateClock();
  clockInterval = setInterval(updateClock, 1000);

  // Use Intersection Observer for scroll animations
  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  // Observe all animatable elements
  document.querySelectorAll('.animate-on-scroll').forEach(el => {
    observer.observe(el);
  });
});

onUnmounted(() => {
  if (clockInterval) clearInterval(clockInterval);
  if (observer) observer.disconnect();
});
</script>

<template>
  <div class="home-root min-h-[300dvh] w-full flex flex-col overflow-x-hidden">

    <div
      ref="heroSection"
      class="relative min-h-screen w-full flex flex-col justify-center items-center md:items-end px-5 md:pl-15 bg-[url('@/assets/imgs/DSC_0355.jpg')] bg-cover bg-center md:bg-fixed"
    >
      <div ref="heroOverlay" class="absolute inset-0 bg-gradient-to-b from-black/35 via-black/10 to-transparent md:bg-gradient-to-l md:from-black/50 md:via-black/30 md:to-transparent pointer-events-none"></div>
      <div class="relative z-10 flex flex-col justify-center items-center md:items-end text-right gap-6 max-w-2xl md:max-w-xl mr-0 md:mr-16 mb-16 md:mb-24">
        
        <h1
          ref="heroTitle"
          class="min-h-[120px] md:min-h-[180px] text-center md:text-right text-4xl md:text-6xl leading-tight font-extrabold text-white drop-shadow-[0_5px_5px_rgba(0,0,0,1)]"
        >
          {{ displayedTitle }}<span class="blinking-cursor text-[#835AF8]">|</span>
        </h1>

        <p
          ref="heroSubtitle"
          class="hero-fade-in delay-1 text-center md:text-right text-lg md:text-xl font-bold tracking-tight px-0 md:px-0 leading-relaxed text-white drop-shadow-[0_4px_4px_rgba(0,0,0,1)]"
        >
          Generate Intramuros itineraries in seconds.<br /><br />Skip the research and get straight<br />to exploring Manila's Walled City!
        </p>

        <Button
          ref="heroButton"
          label="Try Itinero Now!"
          rounded
          raised
          class="hero-fade-in delay-2 w-55 interactive-btn-primary font-extrabold"
          @click="createAndRefresh"
        ></Button>
      </div>
    </div>
    
    <div class="min-h-screen w-full flex flex-col justify-center items-center bg-gradient-to-b from-primary-50/30 to-white" ref="howItWorks">
        <div ref="howItWorksTitle" class="animate-on-scroll section-title text-4xl font-bold mb-12 tracking-tight">
          <span class="gradient-text-animated">How It Works</span>
        </div>
        <div class="flex md:flex-row flex-col gap-6 w-full justify-center flex-wrap p-5" ref="stepCards">
          <div class="animate-on-scroll delay-1 step-card w-full md:h-auto md:w-80 bg-white shadow-xl shadow-[#835AF8]/20 hover:shadow-[#835AF8]/35 rounded-3xl flex flex-col items-center justify-start p-8 border border-[#E5DCFF] transition-all duration-300 ease-out">
            <div class="icon-badge mb-6 w-20 h-20 rounded-2xl bg-gradient-to-br from-[#a855f7] to-[#d946ef] flex items-center justify-center shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="w-full flex flex-col items-center">
              <span class="step-card-title gradient-text-primary font-bold text-xl md:text-2xl mb-2">Tell Us Your Time</span>
              <div class="progress-bar-container w-16 h-1 bg-gray-200 rounded-full mb-4 overflow-hidden">
                <div class="progress-bar h-full bg-gradient-to-r from-[#a855f7] to-[#d946ef] rounded-full"></div>
              </div>
              <span class="section-text text-sm md:text-base text-center leading-relaxed">Pick how much time you have to explore Intramuros.</span>
            </div>
          </div>
          <div class="animate-on-scroll delay-2 step-card w-full md:h-auto md:w-80 bg-white shadow-xl shadow-[#835AF8]/20 hover:shadow-[#835AF8]/35 rounded-3xl flex flex-col items-center justify-start p-8 border border-[#E5DCFF] transition-all duration-300 ease-out">
            <div class="icon-badge mb-6 w-20 h-20 rounded-2xl bg-gradient-to-br from-[#6366f1] to-[#a855f7] flex items-center justify-center shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
            </div>
            <div class="w-full flex flex-col items-center">
              <span class="step-card-title gradient-text-secondary font-bold text-xl md:text-2xl mb-2">Choose the Vibes</span>
              <div class="progress-bar-container w-16 h-1 bg-gray-200 rounded-full mb-4 overflow-hidden">
                <div class="progress-bar h-full bg-gradient-to-r from-[#6366f1] to-[#a855f7] rounded-full"></div>
              </div>
              <span class="section-text text-sm md:text-base text-center leading-relaxed">Mix and match categories like Museums, Cafés, Parks, and more.</span>
            </div>
          </div>
          <div class="animate-on-scroll delay-3 step-card w-full md:h-auto md:w-80 bg-white shadow-xl shadow-[#835AF8]/20 hover:shadow-[#835AF8]/35 rounded-3xl flex flex-col items-center justify-start p-8 border border-[#E5DCFF] transition-all duration-300 ease-out">
            <div class="icon-badge mb-6 w-20 h-20 rounded-2xl bg-gradient-to-br from-[#ec4899] to-[#c026d3] flex items-center justify-center shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
              </svg>
            </div>
            <div class="w-full flex flex-col items-center">
              <span class="step-card-title gradient-text-accent font-bold text-xl md:text-2xl mb-2">Get Your Smart Route</span>
              <div class="progress-bar-container w-16 h-1 bg-gray-200 rounded-full mb-4 overflow-hidden">
                <div class="progress-bar h-full bg-gradient-to-r from-[#ec4899] to-[#c026d3] rounded-full"></div>
              </div>
              <span class="section-text text-sm md:text-base text-center leading-relaxed">See a ready-to-go map, optimized sequence, and tips to keep you on pace.</span>
            </div>
          </div>
        </div>
    </div>

    <div class="w-full">
      <div
        ref="historySection"
        class="min-h-[100dvh] md:h-[70dvh] w-full p-10 md:p-25 flex flex-col md:grid grid-cols-2 grid-rows-3 gap-5 bg-gradient-to-br from-white via-primary-50/45 to-white"
      >
          <div
            ref="historyTitle"
            class="animate-on-scroll section-title text-4xl font-bold md:col-span-1 md:self-end md:text-left text-center"
          >
            <span class="gradient-text-primary">See the History</span> <span class="gradient-text-secondary">You Care About.</span>
          </div>
          <div
            ref="historyText"
            class="animate-on-scroll delay-1 section-text md:row-start-2 md:col-start-1 text-justify text-base md:text-lg leading-relaxed pl-0 pr-6 py-6 rounded-2xl"
          >
            Why use a global map app when you can use one tailored for the unique cobblestone streets of Intramuros? Itinero focuses exclusively on the Walled City, giving you the most accurate and relevant routes. Better yet, you control the sightseeing agenda. Choose from 6 distinct place categories—like Churches, Museums, Cafes, Restaurants, or Parks—to ensure your itinerary is packed only with the historical, cultural, or architectural spots that interest you.
          </div>
          <div
            ref="historyImage"
            class="animate-on-scroll animate-scale delay-2 md:col-start-2 md:row-span-3 md:h-full w-full bg-white rounded-3xl shadow-[0_20px_50px_rgba(130,90,248,0.15)] border border-white/80 p-4 md:p-6 flex flex-col items-center justify-center overflow-hidden"
          >
            <div class="w-full h-full flex flex-col items-center justify-center relative">
              <svg
                viewBox="0 0 600 500"
                class="w-full h-full"
                preserveAspectRatio="xMidYMid meet"
              >
                <rect width="600" height="500" fill="#F3E8FF" />
                
                <g ref="mapElements">
                  <path d="M 0 0 L 600 0 L 600 120 L 450 120 L 400 80 L 350 100 L 300 60 L 250 90 L 200 50 L 150 80 L 100 40 L 50 70 L 0 50 Z" fill="#B3E5FC" opacity="0.6" />
                  <ellipse cx="150" cy="200" rx="40" ry="30" fill="#B3E5FC" opacity="0.5" />
                  <ellipse cx="450" cy="250" rx="35" ry="25" fill="#B3E5FC" opacity="0.5" />
                  <ellipse cx="300" cy="400" rx="30" ry="20" fill="#B3E5FC" opacity="0.5" />
                  
                  <path d="M 80 150 Q 100 130 120 150 Q 140 170 120 190 Q 100 210 80 190 Q 60 170 80 150 Z" fill="#C8E6C9" opacity="0.7" />
                  <path d="M 200 300 Q 230 280 260 300 Q 290 320 260 340 Q 230 360 200 340 Q 170 320 200 300 Z" fill="#C8E6C9" opacity="0.7" />
                  <path d="M 450 350 Q 480 330 510 350 Q 540 370 510 390 Q 480 410 450 390 Q 420 370 450 350 Z" fill="#C8E6C9" opacity="0.7" />
                  
                  <path d="M 250 200 L 500 200 L 500 400 L 250 400 Z" fill="#FFF9C4" opacity="0.4" />
                  
                  <line x1="50" y1="0" x2="50" y2="500" stroke="#9E9E9E" stroke-width="8" />
                  <line x1="550" y1="0" x2="550" y2="500" stroke="#9E9E9E" stroke-width="8" />
                  
                  <circle cx="50" cy="400" r="25" fill="#F5F5F0" stroke="#9E9E9E" stroke-width="8" />
                  
                  <line x1="0" y1="100" x2="600" y2="100" stroke="#BDBDBD" stroke-width="2" />
                  <line x1="0" y1="150" x2="600" y2="150" stroke="#BDBDBD" stroke-width="2" />
                  <line x1="0" y1="200" x2="600" y2="200" stroke="#BDBDBD" stroke-width="2" />
                  <line x1="0" y1="250" x2="600" y2="250" stroke="#BDBDBD" stroke-width="2" />
                  <line x1="0" y1="300" x2="600" y2="300" stroke="#BDBDBD" stroke-width="2" />
                  <line x1="0" y1="350" x2="600" y2="350" stroke="#BDBDBD" stroke-width="2" />
                  <line x1="0" y1="400" x2="600" y2="400" stroke="#BDBDBD" stroke-width="2" />
                  <line x1="0" y1="450" x2="600" y2="450" stroke="#BDBDBD" stroke-width="2" />
                  
                  <line x1="100" y1="0" x2="100" y2="500" stroke="#BDBDBD" stroke-width="2" />
                  <line x1="200" y1="0" x2="200" y2="500" stroke="#BDBDBD" stroke-width="2" />
                  <line x1="300" y1="0" x2="300" y2="500" stroke="#BDBDBD" stroke-width="2" />
                  <line x1="400" y1="0" x2="400" y2="500" stroke="#BDBDBD" stroke-width="2" />
                  <line x1="500" y1="0" x2="500" y2="500" stroke="#BDBDBD" stroke-width="2" />
                  
                  <text x="120" y="95" font-size="10" fill="#757575" font-family="Arial, sans-serif" font-weight="500">Magallanes Dr</text>
                  <text x="220" y="145" font-size="10" fill="#757575" font-family="Arial, sans-serif" font-weight="500">14th St</text>
                  <text x="220" y="195" font-size="10" fill="#757575" font-family="Arial, sans-serif" font-weight="500">11th St</text>
                  <text x="220" y="245" font-size="10" fill="#757575" font-family="Arial, sans-serif" font-weight="500">Atlanta</text>
                  <text x="220" y="295" font-size="10" fill="#757575" font-family="Arial, sans-serif" font-weight="500">16th St</text>
                  <text x="320" y="345" font-size="10" fill="#757575" font-family="Arial, sans-serif" font-weight="500">Muralla St</text>
                  <text x="420" y="345" font-size="10" fill="#757575" font-family="Arial, sans-serif" font-weight="500">Legaspi St</text>
                  <text x="320" y="395" font-size="10" fill="#757575" font-family="Arial, sans-serif" font-weight="500">Solana St</text>
                  <text x="420" y="395" font-size="10" fill="#757575" font-family="Arial, sans-serif" font-weight="500">Sta. Lucia St</text>
                  <text x="320" y="445" font-size="10" fill="#757575" font-family="Arial, sans-serif" font-weight="500">Victoria</text>
                  
                  <rect x="35" y="220" width="30" height="18" fill="#835AF8" rx="3" />
                  <text x="40" y="232" font-size="11" fill="white" font-family="Arial, sans-serif" font-weight="bold">120</text>
                  
                  <rect x="535" y="180" width="30" height="18" fill="#835AF8" rx="3" />
                  <text x="540" y="192" font-size="11" fill="white" font-family="Arial, sans-serif" font-weight="bold">R-9</text>
                  
                  <rect x="535" y="280" width="30" height="18" fill="#835AF8" rx="3" />
                  <text x="540" y="292" font-size="11" fill="white" font-family="Arial, sans-serif" font-weight="bold">R-8</text>
                  
                  <rect x="535" y="380" width="30" height="18" fill="#835AF8" rx="3" />
                  <text x="540" y="392" font-size="11" fill="white" font-family="Arial, sans-serif" font-weight="bold">170</text>
                </g>
                
                <path
                  ref="mapPath"
                  class="route-path animate-on-scroll"
                  d="M 80 50 L 120 80 L 160 110 L 200 140 L 240 170 L 260 200 L 280 230 L 300 260 L 320 290 L 340 320 L 360 350 L 380 380 L 400 400 L 420 410 L 440 420 L 460 430"
                  fill="none"
                  stroke="#835AF8"
                  stroke-width="8"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                
                <g ref="mapMarkers" class="route-markers">
                  <g transform="translate(80, 50)">
                    <path d="M 0 -12 L -8 8 L 0 4 L 8 8 Z" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="6" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="3" fill="white" />
                  </g>
                  
                  <g transform="translate(160, 110)">
                    <path d="M 0 -12 L -8 8 L 0 4 L 8 8 Z" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="6" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="3" fill="white" />
                  </g>
                  
                  <g transform="translate(240, 170)">
                    <path d="M 0 -12 L -8 8 L 0 4 L 8 8 Z" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="6" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="3" fill="white" />
                  </g>
                  
                  <g transform="translate(280, 230)">
                    <path d="M 0 -12 L -8 8 L 0 4 L 8 8 Z" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="6" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="3" fill="white" />
                  </g>
                  
                  <g transform="translate(320, 290)">
                    <path d="M 0 -12 L -8 8 L 0 4 L 8 8 Z" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="6" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="3" fill="white" />
                  </g>
                  
                  <g transform="translate(360, 350)">
                    <path d="M 0 -12 L -8 8 L 0 4 L 8 8 Z" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="6" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="3" fill="white" />
                  </g>
                  
                  <g transform="translate(460, 430)">
                    <path d="M 0 -12 L -8 8 L 0 4 L 8 8 Z" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="6" fill="#835AF8" />
                    <circle cx="0" cy="-8" r="3" fill="white" />
                  </g>
                </g>
                
                <g class="category-markers">
                  <g transform="translate(120, 120)">
                    <circle cx="0" cy="0" r="25" fill="#FFB3D9" />
                    <rect x="-8" y="2" width="16" height="10" fill="white" />
                    <path d="M -6 2 L 0 -8 L 6 2 Z" fill="white" />
                    <line x1="0" y1="-8" x2="0" y2="-12" stroke="white" stroke-width="1.5" stroke-linecap="round" />
                    <line x1="-2" y1="-10" x2="2" y2="-10" stroke="white" stroke-width="1.5" stroke-linecap="round" />
                    <rect x="-2" y="8" width="4" height="4" fill="white" />
                  </g>
                  
                  <g transform="translate(480, 100)">
                    <circle cx="0" cy="0" r="25" fill="#FFE066" />
                    <rect x="-10" y="2" width="20" height="12" fill="white" />
                    <rect x="-8" y="0" width="2.5" height="14" fill="white" />
                    <rect x="-2.5" y="0" width="2.5" height="14" fill="white" />
                    <rect x="3" y="0" width="2.5" height="14" fill="white" />
                    <rect x="8" y="0" width="2.5" height="14" fill="white" />
                    <path d="M -10 0 L 0 -6 L 10 0 Z" fill="white" />
                  </g>
                  
                  <g transform="translate(100, 280)">
                    <circle cx="0" cy="0" r="25" fill="#90EE90" />
                    <path d="M -6 2 Q -6 0 -4 0 L 4 0 Q 6 0 6 2 L 6 8 Q 6 10 4 10 L -4 10 Q -6 10 -6 8 Z" fill="white" />
                    <path d="M 6 4 Q 8 4 8 6 Q 8 8 6 8" fill="none" stroke="white" stroke-width="1.5" stroke-linecap="round" />
                    <ellipse cx="0" cy="0" rx="4" ry="3" fill="white" />
                    <line x1="0" y1="0" x2="0" y2="6" stroke="white" stroke-width="1.5" />
                  </g>
                  
                  <g transform="translate(350, 300)">
                    <circle cx="0" cy="0" r="25" fill="#5FD3D3" />
                    <rect x="-1.5" y="4" width="3" height="8" fill="white" />
                    <ellipse cx="-5" cy="0" rx="4" ry="5" fill="white" />
                    <ellipse cx="5" cy="0" rx="4" ry="5" fill="white" />
                    <ellipse cx="0" cy="-3" rx="5" ry="6" fill="white" />
                    <ellipse cx="0" cy="2" rx="6" ry="5" fill="white" />
                  </g>
                  
                  <g transform="translate(500, 380)">
                    <circle cx="0" cy="0" r="25" fill="#FFB366" />
                    <ellipse cx="0" cy="1" rx="10" ry="5" fill="white" />
                    <ellipse cx="0" cy="1" rx="8" ry="4" fill="none" stroke="white" stroke-width="1" />
                    <g transform="translate(-5, -6)">
                      <line x1="0" y1="0" x2="0" y2="10" stroke="white" stroke-width="1.5" stroke-linecap="round" />
                      <line x1="-0.5" y1="0" x2="0.5" y2="0" stroke="white" stroke-width="1.5" stroke-linecap="round" />
                      <line x1="-0.5" y1="1.5" x2="0.5" y2="1.5" stroke="white" stroke-width="1" stroke-linecap="round" />
                      <line x1="-0.5" y1="3" x2="0.5" y2="3" stroke="white" stroke-width="1" stroke-linecap="round" />
                    </g>
                    <g transform="translate(5, -6)">
                      <line x1="0" y1="0" x2="0" y2="10" stroke="white" stroke-width="1.5" stroke-linecap="round" />
                      <path d="M 0 0 L 1.5 1.5 L 0 3 Z" fill="white" />
                    </g>
                  </g>
                </g>
                
                <g transform="translate(300, 460)">
                  <g transform="translate(-100, 0)">
                    <circle cx="0" cy="0" r="4" fill="#FFB3D9" />
                    <text x="8" y="4" font-size="9" fill="#757575" font-family="Inter, sans-serif" font-weight="500">Churches</text>
                  </g>
                  <g transform="translate(0, 0)">
                    <circle cx="0" cy="0" r="4" fill="#FFE066" />
                    <text x="8" y="4" font-size="9" fill="#757575" font-family="Inter, sans-serif" font-weight="500">Museums</text>
                  </g>
                  <g transform="translate(80, 0)">
                    <circle cx="0" cy="0" r="4" fill="#90EE90" />
                    <text x="8" y="4" font-size="9" fill="#757575" font-family="Inter, sans-serif" font-weight="500">Cafes</text>
                  </g>
                  <g transform="translate(140, 0)">
                    <circle cx="0" cy="0" r="4" fill="#FFB366" />
                    <text x="8" y="4" font-size="9" fill="#757575" font-family="Inter, sans-serif" font-weight="500">Restaurants</text>
                  </g>
                  <g transform="translate(240, 0)">
                    <circle cx="0" cy="0" r="4" fill="#5FD3D3" />
                    <text x="8" y="4" font-size="9" fill="#757575" font-family="Inter, sans-serif" font-weight="500">Parks</text>
                  </g>
                </g>
              </svg>
            </div>
          </div>
      </div>
  
      <div
        ref="maximizeSection"
        class="min-h-[100dvh] md:h-[70dvh] w-full p-10 md:p-25 flex flex-col md:grid grid-cols-2 grid-rows-3 gap-5 bg-gradient-to-bl from-[#F8F6FF] via-white to-[#F2EEFF]"
      >
          <div
            ref="maximizeTitle"
            class="animate-on-scroll section-title text-4xl font-bold md:col-start-2 md:col-span-1 md:self-end text-center md:text-right"
          >
            <span class="gradient-text-secondary">Maximize</span> <span class="gradient-text-primary">Every Minute.</span>
          </div>
          <div
            ref="maximizeText"
            class="animate-on-scroll delay-1 section-text md:row-start-2 md:col-start-2 text-justify text-base md:text-lg leading-relaxed pl-6 md:pl-10 pr-0 py-6 rounded-2xl"
          >
            Whether you have a quick two-hour window or a full day to explore, our Time Constraint Filter is your best friend. Input your total available time, and Itinero intelligently crafts a viable route that fits your schedule without rushing you. See the results instantly visualized: a dynamic map view with polylines connecting your destinations, paired with a detailed, sequential schedule that makes navigation simple and stress-free.
          </div>
          
          <div
            ref="maximizeImage"
            class="animate-on-scroll animate-scale delay-2 md:col-start-1 md:row-start-1 md:row-span-3 h-[420px] md:h-full w-full rounded-3xl shadow-[0_20px_50px_rgba(130,90,248,0.25)] border border-white/50 p-0 overflow-hidden group relative"
          >
            <div class="absolute inset-0 bg-gradient-to-br from-[#6366f1] via-[#8b5cf6] to-[#d946ef]"></div>
            
            <svg
              viewBox="0 0 400 400"
              class="w-full h-full clock-container relative z-10"
            >
              <g opacity="0.3" stroke="white" fill="none">
                 <g transform="translate(30, 360) scale(0.8)">
                   <circle r="20" stroke-width="1.5" stroke-dasharray="4,2"/>
                   <path d="M0 -25 L5 -5 L25 0 L5 5 L0 25 L-5 5 L-25 0 L-5 -5 Z" fill="white" fill-opacity="0.4" stroke="none"/>
                 </g>
                 <path d="M 30 340 Q 110 250 20 150 T 40 50" stroke-width="2" stroke-linecap="round" stroke-dasharray="6,8" />
                 
                 <path d="M 40 300 Q 80 200 10 100" stroke-width="1" stroke-opacity="0.5" stroke-dasharray="4,6" />

                 <g fill="white" stroke="none" opacity="0.8">
                   <circle cx="85" cy="265" r="2" /> <circle cx="45" cy="180" r="2" /> <circle cx="25" cy="110" r="2" />
                   <circle cx="60" cy="220" r="1.5" opacity="0.6" /> <circle cx="20" cy="280" r="1.5" opacity="0.6" />
                   <circle cx="90" cy="180" r="1.5" opacity="0.6" /> <circle cx="15" cy="120" r="1.5" opacity="0.6" />
                   <path d="M 70 280 L 74 280 M 72 278 L 72 282" stroke="white" stroke-width="1" />
                   <path d="M 30 200 L 34 200 M 32 198 L 32 202" stroke="white" stroke-width="1" />
                   <path d="M 100 240 L 104 240 M 102 238 L 102 242" stroke="white" stroke-width="1" opacity="0.5"/>
                 </g>

                 <g transform="translate(40, 50) scale(0.7)" fill="white" fill-opacity="0.6" stroke="none">
                    <path d="M 0 -15 C -10 -15 -15 -8 -15 0 C -15 10 0 25 0 25 C 0 25 15 10 15 0 C 15 -8 10 -15 0 -15 Z" />
                    <circle cy="0" r="5" fill="#8b5cf6"/>
                 </g>
              </g>

              <g opacity="0.3" stroke="white" fill="none">
                  <path d="M 370 60 C 300 150, 420 260, 360 360" stroke-width="2" stroke-linecap="round" stroke-dasharray="5,5" />
                  
                  <path d="M 350 100 Q 390 200 340 300" stroke-width="1" stroke-opacity="0.5" stroke-dasharray="4,6" />

                  <g fill="white" stroke="none" opacity="0.8">
                     <circle cx="340" cy="150" r="1.5" opacity="0.6" /> <circle cx="380" cy="250" r="1.5" opacity="0.6" />
                     <circle cx="330" cy="280" r="1.5" opacity="0.6" />
                     <path d="M 330 120 L 334 120 M 332 118 L 332 122" stroke="white" stroke-width="1" />
                     <path d="M 385 180 L 389 180 M 387 178 L 387 182" stroke="white" stroke-width="1" />
                     <path d="M 345 320 L 349 320 M 347 318 L 347 322" stroke="white" stroke-width="1" />
                     <path d="M 310 160 L 314 160 M 312 158 L 312 162" stroke="white" stroke-width="1" opacity="0.5"/>
                  </g>
                  
                  <g transform="translate(370, 60) scale(0.8)">
                     <circle r="22" stroke="white" stroke-width="1" opacity="0.3" fill="none"/> <circle r="15" fill="white" fill-opacity="0.2" stroke="none"/>
                     <rect x="-10" y="-8" width="20" height="16" rx="2" stroke-width="1.5"/>
                     <circle r="5" stroke-width="1.5"/>
                     <rect x="-5" y="-11" width="6" height="3" rx="1" fill="white"/>
                     <path d="M -20 -10 L -16 -10 M -18 -12 L -18 -8" stroke-width="1" transform="translate(0,0)"/>
                     <path d="M 20 15 L 24 15 M 22 13 L 22 17" stroke-width="1"/>
                  </g>

                  <g transform="translate(350, 210) scale(0.8)">
                    <circle r="20" stroke="white" stroke-width="1" opacity="0.3" fill="none"/> <circle r="15" fill="white" fill-opacity="0.2" stroke="none"/>
                    <path d="M -8 8 L -6 -4 L 8 -4 L 10 8 Z" stroke-width="1.5" stroke-linejoin="round"/>
                    <path d="M 10 0 Q 14 0 14 4 Q 14 8 10 8" stroke-width="1.5" fill="none"/>
                    <path d="M -4 -8 Q -2 -12 0 -8 T 4 -8" stroke-width="1" opacity="0.8"/>
                    <path d="M -22 0 L -18 0 M -20 -2 L -20 2" stroke-width="1"/>
                  </g>

                  <g transform="translate(360, 360) scale(0.8)">
                     <circle r="22" stroke="white" stroke-width="1" opacity="0.3" fill="none"/> <circle r="15" fill="white" fill-opacity="0.2" stroke="none"/>
                     <path d="M -10 10 L 0 -10 L 10 10 Z" stroke-width="1.5" stroke-linejoin="round" fill="white" fill-opacity="0.3"/>
                     <path d="M -5 10 L 0 0 L 5 10 Z" stroke-width="1.5" stroke-linejoin="round" fill="white" fill-opacity="0.5" transform="translate(0, 2)"/>
                     <path d="M -20 -20 L -16 -20 M -18 -22 L -18 -18" stroke-width="1"/>
                     <path d="M 15 -5 L 19 -5 M 17 -7 L 17 -3" stroke-width="1"/>
                  </g>
              </g>


              <g transform="translate(0, -30)">
                <circle cx="200" cy="150" r="90" fill="white" fill-opacity="0.1" stroke="white" stroke-width="3" />
                <g stroke="white" stroke-width="2" stroke-linecap="round" stroke-opacity="0.6">
                  <line x1="200" y1="60" x2="200" y2="70" />
                  <line x1="200" y1="240" x2="200" y2="230" />
                  <line x1="290" y1="150" x2="280" y2="150" />
                  <line x1="110" y1="150" x2="120" y2="150" />
                </g>
                <line x1="200" y1="150" x2="200" y2="100" stroke="white" stroke-width="6" stroke-linecap="round" class="clock-hand" :style="{ transform: 'rotate(' + hourHandRotation + 'deg)', transformOrigin: '200px 150px' }" />
                <line x1="200" y1="150" x2="200" y2="75" stroke="white" stroke-width="4" stroke-linecap="round" class="clock-hand" :style="{ transform: 'rotate(' + minuteHandRotation + 'deg)', transformOrigin: '200px 150px' }" />
                <line x1="200" y1="160" x2="200" y2="65" stroke="#ffb3d9" stroke-width="2" stroke-linecap="round" class="clock-hand" :style="{ transform: 'rotate(' + secondHandRotation + 'deg)', transformOrigin: '200px 150px' }" />
                <circle cx="200" cy="150" r="4" fill="white" />
              </g>

              <g transform="translate(0, -5)">
                 <rect x="140" y="255" width="120" height="36" rx="18" fill="white" fill-opacity="0.2" />
                 <text x="200" y="278" font-family="Inter, sans-serif" font-size="20" font-weight="700" fill="white" text-anchor="middle" dominant-baseline="middle" style="text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                  {{ currentTimeString }}
                 </text>
              </g>

              <g transform="translate(0, 340)">
                 <line x1="60" y1="0" x2="340" y2="0" stroke="white" stroke-width="2" stroke-opacity="0.4" />
                 
                 <text x="200" y="-30" font-family="Inter, sans-serif" text-anchor="middle" font-size="10" font-weight="700" fill="white" opacity="0.8" letter-spacing="1">SELECT DURATION</text>

                 <g transform="translate(60, 0)">
                    <circle r="16" fill="white" />
                    <text y="4" font-family="Inter, sans-serif" text-anchor="middle" font-size="11" font-weight="bold" fill="#8b5cf6">1h</text>
                 </g>
                 <g transform="translate(153, 0)">
                    <circle r="16" fill="white" />
                    <text y="4" font-family="Inter, sans-serif" text-anchor="middle" font-size="11" font-weight="bold" fill="#8b5cf6">2h</text>
                 </g>
                 <g transform="translate(246, 0)">
                    <circle r="16" fill="white" />
                    <text y="4" font-family="Inter, sans-serif" text-anchor="middle" font-size="11" font-weight="bold" fill="#8b5cf6">3h</text>
                 </g>
                 <g transform="translate(340, 0)">
                    <circle r="16" fill="white" />
                    <text y="4" font-family="Inter, sans-serif" text-anchor="middle" font-size="11" font-weight="bold" fill="#8b5cf6">4h</text>
                 </g>
              </g>

            </svg>
          </div>
      </div>
  
      <div
        ref="communitySection"
        class="min-h-[100dvh] md:h-[70dvh] w-full p-10 md:p-25 flex flex-col md:grid grid-cols-2 grid-rows-3 gap-5 bg-gradient-to-br from-white via-[#F4EFFF] to-white"
      >
          <div
            ref="communityTitle"
            class="animate-on-scroll section-title text-4xl font-bold md:col-span-1 md:self-end md:text-left text-center"
          >
            <span class="gradient-text-primary">Join the Itinero Community:</span> <span class="gradient-text-accent">Save, Share, and Swipe.</span>
          </div>
          <div
            ref="communityText"
            class="animate-on-scroll delay-1 section-text md:row-start-2 md:col-start-1 text-justify text-base md:text-lg leading-relaxed pl-0 pr-6 py-6 rounded-2xl"
          >
            Your journey doesn't have to end when you leave Intramuros. By creating a free account, you unlock the Itinero Community! Save your best itineraries to use again or share with friends. Even better, you can explore and "take" the curated, high-rated schedules created by other history buffs. Stop planning from scratch—get inspired by the best-planned tours and contribute your own!
          </div>
          <div
            ref="communityImage"
            class="animate-on-scroll animate-scale delay-2 md:col-start-2 md:row-span-3 h-[420px] md:h-full w-full bg-white rounded-3xl shadow-[0_20px_50px_rgba(130,90,248,0.15)] border border-white/80 relative overflow-hidden community-graphic-container"
          >
            <svg viewBox="0 0 1000 500" class="w-full h-full" preserveAspectRatio="xMidYMid slice">
                <defs>
                    <linearGradient id="purpleBg" x1="0%" y1="0%" x2="100%" y2="100%">
                         <stop offset="0%" style="stop-color:#4c1d95;stop-opacity:1" />
                         <stop offset="50%" style="stop-color:#6d28d9;stop-opacity:1" />
                         <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:1" />
                    </linearGradient>
                    <linearGradient id="shapeGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#a78bfa;stop-opacity:0.4" />
                        <stop offset="100%" style="stop-color:#c4b5fd;stop-opacity:0.1" />
                    </linearGradient>
                    <linearGradient id="shapeGrad2" x1="100%" y1="0%" x2="0%" y2="100%">
                         <stop offset="0%" style="stop-color:#818cf8;stop-opacity:0.3" />
                         <stop offset="100%" style="stop-color:#c084fc;stop-opacity:0.1" />
                    </linearGradient>
                     <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur in="SourceAlpha" stdDeviation="5" />
                        <feOffset dx="0" dy="4" result="offsetblur" />
                        <feComponentTransfer>
                          <feFuncA type="linear" slope="0.2" />
                        </feComponentTransfer>
                        <feMerge>
                          <feMergeNode />
                          <feMergeNode in="SourceGraphic" />
                        </feMerge>
                      </filter>
                </defs>
                
                <rect width="1000" height="500" fill="url(#purpleBg)" />

                <g fill="url(#shapeGrad1)" stroke="none">
                    <circle cx="100" cy="100" r="150" opacity="0.5" />
                    <circle cx="900" cy="400" r="200" opacity="0.4" />
                    <path d="M 0 350 Q 250 250 500 500 L 0 500 Z" opacity="0.3" />
                </g>
                 <g fill="url(#shapeGrad2)" stroke="none">
                    <circle cx="800" cy="100" r="120" opacity="0.4" />
                    <circle cx="200" cy="450" r="100" opacity="0.3" />
                    <path d="M 1000 150 Q 750 250 500 0 L 1000 0 Z" opacity="0.3" />
                </g>
                <g fill="none" stroke="url(#shapeGrad1)" stroke-width="2" opacity="0.5">
                     <path d="M 50 50 Q 200 150 350 50" />
                     <path d="M 650 450 Q 800 350 950 450" />
                     <circle cx="500" cy="250" r="230" stroke-dasharray="10 20" opacity="0.2"/>
                </g>

                <g ref="communityCardsBg" transform="translate(500, 250)">
                    <rect class="stack-card-2" x="-130" y="-160" width="260" height="340" rx="20" fill="white" opacity="0.4" transform="rotate(-5)" />
                    <rect class="stack-card-1" x="-130" y="-160" width="260" height="340" rx="20" fill="white" opacity="0.6" transform="rotate(3)" />
                 </g>

                 <g ref="communityMainCard" class="main-card" transform="translate(500, 250)" filter="url(#cardShadow)">
                     <rect x="-130" y="-170" width="260" height="340" rx="20" fill="white" />
                     
                     <g transform="translate(-100, -135)">
                         <circle r="22" fill="#835AF8" />
                         <text x="0" y="7" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="16" fill="white">JKA</text>
                         <text x="35" y="-5" font-family="Inter, sans-serif" font-weight="700" font-size="14" fill="#333">Juan Karlo Alano</text>
                         <g transform="translate(35, 12)">
                             <path d="M5 0L6.12 3.45H9.75L6.82 5.59L7.94 9.05L5 6.9L2.06 9.05L3.18 5.59L0.25 3.45H3.88L5 0Z" fill="#FFD700"/>
                             <path d="M17 0L18.12 3.45H21.75L18.82 5.59L19.94 9.05L17 6.9L14.06 9.05L15.18 5.59L12.25 3.45H15.88L17 0Z" fill="#FFD700"/>
                             <path d="M29 0L30.12 3.45H33.75L30.82 5.59L31.94 9.05L29 6.9L26.06 9.05L27.18 5.59L24.25 3.45H27.88L29 0Z" fill="#FFD700"/>
                             <path d="M41 0L42.12 3.45H45.75L42.82 5.59L43.94 9.05L41 6.9L38.06 9.05L39.18 5.59L36.25 3.45H39.88L41 0Z" fill="#FFD700"/>
                             <path d="M53 0L54.12 3.45H57.75L54.82 5.59L55.94 9.05L53 6.9L50.06 9.05L51.18 5.59L48.25 3.45H51.88L53 0Z" fill="#FFD700"/>
                             <text x="65" y="7" font-family="Inter, sans-serif" font-weight="600" font-size="12" fill="#777">5.0</text>
                         </g>
                     </g>

                     <text x="-100" y="-80" font-family="Inter, sans-serif" font-weight="800" font-size="18" fill="#5D3AE9">Historical Highlights</text>

                     <g transform="translate(-100, -40)">
                         <g transform="translate(0, 0)">
                             <circle r="12" fill="#E5DCFF" /> <text x="0" y="5" text-anchor="middle" font-family="Inter, sans-serif" font-weight="600" font-size="12" fill="#835AF8">1</text>
                             <text x="25" y="5" font-family="Inter, sans-serif" font-weight="500" font-size="14" fill="#555">Fort Santiago</text>
                         </g>
                         <g transform="translate(0, 40)">
                             <circle r="12" fill="#E5DCFF" /> <text x="0" y="5" text-anchor="middle" font-family="Inter, sans-serif" font-weight="600" font-size="12" fill="#835AF8">2</text>
                             <text x="25" y="5" font-family="Inter, sans-serif" font-weight="500" font-size="14" fill="#555">San Agustin Church</text>
                         </g>
                         <g transform="translate(0, 80)">
                             <circle r="12" fill="#E5DCFF" /> <text x="0" y="5" text-anchor="middle" font-family="Inter, sans-serif" font-weight="600" font-size="12" fill="#835AF8">3</text>
                             <text x="25" y="5" font-family="Inter, sans-serif" font-weight="500" font-size="14" fill="#555">Casa Manila</text>
                         </g>
                         <g transform="translate(0, 120)">
                             <circle r="12" fill="#E5DCFF" /> <text x="0" y="5" text-anchor="middle" font-family="Inter, sans-serif" font-weight="600" font-size="12" fill="#835AF8">4</text>
                             <text x="25" y="5" font-family="Inter, sans-serif" font-weight="500" font-size="14" fill="#555">Baluarte de San Diego
                            </text>
                         </g>
                     </g>

                     <g transform="translate(0, 125)">
                         <line x1="-110" y1="0" x2="110" y2="0" stroke="#eee" stroke-width="1" />
                         <g transform="translate(-50, 25)" class="action-icon icon-save">
                            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="#FF6B6B" transform="scale(0.8) translate(-12, -12)"/>
                            <text x="0" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" fill="#777" font-weight="600">Save</text>
                         </g>
                         <g transform="translate(50, 25)" class="action-icon icon-share">
                            <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.66 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z" fill="#5D3AE9" transform="scale(0.8) translate(-12, -12)"/>
                             <text x="0" y="20" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" fill="#777" font-weight="600">Share</text>
                         </g>
                     </g>
                 </g>
            </svg>
          </div>
      </div>
    </div>

    <div class="h-[40dvh] w-full bg-primary-300"></div>
  
  </div>
</template>

<style scoped>
.home-root {
  font-family: "Inter", sans-serif !important;
}

.home-root * {
  font-family: inherit !important;
}

/* --- Existing Styles --- */

/* Gradient Text Styles */
.gradient-text-primary {
  background: linear-gradient(135deg, #4B1CA8 0%, #5D3AE9 50%, #835AF8 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline;
}

.gradient-text-secondary {
  background: linear-gradient(135deg, #835AF8 0%, #a78bfa 50%, #c4b5fd 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline;
}

.gradient-text-accent {
  background: linear-gradient(135deg, #d946ef 0%, #a855f7 50%, #6366f1 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline;
}

.gradient-text-animated {
  background: linear-gradient(90deg, #4B1CA8, #835AF8, #d946ef, #835AF8, #4B1CA8);
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientShift 4s ease-in-out infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* Section Title Animation */
.section-title {
  position: relative;
}

.section-title.animate-in span {
  animation: textReveal 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.section-title.animate-in span:nth-child(2) {
  animation-delay: 0.15s;
}

@keyframes textReveal {
  0% {
    opacity: 0;
    transform: translateY(30px);
    filter: blur(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}

/* Section Text Animation */
.section-text {
  color: #475569;
  position: relative;
  opacity: 0;
  transform: translateX(-30px);
}

.section-text.animate-in,
.animate-in .section-text {
  animation: textFadeSlide 1s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes textFadeSlide {
  0% {
    opacity: 0;
    transform: translateX(-30px);
    filter: blur(5px);
  }
  60% {
    opacity: 1;
    transform: translateX(5px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
    filter: blur(0);
  }
}

/* Step Card Animations */
.step-card {
  position: relative;
  overflow: hidden;
}

.step-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(131, 90, 248, 0.08), transparent);
  transition: left 0.6s ease;
}

.step-card:hover::before {
  left: 100%;
}

.step-card:hover {
  transform: translateY(-8px);
}

.step-card-title {
  position: relative;
  transition: transform 0.3s ease;
}

.step-card:hover .step-card-title {
  transform: scale(1.05);
}

/* Icon Badge Animation */
.icon-badge {
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.step-card.animate-in .icon-badge {
  animation: iconBounce 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.step-card:hover .icon-badge {
  transform: scale(1.1) rotate(-8deg);
  animation: iconTilt 0.6s ease-in-out infinite;
}

@keyframes iconBounce {
  0% {
    opacity: 0;
    transform: scale(0) rotate(-180deg);
  }
  60% {
    transform: scale(1.15) rotate(10deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

@keyframes iconTilt {
  0%, 100% {
    transform: scale(1.1) rotate(-8deg);
  }
  50% {
    transform: scale(1.1) rotate(8deg);
  }
}

/* Progress Bar Animation */
.progress-bar-container {
  position: relative;
}

.progress-bar {
  width: 0;
  transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1), transform 0.3s ease;
}

.step-card.animate-in .progress-bar {
  animation: fillProgress 1.2s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  animation-delay: 0.4s;
}

.step-card:hover .progress-bar {
  transform: scaleY(1.8);
  box-shadow: 0 0 10px currentColor;
}

@keyframes fillProgress {
  0% {
    width: 0;
  }
  100% {
    width: 100%;
  }
}

/* Scroll Animation Classes */
.animate-on-scroll {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}

.animate-on-scroll.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.animate-on-scroll.delay-1 { transition-delay: 0.1s; }
.animate-on-scroll.delay-2 { transition-delay: 0.2s; }
.animate-on-scroll.delay-3 { transition-delay: 0.3s; }
.animate-on-scroll.delay-4 { transition-delay: 0.4s; }

.animate-scale {
  opacity: 0;
  transform: scale(0.9) translateY(30px);
  transition: opacity 0.9s ease-out, transform 0.9s ease-out;
}

.animate-scale.animate-in {
  opacity: 1;
  transform: scale(1) translateY(0);
}

/* Hero animations */
.hero-fade-in {
  animation: heroFadeIn 1s ease-out forwards;
}

@keyframes heroFadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.hero-fade-in.delay-1 { animation-delay: 0.3s; opacity: 0; }
.hero-fade-in.delay-2 { animation-delay: 0.6s; opacity: 0; }
.hero-fade-in.delay-3 { animation-delay: 0.9s; opacity: 0; }

/* Route path drawing animation */
.route-path {
  stroke-dasharray: 800;
  stroke-dashoffset: 800;
}

.route-path.animate-on-scroll {
  stroke-dashoffset: 800;
  animation: none;
}

.route-path.animate-in {
  animation: drawPath 3s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
  filter: drop-shadow(0 4px 6px rgba(131, 90, 248, 0.25));
}

@keyframes drawPath {
  0% {
    stroke-dashoffset: 800;
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
  to {
    stroke-dashoffset: 0;
    opacity: 1;
  }
}

/* Route markers animation - appear after path draws */
.route-markers > g {
  opacity: 0;
  transform-origin: center;
  animation: popInMarker 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.route-markers > g:nth-child(1) { animation-delay: 0.3s; }
.route-markers > g:nth-child(2) { animation-delay: 0.6s; }
.route-markers > g:nth-child(3) { animation-delay: 0.9s; }
.route-markers > g:nth-child(4) { animation-delay: 1.2s; }
.route-markers > g:nth-child(5) { animation-delay: 1.5s; }
.route-markers > g:nth-child(6) { animation-delay: 1.8s; }

@keyframes popInMarker {
  0% { 
    opacity: 0; 
    transform: scale(0) translateY(10px); 
  }
  60% {
    transform: scale(1.3) translateY(-2px);
  }
  100% { 
    opacity: 1; 
    transform: scale(1) translateY(0); 
  }
}

.category-markers g {
  opacity: 0;
  animation: fadeInMarker 0.6s ease-out forwards;
}
.category-markers g:nth-child(1) { animation-delay: 2.0s; }
.category-markers g:nth-child(2) { animation-delay: 2.2s; }
.category-markers g:nth-child(3) { animation-delay: 2.4s; }
.category-markers g:nth-child(4) { animation-delay: 2.6s; }
.category-markers g:nth-child(5) { animation-delay: 2.8s; }

@keyframes fadeInMarker {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}

.blinking-cursor {
  font-weight: 100;
  margin-left: 2px;
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.clock-container {
  transition: transform 0.3s ease-in-out, filter 0.3s ease-in-out;
}
.group:hover .clock-container {
  transform: scale(1.05);
  filter: brightness(1.1);
}
.clock-hand {
  transition: transform 0.1s cubic-bezier(0.4, 2.08, 0.55, 0.44);
}


.community-graphic-container {
    cursor: pointer;
}

.main-card, .stack-card-1, .stack-card-2 {
    transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.action-icon {
    transition: transform 0.3s ease, filter 0.3s ease;
}


.community-graphic-container:hover .main-card {
    transform: translate(500px, 240px) rotate(2deg) !important; 
}

.community-graphic-container:hover .stack-card-1 {
    transform: rotate(8deg) translate(10px, 0px) !important; 
}

.community-graphic-container:hover .stack-card-2 {
    transform: rotate(-12deg) translate(-10px, 5px) !important; 
}

.community-graphic-container:hover .icon-save {
    transform: translate(-50px, 22px) scale(1.1);
    filter: drop-shadow(0 4px 6px rgba(255, 107, 107, 0.4));
}
.community-graphic-container:hover .icon-share {
    transform: translate(50px, 22px) scale(1.1);
    filter: drop-shadow(0 4px 6px rgba(93, 58, 233, 0.4));
}
</style>