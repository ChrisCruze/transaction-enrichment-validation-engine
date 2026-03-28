# Transaction Enrichment Validation Engine (TEVE)

**Measure, score, and visualize the accuracy of transaction enrichment at scale.**

TEVE is an end-to-end validation platform that evaluates how well raw, cryptic payment strings (e.g., `SQ *BLUEBTL COFFEE #112`) are enriched into structured merchant data — including merchant name, address, phone number, and logo. It combines multiple scoring algorithms into a single composite accuracy score, processes thousands of records efficiently through intelligent categorization, and surfaces results in a real-time dashboard.

---

## Table of Contents

- [Project Objective](#project-objective)
- [Why TEVE Exists](#why-teve-exists)
- [Methods & Approach](#methods--approach)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Dashboard](#dashboard)
- [Contributing](#contributing)
- [License](#license)

---

## Project Objective

Transaction enrichment transforms raw payment descriptors like `AMZN Mktp US*2X9AB` into clean, structured merchant records: **Amazon Marketplace**, with a verified address, phone number, and brand logo. But there is no universal ground truth for what "correct" enrichment looks like.

TEVE solves this by providing a **repeatable, explainable, and scalable framework** to measure enrichment accuracy across all four enrichment fields:

| Field | What It Measures |
|---|---|
| **Merchant Name** | Does the enriched name correctly identify the merchant? |
| **Merchant Address** | Does the enriched address match a verified location? |
| **Merchant Phone** | Is the phone number associated with the correct merchant? |
| **Merchant Logo** | Does the logo visually represent the correct brand? |

---

## Why TEVE Exists

Raw transaction descriptions are shaped by legacy payment infrastructure — card network character limits (22–25 characters), POS terminal software behavior, payment aggregator prefixing, and merchant descriptor misconfiguration. The result is that customers see strings like `WHOLEFDS MKT #102` or `PAYPAL *NETFLIX` instead of clean merchant names.

Enrichment vendors resolve these strings into structured data, but measuring their accuracy has historically been manual, inconsistent, and difficult to scale. TEVE automates this measurement using a hybrid approach that combines fast deterministic methods with external knowledge validation.

---

## Methods & Approach

TEVE uses a **tiered hybrid scoring system** that applies the right technique to each enrichment field:

### Merchant Name Scoring

1. **Fuzzy String Matching** — Levenshtein distance, Jaro-Winkler similarity, and token-set ratio provide a fast baseline score. Highly interpretable but struggles with abbreviations and aliases.
2. **Semantic Embedding Matching** — Sentence transformer models (`all-MiniLM-L6-v2`) convert raw and enriched merchant strings to vector embeddings and compute cosine similarity. Captures meaning rather than characters — handles `TRDR JOE'S` → `Trader Joe's` correctly.
3. **LLM-as-Evaluator** — For ambiguous cases where string and semantic methods disagree, an LLM evaluates whether the enriched name correctly identifies the merchant from the raw string. Returns a confidence score with reasoning.

### Address Validation

- **Google Places API** cross-references the enriched merchant name and address against verified business listings.
- **Geospatial consistency checks** compare the enriched location against the raw transaction's state and zip code fields.

### Phone Number Validation

- **Reverse lookup** validates that the enriched phone number is associated with the enriched merchant name.
- **Format validation** confirms the number is a valid, dialable format.

### Logo Validation

- **URL reachability** confirms the logo URL returns a valid image (HTTP 200, correct content-type).
- **Perceptual hashing** compares the enriched logo against a reference brand logo database using pHash to detect visual similarity.
- **Brand consistency** cross-checks the logo's merchant ID against the enriched merchant name.

### Transaction Categorization for Efficiency

Before scoring, TEVE classifies each transaction into one of six categories to optimize processing:

| Category | Example | Optimization |
|---|---|---|
| POS Terminal Variants | `SQ *BLUE BOTTLE SF CA` | Strip aggregator prefix before matching |
| Merchant Abbreviations | `WHOLEFDS MKT #102` | Apply abbreviation expansion dictionary |
| Aggregator/Marketplace | `PAYPAL *NETFLIX` | Evaluate underlying merchant, not aggregator |
| Location-Encoded | `STARBUCKS 12345 NEW YORK` | Extract merchant name, validate location separately |
| Truncated/Encoded | `APL*ITUNES.COM/BILL` | Expand known patterns before scoring |
| International | `UBER BV AMSTERDAM` | Map legal entities to consumer brands |

This categorization allows TEVE to apply targeted preprocessing per category, significantly improving both speed and accuracy.

---

## Tech Stack

### Backend

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Core runtime |
| **FastAPI** | REST API framework |
| **Pandas** | Data ingestion and transformation |
| **scikit-learn** | TF-IDF and cosine similarity utilities |
| **sentence-transformers** | Semantic embedding generation |
| **RapidFuzz** | High-performance fuzzy string matching |
| **FAISS** | Vector similarity search at scale |
| **httpx** | Async HTTP client for external API calls |
| **Pydantic** | Request/response validation |
| **SQLite / PostgreSQL** | Result storage and audit trail |

### Frontend

| Technology | Purpose |
|---|---|
| **React 18** | UI framework |
| **TypeScript** | Type-safe frontend code |
| **Recharts** | Accuracy charts and score distributions |
| **TanStack Table** | Sortable, filterable transaction result tables |
| **Tailwind CSS** | Utility-first styling |
| **Vite** | Build tool and dev server |

### External APIs

| Service | Purpose |
|---|---|
| **Google Places API** | Address and merchant verification |
| **Google Custom Search API** | Merchant entity resolution from raw strings |
| **Brandfetch / Clearbit** | Reference logo retrieval for comparison |

---

## Features

- **Batch transaction ingestion** — Upload CSV/XLSX files with raw and enriched transaction data. TEVE parses, categorizes, and queues records for scoring.
- **Multi-method accuracy scoring** — Each enrichment field is scored independently using the most appropriate method. Scores are composited into a single per-record accuracy rating.
- **Intelligent categorization** — Transactions are classified by type (POS, aggregator, truncated, international, etc.) so preprocessing and scoring are optimized per category.
- **Interactive accuracy dashboard** — Real-time visualization of accuracy distributions, category-level breakdowns, field-level drill-downs, and trend analysis.
- **Explainable scores** — Every accuracy score includes a traceable explanation: which method was used, what the raw inputs were, and why the score was assigned.
- **Configurable thresholds** — Define what "accurate" means for your use case. Set pass/fail thresholds per field and per category.
- **Export and reporting** — Download accuracy reports as CSV or PDF. Generate executive summaries with aggregate metrics.
- **API-first design** — Every capability is exposed via REST API. The dashboard is one consumer; integrate TEVE into CI/CD pipelines, batch jobs, or other systems.

---

## Project Structure

```
transaction-enrichment-validation-engine/
├── README.md
├── docker-compose.yml
├── .env.example
│
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI application entry point
│   │   ├── config.py                # Environment and configuration
│   │   ├── models/
│   │   │   ├── transaction.py       # Pydantic models for transactions
│   │   │   ├── score.py             # Scoring result models
│   │   │   └── report.py            # Report generation models
│   │   ├── routers/
│   │   │   ├── ingest.py            # /ingest endpoints
│   │   │   ├── score.py             # /score endpoints
│   │   │   ├── reports.py           # /reports endpoints
│   │   │   └── health.py            # /health endpoint
│   │   ├── services/
│   │   │   ├── categorizer.py       # Transaction type classification
│   │   │   ├── preprocessor.py      # Per-category string normalization
│   │   │   ├── scoring/
│   │   │   │   ├── fuzzy.py         # Fuzzy string matching scorer
│   │   │   │   ├── semantic.py      # Embedding-based semantic scorer
│   │   │   │   ├── llm_evaluator.py # LLM-as-judge scorer
│   │   │   │   ├── address.py       # Address validation scorer
│   │   │   │   ├── phone.py         # Phone number validation scorer
│   │   │   │   ├── logo.py          # Logo validation scorer
│   │   │   │   └── composite.py     # Weighted composite score aggregator
│   │   │   ├── external/
│   │   │   │   ├── google_places.py # Google Places API client
│   │   │   │   ├── google_search.py # Google Custom Search client
│   │   │   │   └── brandfetch.py    # Brand logo retrieval client
│   │   │   └── report_generator.py  # Report compilation service
│   │   ├── db/
│   │   │   ├── database.py          # Database connection and session
│   │   │   ├── tables.py            # SQLAlchemy table definitions
│   │   │   └── migrations/          # Alembic migrations
│   │   └── utils/
│   │       ├── abbreviations.py     # Merchant abbreviation dictionary
│   │       ├── aggregators.py       # Known aggregator prefix patterns
│   │       └── validators.py        # Shared validation utilities
│   ├── tests/
│   │   ├── test_categorizer.py
│   │   ├── test_fuzzy_scorer.py
│   │   ├── test_semantic_scorer.py
│   │   ├── test_composite_scorer.py
│   │   └── test_api.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── Dashboard.tsx         # Main dashboard layout
│   │   │   ├── AccuracyOverview.tsx   # Aggregate accuracy cards
│   │   │   ├── CategoryBreakdown.tsx  # Per-category score charts
│   │   │   ├── FieldDrilldown.tsx     # Per-field accuracy detail
│   │   │   ├── TransactionTable.tsx   # Sortable results table
│   │   │   ├── UploadPanel.tsx        # File upload interface
│   │   │   └── ScoreExplainer.tsx     # Individual score explanation
│   │   ├── hooks/
│   │   │   ├── useTransactions.ts
│   │   │   └── useScores.ts
│   │   ├── api/
│   │   │   └── client.ts             # API client configuration
│   │   └── types/
│   │       └── index.ts              # TypeScript type definitions
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
└── data/
    ├── sample_transactions.csv       # Sample input dataset
    └── abbreviation_dictionary.json  # Merchant abbreviation mappings
```

---

## Installation & Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Places API key (for address validation)
- Google Custom Search API key + Search Engine ID (optional, for merchant resolution)

### 1. Clone the Repository

```bash
git clone https://github.com/ChrisCruze/transaction-enrichment-validation-engine.git
cd transaction-enrichment-validation-engine
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Backend
GOOGLE_PLACES_API_KEY=your_google_places_key
GOOGLE_SEARCH_API_KEY=your_google_search_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
DATABASE_URL=sqlite:///./teve.db
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The dashboard will be available at `http://localhost:5173` and the API at `http://localhost:8000`.

### 5. Docker (Alternative)

```bash
docker-compose up --build
```

This starts both the backend API (port 8000) and frontend dashboard (port 3000).

---

## API Endpoints

### Health

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health check |

### Ingestion

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ingest/upload` | Upload a CSV/XLSX file of transactions |
| `POST` | `/ingest/records` | Submit transactions as JSON array |
| `GET` | `/ingest/status/{job_id}` | Check ingestion job status |

### Scoring

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/score/batch` | Score a batch of ingested transactions |
| `POST` | `/score/single` | Score a single transaction record |
| `GET` | `/score/results/{job_id}` | Retrieve scoring results for a job |
| `GET` | `/score/results/{job_id}/export` | Export results as CSV |

### Reports

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/reports/summary/{job_id}` | Aggregate accuracy summary |
| `GET` | `/reports/by-category/{job_id}` | Accuracy broken down by transaction category |
| `GET` | `/reports/by-field/{job_id}` | Accuracy broken down by enrichment field |
| `GET` | `/reports/distribution/{job_id}` | Score distribution histogram data |
| `GET` | `/reports/failures/{job_id}` | Lowest-scoring records for review |

### Transactions

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/transactions/{job_id}` | List all transactions for a job |
| `GET` | `/transactions/{job_id}/{txn_id}` | Get a single transaction with score explanation |

---

## Usage Examples

### Upload and Score a Transaction File

```bash
# Upload a CSV file
curl -X POST http://localhost:8000/ingest/upload \
  -F "file=@data/sample_transactions.csv" \
  -H "Content-Type: multipart/form-data"

# Response:
# { "job_id": "teve-20260327-001", "records_ingested": 10000, "status": "ready" }

# Trigger scoring
curl -X POST http://localhost:8000/score/batch \
  -H "Content-Type: application/json" \
  -d '{ "job_id": "teve-20260327-001" }'

# Response:
# { "job_id": "teve-20260327-001", "status": "processing", "estimated_time_seconds": 120 }
```

### Score a Single Transaction

```bash
curl -X POST http://localhost:8000/score/single \
  -H "Content-Type: application/json" \
  -d '{
    "raw_merchant_name": "SQ *BLUEBTL COFFEE #112",
    "raw_city": "San Francisco",
    "raw_state": "CA",
    "raw_zip": "94107",
    "enriched_merchant_name": "Blue Bottle Coffee",
    "enriched_address": "66 Mint St, San Francisco, CA 94103",
    "enriched_phone": "5106533394",
    "enriched_logo_url": "https://example.com/logos/blue-bottle.png"
  }'
```

**Response:**

```json
{
  "transaction_id": "txn_abc123",
  "category": "pos_terminal_variant",
  "composite_score": 0.94,
  "field_scores": {
    "merchant_name": {
      "score": 0.97,
      "method": "semantic_embedding",
      "explanation": "Semantic similarity between 'SQ *BLUEBTL COFFEE #112' and 'Blue Bottle Coffee' is 0.97 after stripping aggregator prefix 'SQ *'."
    },
    "address": {
      "score": 0.92,
      "method": "google_places_verification",
      "explanation": "Google Places confirms 'Blue Bottle Coffee' at '66 Mint St, San Francisco, CA' — address verified, zip code differs by one digit (94107 vs 94103)."
    },
    "phone": {
      "score": 0.95,
      "method": "reverse_lookup",
      "explanation": "Phone 5106533394 is associated with Blue Bottle Coffee Inc."
    },
    "logo": {
      "score": 0.91,
      "method": "phash_comparison",
      "explanation": "Logo URL returns valid image. Perceptual hash similarity to reference Blue Bottle logo: 0.91."
    }
  }
}
```

### Retrieve an Accuracy Summary

```bash
curl http://localhost:8000/reports/summary/teve-20260327-001
```

**Response:**

```json
{
  "job_id": "teve-20260327-001",
  "total_records": 10000,
  "overall_accuracy": 0.923,
  "field_accuracy": {
    "merchant_name": 0.941,
    "address": 0.957,
    "phone": 0.962,
    "logo": 0.889
  },
  "records_above_threshold": 8847,
  "records_below_threshold": 1153,
  "processing_time_seconds": 98.4,
  "throughput_per_hour": 365853
}
```

---

## Dashboard

The React dashboard provides four primary views:

1. **Accuracy Overview** — Top-line composite accuracy score with field-level breakdowns displayed as gauge charts. Color-coded pass/fail against configurable thresholds.

2. **Category Breakdown** — Bar and radar charts showing accuracy by transaction category (POS variants, aggregators, truncated, international, etc.). Identifies which categories the enrichment engine handles well and where it struggles.

3. **Transaction Explorer** — A searchable, sortable table of all scored transactions. Click any row to see the full score explanation: raw input, enriched output, method used, and reasoning.

4. **Trend Analysis** — When multiple scoring jobs are run, track accuracy improvements over time. Compare before/after when enrichment rules are updated.

---

## Contributing

Contributions are welcome. Here's how to get started:

### Development Workflow

1. **Fork** the repository and create a feature branch from `main`.
2. **Follow existing patterns** — the backend uses FastAPI routers with Pydantic models; the frontend uses React functional components with TypeScript.
3. **Write tests** — backend changes should include pytest tests in `backend/tests/`. Frontend changes should include component tests.
4. **Keep commits focused** — one logical change per commit, with a clear message.
5. **Open a pull request** against `main` with a description of what changed and why.

### Adding a New Scoring Method

1. Create a new scorer in `backend/app/services/scoring/` implementing the `BaseScorer` interface.
2. Register it in the composite scorer's method registry.
3. Add tests in `backend/tests/`.
4. Update the frontend's `ScoreExplainer` component if the new method requires a unique explanation format.

### Code Standards

- **Backend**: Python 3.11+, type hints on all public functions, Black formatting, Ruff linting.
- **Frontend**: TypeScript strict mode, ESLint + Prettier, functional components with hooks.
- **Documentation**: Update this README if your change affects setup, API surface, or project structure.

### Reporting Issues

Open a GitHub issue with a clear description, steps to reproduce, and expected vs. actual behavior. Include sample transaction data if the issue relates to scoring accuracy.

---

## License

This project is developed as part of an internal initiative. Contact the repository owner for licensing details.

---

*Built to answer a simple question: how accurate is our transaction enrichment, really?*
