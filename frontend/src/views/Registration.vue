<script setup>
import FloatLabel from 'primevue/floatlabel';
import InputText from 'primevue/inputtext'
</script>

<template>
    <section class="h-[100dvh] w-screen flex justify-center items-center">
        <div class="ml-10 h-[80%] w-[40%] flex flex-col justify-start items-start gap-6 p-15">
            <div class="text-5xl font-bold font-[Poppins] text-primary-500">Sign In</div>

            <FloatLabel>
                <InputText id="Username" fluid></InputText>
                <label for="Username">Username</label>
            </FloatLabel>
            <FloatLabel>
                <InputText id="Password" fluid></InputText>
                <label for="Password">Password</label>
            </FloatLabel>

            <Button label="Sign In" fluid></Button>
            <Button label="Create new account" severity="secondary" fluid></Button>

        </div>
        <div class="h-full w-[60%] p-4">
            <div class="h-full w-full rounded-xl bg-[url('@/assets/imgs/DSC_0368.jpg')] bg-cover shadow-[0_0_10px_rgba(0,0,0,0.5)]"></div>
        </div>
    </section>

</template>