<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

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
const maximizeSection = ref(null);
const maximizeTitle = ref(null);
const maximizeText = ref(null);
const maximizeImage = ref(null);
const communitySection = ref(null);
const communityTitle = ref(null);
const communityText = ref(null);
const communityImage = ref(null);
let ctx;

onMounted(() => {
  ctx = gsap.context(() => {
    if (
      heroSection.value &&
      heroTitle.value &&
      heroSubtitle.value &&
      heroButton.value &&
      heroOverlay.value
    ) {
      const heroTimeline = gsap.timeline({
        defaults: { ease: "power3.out", duration: 0.9 },
      });

      heroTimeline
        .from(heroOverlay.value, {
          opacity: 0,
          duration: 1.2,
          ease: "power2.out",
        })
        .from(
          heroTitle.value,
          {
            opacity: 0,
            y: 40,
          },
          "-=0.8"
        )
        .from(
          heroSubtitle.value,
          {
            opacity: 0,
            y: 30,
          },
          "-=0.6"
        )
        .from(
          heroButton.value,
          {
            opacity: 0,
            y: 25,
            scale: 0.95,
          },
          "-=0.5"
        );
    }

    if (howItWorks.value && howItWorksTitle.value) {
      gsap.from(howItWorksTitle.value, {
        opacity: 0,
        y: 35,
        duration: 0.8,
        ease: "power2.out",
        scrollTrigger: {
          trigger: howItWorks.value,
          start: "top 85%",
          toggleActions: "play none none reverse",
        },
      });
    }

    if (stepCards.value && howItWorks.value) {
      const cards = stepCards.value.children;

      gsap.from(cards, {
        opacity: 0,
        y: 60,
        duration: 0.8,
        stagger: 0.2,
        ease: "power2.out",
        scrollTrigger: {
          trigger: howItWorks.value, 
          start: "top 75%", 
          toggleActions: "play none none reverse",
        },
      });
    }

    const makeSectionTimeline = (sectionRefs) => {
      const { section, title, text, image } = sectionRefs;

      if (section.value && title.value && text.value && image.value) {
        const tl = gsap.timeline({
          defaults: { ease: "power2.out", duration: 0.85 },
          scrollTrigger: {
            trigger: section.value,
            start: "top 70%",
            toggleActions: "play none none reverse",
          },
        });

        tl.from(title.value, { opacity: 0, y: 40 })
          .from(
            text.value,
            { opacity: 0, y: 35 },
            "-=0.55"
          )
          .from(
            image.value,
            { opacity: 0, scale: 0.92, y: 30 },
            "-=0.55"
          );
      }
    };

    makeSectionTimeline({
      section: historySection,
      title: historyTitle,
      text: historyText,
      image: historyImage,
    });

    makeSectionTimeline({
      section: maximizeSection,
      title: maximizeTitle,
      text: maximizeText,
      image: maximizeImage,
    });

    makeSectionTimeline({
      section: communitySection,
      title: communityTitle,
      text: communityText,
      image: communityImage,
    });
  }); 
});

onUnmounted(() => {

  if (ctx) {
    ctx.revert();
  }
});
</script>

