"""Village Hacks — ID Verification API (mock responses)"""

import base64
from typing import Any, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from levels.level1 import check_authenticity
from levels.level2 import extract_fields
from levels.level3 import match_documents
from levels.level4 import check_compliance

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(title="Village Hacks ID Verification API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


class Level1Request(BaseModel):
    image: str  # base64-encoded image


class Level2Request(BaseModel):
    image: str


class Level3Request(BaseModel):
    image: str
    form1003: dict = {}


class Level4Request(BaseModel):
    image: str
    property_state: str = "TX"


class FullRequest(BaseModel):
    image: str
    form1003: dict = {}
    property_state: str = "TX"


# ---------------------------------------------------------------------------
# Mock response data
# ---------------------------------------------------------------------------

MOCK_LEVEL1 = {
    "level": "LV1",
    "overall_result": "PASS",
    "confidence": 0.92,
    "flags": [
        {"check": "image_resolution", "status": "PASS", "detail": "Sufficient resolution"},
        {"check": "required_fields_present", "status": "PASS", "detail": "All fields found"},
        {"check": "dob_format", "status": "PASS", "detail": "MM/DD/YYYY confirmed"},
        {"check": "license_number_length", "status": "PASS", "detail": "Length matched"},
        {"check": "layout_field_order", "status": "PASS", "detail": "Name at top"},
    ],
    "fraud_case_reference": (
        "Brooklyn $2.1M — AI fake IDs fooled notaries on visual inspection"
    ),
}

MOCK_LEVEL2 = {
    "level": "LV2",
    "extraction_confidence": 0.87,
    "fields": {
        "first_name": "Jane",
        "last_name": "Doe",
        "middle_name": "Marie",
        "dob": "1985-04-12",
        "id_number": "D12345678",
        "expiration": "2028-06-15",
        "address": "1420 Elm St Denver CO 80203",
        "license_class": "D",
        "issuing_state": "CO",
        "id_type": "drivers_license",
    },
    "uncertain_fields": [],
}

MOCK_LEVEL3 = {
    "level": "LV3",
    "overall_identity_match": "MATCH",
    "fields": [
        {
            "field": "first_name",
            "id_value": "Jane",
            "doc_value": "Jane",
            "match": True,
            "confidence": 1.0,
            "flag": "MATCH",
        },
        {
            "field": "last_name",
            "id_value": "Doe",
            "doc_value": "Doe",
            "match": True,
            "confidence": 1.0,
            "flag": "MATCH",
        },
        {
            "field": "dob",
            "id_value": "1985-04-12",
            "doc_value": "1985-04-12",
            "match": True,
            "confidence": 1.0,
            "flag": "MATCH",
        },
        {
            "field": "address",
            "id_value": "1420 Elm St Denver CO 80203",
            "doc_value": "1420 Elm St Denver CO 80203",
            "match": True,
            "confidence": 0.98,
            "flag": "MATCH",
        },
    ],
    "fraud_case_reference": (
        "Ohio Salone v. Stovall — name/address mismatch across pages went undetected"
    ),
}

MOCK_LEVEL4 = {
    "level": "LV4",
    "overall_compliance": "PASS",
    "checks": [
        {
            "rule": "id_expiration",
            "status": "PASS",
            "detail": "Expires 2028-06-15 — 800 days remaining",
            "citation": "NIST SP 800-63-3 IAL2",
        },
        {
            "rule": "instate_requirement",
            "status": "PASS",
            "detail": "N/A — no in-state requirement",
            "citation": "TX/FL in-state ID requirement",
        },
        {
            "rule": "mismo_recording",
            "status": "PASS",
            "detail": "ID type and expiration present",
            "citation": "MISMO standard",
        },
        {
            "rule": "notary_commission",
            "status": "PASS",
            "detail": "Commission valid until 2026-12-31",
            "citation": "State Notary Public Act",
        },
    ],
    "fraud_case_reference": (
        "Queens NY $1.5M — complicit notary with lapsed commission notarized forged deed"
    ),
    "compliance_note": (
        "Compliance rules reflect guide specification for demo purposes "
        "(Notary Everyday x VillageHacks 2026)"
    ),
}

MOCK_DECISION = {
    "final_decision": "PASS",
    "decision_reasons": [],
    "recommended_action": "Proceed with notarization",
}

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/verify/level1")
def verify_level1(body: Level1Request) -> dict:
    # Decode image (available for future use when stub is implemented)
    _image_bytes = base64.b64decode(body.image)
    # check_authenticity(_image_bytes) — not called yet
    return MOCK_LEVEL1


@app.post("/api/v1/verify/level2")
def verify_level2(body: Level2Request) -> dict:
    _image_bytes = base64.b64decode(body.image)
    # extract_fields(_image_bytes) — not called yet
    return MOCK_LEVEL2


@app.post("/api/v1/verify/level3")
def verify_level3(body: Level3Request) -> dict:
    _image_bytes = base64.b64decode(body.image)
    # match_documents({}, body.form1003) — not called yet
    return MOCK_LEVEL3


@app.post("/api/v1/verify/level4")
def verify_level4(body: Level4Request) -> dict:
    _image_bytes = base64.b64decode(body.image)
    # check_compliance({}, body.property_state) — not called yet
    return MOCK_LEVEL4


@app.post("/api/v1/verify/full")
def verify_full(body: FullRequest) -> dict:
    _image_bytes = base64.b64decode(body.image)
    return {
        **MOCK_LEVEL1,
        **MOCK_LEVEL2,
        **MOCK_LEVEL3,
        **MOCK_LEVEL4,
        "decision": MOCK_DECISION,
    }
