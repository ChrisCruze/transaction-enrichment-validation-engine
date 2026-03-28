"""
Enrichment validation service.

Implements the tiered hybrid scoring system for evaluating transaction enrichment accuracy:
  - Merchant Name: fuzzy string matching -> semantic embeddings -> LLM evaluator
  - Address: Google Places cross-reference + geospatial consistency
  - Phone: reverse lookup + format validation
  - Logo: URL reachability + perceptual hashing + brand consistency
"""

import re
from difflib import SequenceMatcher
from app.models.transaction import EnrichedTransaction, FieldScore, ValidationResult

# Weights for the composite score
SCORE_WEIGHTS = {
    "merchant_name": 0.40,
    "merchant_address": 0.25,
    "merchant_phone": 0.20,
    "merchant_logo": 0.15,
}


def _fuzzy_name_score(raw: str, enriched: str) -> float:
    """Basic fuzzy string similarity using SequenceMatcher (Levenshtein proxy)."""
    raw_clean = raw.upper().strip()
    enriched_clean = enriched.upper().strip()
    return SequenceMatcher(None, raw_clean, enriched_clean).ratio()


def score_merchant_name(raw_descriptor: str, merchant_name: str | None) -> FieldScore:
    """Score merchant name accuracy using fuzzy matching (placeholder for full pipeline)."""
    if not merchant_name:
        return FieldScore(score=0.0, method="none", notes="No merchant name provided")

    score = _fuzzy_name_score(raw_descriptor, merchant_name)
    return FieldScore(
        score=round(score, 4),
        method="fuzzy",
        notes="Levenshtein-based fuzzy match; semantic and LLM layers not yet wired",
    )


def score_merchant_address(address: str | None, state: str | None, zip_code: str | None) -> FieldScore:
    """Score address validity (stub — full implementation uses Google Places API)."""
    if not address:
        return FieldScore(score=0.0, method="none", notes="No address provided")

    # Stub: check that address contains a digit (rough plausibility check)
    has_number = bool(re.search(r"\d", address))
    score = 0.5 if has_number else 0.2
    return FieldScore(
        score=score,
        method="format_check",
        notes="Stub score; Google Places validation not yet integrated",
    )


def score_merchant_phone(phone: str | None, merchant_name: str | None) -> FieldScore:
    """Score phone number validity (stub — full implementation uses reverse lookup)."""
    if not phone:
        return FieldScore(score=0.0, method="none", notes="No phone number provided")

    # Stub: validate E.164 or NANP format
    digits = re.sub(r"\D", "", phone)
    valid_format = len(digits) in (10, 11)
    score = 0.6 if valid_format else 0.1
    return FieldScore(
        score=score,
        method="format_validation",
        notes="Stub score; reverse lookup not yet integrated",
    )


def score_merchant_logo(logo_url: str | None, merchant_name: str | None) -> FieldScore:
    """Score logo validity (stub — full implementation checks URL + perceptual hash)."""
    if not logo_url:
        return FieldScore(score=0.0, method="none", notes="No logo URL provided")

    is_https = logo_url.startswith("https://")
    looks_like_image = any(logo_url.lower().endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".svg", ".webp"))
    score = 0.5 if is_https else 0.2
    if looks_like_image:
        score += 0.2
    return FieldScore(
        score=min(round(score, 4), 1.0),
        method="url_check",
        notes="Stub score; URL reachability and pHash validation not yet integrated",
    )


def categorize_transaction(raw_descriptor: str) -> str:
    """Classify transaction into a processing category to optimize scoring pipeline."""
    descriptor = raw_descriptor.upper()
    if any(kw in descriptor for kw in ("PAYPAL", "SQ *", "STRIPE")):
        return "payment_aggregator"
    if any(kw in descriptor for kw in ("AMZN", "AMAZON", "EBAY", "ETSY")):
        return "ecommerce"
    if any(kw in descriptor for kw in ("ATM", "CASH", "WITHDRAW")):
        return "atm_cash"
    if any(kw in descriptor for kw in ("RECURRING", "SUBSCR", "NETFLIX", "SPOTIFY")):
        return "subscription"
    if any(kw in descriptor for kw in ("REFUND", "RETURN", "CREDIT")):
        return "refund"
    return "standard"


def validate_transaction(txn: EnrichedTransaction, state: str | None = None, zip_code: str | None = None) -> ValidationResult:
    """Run full validation pipeline on a single enriched transaction."""
    name_score = score_merchant_name(txn.raw_descriptor, txn.merchant_name)
    address_score = score_merchant_address(txn.merchant_address, state, zip_code)
    phone_score = score_merchant_phone(txn.merchant_phone, txn.merchant_name)
    logo_score = score_merchant_logo(txn.merchant_logo_url, txn.merchant_name)

    composite = (
        name_score.score * SCORE_WEIGHTS["merchant_name"]
        + address_score.score * SCORE_WEIGHTS["merchant_address"]
        + phone_score.score * SCORE_WEIGHTS["merchant_phone"]
        + logo_score.score * SCORE_WEIGHTS["merchant_logo"]
    )

    return ValidationResult(
        transaction_id=txn.transaction_id,
        raw_descriptor=txn.raw_descriptor,
        composite_score=round(composite, 4),
        merchant_name_score=name_score,
        merchant_address_score=address_score,
        merchant_phone_score=phone_score,
        merchant_logo_score=logo_score,
        category=categorize_transaction(txn.raw_descriptor),
    )
