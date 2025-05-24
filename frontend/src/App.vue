<script setup>
import { ref, onMounted, watch } from 'vue'
import { useTheme } from 'vuetify'

const theme = useTheme()
const isDark = ref(false)

// Load saved preference on mount
onMounted(() => {
  const saved = localStorage.getItem('theme')
  if (saved === 'dark') {
    isDark.value = true
    theme.global.name.value = 'dark'
  } else {
    isDark.value = false
    theme.global.name.value = 'coffee'
  }
})

// Watch toggle and store preference
watch(isDark, (val) => {
  theme.global.name.value = val ? 'dark' : 'coffee'
  localStorage.setItem('theme', val ? 'dark' : 'coffee')
})
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
        <v-list-item to="/upload">
          <v-list-item-title>Upload Recipe</v-list-item-title>
        </v-list-item>
        <v-list-item to="/map">
          <v-list-item-title>Map</v-list-item-title>
        </v-list-item>
        <v-list-item to="/gallery">
          <v-list-item-title>Gallery</v-list-item-title>
        </v-list-item>
        <v-list-item to="/contact">
          <v-list-item-title>Contact</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <router-view />
    </v-main>

    <!-- Footer with Theme Toggle -->
    <v-footer app>
      <v-container class="d-flex justify-space-between align-center">
        <span>© 2025 CoffeeTime</span>
        <v-switch v-model="isDark" inset color="primary" :label="isDark ? '🌙 Dark Mode' : '☕ Coffee Mode'" />
      </v-container>
    </v-footer>
  </v-app>
</template>
