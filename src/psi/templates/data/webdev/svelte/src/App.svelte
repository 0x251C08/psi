<script lang="ts">
  let count = 0;
</script>

<div class="app">
  <header>
    <h1>${project_name}</h1>
    <p>A Svelte project</p>
  </header>
  <main>
    <button onclick={() => count++}>Count: {count}</button>
  </main>
</div>

<style>
  .app {
    width: 100%;
    max-width: 400px;
  }
</style>