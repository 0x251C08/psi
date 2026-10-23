<script setup lang="ts">
import { ref } from "vue";

const count = ref(0);
</script>

<template>
  <div class="app">
    <header>
      <h1>${project_name}</h1>
      <p>A Vue project</p>
    </header>
    <main>
      <button @click="count++">Count: {{ count }}</button>
    </main>
  </div>
</template>

<style scoped>
.app {
  width: 100%;
  max-width: 400px;
}
</style>