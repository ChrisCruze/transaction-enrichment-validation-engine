# TEVE Backend

Python FastAPI backend for the Transaction Enrichment Validation Engine.

## Requirements

- Python 3.11+
- pip

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```bash
uvicorn app.main:app --reload --port 8000
```

API docs available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Project Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app entry point, CORS, router registration
│   ├── routes/
│   │   └── transactions.py  # POST /validate, POST /validate/batch, GET /example
│   ├── services/
│   │   └── enrichment.py    # Scoring logic: fuzzy, semantic, LLM, address, phone, logo
│   └── models/
│       └── transaction.py   # Pydantic models for requests and responses
└── requirements.txt
```

## Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/transactions/validate` | Validate a single enriched transaction |
| `POST` | `/api/transactions/validate/batch` | Validate a batch of transactions |
| `GET`  | `/api/transactions/example` | Fetch example transactions |
| `GET`  | `/health` | Health check |

## Scoring

Each enriched transaction is scored across four fields with a weighted composite:

| Field | Weight | Method |
|-------|--------|--------|
| Merchant Name | 40% | Fuzzy → Semantic → LLM |
| Merchant Address | 25% | Google Places + geospatial |
| Merchant Phone | 20% | Reverse lookup + format |
| Merchant Logo | 15% | URL check + pHash |
