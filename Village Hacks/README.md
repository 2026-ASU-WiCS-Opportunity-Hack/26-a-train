# NotaryGuard — ID Verify AI
**VillageHacks 2026 | Notary Everyday x VillageHacks**

Fraud-aware identity verification rail for Remote Online Notary (RON) platforms.

## Stack
- **Backend:** Python 3.11 + FastAPI + PaddleOCR + python-Levenshtein
- **Frontend:** React + TypeScript + shadcn/ui
- **Free/open-source only**

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Test Data
```bash
python test_data/generator.py   # generates 3 synthetic ID images + form1003 JSONs
```

## 4 Verification Levels

| Level | Name | What it does |
|---|---|---|
| LV1 | Document Authenticity | Regex + heuristics — resolution, field presence, DOB format, layout |
| LV2 | Field Extraction | PaddleOCR pipeline → structured JSON fields |
| LV3 | Cross-Doc Match | Fuzzy match + nickname map vs Form 1003 |
| LV4 | Compliance Flagging | Expiration, in-state rules, notary commission check |

## API
```
POST /api/v1/verify/level1   { image: base64 }
POST /api/v1/verify/level2   { image: base64 }
POST /api/v1/verify/level3   { image: base64, form1003: {...} }
POST /api/v1/verify/level4   { image: base64, property_state: "TX" }
POST /api/v1/verify/full     { image: base64, form1003: {...}, property_state: "TX" }
```

See `contracts/api_routes.md` for full contract. See `contracts/json_schemas.json` for response shapes.

## Demo Mode
Edit `backend/config.py` → `DEMO_MODE["notary_commission"]["expiry"]`:
- `"2026-12-31"` → PASS path (default)
- `"2025-11-15"` → FAIL path
- `"2026-04-20"` → REVIEW path

## Edge Cases Handled
1. ID expiring in 12 days → WARN "⚠ Expiring Soon", never FAIL
2. Out-of-state signer on TX/FL property → FAIL with rule citation
3. "Jennifer" vs "Jen" → nickname map → PARTIAL_MATCH, never MISMATCH
4. Notary commission expired → isolated JSON block, never merged with ID validity

## Fraud Case References
- **Brooklyn $2.1M** — AI fake IDs fooled notaries on visual inspection (LV1)
- **Ohio Salone v. Stovall** — name/address mismatch went undetected (LV3)
- **Queens NY $1.5M** — complicit notary with lapsed commission (LV4)
- **Graceland 2024** — forged signature; font/layout inconsistencies (LV1)

## Repo Structure
```
Village-Hacks/
├── backend/
│   ├── main.py            FastAPI app — 5 routes
│   ├── config.py          DEMO_MODE config
│   ├── requirements.txt
│   └── levels/
│       ├── level1.py      Document Authenticity
│       ├── level2.py      Field Extraction
│       ├── level3.py      Cross-Doc Match
│       └── level4.py      Compliance Flagging
├── frontend/              React + TypeScript
├── contracts/
│   ├── api_routes.md      Full API contract
│   └── json_schemas.json  Response shapes
└── test_data/
    ├── generator.py       Synthetic data (Faker + Pillow)
    ├── pass_case/
    ├── fail_case/
    └── review_case/
```

## Team
Notary Everyday x VillageHacks 2026
