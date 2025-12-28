<script setup>
  import Navbar from '@/components/Navbar.vue';
  import NavbarMobile from '@/components/NavbarMobile.vue';
  import NavbarMobileOverlay from '@/components/NavbarMobileOverlay.vue';
</script>



<template>
  <div class="relative h-full w-screen flex flex-col">

    <!-- Mobile Top Overlay (fixed positioning) -->
    <div class="md:hidden">
      <NavbarMobileOverlay />
    </div>

    <!-- Main Content (full width on desktop) -->
    <main class="flex-1 overflow-auto">
      <router-view />
    </main>

    <!-- Mobile Bottom Navbar (part of content flow) -->
    <div class="md:hidden flex-shrink-0">
      <NavbarMobile />
    </div>

    <!-- Desktop Navbar Overlay -->
    <div class="hidden md:block min-w-18 h-full flex-shrink-0 fixed z-10 left-0">
      <Navbar />
    </div>

  </div>
</template>

