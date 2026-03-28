from fastapi import APIRouter, HTTPException
from app.models.transaction import (
    BatchValidationRequest,
    BatchValidationResponse,
    EnrichedTransaction,
    ValidationResult,
)
from app.services.enrichment import validate_transaction

router = APIRouter()


@router.post("/validate", response_model=ValidationResult)
def validate_single(transaction: EnrichedTransaction):
    """Validate a single enriched transaction and return its accuracy scores."""
    return validate_transaction(transaction)


@router.post("/validate/batch", response_model=BatchValidationResponse)
def validate_batch(request: BatchValidationRequest):
    """Validate a batch of enriched transactions and return results with summary stats."""
    if not request.transactions:
        raise HTTPException(status_code=400, detail="No transactions provided")

    results = [validate_transaction(txn) for txn in request.transactions]
    avg_score = sum(r.composite_score for r in results) / len(results)

    return BatchValidationResponse(
        total=len(results),
        avg_composite_score=round(avg_score, 4),
        results=results,
    )


@router.get("/example", response_model=list[EnrichedTransaction])
def get_example_transactions():
    """Return example transactions to help explore the API."""
    return [
        EnrichedTransaction(
            transaction_id="txn_001",
            raw_descriptor="SQ *BLUEBTL COFFEE #112",
            merchant_name="Blue Bottle Coffee",
            merchant_address="300 Webster St, Oakland, CA 94607",
            merchant_phone="(510) 653-3394",
            merchant_logo_url="https://example.com/logos/bluebottle.png",
        ),
        EnrichedTransaction(
            transaction_id="txn_002",
            raw_descriptor="WHOLEFDS MKT #102",
            merchant_name="Whole Foods Market",
            merchant_address="1765 California St, San Francisco, CA 94109",
            merchant_phone="(415) 674-0500",
            merchant_logo_url="https://example.com/logos/wholefoods.png",
        ),
        EnrichedTransaction(
            transaction_id="txn_003",
            raw_descriptor="AMZN Mktp US*2X9AB",
            merchant_name="Amazon Marketplace",
            merchant_address=None,
            merchant_phone=None,
            merchant_logo_url="https://example.com/logos/amazon.png",
        ),
    ]
