<script setup lang="ts">
const count = ref(0);
</script>

<template>
  <div class="app">
    <header>
      <h1>${project_name}</h1>
      <p>A Nuxt project</p>
    </header>
    <main>
      <button @click="count++">Count: {{ count }}</button>
    </main>
  </div>
</template>

<style>
.app {
  font-family: system-ui, -apple-system, sans-serif;
  background: #f8fafc;
  color: #1e293b;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
}
header { text-align: center; margin-bottom: 2rem; }
h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; }
header p { color: #64748b; }
main {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}
button:hover { background: #2563eb; }
</style>