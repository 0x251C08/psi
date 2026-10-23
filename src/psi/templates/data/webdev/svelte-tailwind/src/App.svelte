<script lang="ts">
  let count = 0;
</script>

<div class="min-h-screen bg-slate-50 flex flex-col items-center p-8">
  <header class="text-center mb-8">
    <h1 class="text-4xl font-bold text-slate-800 mb-2">${project_name}</h1>
    <p class="text-slate-500">A Svelte + Tailwind project</p>
  </header>
  <main class="bg-white border border-slate-200 rounded-xl p-8 shadow-sm w-full max-w-md">
    <button onclick={() => count++} class="w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-4 rounded-lg transition-colors">
      Count: {count}
    </button>
  </main>
</div>

<style>
  /* Tailwind handles all styling */
</style>