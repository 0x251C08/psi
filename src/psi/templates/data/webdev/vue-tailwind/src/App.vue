<script setup lang="ts">
import { ref } from "vue";

const count = ref(0);
</script>

<template>
  <div class="min-h-screen bg-slate-50 flex flex-col items-center p-8">
    <header class="text-center mb-8">
      <h1 class="text-4xl font-bold text-slate-800 mb-2">${project_name}</h1>
      <p class="text-slate-500">A Vue + Tailwind project</p>
    </header>
    <main class="bg-white border border-slate-200 rounded-xl p-8 shadow-sm w-full max-w-md">
      <button @click="count++" class="w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-4 rounded-lg transition-colors">
        Count: {{ count }}
      </button>
    </main>
  </div>
</template>

<style scoped>
/* Tailwind handles all styling */
</style>