# TEVE Frontend

React + TypeScript workflow app for the Transaction Enrichment Validation Engine.

## Requirements

- Node.js 18+
- npm

## Setup

```bash
cd frontend
npm install
```

## Running

Start the backend first (see `../backend/README.md`), then:

```bash
npm start
```

App available at [http://localhost:3000](http://localhost:3000).

API calls are proxied to `http://localhost:8000` via the `proxy` field in `package.json`.

## Project Structure

```
frontend/src/
├── App.tsx                        # Root component, layout, and state
├── components/
│   ├── TransactionInput.tsx       # JSON input form, calls POST /validate/batch
│   └── Dashboard.tsx              # Results table with per-field and composite scores
└── types/
    └── index.ts                   # Shared TypeScript interfaces (mirrors API models)
```

## Usage

1. Paste a JSON array of enriched transactions into the input area.
2. Click **Validate Transactions**.
3. The dashboard renders per-field accuracy scores and a weighted composite score for each transaction, color-coded green/amber/red.

### Example Input

```json
[
  {
    "transaction_id": "txn_001",
    "raw_descriptor": "SQ *BLUEBTL COFFEE #112",
    "merchant_name": "Blue Bottle Coffee",
    "merchant_address": "300 Webster St, Oakland, CA 94607",
    "merchant_phone": "(510) 653-3394",
    "merchant_logo_url": "https://example.com/logos/bluebottle.png"
  }
]
```
