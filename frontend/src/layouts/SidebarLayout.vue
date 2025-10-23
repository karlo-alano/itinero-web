<script setup>
    import Navbar from '@/components/Navbar.vue';
    import Sidebar from '@/components/Sidebar.vue';
    import NavbarMobile from '@/components/NavbarMobile.vue';
    import SidebarMobile from '@/components/SidebarMobile.vue';



</script>



<template>
  <div class="relative h-screen w-screen overflow-hidden">
    <!-- Page content -->
    <main class="absolute inset-0 z-0">
      <router-view />
    </main>

    <!-- Top navbar -->
    <div class="hidden md:block w-25 h-full flex-shrink-0 fixed z-10">
      <Navbar />
    </div>

    <div class="absolute md:hidden left-0 right-0 z-10 pointer-events-none">
      <NavbarMobile />
    </div>



    <!-- Sidebar -->
    <div class="md:absolute md:block hidden right-0 h-full w-[25%] z-10">
      <Sidebar />
    </div>

    <div class="absolute md:hidden top-[calc(4rem)] left-0 h-[calc(100%-8.5rem)] w-full z-5 pointer-events-none">
      <SidebarMobile />
    </div>


  </div>
</template>


