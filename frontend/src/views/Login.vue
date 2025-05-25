<template>
  <v-container>
    <h2>Login</h2>
    <v-text-field v-model="username" label="Username" />
    <v-text-field v-model="password" label="Password" type="password" />
    <v-btn @click="login" color="primary">Login</v-btn>
    <v-alert v-if="error" type="error" class="mt-2">{{ error }}</v-alert>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { auth } from '../services/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const login = async () => {
  error.value = ''
  const res = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: username.value, password: password.value })
  })

  if (res.ok) {
    const data = await res.json()
    auth.setToken(data.access_token)
    router.push('/')
  } else {
    error.value = 'Login failed'
  }
}
</script>
