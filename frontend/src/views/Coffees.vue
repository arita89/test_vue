<template>
  <v-container>

    <!-- Carousel on top -->
    <v-carousel cycle hide-delimiter-background height="300" class="mb-10">
      <v-carousel-item v-for="(coffee, i) in coffees" :key="i" :src="coffee.image">
        <v-row class="fill-height" align="center" justify="center">
          <h2 class="text-white">{{ coffee.name }}</h2>
        </v-row>
      </v-carousel-item>
    </v-carousel>

    <!-- Heading and dropdown -->
    <h2>Select a Coffee</h2>

    <v-select :items="coffees" item-title="name" item-value="id" v-model="selected" label="Choose coffee" />

    <v-btn @click="brew" class="mt-2">BREW IT</v-btn>

    <!-- Brew instructions + scroll target -->
    <v-alert v-if="instructions" ref="instructionsRef" type="info" class="mt-4 scroll-target">
      {{ instructions }}
    </v-alert>

  </v-container>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

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

  const res = await fetch(`http://localhost:8000/brew/${selected.value}`)
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
