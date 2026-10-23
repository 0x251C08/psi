import { createSignal } from "solid-js";
import "./App.css";

function App() {
  const [count, setCount] = createSignal(0);

  return (
    <div class="app">
      <header>
        <h1>${project_name}</h1>
        <p>A SolidJS project</p>
      </header>
      <main>
        <button onClick={() => setCount(c => c + 1)}>
          Count: {count()}
        </button>
      </main>
    </div>
  );
}

export default App;