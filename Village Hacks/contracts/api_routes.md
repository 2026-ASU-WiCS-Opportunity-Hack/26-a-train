# NotaryGuard API Routes — Contract v1

Base URL: `http://localhost:8000/api/v1`

All endpoints accept `Content-Type: application/json`.
All responses return `Content-Type: application/json`.

---

## POST /api/v1/verify/level1
**Description:** Document Authenticity Check — regex + heuristics, no ML.

**Request Body:**
```json
{
  "image": "<base64-encoded PNG/JPEG>"
}
```

**Response Shape:**
```json
{
  "level": "LV1",
  "overall_result": "PASS | REVIEW | FAIL",
  "confidence": 0.0,
  "flags": [
    { "check": "image_resolution",       "status": "PASS | WARN | FAIL", "detail": "..." },
    { "check": "required_fields_present","status": "PASS | WARN | FAIL", "detail": "..." },
    { "check": "dob_format",             "status": "PASS | WARN | FAIL", "detail": "..." },
    { "check": "license_number_length",  "status": "PASS | WARN | FAIL", "detail": "..." },
    { "check": "layout_field_order",     "status": "PASS | WARN | FAIL", "detail": "..." }
  ],
  "fraud_case_reference": "..."
}
```

---

## POST /api/v1/verify/level2
**Description:** Field Extraction & Structuring via PaddleOCR + post-processing pipeline.

**Request Body:**
```json
{
  "image": "<base64-encoded PNG/JPEG>"
}
```

**Response Shape:**
```json
{
  "level": "LV2",
  "extraction_confidence": 0.0,
  "fields": {
    "first_name":    "string | null",
    "last_name":     "string | null",
    "middle_name":   "string | null",
    "dob":           "YYYY-MM-DD | null",
    "id_number":     "string | null",
    "expiration":    "YYYY-MM-DD | null",
    "address":       "string | null",
    "license_class": "string | null",
    "issuing_state": "string | null",
    "id_type":       "string | null"
  },
  "uncertain_fields": ["field_name", "..."]
}
```

---

## POST /api/v1/verify/level3
**Description:** Cross-Document Identity Match — fuzzy logic + nickname map.

**Request Body:**
```json
{
  "image": "<base64-encoded PNG/JPEG>",
  "form1003": {
    "borrower_first_name": "string",
    "borrower_last_name":  "string",
    "borrower_dob":        "YYYY-MM-DD",
    "borrower_address":    "string",
    "property_state":      "XX"
  }
}
```

**Response Shape:**
```json
{
  "level": "LV3",
  "overall_identity_match": "MATCH | PARTIAL_MATCH | MISMATCH",
  "fields": [
    {
      "field":      "first_name | last_name | dob | address",
      "id_value":   "string",
      "doc_value":  "string",
      "match":      true,
      "confidence": 0.0,
      "flag":       "MATCH | PARTIAL_MATCH | MISMATCH | NOT_FOUND"
    }
  ],
  "fraud_case_reference": "..."
}
```

---

## POST /api/v1/verify/level4
**Description:** Expiration & Compliance Flagging — rules engine, config-driven commission check.

**Request Body:**
```json
{
  "image": "<base64-encoded PNG/JPEG>",
  "property_state": "XX"
}
```

**Response Shape:**
```json
{
  "level": "LV4",
  "overall_compliance": "PASS | REVIEW | FAIL",
  "checks": [
    {
      "rule":     "id_expiration | instate_requirement | mismo_recording | notary_commission",
      "status":   "PASS | WARN | FAIL",
      "detail":   "...",
      "citation": "..."
    }
  ],
  "fraud_case_reference": "...",
  "compliance_note": "..."
}
```

---

## POST /api/v1/verify/full
**Description:** Runs all 4 levels and returns a final decision.

**Request Body:**
```json
{
  "image": "<base64-encoded PNG/JPEG>",
  "form1003": {
    "borrower_first_name": "string",
    "borrower_last_name":  "string",
    "borrower_dob":        "YYYY-MM-DD",
    "borrower_address":    "string",
    "property_state":      "XX"
  },
  "property_state": "XX"
}
```

**Response Shape:**
```json
{
  "lv1": "<level1 shape>",
  "lv2": "<level2 shape>",
  "lv3": "<level3 shape>",
  "lv4": "<level4 shape>",
  "decision": {
    "final_decision":     "PASS | REVIEW | FAIL",
    "decision_reasons":   ["..."],
    "recommended_action": "..."
  }
}
```

---

## GET /health
**Response:** `{ "status": "ok" }`

---

## Decision Rules

### FAIL if ANY:
- DOB mismatch (LV3)
- ID expired > 5 years (LV4)
- Notary commission expired (LV4)
- Required fields missing (LV1)
- TX/FL out-of-state ID violation (LV4)

### REVIEW if ANY (and no FAIL):
- Name PARTIAL_MATCH (LV3)
- ID expiring within 30 days (LV4)
- ID expired within 5 years (LV4)
- LV1 SUSPICIOUS flags

### PASS:
- All checks clean
