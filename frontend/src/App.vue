<template>
  <v-app>
    <!-- Sidebar Navigation -->
    <v-navigation-drawer app permanent>
      <v-list>
        <v-list-item to="/">
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item>
        <v-list-item to="/coffees">
          <v-list-item-title>Coffees</v-list-item-title>
        </v-list-item>
        <v-list-item to="/upload">
          <v-list-item-title>Upload Recipe</v-list-item-title>
        </v-list-item>
        <v-list-item to="/contact">
          <v-list-item-title>Contact</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <router-view />
    </v-main>

    <!-- Footer -->
    <v-footer app>
      <v-col class="text-center">© 2025 CoffeeTime</v-col>
    </v-footer>
  </v-app>
</template>
