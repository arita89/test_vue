<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useTheme } from 'vuetify'
import { useRouter } from 'vue-router'
import { auth } from './services/auth'

const theme = useTheme()
const router = useRouter()
const isDark = ref(false)

onMounted(() => {
  auth.fetchUser()
  const saved = localStorage.getItem('theme')
  isDark.value = saved === 'dark'
  theme.global.name.value = isDark.value ? 'dark' : 'coffee'
})

watch(isDark, (val) => {
  theme.global.name.value = val ? 'dark' : 'coffee'
  localStorage.setItem('theme', val ? 'dark' : 'coffee')
})

const isAuthenticated = auth.isAuthenticated
//const username = auth.getUser
// const username = computed(() => auth.getUser || '')

const username = computed(() => auth.getUser.value?.username || '')


const logout = () => {
  auth.clearToken()
  router.push('/login')
}
</script>

<template>
  <v-app>
    <!-- Sidebar Navigation -->
    <v-navigation-drawer app permanent>
      <v-list>
        <v-list-item to="/">
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item>
        <v-list-item to="/coffees">
          <v-list-item-title>Coffees</v-list-item-title>
        </v-list-item>
        <v-list-item to="/map">
          <v-list-item-title>Map</v-list-item-title>
        </v-list-item>
        <template v-if="isAuthenticated">
          <v-list-item to="/upload">
            <v-list-item-title>Upload Recipe</v-list-item-title>
          </v-list-item>
          <v-list-item to="/gallery">
            <v-list-item-title>Gallery</v-list-item-title>
          </v-list-item>
        </template>
        <v-list-item to="/contact">
          <v-list-item-title>Contact</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <transition name="fade" mode="out-in">
        <router-view />
      </transition>
    </v-main>

    <!-- Footer -->
    <v-footer app>
      <v-container class="d-flex justify-space-between align-center">
        <div>
          <span>© 2025 CoffeeTime</span>
          <template v-if="isAuthenticated">
            <span class="ml-3">👤 {{ username }}</span>
            <v-btn text size="small" class="ml-2" @click="logout">Logout</v-btn>
          </template>
          <template v-else>
            <v-btn text size="small" class="ml-2" to="/login">Login</v-btn>
          </template>
        </div>
        <v-switch
          v-model="isDark"
          inset
          color="primary"
          :label="isDark ? '🌙 Dark Mode' : '☕ Coffee Mode'"
        />
      </v-container>
    </v-footer>
  </v-app>
</template>
