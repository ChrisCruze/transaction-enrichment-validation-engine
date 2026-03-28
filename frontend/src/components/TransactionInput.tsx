import React, { useState } from "react";
import { EnrichedTransaction, BatchValidationResponse } from "../types";

interface TransactionInputProps {
  onResults: (data: BatchValidationResponse) => void;
}

const PLACEHOLDER_JSON = JSON.stringify(
  [
    {
      transaction_id: "txn_001",
      raw_descriptor: "SQ *BLUEBTL COFFEE #112",
      merchant_name: "Blue Bottle Coffee",
      merchant_address: "300 Webster St, Oakland, CA 94607",
      merchant_phone: "(510) 653-3394",
      merchant_logo_url: "https://example.com/logos/bluebottle.png",
    },
  ],
  null,
  2
);

export const TransactionInput: React.FC<TransactionInputProps> = ({ onResults }) => {
  const [inputJson, setInputJson] = useState(PLACEHOLDER_JSON);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    let transactions: EnrichedTransaction[];
    try {
      transactions = JSON.parse(inputJson);
      if (!Array.isArray(transactions)) {
        transactions = [transactions];
      }
    } catch {
      setError("Invalid JSON. Please check your input.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/transactions/validate/batch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transactions }),
      });
      if (!res.ok) {
        const detail = await res.json();
        throw new Error(detail?.detail ?? `Server error ${res.status}`);
      }
      const data: BatchValidationResponse = await res.json();
      onResults(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      <label htmlFor="txn-input" style={{ fontWeight: 600 }}>
        Paste enriched transactions (JSON array):
      </label>
      <textarea
        id="txn-input"
        rows={14}
        value={inputJson}
        onChange={(e) => setInputJson(e.target.value)}
        style={{
          fontFamily: "monospace",
          fontSize: 13,
          padding: "10px 12px",
          borderRadius: 6,
          border: "1px solid #d1d5db",
          resize: "vertical",
        }}
      />
      {error && (
        <p style={{ color: "#dc2626", margin: 0, fontSize: 14 }}>{error}</p>
      )}
      <button
        type="submit"
        disabled={loading}
        style={{
          alignSelf: "flex-start",
          padding: "8px 20px",
          background: "#2563eb",
          color: "#fff",
          border: "none",
          borderRadius: 6,
          fontWeight: 600,
          cursor: loading ? "not-allowed" : "pointer",
          opacity: loading ? 0.7 : 1,
        }}
      >
        {loading ? "Validating…" : "Validate Transactions"}
      </button>
    </form>
  );
};
