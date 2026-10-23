import { useState } from "react";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="app">
      <header>
        <h1>${project_name}</h1>
        <p>A React project</p>
      </header>
      <main>
        <button onClick={() => setCount(c => c + 1)}>
          Count: {count}
        </button>
      </main>
    </div>
  );
}

export default App;