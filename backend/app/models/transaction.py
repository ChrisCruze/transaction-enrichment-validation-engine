from pydantic import BaseModel, Field
from typing import Optional


class RawTransaction(BaseModel):
    """Represents a raw, unenriched payment transaction."""
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    raw_descriptor: str = Field(..., description="Raw payment descriptor, e.g. 'SQ *BLUEBTL COFFEE #112'")
    amount: float = Field(..., description="Transaction amount in dollars")
    state: Optional[str] = Field(None, description="State where the transaction occurred")
    zip_code: Optional[str] = Field(None, description="ZIP code where the transaction occurred")


class EnrichedTransaction(BaseModel):
    """Represents an enriched transaction with merchant details."""
    transaction_id: str
    raw_descriptor: str
    merchant_name: Optional[str] = None
    merchant_address: Optional[str] = None
    merchant_phone: Optional[str] = None
    merchant_logo_url: Optional[str] = None


class FieldScore(BaseModel):
    """Accuracy score for a single enrichment field."""
    score: float = Field(..., ge=0.0, le=1.0, description="Accuracy score between 0.0 and 1.0")
    method: str = Field(..., description="Scoring method used (fuzzy, semantic, llm, etc.)")
    notes: Optional[str] = None


class ValidationResult(BaseModel):
    """Full validation result for a single transaction."""
    transaction_id: str
    raw_descriptor: str
    composite_score: float = Field(..., ge=0.0, le=1.0, description="Weighted composite accuracy score")
    merchant_name_score: Optional[FieldScore] = None
    merchant_address_score: Optional[FieldScore] = None
    merchant_phone_score: Optional[FieldScore] = None
    merchant_logo_score: Optional[FieldScore] = None
    category: Optional[str] = Field(None, description="Transaction category for processing optimization")


class BatchValidationRequest(BaseModel):
    """Request body for batch validation of enriched transactions."""
    transactions: list[EnrichedTransaction]


class BatchValidationResponse(BaseModel):
    """Response for batch validation containing all results and summary stats."""
    total: int
    avg_composite_score: float
    results: list[ValidationResult]
