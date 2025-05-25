import { createApp } from 'vue'
import App from './App.vue'
import './assets/transitions.css'

import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import 'leaflet/dist/leaflet.css'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Coffees from './views/Coffees.vue'
import UploadRecipe from './views/UploadRecipe.vue'
import Contact from './views/Contact.vue'
import MapView from './views/Map.vue'
import Gallery from './views/Gallery.vue'

// 1️⃣ Custom Coffee Theme
const myCoffeeTheme = {
  dark: false,
  colors: {
    background: '#fdf6f0',
    surface: '#f0e7dd',
    primary: '#8d6e63',
    secondary: '#d7ccc8',
    success: '#a1887f',
    info: '#bcaaa4',
    error: '#5d4037',
  },
}

// 2️⃣ Vuetify setup with theme
const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'coffee',
    themes: {
      coffee: myCoffeeTheme,
      dark: { dark: true }
    }
  }
})

// 3️⃣ Router setup
const routes = [
  { path: '/', component: Home },
  { path: '/coffees', component: Coffees },
  { path: '/upload', component: UploadRecipe },
  { path: '/contact', component: Contact },
  { path: '/map', component: MapView },
  { path: '/gallery', component: Gallery }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 4️⃣ Mount app
createApp(App).use(router).use(vuetify).mount('#app')
