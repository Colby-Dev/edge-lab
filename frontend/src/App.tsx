import './App.css'
import { useEffect, useState } from "react";

function App() {
  const [status, setStatus] = useState("loading");

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/health`)
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("error"));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Edge Lab</h1>
      <p>API Status: {status}</p>
    </div>
  );
}

export default App;