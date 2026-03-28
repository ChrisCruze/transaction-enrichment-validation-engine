import React from "react";
import { BatchValidationResponse, ValidationResult } from "../types";

interface DashboardProps {
  data: BatchValidationResponse;
}

const scoreColor = (score: number): string => {
  if (score >= 0.75) return "#16a34a";
  if (score >= 0.50) return "#d97706";
  return "#dc2626";
};

const ScoreBadge: React.FC<{ score: number }> = ({ score }) => (
  <span
    style={{
      display: "inline-block",
      padding: "2px 10px",
      borderRadius: 12,
      fontWeight: 700,
      fontSize: 13,
      color: "#fff",
      background: scoreColor(score),
    }}
  >
    {(score * 100).toFixed(1)}%
  </span>
);

const ResultRow: React.FC<{ result: ValidationResult }> = ({ result }) => (
  <tr style={{ borderBottom: "1px solid #e5e7eb" }}>
    <td style={{ padding: "10px 12px", fontFamily: "monospace", fontSize: 13 }}>
      {result.raw_descriptor}
    </td>
    <td style={{ padding: "10px 12px" }}>
      {result.merchant_name_score ? (
        <ScoreBadge score={result.merchant_name_score.score} />
      ) : (
        "—"
      )}
    </td>
    <td style={{ padding: "10px 12px" }}>
      {result.merchant_address_score ? (
        <ScoreBadge score={result.merchant_address_score.score} />
      ) : (
        "—"
      )}
    </td>
    <td style={{ padding: "10px 12px" }}>
      {result.merchant_phone_score ? (
        <ScoreBadge score={result.merchant_phone_score.score} />
      ) : (
        "—"
      )}
    </td>
    <td style={{ padding: "10px 12px" }}>
      {result.merchant_logo_score ? (
        <ScoreBadge score={result.merchant_logo_score.score} />
      ) : (
        "—"
      )}
    </td>
    <td style={{ padding: "10px 12px" }}>
      <ScoreBadge score={result.composite_score} />
    </td>
    <td style={{ padding: "10px 12px", fontSize: 12, color: "#6b7280" }}>
      {result.category ?? "—"}
    </td>
  </tr>
);

export const Dashboard: React.FC<DashboardProps> = ({ data }) => (
  <div>
    <div
      style={{
        display: "flex",
        gap: 24,
        marginBottom: 24,
        flexWrap: "wrap",
      }}
    >
      <StatCard label="Transactions Validated" value={String(data.total)} />
      <StatCard
        label="Avg Composite Score"
        value={`${(data.avg_composite_score * 100).toFixed(1)}%`}
        color={scoreColor(data.avg_composite_score)}
      />
    </div>

    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
        <thead>
          <tr style={{ background: "#f3f4f6", textAlign: "left" }}>
            {[
              "Raw Descriptor",
              "Name",
              "Address",
              "Phone",
              "Logo",
              "Composite",
              "Category",
            ].map((h) => (
              <th key={h} style={{ padding: "10px 12px", fontWeight: 600 }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.results.map((r) => (
            <ResultRow key={r.transaction_id} result={r} />
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

const StatCard: React.FC<{ label: string; value: string; color?: string }> = ({
  label,
  value,
  color,
}) => (
  <div
    style={{
      background: "#f9fafb",
      border: "1px solid #e5e7eb",
      borderRadius: 8,
      padding: "16px 24px",
      minWidth: 180,
    }}
  >
    <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 4 }}>{label}</div>
    <div style={{ fontSize: 28, fontWeight: 700, color: color ?? "#111827" }}>{value}</div>
  </div>
);
