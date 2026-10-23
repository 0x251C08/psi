// ${project_name} - TypeScript app

interface CounterState {
  count: number;
}

const state: CounterState = { count: 0 };

function render() {
  const app = document.getElementById("app");
  if (!app) return;

  app.innerHTML = `
    <header>
      <h1>${project_name}</h1>
      <p>A TypeScript project</p>
    </header>
    <main>
      <button id="counter-btn">Count: ${state.count}</button>
    </main>
  `;

  const btn = document.getElementById("counter-btn");
  btn?.addEventListener("click", () => {
    state.count++;
    render();
  });
}

render();
console.log("${project_name} loaded!");