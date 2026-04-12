from datetime import date

DEMO_MODE = {
    "notary_commission": {
        "expiry": "2026-12-31",   # PASS path   ← active by default
        # "expiry": "2025-11-15", # FAIL path   ← uncomment to demo failure
        # "expiry": "2026-04-20", # REVIEW path ← uncomment to demo warning
        "notary_name": "Demo Notary — John Rivera"
    }
}

STATE_ID_LENGTHS = {
    "CO": 9,
    "TX": 8,
    "CA": 7,
    "FL": 13,
    "NY": 9,
}

INSTATE_REQUIRED_STATES = ["TX", "FL"]
