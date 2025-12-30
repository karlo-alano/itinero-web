<script setup>
    import { ref,onMounted } from 'vue';
    import Avatar from 'primevue/avatar';
    import InputText from 'primevue/inputtext';
    import Textarea from 'primevue/textarea';
    import { useUserStore } from '@/store/userStore';
    import { useRouter } from 'vue-router';
    import AccountsTabs from '@/components/AccountsTabs.vue';

    const router = useRouter();
    const userStore = useUserStore();

    const username = userStore.profile.user_name;
    const usernameProfileLetter = username[0];

    const signOutFunction = () => {
        userStore.signOut()
        router.push('/')
    }

    const isEditing = ref(false);
    const editedUsername = ref('');
    const editedDescription = ref('');

    const startEditing = () => {
        editedUsername.value = userStore.profile.user_name;
        editedDescription.value = userStore.profile.bio || '';
        isEditing.value = true;
    };

    const cancelEditing = () => {
        isEditing.value = false;
    };

    const saveChanges = async () => {
        const { success, error } = await userStore.updateProfile({
            user_name: editedUsername.value,
            bio: editedDescription.value
        });

        if (!success) {
            console.error('Error saving profile changes:', error);
            // Optionally, show a user-friendly error message
            return;
        }
        await userStore.loadProfile(userStore.user.id);
        isEditing.value = false;
    };


</script>
<template>
    <section class="min-h-full md:h-full w-full gradient-5 md:pl-25 p-4 flex gap-4 flex-col animate-enter" style="--delay:0s">
        <div class="md:h-[40%] flex md:flex-row flex-col items-center gap-4 animate-enter" style="--delay:0.1s">
            <div class="h-full flex flex-col items-center gap-2">
                <Avatar :label="usernameProfileLetter" class="bg-primary-500 text-white w-40 h-40 rounded-xl" size="xlarge" />
            </div>
            <div class="h-full flex flex-col md:justify-between sm:items-center ">
                <template v-if="!isEditing">
                    <h1 class="text-4xl font-bold text-slate-800 pb-4 ">{{username}}</h1>
                    <p class="text-slate-600 md:w-[60%] w-full p-4">{{userStore.profile.bio || 'No description available.'}}</p>
                </template>
                <template v-else>
                    <div class="flex flex-col gap-2 mb-4">
                        <InputText v-model="editedUsername" class="text-4xl font-bold text-slate-800 pb-4 w-full field-input" />
                        <Textarea v-model="editedDescription" autoResize rows="5" cols="30" class="text-slate-600 md:w-[60%] w-full p-4 field-input" />
                    </div>
                </template>
                <div class="flex justify-end gap-2 animate-enter" style="--delay:0.3s">
                    <Button v-if="!isEditing" label="Edit Profile" @click="startEditing" class="interactive-btn-secondary !text-black text-sm min-w-40"></Button>
                    <Button v-else label="Save Changes" @click="saveChanges" class="interactive-btn-primary !text-white text-sm min-w-40 text-sm"></Button>
                    <Button v-if="isEditing" label="Cancel" @click="cancelEditing" class="interactive-btn-secondary min-w-40 text-sm"></Button>
                    <Button v-if="!isEditing" label="Sign Out" icon="pi pi-sign-out" @click="signOutFunction" class="interactive-btn-danger min-w-40"></Button>
                </div>


            </div>
        </div>
        <div class="card bg-white md:h[60%] h-120 animate-enter" style="--delay:0.2s">
            <AccountsTabs />
        </div>
    </section>
</template>