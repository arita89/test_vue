<template>
    <v-container>
        <h2 class="mb-4">Image Gallery</h2>

        <!-- Upload Section -->
        <v-file-input v-model="uploadFiles" label="Add image(s) to gallery" accept="image/*" multiple
            prepend-icon="mdi-upload" />
        <v-btn @click="uploadImages" color="primary" class="mb-6">Upload</v-btn>

        <!-- Image Grid -->
        <v-row>
            <v-col cols="4" v-for="(img, i) in images" :key="i">
                <v-img :src="img" @click="showImage(i)" class="cursor-pointer" />
            </v-col>
        </v-row>

        <!-- Lightbox -->
        <vue-easy-lightbox :visible="visible" :imgs="images" :index="index" @hide="visible = false" />
    </v-container>
</template>


<script setup>
import VueEasyLightbox from 'vue-easy-lightbox'
import { ref, onMounted } from 'vue'

const images = ref([])
const visible = ref(false)
const index = ref(0)
const uploadFiles = ref([])

const fetchGallery = async () => {
    const res = await fetch('http://localhost:8000/gallery')
    images.value = await res.json()
}

onMounted(fetchGallery)

const showImage = i => {
    index.value = i
    visible.value = true
}

const uploadImages = async () => {
    if (!uploadFiles.value.length) return

    const formData = new FormData()
    uploadFiles.value.forEach(file => {
        formData.append('images', file)
    })

    await fetch('http://localhost:8000/gallery/upload', {
        method: 'POST',
        body: formData,
    })

    uploadFiles.value = []
    await fetchGallery()
}
</script>
