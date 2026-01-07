<script setup>
  import { ref, onMounted, onUnmounted, watch } from 'vue';
  import FloatLabel from 'primevue/floatlabel';
  import InputText from 'primevue/inputtext';
  import Button from 'primevue/button';
  import Password from 'primevue/password';
  import Checkbox from 'primevue/checkbox'; // NEW IMPORT
  import Dialog from 'primevue/dialog';     // NEW IMPORT
  
  import { useUserStore } from '@/store/userStore';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const userStore = useUserStore();

  import { useToastStore } from '@/store/toastStore';
  const toastStore = useToastStore();
  
  // --- STATE ---
  const displayedText = ref('');
  const isSignInMode = ref(true);
  const isSignedUp = ref(false);
  const isLoading = ref(false);
  const isForgotPasswordMode = ref(false);
  const resetEmailSent = ref(false);
  let animationTimeout = null;
  
  // Terms & Conditions State
  const acceptedTerms = ref(false);
  const showTermsDialog = ref(false);

  // Form Fields
  const email = ref('');
  const username = ref('');
  const password = ref('');
  const confirmPassword = ref('');
  
  // Error Handling
  const errorMessage = ref('');
  
  // --- MODES & UI ---
  
  const toggleForgotPassword = () => {
      errorMessage.value = '';
      isForgotPasswordMode.value = !isForgotPasswordMode.value;
      resetEmailSent.value = false;
      
      // Update header text based on mode
      if (isForgotPasswordMode.value) {
          startTypewriter("Reset Password");
      } else {
          startTypewriter("Sign In to Itinero");
      }
  };
  
  const toggleAccountMode = () => {
      errorMessage.value = '';
      isSignInMode.value = !isSignInMode.value;
      // Ensure we aren't in forgot password mode if switching between Sign In/Up
      isForgotPasswordMode.value = false; 
      
      // Reset Terms
      acceptedTerms.value = false;

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

  // --- TERMS LOGIC ---
  const openTermsDialog = () => {
    showTermsDialog.value = true;
  };

  const acceptTerms = () => {
    acceptedTerms.value = true;
    showTermsDialog.value = false;
  };
  
  // --- VALIDATION LOGIC ---
  
  const validateEmail = (email) => {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };
  
  const validateUsername = (user) => {
      if (/\s/.test(user)) return { valid: false, msg: "Username cannot contain spaces." };
      if (user.length < 3 || user.length > 25) return { valid: false, msg: "Username must be between 3 and 25 characters." };
      if (!/^[a-zA-Z0-9_]+$/.test(user)) return { valid: false, msg: "Username can only contain letters, numbers, and underscores." };
      return { valid: true };
  };
  
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
  
  // --- API ACTIONS ---
  
  const handlePasswordReset = async () => {
      const payloadEmail = email.value.trim();
  
      if (!payloadEmail) {
          errorMessage.value = "Please enter your email address.";
          return;
      }
      
      if (!validateEmail(payloadEmail)) {
           errorMessage.value = "Please enter a valid email address.";
           return;
      }
  
      isLoading.value = true;
      errorMessage.value = '';
  
      const result = await userStore.resetPassword(payloadEmail);
  
      isLoading.value = false;
  
      if (result.success) {
          resetEmailSent.value = true;
      } else {
          errorMessage.value = result.error;
      }
  };
  
  const submitHandler = async () => {
      if (isLoading.value) return; 
      errorMessage.value = '';
  
      if (isForgotPasswordMode.value) {
          await handlePasswordReset();
          return;
      }
      
      const payloadEmail = email.value.trim();
      const payloadUsername = username.value.trim();
      const payloadPassword = password.value; 
  
      // 1. Basic Fields Check (Email is always required)
      if (!payloadEmail) {
          errorMessage.value = "Email is required.";
          return;
      }
      if (!validateEmail(payloadEmail)) {
          errorMessage.value = "Please enter a valid email address.";
          return;
      }
  
      // 2. Sign In Validation
      if (isSignInMode.value) {
          if (!payloadPassword) {
              errorMessage.value = "Password is required.";
              return;
          }
      }
  
      // 3. Sign Up Validation
      if (!isSignInMode.value) {
          // --- NEW: Terms Check ---
          if (!acceptedTerms.value) {
            errorMessage.value = "You must read and accept the Terms & Conditions to continue.";
            return;
          }

          if (!payloadPassword) {
              errorMessage.value = "Password is required.";
              return;
          }
          if (!payloadUsername) {
              errorMessage.value = "Username is required.";
              return;
          }
  
          const userCheck = validateUsername(payloadUsername);
          if (!userCheck.valid) {
              errorMessage.value = userCheck.msg;
              return;
          }
  
          const passCheck = validatePassword(payloadPassword);
          if (!passCheck.valid) {
              errorMessage.value = passCheck.msg;
              return;
          }
  
          if (payloadPassword !== confirmPassword.value) {
              errorMessage.value = "Passwords do not match.";
              return;
          }
      }
  
      // 4. API Interaction
      try {
          isLoading.value = true;
          let result;
          
          if (!isSignInMode.value) {
              result = await userStore.signUp(payloadEmail, payloadPassword, payloadUsername);
          } else {
              result = await userStore.signIn(payloadEmail, payloadPassword);
          }
  
          if (result && result.success) {
              if (!isSignInMode.value) {
                  isSignedUp.value = true;
                  startTypewriter("Verify your email");
              } else {
                toastStore.trigger({
                    severity: 'success',
                    summary: 'Success',
                    detail: 'Signed-In Successfully!',
                    life: 3000
                });
                  router.push('/');
              }
          } else {
              errorMessage.value = result?.error || "Invalid credentials or server error.";
          }
      } catch (error) {
          console.error('Submission Error:', error);
          errorMessage.value = "Unable to connect to server. Please try again later.";
      } finally {
          isLoading.value = false;
      }
  };
  
  const resetToLogin = () => {
      isSignedUp.value = false;
      isSignInMode.value = true;
      clearForm();
      errorMessage.value = '';
      startTypewriter("Sign In to Itinero");
  };
  
  // --- ANIMATION UTILS ---
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
  
  watch([email, username, password, confirmPassword], () => {
      if (errorMessage.value) errorMessage.value = '';
  });
  
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
                      <p v-if="!isSignedUp && !resetEmailSent" class="text-surface-600 font-medium italic">Please enter your details to continue.</p>
                  </div>
  
                  <div v-if="errorMessage" class="animate-shake card bg-white flex items-start gap-3 mb-2 p-3 rounded-xl shadow-sm border border-red-100">
                      <i class="pi pi-exclamation-circle text-red-500 text-xl mt-0.5"></i>
                      <div class="flex-1">
                          <p class="text-sm font-bold text-red-700">Action Failed</p>
                          <p class="text-sm text-red-600 leading-tight">{{ errorMessage }}</p>
                      </div>
                      <button @click="errorMessage = ''" class="text-red-400 hover:text-red-600">
                          <i class="pi pi-times"></i>
                      </button>
                  </div>
  
                  <div v-if="!isSignedUp && !resetEmailSent" class="flex flex-col gap-8 animate-enter" style="--delay: 0.1s">
                      <div class="flex flex-col gap-6">
  
                          <FloatLabel v-if="!isSignInMode && !isForgotPasswordMode">
                              <InputText 
                                  id="Username" 
                                  v-model="username" 
                                  :disabled="isLoading"
                                  class="field-input w-full !rounded-xl !py-3 !bg-white/60 backdrop-blur-sm !border-surface-300" 
                                  fluid 
                              />
                              <label for="Username" class="text-surface-500">Username</label>
                          </FloatLabel>
  
                          <FloatLabel>
                              <InputText 
                                  id="Email" 
                                  v-model="email" 
                                  type="email" 
                                  :disabled="isLoading"
                                  class="field-input w-full !rounded-xl !py-3 !bg-white/60 backdrop-blur-sm !border-surface-300" 
                                  fluid 
                              />
                              <label for="Email" class="text-surface-500">Email</label>
                          </FloatLabel>
  
                          <FloatLabel v-if="!isForgotPasswordMode">
                              <Password 
                                  id="Password" 
                                  v-model="password" 
                                  :feedback="!isSignInMode" 
                                  :toggleMask="true"
                                  :disabled="isLoading"
                                  inputClass="w-full !rounded-xl !py-3 !bg-white/60 backdrop-blur-sm !border-surface-300" 
                                  class="w-full"
                              >
                                  <template #header>
                                      <div class="font-semibold text-sm mb-2">Pick a password</div>
                                  </template>
                                  <template #footer>
                                      <div class="border-t border-gray-300 mt-2 pt-2">
                                          <p class="mt-2 text-xs">Suggestions</p>
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
                              <label for="Password" class="text-surface-500">Password</label>
                          </FloatLabel>
  
                          <FloatLabel v-if="!isSignInMode && !isForgotPasswordMode">
                              <Password 
                                  id="ConfirmPassword" 
                                  v-model="confirmPassword" 
                                  :feedback="false"
                                  :disabled="isLoading"
                                  inputClass="w-full !rounded-xl !py-3 !bg-white/60 backdrop-blur-sm !border-surface-300"
                                  :class="{'!border-red-300 !bg-red-50': confirmPassword && password !== confirmPassword}" 
                                  class="w-full"
                              />
                              <label for="ConfirmPassword" class="text-surface-500">Confirm Password</label>
                          </FloatLabel>
                      </div>

                      <div v-if="!isSignInMode && !isForgotPasswordMode" class="flex items-start gap-3 px-1">
                        <div class="pt-0.5">
                            <Checkbox v-model="acceptedTerms" :binary="true" inputId="acceptTerms" :readonly="true" class="pointer-events-none" /> 
                        </div>
                        <label for="acceptTerms" class="text-sm text-surface-600 leading-snug">
                            I have read and agree to the 
                            <span @click="openTermsDialog" class="text-purple-600 font-bold cursor-pointer hover:underline">Terms & Conditions</span>
                            and Privacy Policy.
                        </label>
                      </div>
  
                      <div v-if="isSignInMode && !isForgotPasswordMode" class="flex justify-end -mt-4 mb-4">
                          <button 
                              @click="toggleForgotPassword" 
                              class="text-sm font-semibold text-purple-600 hover:text-purple-800 hover:underline transition-colors cursor-pointer"
                          >
                              Forgot Password?
                          </button>
                      </div>
  
                      <div v-if="isForgotPasswordMode" class="flex justify-start -mt-4 mb-4">
                          <button 
                              @click="toggleForgotPassword" 
                              class="text-sm font-semibold text-gray-500 hover:text-gray-700 hover:underline flex items-center gap-1 transition-colors cursor-pointer"
                          >
                              <i class="pi pi-arrow-left text-xs"></i> Back to Sign In
                          </button>
                      </div>
  
                      <div class="flex flex-col gap-4">
                          <Button 
                              :label="isLoading ? 'Processing...' : (isForgotPasswordMode ? 'Send Reset Link' : (isSignInMode ? 'Sign In' : 'Create Account'))" 
                              :loading="isLoading"
                              class="interactive-btn-primary" 
                              fluid 
                              @click="submitHandler" 
                          />
                          <Button 
                              v-if="!isForgotPasswordMode"
                              :label="isSignInMode ? 'Create new account' : 'Sign In to Existing Account'" 
                              severity="secondary" 
                              :disabled="isLoading"
                              class="interactive-btn-secondary !bg-white/80 backdrop-blur-md !text-surface-600 !border-transparent !font-semibold !rounded-xl !py-3.5 hover:!bg-white hover:!text-purple-700 hover:shadow-md" 
                              fluid 
                              @click="toggleAccountMode" 
                          />
  
                          <Button label="Continue Without Registration" class="bg-transparent! border-0! text-primary! mt-5" @click="router.push('/Create')"/>
                      </div>
                  </div>
  
                  <div v-else-if="resetEmailSent" class="flex flex-col gap-6 animate-enter card bg-white backdrop-blur-md">
                      <div class="text-center">
                          <i class="pi pi-check-circle text-4xl text-green-500 mb-3"></i>
                          <h3 class="text-xl font-bold text-surface-800">Check your email</h3>
                      </div>
                      <p class="text-surface-600 text-center leading-relaxed">
                          We've sent password reset instructions to <span class="font-bold text-purple-700">{{ email }}</span>.
                      </p>
                      <Button 
                          label="Return to Sign In" 
                          class="mt-4 !bg-purple-600 hover:!bg-purple-700 !rounded-xl" 
                          fluid 
                          @click="toggleForgotPassword" 
                      />
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

          <Dialog v-model:visible="showTermsDialog" modal header="Terms and Conditions" :style="{ width: '50rem' }" :breakpoints="{ '1199px': '75vw', '575px': '90vw' }">
            <div class="h-[400px] overflow-y-auto pr-4 text-sm text-surface-600 leading-relaxed text-justify">
                <h3 class="font-bold text-lg mb-2 text-surface-900">1. Introduction</h3>
                <p class="mb-4">Welcome to Itinero. By creating an account, you agree to comply with and be bound by the following terms and conditions of use.</p>
                
                <h3 class="font-bold text-lg mb-2 text-surface-900">2. Privacy Policy</h3>
                <p class="mb-4">We respect your privacy. We collect your email and username solely for the purpose of account management and itinerary generation. We do not sell your data to third parties.</p>
                
                <h3 class="font-bold text-lg mb-2 text-surface-900">3. User Conduct</h3>
                <p class="mb-4">You agree not to use this service for any unlawful purpose. You are responsible for maintaining the confidentiality of your account and password.</p>

                <h3 class="font-bold text-lg mb-2 text-surface-900">4. Liability</h3>
                <p class="mb-4">Itinero provides travel recommendations based on available data. We are not responsible for closed establishments, incorrect timings, or any issues arising from your trip.</p>
                
                <h3 class="font-bold text-lg mb-2 text-surface-900">5. Termination</h3>
                <p class="mb-4">We reserve the right to terminate accounts that violate these terms without prior notice.</p>
                
                <p class="italic text-xs mt-8">Last updated: January 2026</p>
            </div>
            <template #footer>
                <Button label="Cancel" text severity="secondary" @click="showTermsDialog = false" />
                <Button label="I Read and Accept" icon="pi pi-check" @click="acceptTerms" class="interactive-btn-primary" />
            </template>
        </Dialog>

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
      to { opacity: 1; transform: translateY(0); }
  }
  </style>