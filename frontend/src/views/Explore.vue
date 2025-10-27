<script setup>
import InputText from 'primevue/inputtext';

const catalog = 9

const search = null;
</script>

<template>
    <div class="h-[128dvh] w-full bg-slate-50">
        <section class="h-[28dvh] w-screen flex flex-col justify-center items-center md:p-4 gap-2">
            <div class="text-7xl font-extrabold text-slate-800 font-[Poppins]">Explore</div>
            <div class="flex gap-2 justify-center items-center w-full">
                <InputText type="text" v-model="search" class="w-[40%] rounded-full"/>
                <Button icon="pi pi-search" rounded class=""></Button>
            </div>
        </section>
        <section class="h-[100dvh] w-screen flex flex-col-reverse md:flex-row md:pl-15 md:pr-4">
            <div class="md:h-full md:w-[75%] h-[25%] w-screen md:grid md:grid-rows-3 md:grid-cols-3 flex flex-cols gap-4 p-4">
              
                <div v-for="card in catalog" class="h-full w-full bg-white rounded-xl drop-shadow-2xl p-4 gap-2 cursor-pointer hover:scale-101 transition-all ease-in-out hover:bg-slate-200">
                  <div class="flex flex-row justify-between mb-2">
                    <div class="text-3xl font-bold text-slate-600">Title</div>
                    <span class="p-2 rounded-full bg-yellow-400 font-bold w-20 flex justify-center">Tag</span>
                  </div>
                  <div class="w-full h-[60%] bg-slate-300 rounded-xl"></div>
                  <div class="overflow-hidden ">Lorem ipsum dolor sit amet </div>
                </div>

            </div>
              <div class="md:h-full md:w-[25%] w-full h-[25%] p-4">
                    <div class="h-full w-full bg-white rounded-xl drop-shadow-2xl">

                    </div>
            </div>
        </section>






    </div>
</template>