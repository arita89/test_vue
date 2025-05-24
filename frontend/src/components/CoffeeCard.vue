
<template>
  <v-card class="ma-4" max-width="344">
    <v-img :src="image" height="200px" />
    <v-card-title>{{ title }}</v-card-title>
    <v-card-subtitle>{{ subtitle }}</v-card-subtitle>
    <v-card-actions>
      <v-btn @click="$emit('brew')">Brew</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
defineProps(["title", "subtitle", "image"])
defineEmits(["brew"])
</script>
