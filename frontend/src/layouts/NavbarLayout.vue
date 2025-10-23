<script setup>
  import Navbar from '@/components/Navbar.vue';
  import NavbarMobile from '@/components/NavbarMobile.vue';
</script>



<template>
  <div class="relative h-screen w-screen">

    <!-- Page content -->


    <div class="hidden md:block w-25 h-full flex-shrink-0 fixed z-10">
      <Navbar />
    </div>
    <main class="flex-1">
      <router-view />
    </main>
    
    <div class="absolute md:hidden left-0 right-0 z-10 pointer-events-none">
      <NavbarMobile />
    </div>


  </div>
</template>

<!-- 
    <main class="absolute inset-0 z-0">
      <router-view />
    </main>

    <div class="md:fixed md:top-0 hidden md:block left-0 right-0 z-10">
      <Navbar />
    </div> -->
