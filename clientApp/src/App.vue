<script setup lang="ts">
import StorefrontPage from './features/store/StorefrontPage.vue'
</script>

<template>
  <StorefrontPage />
</template>

<style>
:root {
  color: #111827;
  background: #f7f8fb;
  font-family:
    Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  min-width: 320px;
  margin: 0;
}

button,
input {
  font: inherit;
}

button:focus-visible,
a:focus-visible,
input:focus-visible {
  outline: 3px solid rgba(252, 163, 17, 0.45);
  outline-offset: 2px;
}
</style>
