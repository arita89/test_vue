<template>
  <v-container>
    <h2>Create a New Coffee Recipe</h2>

    <v-form @submit.prevent="submitForm" class="mt-4" ref="formRef">
      <v-text-field v-model="form.name" label="Name" required />
      <v-textarea v-model="form.description" label="Description" required />

      <v-file-input
        v-model="images"
        label="Add optional image(s)"
        multiple
        show-size
        prepend-icon="mdi-camera"
      />

      <v-btn type="submit" color="primary" class="mt-4">Submit</v-btn>
    </v-form>

    <v-snackbar v-model="snackbar.visible" :timeout="3000" location="top right">
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { auth } from '../services/auth'

const form = ref({
  name: '',
  description: ''
})
const images = ref([])
const formRef = ref(null)

const snackbar = ref({
  visible: false,
  message: ''
})

const showSnackbar = (msg) => {
  snackbar.value.message = msg
  snackbar.value.visible = true
}

const submitForm = async () => {
  snackbar.value.visible = false

  const fd = new FormData()
  fd.append('name', form.value.name)
  fd.append('description', form.value.description)
  for (let i = 0; i < images.value.length; i++) {
    fd.append('images', images.value[i])
  }

  try {
    const res = await fetch('http://localhost:8000/recipes', {
      method: 'POST',
      headers: {
            Authorization: `Bearer ${auth.getToken()}`
        },
      body: fd
    })

    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.detail || 'Upload failed')
    }

    showSnackbar('✅ Recipe created successfully!')
    form.value.name = ''
    form.value.description = ''
    images.value = []
    formRef.value?.resetValidation?.()
  } catch (e) {
    showSnackbar('❌ ' + e.message)
  }
}
</script>
