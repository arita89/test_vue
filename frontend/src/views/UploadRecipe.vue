<template>
    <v-container>
        <h2>Upload Your Coffee Recipe</h2>

        <v-form @submit.prevent="upload" class="mt-4">
            <v-file-input label="Choose file" v-model="file" accept=".txt,.md,.json,.pdf" :rules="[fileRequired]"
                prepend-icon="mdi-file-upload" />
            <v-btn type="submit" color="primary" class="mt-2">Upload</v-btn>
        </v-form>

        <v-alert v-if="success" type="success" class="mt-4">
            Upload complete!
        </v-alert>
    </v-container>
</template>

<script setup>
import { ref } from 'vue'

const file = ref(null)
const success = ref(false)

const fileRequired = value => !!value || 'Please select a file'

const upload = async () => {
    if (!file.value) return

    const formData = new FormData()
    formData.append('file', file.value)

    const res = await fetch('http://localhost:8000/upload-recipe', {
        method: 'POST',
        body: formData
    })

    if (res.ok) {
        success.value = true
        file.value = null
    }
}
</script>