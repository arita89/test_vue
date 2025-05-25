<template>
  <v-container>
    <LMap :zoom="2" :center="[20, 0]" style="height: 500px">
      <LTileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <LMarker v-for="coffee in coffees" :key="coffee.id" :lat-lng="[coffee.latitude, coffee.longitude]"
        :icon="coffeeIcon">
        <LPopup>{{ coffee.name }} - {{ coffee.location }}</LPopup>
      </LMarker>
      <LMarker v-for="img in galleryImages" :key="'img-' + img.id" :lat-lng="[img.latitude, img.longitude]"
        :icon="getImageIcon()">
        <LPopup>
          <img :src="img.url" alt="photo" style="max-width: 200px; border-radius: 8px;"
            @error="e => e.target.style.display = 'none'" />
          <div class="mt-2">
            <strong>📍 Location:</strong><br />
            {{ img.latitude }}, {{ img.longitude }}
          </div>
        </LPopup>
      </LMarker>
    </LMap>
  </v-container>
</template>

<script setup>
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import { ref, onMounted } from 'vue'
import L from 'leaflet'

const coffees = ref([])

onMounted(async () => {
  const res = await fetch('http://localhost:8000/coffees/map')
  coffees.value = await res.json()
})

const coffeeIcon = new L.Icon({
  iconUrl: '/markers/coffee-cup.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
  shadowSize: [41, 41]
})

const galleryImages = ref([])

onMounted(async () => {
  const [coffeeRes, galleryRes] = await Promise.all([
    fetch('http://localhost:8000/coffees/map'),
    fetch('http://localhost:8000/gallery/map')
  ])

  coffees.value = await coffeeRes.json()
  galleryImages.value = await galleryRes.json()

  console.log("📸 Gallery Images with Locations:", galleryImages.value)
})

const getImageIcon = () =>
  new L.Icon({
    iconUrl: '/markers/photo.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -30],
    shadowSize: [41, 41]
  })

</script>
