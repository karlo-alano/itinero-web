<script setup></script>

<template>
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
</template>