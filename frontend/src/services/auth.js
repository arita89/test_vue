import { ref, computed } from 'vue'

const token = ref(localStorage.getItem('authToken') || '')
const user = ref(null)

export const auth = {
    setToken(value) {
        token.value = value
        localStorage.setItem('authToken', value)
    },

    getToken() {
        return token.value
    },

    clearToken() {
        token.value = ''
        user.value = null
        localStorage.removeItem('authToken')
    },

    async fetchUser() {
        if (!token.value) return
        try {
            const res = await fetch('http://localhost:8000/auth/me', {
                headers: {
                    Authorization: `Bearer ${token.value}`,
                },
            })
            if (!res.ok) throw new Error('Invalid token')
            user.value = await res.json()
            console.log('User fetched:', user.value)
        } catch (err) {
            console.error('fetchUser failed:', err)
            this.clearToken()
        }
    },

    isAuthenticated: computed(() => !!token.value),

    getUser: computed(() => user.value),
}
