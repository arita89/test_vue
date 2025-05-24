<script setup>
import bgImage from '../assets/family_coffee.png'
</script>

<template>
  <v-container class="home-hero" :style="{ backgroundImage: `url(${bgImage})` }" fluid>
    <div class="overlay animate-fade-in">
      <h1 class="welcome-message">Welcome to the Coffee App</h1>
    </div>
  </v-container>
</template>

<style scoped>
.home-hero {
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 2rem;
}

.overlay {
  background-color: rgba(255, 255, 255, 0.75);
  padding: 2rem 3rem;
  border-radius: 16px;
  text-align: center;
  max-width: 90%;
  width: 100%;
  max-width: 500px;
}

.welcome-message {
  font-size: 2.5rem;
  font-weight: bold;
  color: #4e342e;
}

@keyframes fade-in {
  0% {
    opacity: 0;
    transform: translateY(15px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 1s ease-out;
}
</style>
