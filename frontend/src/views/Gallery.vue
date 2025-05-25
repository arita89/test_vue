<template>
    <v-container>
        <h2 class="mb-4">Image Gallery</h2>

        <!-- Upload Section -->
        <v-file-input v-model="uploadFiles" label="Drop or select images" accept="image/*" multiple show-size
            prepend-icon="mdi-camera" class="mb-6" clearable @change="uploadImages" />

        <!-- <v-btn @click="uploadImages" color="primary" class="mb-6">Upload</v-btn>-->

        <!-- Gallery Grid -->
        <v-row>
            <v-col cols="4" v-for="(img, i) in images" :key="i">
                <v-img :src="img" @click="showImage(i)" class="cursor-pointer" />
            </v-col>
        </v-row>

        <!-- Lightbox -->
        <vue-easy-lightbox :visible="visible" :imgs="images" :index="index" @hide="visible = false" />

        <!-- 📍 Location Confirmation Dialog with Map -->
        <v-dialog v-model="locationDialog" max-width="500">
            <v-card>
                <v-card-title class="headline">Location Found</v-card-title>
                <v-card-text>
                    <div class="mb-4">
                        This image was taken at:<br />
                        <strong>Lat:</strong> {{ gps.latitude }}<br />
                        <strong>Lon:</strong> {{ gps.longitude }}
                    </div>
                    <LMap :zoom="13" :center="[gps.latitude, gps.longitude]" style="height: 250px">
                        <LTileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                        <LMarker :lat-lng="[gps.latitude, gps.longitude]">
                            <LPopup>Photo location</LPopup>
                        </LMarker>
                    </LMap>
                </v-card-text>
                <v-card-actions>
                    <v-spacer />
                    <v-btn color="primary" @click="confirmLocation(true)">Save</v-btn>
                    <v-btn color="secondary" @click="confirmLocation(false)">Discard</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- ✅ Snackbar -->
        <v-snackbar v-model="snackbar.visible" :timeout="3000" location="top">
            {{ snackbar.message }}
        </v-snackbar>
    </v-container>
</template>

<script setup>
import VueEasyLightbox from 'vue-easy-lightbox'
import { ref, onMounted } from 'vue'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import { auth } from '../services/auth'

const images = ref([])
const visible = ref(false)
const index = ref(0)
const uploadFiles = ref([])

const locationDialog = ref(false)
const gps = ref({})
const pendingUploadFile = ref(null)

const snackbar = ref({
    visible: false,
    message: ''
})

const fetchGallery = async () => {
    const res = await fetch('http://localhost:8000/gallery',{
        headers: {
            Authorization: `Bearer ${auth.getToken()}`
        },}
    )
    images.value = await res.json()
}

onMounted(fetchGallery)

const showImage = i => {
    index.value = i
    visible.value = true
}

const uploadImages = async () => {
    if (!uploadFiles.value.length) return

    for (const file of uploadFiles.value) {
        const formData = new FormData()
        formData.append('image', file)

        const res = await fetch('http://localhost:8000/gallery/upload-with-meta', {
            method: 'POST',
            headers: { Authorization: `Bearer ${auth.getToken()}` },
            body: formData,
        })

        const result = await res.json()

        if (result.location) {
            gps.value = result.location
            pendingUploadFile.value = result.filename
            locationDialog.value = true
            // Pause here — wait for user to confirm before continuing
            return
        } else {
            snackbar.value.message = `Uploaded ${file.name} (no location)`
            snackbar.value.visible = true
        }
    }

    uploadFiles.value = []
    await fetchGallery()
}

const confirmLocation = async (useIt) => {
    locationDialog.value = false

    if (useIt) {
        await fetch(`http://localhost:8000/gallery/set-location`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json',Authorization: `Bearer ${auth.getToken()}` },
            body: JSON.stringify({
                filename: pendingUploadFile.value,
                latitude: gps.value.latitude,
                longitude: gps.value.longitude,
            })
        })
    }

    await fetchGallery()
    gps.value = {}
    pendingUploadFile.value = null
}
</script>