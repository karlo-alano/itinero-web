<script setup>
    import { ref, onMounted, onUnmounted, watch } from 'vue';
    import FloatLabel from 'primevue/floatlabel';
    import InputText from 'primevue/inputtext';
    import Button from 'primevue/button';
    import Message from 'primevue/message'; // Optional if you use PrimeVue messages, but I built a custom Tailwind one below
    import { useUserStore } from '@/store/userStore';
    import { useRouter } from 'vue-router';
    
    const router = useRouter();
    const userStore = useUserStore();
    
    // --- STATE ---
    const displayedText = ref('');
    const isSignInMode = ref(true);
    const isSignedUp = ref(false); 
    let animationTimeout = null;
    
    // Form Fields
    const email = ref('');
    const username = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    
    // Error Handling State
    const errorMessage = ref('');
    
    // --- TYPING ANIMATION ---
    const startTypewriter = (text) => {
      if (animationTimeout) clearTimeout(animationTimeout);
    
      displayedText.value = '';
      let i = 0;
    
      const typeWriter = () => {
        if (i < text.length) {
          displayedText.value += text.charAt(i);
          i++;
          animationTimeout = setTimeout(typeWriter, 80); 
        } else {
          animationTimeout = null;
        }
      };
      typeWriter();
    };
    
    const toggleAccountMode = () => {
      errorMessage.value = ''; // Clear errors on switch
      isSignInMode.value = !isSignInMode.value;
      const text = isSignInMode.value ? "Sign In to Itinero" : "Create an Account";
      startTypewriter(text);
      clearForm();
    };
    
    const clearForm = () => {
        email.value = '';
        username.value = '';
        password.value = '';
        confirmPassword.value = '';
    };
    
    // Watch for typing to clear errors automatically (UX Improvement)
    watch([email, username, password, confirmPassword], () => {
        if (errorMessage.value) errorMessage.value = '';
    });
    
    const submitHandler = async () => {
      errorMessage.value = ''; // Reset error
    
      // 1. Client-Side Validation
      if (!email.value || !password.value) {
          errorMessage.value = "Please fill in all required fields.";
          return;
      }
    
      if (!isSignInMode.value) {
          // Sign Up Validation
          if (!username.value) {
              errorMessage.value = "Username is required.";
              return;
          }
          if (password.value !== confirmPassword.value) {
              errorMessage.value = "Passwords do not match.";
              return;
          }
          if (password.value.length < 6) {
              errorMessage.value = "Password must be at least 6 characters.";
              return;
          }
      }
    
      // 2. API Interaction
      try {
        let result;
        if (!isSignInMode.value) {
          result = await userStore.signUp(email.value, password.value, username.value);
        } else {
          result = await userStore.signIn(email.value, password.value);
        }
    
        if (result && result.success) {
          if (!isSignInMode.value) {
            isSignedUp.value = true;
            startTypewriter("Verify your email");
          } else {
            router.push('/');
          }
        } else {
          // 3. Handle Backend Errors (e.g., "User already exists")
          // Assuming result.error returns a string message
          errorMessage.value = result?.error || "An unexpected error occurred. Please try again.";
        }
      } catch (error) {
        console.log('Error:', error);
        errorMessage.value = "Network error. Please check your connection.";
      }
    };
    
    const resetToLogin = () => {
        isSignedUp.value = false;
        isSignInMode.value = true;
        clearForm();
        errorMessage.value = '';
        startTypewriter("Sign In to Itinero");
    };
    
    onMounted(() => {
      setTimeout(() => startTypewriter("Sign In to Itinero"), 600);
    });
    
    onUnmounted(() => {
      if (animationTimeout) clearTimeout(animationTimeout);
    });
    </script>
    
    <template>
      <section class="h-full md:h-[100dvh] w-screen flex bg-gradient-to-tr from-purple-300 via-purple-100 to-white overflow-hidden font-['Inter']">
        <div class="w-full lg:w-1/2 flex flex-col justify-center items-start p-4 md:pl-25 lg:pl-40 pr-8 relative">
          <div class="w-full max-w-md flex flex-col gap-6">
            
            <div class="animate-enter" style="--delay: 0s">
              <h1 class="min-h-[120px] md:min-h-[60px] text-5xl font-extrabold tracking-tight leading-tight pb-2 bg-gradient-to-r from-purple-700 via-purple-600 to-indigo-500 bg-clip-text text-transparent drop-shadow-sm">
                {{ displayedText }}<span class="blinking-cursor text-purple-600">|</span>
              </h1>
              <p v-if="!isSignedUp" class="text-surface-600 font-medium italic">Please enter your details to continue.</p>
            </div>
    
            <div v-if="errorMessage" class="animate-shake card bg-white flex items-start gap-3 mb-2">
                <i class="pi pi-exclamation-circle text-red-500 text-xl mt-0.5"></i>
                <div class="flex-1">
                    <p class="text-sm font-bold text-red-700">Action Failed</p>
                    <p class="text-sm text-red-600">{{ errorMessage }}</p>
                </div>
                <button @click="errorMessage = ''" class="text-red-400 hover:text-red-600">
                    <i class="pi pi-times"></i>
                </button>
            </div>
    
            <div v-if="!isSignedUp" class="flex flex-col gap-8 animate-enter" style="--delay: 0.1s">
              <div class="flex flex-col gap-6">
                
                <FloatLabel v-if="!isSignInMode">
                  <InputText id="Username" v-model="username" class="field-input w-full !rounded-xl !py-3 !bg-white/60 backdrop-blur-sm !border-surface-300" fluid />
                  <label for="Username" class="text-surface-500">Username</label>
                </FloatLabel>
    
                <FloatLabel>
                  <InputText id="Email" v-model="email" type="email" class="field-input w-full !rounded-xl !py-3 !bg-white/60 backdrop-blur-sm !border-surface-300" fluid />
                  <label for="Email" class="text-surface-500">Email</label>
                </FloatLabel>
    
                <FloatLabel>
                  <InputText id="Password" v-model="password" type="password" class="field-input w-full !rounded-xl !py-3 !bg-white/60 backdrop-blur-sm !border-surface-300" fluid />
                  <label for="Password" class="text-surface-500">Password</label>
                </FloatLabel>
    
                <FloatLabel v-if="!isSignInMode">
                  <InputText 
                    id="ConfirmPassword" 
                    v-model="confirmPassword" 
                    type="password" 
                    class="field-input w-full !rounded-xl !py-3 !bg-white/60 backdrop-blur-sm !border-surface-300"
                    :class="{'!border-red-300 !bg-red-50': confirmPassword && password !== confirmPassword}" 
                    fluid 
                  />
                  <label for="ConfirmPassword" class="text-surface-500">Confirm Password</label>
                </FloatLabel>
              </div>
    
              <div class="flex flex-col gap-4">
                <Button :label="isSignInMode ? 'Sign In' : 'Create Account'" class="interactive-btn-primary" fluid @click="submitHandler" />
                <Button 
                    :label="isSignInMode ? 'Create new account' : 'Sign In to Existing Account'" 
                    severity="secondary" 
                    class="interactive-btn-secondary !bg-white/80 backdrop-blur-md !text-surface-600 !border-transparent !font-semibold !rounded-xl !py-3.5 hover:!bg-white hover:!text-purple-700 hover:shadow-md" 
                    fluid 
                    @click="toggleAccountMode" 
                />
              </div>
            </div>
    
            <div v-else class="flex flex-col gap-6 animate-enter bg-white/40 p-8 rounded-3xl border border-white/50 shadow-xl backdrop-blur-md" style="--delay: 0.1s">
              <div class="flex flex-col gap-2">
                <p class="text-xl text-surface-800 font-semibold text-center">We've sent a link to:</p>
                <p class="text-lg text-purple-700 font-bold text-center underline italic">{{ email }}</p>
              </div>
              <p class="text-surface-600 text-center leading-relaxed">
                Please check your inbox (and spam folder) to activate your Itinero account.
              </p>
              <Button 
                label="Return to Sign In" 
                icon="pi pi-arrow-left" 
                class="mt-4 !bg-purple-600 hover:!bg-purple-700 !rounded-xl !border-none" 
                fluid 
                @click="resetToLogin" 
              />
            </div>
    
          </div>
        </div>
    
        <div class="hidden lg:block h-full w-1/2 p-4 image-hover-trigger">
          <div class="animate-image-enter h-full w-full rounded-[2rem] overflow-hidden shadow-2xl relative">
            <div class="interactive-bg-image h-full w-full bg-[url('@/assets/imgs/DSC_0368.jpg')] bg-cover bg-center">
              <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
            </div>
          </div>
        </div>
      </section>
    </template>
    
    <style scoped>
    .blinking-cursor {
      animation: blink 1s step-end infinite;
    }
    
    @keyframes blink {
      from, to { opacity: 1; }
      50% { opacity: 0; }
    }
    
    .animate-enter {
      animation: slideUp 0.5s ease-out forwards;
      opacity: 0;
      transform: translateY(10px);
    }
    
    /* Shake animation for error card */
    .animate-shake {
        animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
    }
    
    @keyframes shake {
      10%, 90% { transform: translate3d(-1px, 0, 0); }
      20%, 80% { transform: translate3d(2px, 0, 0); }
      30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
      40%, 60% { transform: translate3d(4px, 0, 0); }
    }
    
    @keyframes slideUp {
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    </style>