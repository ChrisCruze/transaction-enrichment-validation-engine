from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import transactions

app = FastAPI(
    title="Transaction Enrichment Validation Engine (TEVE)",
    description="Measure, score, and visualize the accuracy of transaction enrichment at scale.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])


@app.get("/")
def root():
    return {"message": "TEVE API is running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
