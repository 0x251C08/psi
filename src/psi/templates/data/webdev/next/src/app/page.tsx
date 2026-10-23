"use client";

import { useState } from "react";

export default function Home() {
  const [count, setCount] = useState(0);

  return (
    <main className="main">
      <header>
        <h1>${project_name}</h1>
        <p>A Next.js project</p>
      </header>
      <button onClick={() => setCount(c => c + 1)}>
        Count: {count}
      </button>
    </main>
  );
}