<template>
  <div class="home-root min-h-[300dvh] w-full flex flex-col overflow-x-hidden">

    <div
      ref="heroSection"
      class="relative min-h-screen w-full flex flex-col justify-center items-center px-5 py-16 md:p-16 bg-[url('@/assets/imgs/IMG_6906.jpg')] md:bg-[url('@/assets/imgs/IMG_8186.jpg')] bg-cover bg-center md:bg-fixed"
    >
      <div
        ref="heroOverlay"
        class="absolute inset-0 bg-gradient-to-b from-black/35 via-black/10 to-transparent md:bg-gradient-to-r md:from-black/40 md:via-transparent md:to-transparent pointer-events-none"
      ></div>
      <div class="relative z-10 flex flex-col items-center text-center gap-6 max-w-3xl">
        <h1
          ref="heroTitle"
          class="text-4xl md:text-7xl leading-tight font-bold text-white [text-shadow:4px_4px_0px_#4E1E95]"
        >
          Plan Your Intramuros Trip in a Minute
        </h1>
        <p
          ref="heroSubtitle"
          class="text-lg md:text-xl font-semibold tracking-tight px-4 md:px-6 leading-relaxed text-white [text-shadow:0_0_18px_rgba(116,68,221,0.75),0_0_36px_rgba(204,169,255,0.6)]"
        >
          Generate Intramuros itineraries in seconds.<br />
          Skip the research and get straight to exploring Manila's Walled City!
        </p>
        <Button
          ref="heroButton"
          label="Create Itinerary"
          rounded
          raised
          class="w-55 transition-transform transition-colors ease-out duration-300 bg-[#835AF8] hover:bg-[#9C7BFF] hover:scale-110 text-white border-0 shadow-[0_22px_48px_rgba(98,54,210,0.6)] focus:outline-none focus-visible:ring-4 focus-visible:ring-[#C5B6FE]/60"
          @click="createAndRefresh"
        ></Button>
      </div>
    </div>
    
    <div class="min-h-screen w-full flex flex-col justify-center items-center bg-gradient-to-b from-primary-50/30 to-white" ref="howItWorks">
        <div ref="howItWorksTitle" class="text-4xl font-bold mb-6 tracking-tight drop-shadow-[0_8px_22px_rgba(92,45,190,0.35)] text-transparent bg-clip-text bg-gradient-to-r from-[#4B1CA8] to-[#835AF8]">
          How It Works
        </div>
        <div class="flex md:flex-row flex-col gap-4 w-full justify-center flex-wrap p-5" ref="stepCards">
          <div class="w-full h-28 md:h-120 md:w-75 bg-white shadow-xl shadow-[#835AF8]/20 hover:shadow-[#835AF8]/35 rounded-2xl flex flex-col items-center justify-center p-6 border border-[#E5DCFF] transition-shadow duration-300 ease-out">
            <span class="text-[#5D3AE9] font-semibold text-lg md:text-xl drop-shadow-[0_4px_12px_rgba(93,58,233,0.25)]">Tell Us Your Time</span>
            <span class="text-slate-600 text-sm md:text-base text-center mt-2">Pick how much time you have to explore Intramuros.</span>
          </div>
          <div class="w-full h-28 md:h-120 md:w-75 bg-white shadow-xl shadow-[#835AF8]/20 hover:shadow-[#835AF8]/35 rounded-2xl flex flex-col items-center justify-center p-6 border border-[#E5DCFF] transition-shadow duration-300 ease-out">
            <span class="text-[#5D3AE9] font-semibold text-lg md:text-xl drop-shadow-[0_4px_12px_rgba(93,58,233,0.25)]">Choose the Vibes</span>
            <span class="text-slate-600 text-sm md:text-base text-center mt-2">Mix and match categories like Museums, Cafés, Parks, and more.</span>
          </div>
          <div class="w-full h-28 md:h-120 md:w-75 bg-white shadow-xl shadow-[#835AF8]/20 hover:shadow-[#835AF8]/35 rounded-2xl flex flex-col items-center justify-center p-6 border border-[#E5DCFF] transition-shadow duration-300 ease-out">
            <span class="text-[#5D3AE9] font-semibold text-lg md:text-xl drop-shadow-[0_4px_12px_rgba(93,58,233,0.25)]">Get Your Smart Route</span>
            <span class="text-slate-600 text-sm md:text-base text-center mt-2">See a ready-to-go map, optimized sequence, and tips to keep you on pace.</span>
          </div>
        </div>
    </div>


    <div class="md:block flex flex-col gap-2">
      <div
        ref="historySection"
        class="h-[100dvh] md:h-[70dvh] w-full p-10 md:p-25 md:grid grid-cols-2 grid-rows-3 gap-5 bg-gradient-to-br from-white via-primary-50/45 to-white"
      >
          <div
            ref="historyTitle"
            class="text-4xl text-[#5D3AE9] font-bold col-span-1 self-end md:text-left text-center drop-shadow-[0_14px_30px_rgba(93,58,233,0.35)]"
          >
            See the History You Care About.
          </div>
          <div
            ref="historyText"
            class="row-start-2 col-start-1 text-justify text-slate-700 leading-relaxed pl-0 pr-6 py-6 rounded-2xl"
          >
            Why use a global map app when you can use one tailored for the unique cobblestone streets of Intramuros? Itinero focuses exclusively on the Walled City, giving you the most accurate and relevant routes. Better yet, you control the sightseeing agenda. Choose from 6 distinct place categories—like Churches, Museums, Cafes, Restaurants, or Parks—to ensure your itinerary is packed only with the historical, cultural, or architectural spots that interest you.
          </div>
          <div
            ref="historyImage"
            class="col-start-2 row-span-3 md:h-full w-full bg-white rounded-3xl shadow-[0_20px_50px_rgba(130,90,248,0.15)] border border-white/80"
          ></div>
      </div>
  
      <div
        ref="maximizeSection"
        class="h-[100dvh] md:h-[70dvh] w-full p-10 md:p-25 md:grid grid-cols-2 grid-rows-3 gap-5 bg-gradient-to-bl from-[#F8F6FF] via-white to-[#F2EEFF]"
      >
          <div
            ref="maximizeTitle"
            class="text-4xl text-[#5D3AE9] font-bold col-start-2 col-span-1 self-end text-center md:text-right drop-shadow-[0_14px_30px_rgba(93,58,233,0.35)]"
          >
            Maximize Every Minute.
          </div>
          <div
            ref="maximizeText"
            class="row-start-2 col-start-2 text-justify text-slate-700 leading-relaxed pl-6 md:pl-10 pr-0 py-6 rounded-2xl"
          >
            Whether you have a quick two-hour window or a full day to explore, our Time Constraint Filter is your best friend. Input your total available time, and Itinero intelligently crafts a viable route that fits your schedule without rushing you. See the results instantly visualized: a dynamic map view with polylines connecting your destinations, paired with a detailed, sequential schedule that makes navigation simple and stress-free.
          </div>
          <div
            ref="maximizeImage"
            class="col-start-1 row-start-1 row-span-3 md:h-full w-full bg-white rounded-3xl shadow-[0_20px_50px_rgba(130,90,248,0.15)] border border-white/80"
          ></div>
      </div>
  
      <div
        ref="communitySection"
        class="h-[100dvh] md:h-[70dvh] w-full p-10 md:p-25 md:grid grid-cols-2 grid-rows-3 gap-5 bg-gradient-to-br from-white via-[#F4EFFF] to-white"
      >
          <div
            ref="communityTitle"
            class="text-4xl text-[#5D3AE9] font-bold col-span-1 self-end md:text-left text-center drop-shadow-[0_14px_30px_rgba(93,58,233,0.35)]"
          >
            Join the Itinero Community: Save, Share, and Swipe.
          </div>
          <div
            ref="communityText"
            class="row-start-2 col-start-1 text-justify text-slate-700 leading-relaxed pl-0 pr-6 py-6 rounded-2xl"
          >
            Your journey doesn't have to end when you leave Intramuros. By creating a free account, you unlock the Itinero Community! Save your best itineraries to use again or share with friends. Even better, you can explore and "take" the curated, high-rated schedules created by other history buffs. Stop planning from scratch—get inspired by the best-planned tours and contribute your own!
          </div>
          <div
            ref="communityImage"
            class="col-start-2 row-span-3 md:h-full w-full bg-white rounded-3xl shadow-[0_20px_50px_rgba(130,90,248,0.15)] border border-white/80"
          ></div>
      </div>
    </div>

    <div class="h-[40dvh] w-full bg-primary-300"></div>


  
    
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Ubuntu:wght@400;500;700&display=swap");

.home-root {
  font-family: "Ubuntu", "Poppins", sans-serif !important;
}

.home-root * {
  font-family: inherit !important;
}
</style>

