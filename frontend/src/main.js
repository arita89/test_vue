
import { createApp } from 'vue'
import App from './App.vue'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import { createRouter, createWebHistory } from 'vue-router'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import Home from './views/Home.vue'
import Coffees from './views/Coffees.vue'

const vuetify = createVuetify({ components, directives })

const routes = [
  { path: '/', component: Home },
  { path: '/coffees', component: Coffees }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App).use(router).use(vuetify).mount('#app')
