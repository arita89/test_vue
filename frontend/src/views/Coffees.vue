
<template>
  <v-container>
    <h2>Select a Coffee</h2>
    <v-select :items="coffees" item-title="name" v-model="selected" label="Choose coffee" />
    <v-btn @click="brew">Brew it</v-btn>
    <v-alert v-if="instructions" type="success">{{ instructions }}</v-alert>
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
  const res = await fetch(`http://localhost:8000/brew/${selected.value.id}`)
  const data = await res.json()
  instructions.value = data.instructions
}
</script>
