<template>
  <v-container>
    <h2>Select a Coffee</h2>

    <!-- Dropdown -->
    <v-select :items="coffees" item-title="name" item-value="id" v-model="selected" label="Choose coffee" />

    <!-- Brew Button -->
    <v-btn @click="brew" class="mt-2">BREW IT</v-btn>

    <!-- Brew Instructions -->
    <v-alert v-if="instructions" type="info" class="mt-4">
      {{ instructions }}
    </v-alert>

    <!-- Carousel -->
    <v-carousel cycle hide-delimiter-background height="300" class="mt-10">
      <v-carousel-item v-for="(coffee, i) in coffees" :key="i"
        :src="coffee.image || 'https://via.placeholder.com/600x300?text=' + coffee.name">
        <v-row class="fill-height" align="center" justify="center">
          <h2 class="text-white">{{ coffee.name }}</h2>
        </v-row>
      </v-carousel-item>
    </v-carousel>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const coffees = ref([])
const selected = ref(null)
const instructions = ref("")

onMounted(async () => {
  const res = await fetch("http://localhost:8000/coffees")
  coffees.value = await res.json()
})

const brew = async () => {
  if (!selected.value) return
  const res = await fetch(`http://localhost:8000/brew/${selected.value}`)
  const data = await res.json()
  instructions.value = data.instructions
}
</script>
