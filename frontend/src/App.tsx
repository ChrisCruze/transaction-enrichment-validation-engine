import React, { useState } from "react";
import { TransactionInput } from "./components/TransactionInput";
import { Dashboard } from "./components/Dashboard";
import { BatchValidationResponse } from "./types";

const App: React.FC = () => {
  const [results, setResults] = useState<BatchValidationResponse | null>(null);

  return (
    <div style={{ minHeight: "100vh", background: "#f9fafb", fontFamily: "Inter, system-ui, sans-serif" }}>
      <header
        style={{
          background: "#1e3a5f",
          color: "#fff",
          padding: "18px 32px",
          display: "flex",
          alignItems: "center",
          gap: 16,
        }}
      >
        <div>
          <h1 style={{ margin: 0, fontSize: 20, fontWeight: 700, letterSpacing: "-0.3px" }}>
            Transaction Enrichment Validation Engine
          </h1>
          <p style={{ margin: 0, fontSize: 13, opacity: 0.75 }}>
            Measure, score, and visualize enrichment accuracy at scale
          </p>
        </div>
      </header>

      <main style={{ maxWidth: 1100, margin: "0 auto", padding: "32px 24px" }}>
        <section
          style={{
            background: "#fff",
            border: "1px solid #e5e7eb",
            borderRadius: 10,
            padding: 28,
            marginBottom: 32,
          }}
        >
          <h2 style={{ margin: "0 0 16px", fontSize: 16, fontWeight: 600 }}>
            Submit Enriched Transactions
          </h2>
          <TransactionInput onResults={setResults} />
        </section>

        {results && (
          <section
            style={{
              background: "#fff",
              border: "1px solid #e5e7eb",
              borderRadius: 10,
              padding: 28,
            }}
          >
            <h2 style={{ margin: "0 0 20px", fontSize: 16, fontWeight: 600 }}>
              Validation Results
            </h2>
            <Dashboard data={results} />
          </section>
        )}
      </main>
    </div>
  );
};

export default App;
