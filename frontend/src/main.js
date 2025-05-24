
import { createApp } from 'vue'
import App from './App.vue'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import { createRouter, createWebHistory } from 'vue-router'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import Home from './views/Home.vue'
import Coffees from './views/Coffees.vue'
import UploadRecipe from './views/UploadRecipe.vue'
import Contact from './views/Contact.vue'

const vuetify = createVuetify({ components, directives })

const routes = [
  { path: '/', component: Home },
  { path: '/coffees', component: Coffees },
  { path: '/upload', component: UploadRecipe },
  { path: '/contact', component: Contact },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App).use(router).use(vuetify).mount('#app')
