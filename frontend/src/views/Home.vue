<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

const stepCards = ref(null);
const howItWorks = ref(null);
let ctx;

onMounted(() => {
  ctx = gsap.context(() => {
    // Check for both refs now
    if (stepCards.value && howItWorks.value) { 
      const cards = stepCards.value.children;

      gsap.from(cards, {
        opacity: 0,
        y: 60,
        duration: 0.8,
        stagger: 0.2,
        ease: "power2.out",
        scrollTrigger: {
          trigger: howItWorks.value, // <-- 2. Use the SECTION as the trigger
          start: "top 75%", // <-- 3. Change start position
          toggleActions: "play none none reverse",
        },
      });
    }
  }); // You can scope context to the root element if you have one
});

onUnmounted(() => {
  // All animations and ScrollTriggers created in the context are reverted/killed
  if (ctx) {
    ctx.revert();
  }
});
</script>

<template>
  <div class="min-h-[300dvh] w-full flex flex-col overflow-x-hidden">

    <div class="min-h-screen w-full p-4 md:p-10 flex flex-col justify-center items-center bg-[url('@/assets/imgs/IMG_6906.jpg')] md:bg-[url('@/assets/imgs/IMG_8186.jpg')] bg-cover bg-fixed">
      <h1 class="text-4xl md:text-7xl font-bold text-white font-[Poppins] w-full md:w-[60%] text-center text-shadow">Plan Your Intramuros Trip in a Minute</h1>
      <p class="text-2xl mb-10 text-center text-pink-200 w-[70%] text-shadow2 font-[Poppins] font-bold">
        Generate intramuros itineraries in seconds<br></br>
        Skip the research and get straight to exploring Manila's Walled City!
      </p>
      <Button label="Create Itinerary" rounded raised class=" w-55 transition-all ease-in-out duration-250 hover:scale-115 hover:ring-primary-200 hover:text-black border-0"></Button>
    </div>
    
    <div class="min-h-screen w-full flex flex-col justify-center items-center" ref="howItWorks">
        <div class="text-4xl text-primary-500 font-bold font-[Poppins] mb-4">How It Works</div>
        <div class="flex md:flex-row flex-col gap-4 w-full justify-center flex-wrap p-5" ref="stepCards">
          <div class="w-full h-20 md:h-120 md:w-75 bg-primary-200 rounded-xl flex flex-col items-center p-4"></div>
          <div class="w-full h-20 md:h-120 md:w-75 bg-primary-200 rounded-xl flex flex-col items-center p-4"></div>
          <div class="w-full h-20 md:h-120 md:w-75 bg-primary-200 rounded-xl flex flex-col items-center p-4"></div>
        </div>
    </div>


    <div class="md:block flex flex-col gap-2">
      <div class="h-10 w-full bg-primary-100"></div>
      <div class="h-[100dvh] md:h-[70dvh] w-full p-10 md:p-25 md:grid grid-cols-2 grid-rows-3 gap-5 bg-primary-50">
          <div class="font-[Poppins] text-4xl text-primary-500 font-bold col-span-1 self-end md:text-left text-center ">See the History You Care About.</div>
          <div class="row-start-2 col-start-1 text-justify">
            Why use a global map app when you can use one tailored for the unique cobblestone streets of Intramuros? Itinero focuses exclusively on the Walled City, giving you the most accurate and relevant routes. Better yet, you control the sightseeing agenda. Choose from 6 distinct place categories—like Churches, Museums, Cafes, Restaurants, or Parks—to ensure your itinerary is packed only with the historical, cultural, or architectural spots that interest you.
          </div>
          <div class="col-start-2 row-span-3 md:h-full w-full bg-slate-200 rounded-xl"></div>
      </div>
  
      <div class="h-[100dvh] md:h-[70dvh] w-full p-10 md:p-25 md:grid grid-cols-2 grid-rows-3 gap-5 bg-primary-100">
          <div class="font-[Poppins] text-4xl text-primary-500 font-bold col-start-2 col-span-1 self-end">Maximize Every Minute.</div>
          <div class="row-start-2 col-start-2 text-justify">
            Whether you have a quick two-hour window or a full day to explore, our Time Constraint Filter is your best friend. Input your total available time, and Itinero intelligently crafts a viable route that fits your schedule without rushing you. See the results instantly visualized: a dynamic map view with polylines connecting your destinations, paired with a detailed, sequential schedule that makes navigation simple and stress-free.
          </div>
          <div class="col-start-1 row-start-1 row-span-3 md:h-full w-full bg-slate-200 rounded-xl"></div>
      </div>
  
      <div class="h-[100dvh] md:h-[70dvh] w-full p-10 md:p-25 md:grid grid-cols-2 grid-rows-3 gap-5 bg-primary-50">
          <div class="font-[Poppins] text-4xl text-primary-500 font-bold col-span-1 self-end">Join the Itinero Community: Save, Share, and Swipe.</div>
          <div class="row-start-2 col-start-1 text-justify">
            Your journey doesn't have to end when you leave Intramuros. By creating a free account, you unlock the Itinero Community! Save your best itineraries to use again or share with friends. Even better, you can explore and "take" the curated, high-rated schedules created by other history buffs. Stop planning from scratch—get inspired by the best-planned tours and contribute your own!        </div>
          <div class="col-start-2 row-span-3 md:h-full w-full bg-slate-200 rounded-xl"></div>
      </div>
    </div>

    <div class="h-[40dvh] w-full bg-primary-300"></div>


  
    
  </div>
</template>

