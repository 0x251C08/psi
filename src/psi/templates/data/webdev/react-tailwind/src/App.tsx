import { useState } from "react";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="app min-h-screen bg-slate-50 flex flex-col items-center p-8">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-bold text-slate-800 mb-2">${project_name}</h1>
        <p className="text-slate-500">A React + Tailwind project</p>
      </header>
      <main className="bg-white border border-slate-200 rounded-xl p-8 shadow-sm w-full max-w-md">
        <button
          onClick={() => setCount(c => c + 1)}
          className="w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-4 rounded-lg transition-colors"
        >
          Count: {count}
        </button>
      </main>
    </div>
  );
}

export default App;