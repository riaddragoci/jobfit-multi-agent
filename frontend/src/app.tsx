import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import ResultsDashboard from "./components/ResultsDashboard";
import { AnalyzeResponse } from "./types";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (cvText: string, jdText: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cv_text: cvText, jd_text: jdText }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || `Server error: ${response.status}`);
      }

      const data: AnalyzeResponse = await response.json();
      setResults(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong. Is the backend running?");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="app__header">
        <div className="app__header-inner">
          <div className="app__logo">
            <span className="app__logo-icon">⚡</span>
            <h1 className="app__title">CV ↔ JD Matcher</h1>
          </div>
          <p className="app__subtitle">
            Multi-agent AI system that analyzes your CV against any job description
          </p>
        </div>
      </header>

      <main className="app__main">
        {error && (
          <div className="app__error">
            <span className="app__error-icon">⚠</span>
            <p>{error}</p>
            <button onClick={() => setError(null)} className="app__error-close">
              ✕
            </button>
          </div>
        )}

        {!results ? (
          <UploadForm onSubmit={handleSubmit} isLoading={isLoading} />
        ) : (
          <ResultsDashboard data={results} onReset={handleReset} />
        )}
      </main>

      <footer className="app__footer">
        <p>Powered by Ollama &amp; LLaMA 3.1 — Multi-Agent Architecture</p>
      </footer>
    </div>
  );
}

export default App;