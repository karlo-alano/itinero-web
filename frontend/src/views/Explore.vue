<script setup>
import InputText from 'primevue/inputtext';


const search = null;
</script>

<template>
    <div class="h-[300dvh] w-full bg-pink-50">
        <section class="h-[28dvh] w-screen flex flex-col justify-center items-center md:p-4 gap-2">
            <div class="text-7xl font-extrabold text-slate-700 font-[Poppins]">Explore</div>
            <div class="flex gap-2 justify-center items-center w-full">
                <InputText type="text" v-model="search" class="w-[40%] rounded-full"/>
                <Button icon="pi pi-search" rounded class=""></Button>
            </div>
        </section>
        <section class="h-[100dvh] w-screen flex md:flex-row md:pl-15 md:pr-4">
            <div class="h-full w-[75%] grid grid-rows-3 grid-cols-3 gap-4 p-4">
                <div class="h-full w-full bg-slate-200 rounded-xl"></div>
                <div class="h-full w-full bg-slate-200 rounded-xl"></div>
                <div class="h-full w-full bg-slate-200 rounded-xl"></div>
                <div class="h-full w-full bg-slate-200 rounded-xl"></div>
                <div class="h-full w-full bg-slate-200 rounded-xl"></div>

            </div>
              <div class="h-full w-[25%] p-2">
                <div class="h-full w-full rounded-xl bg-slate-100 p-2">
                    <div class="h-full w-full bg-white rounded-xl drop-shadow-2xl"></div>
                </div>
            </div>
        </section>

    <div class="h-[100dvh] w-screen flex flex-col md:flex-row justify-center items-center md:p-20">
      <div class="flex flex-col md:flex-row justify-center gap-2 p-2">

        <div class="h-full flex flex-col p-4 rounded-xl bg-primary-50 transition-all ease-in-out duration-250 hover:scale-101 cursor-pointer w-100">
          <p class="font-extrabold text-black text-2xl mb-4">Popular Trips</p>
          <div class="bg-white md:h-50 h-25 rounded-xl" ></div>
          <p class="">Come check out the most popular trips in other users made!</p>
          <Button label="View more" rounded class="md:w-45"></Button>          
        </div>

        <div class="flex md:min-w-[1/3] flex-col p-4 rounded-xl bg-primary-50 transition-all ease-in-out duration-250 hover:scale-101 cursor-pointer min-w-100">
          <p class="font-extrabold text-black text-2xl mb-4">Reccomended</p>
          <div class="bg-white md:h-50 h-25 rounded-xl" ></div>
          <p class="">Places that the dev team recommend ;D</p>
          <Button label="View more" rounded class="md:w-45"></Button>          
        </div>

        <div class="flex md:w-50 flex-col p-4 rounded-xl bg-primary-50 transition-all ease-in-out duration-250 hover:scale-101 cursor-pointer min-w-100">
          <p class="font-extrabold text-black text-2xl mb-4">Travel Guides</p>
          <div class="bg-white md:h-50 h-25 rounded-xl" ></div>
          <p class="">Check out travel guides from esteemed bloggers*</p>
          <Button label="View more" rounded class="md:w-45"></Button>          
        </div>
      </div>

    </div>




    </div>
</template>