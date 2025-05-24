<template>
    <v-container>
        <h2>Upload Your Coffee Recipe</h2>
        <v-file-input label="Choose file" v-model="file" class="mt-4" />
        <v-btn @click="upload" color="primary" class="mt-2">Upload</v-btn>
        <v-alert v-if="success" type="success" class="mt-4">Upload complete!</v-alert>
    </v-container>
</template>

<script setup>
import { ref } from 'vue'

const file = ref(null)
const success = ref(false)

const upload = async () => {
    if (!file.value) return
    const formData = new FormData()
    formData.append("file", file.value)
    await fetch("http://localhost:8000/upload-recipe", {
        method: "POST",
        body: formData,
    })
    success.value = true
}
</script>