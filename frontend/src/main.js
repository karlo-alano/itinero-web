import { createApp } from 'vue'
import App from './App.vue'
import './assets/styles.css';
import router from './router'


// PrimeVue
import PrimeVue from 'primevue/config';
import { definePreset } from '@primeuix/themes';
import Aura from '@primeuix/themes/aura';

//PrimeVue components
import Button from 'primevue/button';
import Avatar from 'primevue/avatar';


//pinia
import { createPinia } from 'pinia';
const pinia = createPinia(); 

//Theme
const itineroTheme = definePreset(Aura, {
    semantic: {
        primary: {
            50: ' #CCAAEE',
            100: ' #C298EB',
            200: ' #AD76E4',
            300: '#9954DD',
            400: '#8432D6',
            500: '#7025BB',
            600: '#541C8C',
            700: '#38125D',
            800: '#1C092E',
            900: '#000000',
            950: '#000000'
        },
        secondary: {
            50: ' #7E7E7E',
            100: ' #747474',
            200: ' #5F5F5F',
            300: '#4B4B4B',
            400: '#363636',
            500: '#222222',
            600: '#060606',
            700: '#000000',
            800: '#000000',
            900: '#000000',
            950: '#000000'
        },
        text: {
            primary: '#ffffff',
            secondary: '#000000'
        },
        colorScheme: {
            light: {
                surface: {
                    0: '#ffffff',
                    50: '{zinc.50}',
                    100: '{zinc.100}',
                    200: '{zinc.200}',
                    300: '{zinc.300}',
                    400: '{zinc.400}',
                    500: '{zinc.500}',
                    600: '{zinc.600}',
                    700: '{zinc.700}',
                    800: '{zinc.800}',
                    900: '{zinc.900}',
                    950: '{zinc.950}'
                }
            },
            dark: {
                surface: {
                    0: '#ffffff',
                    50: '{slate.50}',
                    100: '{slate.100}',
                    200: '{slate.200}',
                    300: '{slate.300}',
                    400: '{slate.400}',
                    500: '{slate.500}',
                    600: '{slate.600}',
                    700: '{slate.700}',
                    800: '{slate.800}',
                    900: '{slate.900}',
                    950: '{slate.950}'
                }
            }
        }    
    }
});


const app = createApp(App)
app.use(pinia)
app.component('Button', Button)
app.component('Avatar', Avatar)
app.use(router)
app.use(PrimeVue, {
    ripple: true,
    theme: {
        preset: itineroTheme,
        options: {
            //CHANGE THIS WHEN YOU HAVE A TOGGLE FOR DARK/LIGHT
            darkModeSelector: false,
            cssLayer: {
                name: 'primevue',
                order: 'theme, base, primevue'
            }
        }
        
    }
});



app.mount('#app')


