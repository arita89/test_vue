<template>
    <v-container>
        <h2>Create a New Coffee Recipe</h2>

        <v-form @submit.prevent="submitForm" class="mt-4" ref="formRef">
            <v-text-field v-model="form.name" label="Name" required />
            <v-textarea v-model="form.description" label="Description" required />

            <v-file-input v-model="images" label="Add optional image(s)" multiple show-size prepend-icon="mdi-camera" />

            <v-btn type="submit" color="primary" class="mt-4">Submit</v-btn>
        </v-form>

        <v-alert v-if="success" type="success" class="mt-4">
            Coffee recipe created!
        </v-alert>
    </v-container>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
    name: '',
    description: ''
})
const images = ref([])
const success = ref(false)
const formRef = ref(null)

const submitForm = async () => {
    const fd = new FormData()
    fd.append('name', form.value.name)
    fd.append('description', form.value.description)
    for (let i = 0; i < images.value.length; i++) {
        fd.append('images', images.value[i])
    }

    const res = await fetch('http://localhost:8000/recipes', {
        method: 'POST',
        body: fd
    })

    if (res.ok) {
        success.value = true
        form.value.name = ''
        form.value.description = ''
        images.value = []
        formRef.value.resetValidation?.()
    }
}
</script>