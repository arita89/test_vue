<template>
  <v-container>

    <!-- Dynamic Image Carousel -->
    <v-carousel cycle hide-delimiter-background height="300" class="mb-10">
      <v-carousel-item v-for="(img, i) in coffeeImages" :key="i" :src="img">
        <!-- Text over carousel
          <v-row class="fill-height" align="center" justify="center">
          <h2 class="text-white">Coffee Moment {{ i + 1 }}</h2>
        </v-row>
      -->
      </v-carousel-item>
    </v-carousel>

    <!-- Dropdown + Brew Button -->
    <h2>Select a Coffee</h2>
    <v-select :items="coffees" item-title="name" item-value="id" v-model="selected" label="Choose coffee" />
    <v-btn @click="brew" class="mt-2">BREW IT</v-btn>

    <v-alert v-if="instructions" ref="instructionsRef" type="info" class="mt-4 scroll-target">
      {{ instructions }}
    </v-alert>

  </v-container>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

// Dynamically load all carousel images from assets/carousel/
const imageModules = import.meta.glob('./../assets/carousel/*.{png,jpg,jpeg}', { eager: true })
const coffeeImages = Object.values(imageModules).map(mod => mod.default)

const coffees = ref([])
const selected = ref(null)
const instructions = ref("")
const instructionsRef = ref(null)

onMounted(async () => {
  const res = await fetch("http://localhost:8000/coffees")
  coffees.value = await res.json()
})

const brew = async () => {
  if (!selected.value) return
  const res = await fetch(`http://localhost:8000/coffees/brew/${selected.value}`)
  const data = await res.json()
  instructions.value = data.instructions

  await nextTick()
  const el = instructionsRef.value?.$el || instructionsRef.value?.$?.vnode?.el
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    el.classList.add('highlight')
    setTimeout(() => el.classList.remove('highlight'), 1000)
  }
}
</script>

<style scoped>
.highlight {
  animation: pulse 1s ease-out;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0px rgba(0, 150, 255, 0.8);
  }

  50% {
    box-shadow: 0 0 20px rgba(0, 150, 255, 0.8);
  }

  100% {
    box-shadow: 0 0 0px rgba(0, 150, 255, 0.8);
  }
}
</style>
