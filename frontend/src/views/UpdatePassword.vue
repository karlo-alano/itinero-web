<script setup>
    import { ref, onMounted } from 'vue';
    import { useRouter } from 'vue-router';
    import { supabase } from '@/lib/supabase';
    import Password from 'primevue/password';
    import Button from 'primevue/button';
    import Message from 'primevue/message';
    
    const router = useRouter();
    
    // --- STATE ---
    const password = ref('');
    const loading = ref(false);
    const successMessage = ref('');
    const errorMessage = ref('');
    const isSessionValid = ref(true);
    
    // --- VALIDATION (Matches Registration.vue) ---
    const validatePassword = (pass) => {
        if (pass.length < 8) return { valid: false, msg: "Password must be at least 8 characters long." };
        
        const hasNumber = /\d/.test(pass);
        const hasUpper = /[A-Z]/.test(pass);
        const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(pass);
    
        if (!hasNumber || !hasUpper || !hasSpecial) {
            return { valid: false, msg: "Password must include a number, an uppercase letter, and a special character." };
        }
        return { valid: true };
    };
    
    onMounted(async () => {
        // 1. Verify the user is actually authenticated via the email link
        // Supabase automatically handles the access_token in the URL and sets the session
        const { data: { session }, error } = await supabase.auth.getSession();
        
        if (error || !session) {
            isSessionValid.value = false;
            errorMessage.value = "This password reset link is invalid or has expired.";
        }
    });
    
    const handleUpdatePassword = async () => {
        errorMessage.value = '';
        
        // 1. Validate Password Strength
        const passCheck = validatePassword(password.value);
        if (!passCheck.valid) {
            errorMessage.value = passCheck.msg;
            return;
        }
    
        loading.value = true;
        
        // 2. Call Supabase API
        const { error } = await supabase.auth.updateUser({ 
            password: password.value 
        });
    
        if (error) {
            errorMessage.value = error.message;
            loading.value = false;
        } else {
            successMessage.value = "Password updated successfully!";
            loading.value = false;
            
            // 3. Redirect after delay
            setTimeout(() => {
                router.push('/'); // Redirect to Login/Home
            }, 2000);
        }
    };
    </script>
    
    <template>
        <div class="h-full flex items-center justify-center bg-gradient-to-tr from-purple-300 via-purple-100 to-white font-['Inter'] p-4">
            
            <div class="w-full max-w-md card bg-white">
                
                <div class="text-center mb-8">
                    <h1 class="text-3xl font-bold bg-gradient-to-r from-purple-700 via-purple-600 to-indigo-500 bg-clip-text text-transparent">
                        Set New Password
                    </h1>
                    <p class="text-surface-500 mt-2 text-sm">Please enter a secure password for your account.</p>
                </div>
    
                <div v-if="errorMessage" class="mb-6 p-4 rounded-xl bg-red-50 border border-red-100 flex items-start gap-3">
                    <i class="pi pi-exclamation-circle text-red-500 text-xl mt-0.5"></i>
                    <div>
                        <p class="font-bold text-red-700 text-sm">Error</p>
                        <p class="text-red-600 text-sm leading-tight">{{ errorMessage }}</p>
                    </div>
                </div>
    
                <div v-if="successMessage" class="mb-6 p-4 rounded-xl bg-green-50 border border-green-100 flex items-center gap-3">
                    <i class="pi pi-check-circle text-green-500 text-2xl"></i>
                    <div>
                        <p class="font-bold text-green-700 text-sm">Success!</p>
                        <p class="text-green-600 text-sm">Redirecting you to login...</p>
                    </div>
                </div>
    
                <div v-if="isSessionValid && !successMessage" class="flex flex-col gap-6">
                    
                    <div class="flex flex-col gap-2">
                        <label for="newPassword" class="text-surface-600 font-medium ml-1">New Password</label>
                        <Password 
                            id="newPassword"
                            v-model="password" 
                            toggleMask 
                            :feedback="true"
                            inputClass="w-full !rounded-xl !py-3 !bg-white border-surface-300" 
                            class="w-full"
                        >
                            <template #header>
                                <div class="font-semibold text-sm mb-2">Pick a password</div>
                            </template>
                            <template #footer>
                                <div class="border-t border-gray-300 mt-2 pt-2">
                                    <ul class="pl-2 ml-2 mt-0 list-disc text-xs text-gray-600">
                                        <li>At least one lowercase</li>
                                        <li>At least one uppercase</li>
                                        <li>At least one numeric</li>
                                        <li>At least one special char</li>
                                        <li>Minimum 8 characters</li>
                                    </ul>
                                </div>
                            </template>
                        </Password>
                    </div>
    
                    <Button 
                        label="Update Password" 
                        :loading="loading"
                        class="!bg-purple-600 hover:!bg-purple-700 !rounded-xl !py-3.5 !font-bold !border-none" 
                        fluid 
                        @click="handleUpdatePassword" 
                    />
                </div>
    
                <div v-if="!isSessionValid" class="flex flex-col gap-4 ">
                    <Button 
                        label="Back to Sign In" 
                        severity="secondary" 
                        class="interactive-btn-primary" 
                        fluid 
                        @click="router.push('/')" 
                    />
                </div>
    
            </div>
        </div>
    </template>