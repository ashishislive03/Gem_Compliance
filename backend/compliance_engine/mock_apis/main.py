"""
Mock Government Portal APIs
============================
Simulates GSTN, PAN/Income Tax, Udyam, EPFO/ESIC, Make in India, and
Blacklist/Debarment verification services, backed by the synthetic
bidders.json dataset generated in Step 2.

Each endpoint is designed to mimic the *shape* a real government API
response would have, so swapping a mock endpoint for a real one later
only requires changing the URL, not your backend logic.

Run:
    cd mock_apis
    uvicorn main:app --reload --port 8001

Then visit http://localhost:8001/docs for interactive Swagger UI.
"""

import json
import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Mock Government Portal APIs",
    description="Simulated GSTN / PAN / Udyam / EPFO / MII / Blacklist verification services for the GeM Bid Compliance Platform prototype.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Load synthetic dataset once at startup
# ---------------------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "bidders.json")

with open(DATA_PATH, "r") as f:
    BIDDERS = json.load(f)

# Build quick lookup indexes
BY_GSTIN = {b["gstin"]: b for b in BIDDERS}
BY_PAN = {b["pan"]: b for b in BIDDERS}
BY_UDYAM = {b["udyam_number"]: b for b in BIDDERS}
BY_BIDDER_ID = {b["bidder_id"]: b for b in BIDDERS}


def get_check(bidder: dict, check_type: str) -> Optional[dict]:
    for c in bidder["compliance_checks"]:
        if c["check_type"] == check_type:
            return c
    return None


def now_iso():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def not_found(field_name: str, value: str):
    raise HTTPException(
        status_code=404,
        detail=f"No record found for {field_name}='{value}'. This mock simulates a real portal's 'not found' response."
    )


# ---------------------------------------------------------------------------
# 1. GSTN Mock API
# ---------------------------------------------------------------------------
@app.get("/mock/gst/verify", tags=["GSTN"])
def verify_gst(gstin: str = Query(..., description="15-character GSTIN")):
    bidder = BY_GSTIN.get(gstin)
    if not bidder:
        not_found("gstin", gstin)
    check = get_check(bidder, "GST_COMPLIANCE")
    return {
        "source": "MOCK_GSTN_API",
        "gstin": gstin,
        "legal_name": bidder["company_name"],
        "status": check["status"],
        "details": check["details"],
        "checked_at": now_iso()
    }


# ---------------------------------------------------------------------------
# 2. PAN / Income Tax Mock API
# ---------------------------------------------------------------------------
@app.get("/mock/pan/verify", tags=["PAN / Income Tax"])
def verify_pan(pan: str = Query(..., description="10-character PAN")):
    bidder = BY_PAN.get(pan)
    if not bidder:
        not_found("pan", pan)
    check = get_check(bidder, "PAN_ITR_COMPLIANCE")
    return {
        "source": "MOCK_PAN_ITR_API",
        "pan": pan,
        "name_on_pan": bidder["company_name"],
        "status": check["status"],
        "details": check["details"],
        "checked_at": now_iso()
    }


# ---------------------------------------------------------------------------
# 3. Udyam / MSME Mock API
# ---------------------------------------------------------------------------
@app.get("/mock/udyam/verify", tags=["Udyam / MSME"])
def verify_udyam(udyam_number: str = Query(..., description="Udyam Registration Number")):
    bidder = BY_UDYAM.get(udyam_number)
    if not bidder:
        not_found("udyam_number", udyam_number)
    check = get_check(bidder, "UDYAM_MSME")
    return {
        "source": "MOCK_UDYAM_API",
        "udyam_number": udyam_number,
        "enterprise_name": bidder["company_name"],
        "category": bidder["msme_category"],
        "status": check["status"],
        "details": check["details"],
        "checked_at": now_iso()
    }


# ---------------------------------------------------------------------------
# 4. EPFO / ESIC Mock API
# ---------------------------------------------------------------------------
@app.get("/mock/epfo/verify", tags=["EPFO / ESIC"])
def verify_epfo(bidder_id: str = Query(..., description="Internal bidder ID (real portal would use establishment code)")):
    bidder = BY_BIDDER_ID.get(bidder_id)
    if not bidder:
        not_found("bidder_id", bidder_id)
    check = get_check(bidder, "EPFO_ESIC_COMPLIANCE")
    return {
        "source": "MOCK_EPFO_ESIC_API",
        "bidder_id": bidder_id,
        "status": check["status"],
        "details": check["details"],
        "checked_at": now_iso()
    }


# ---------------------------------------------------------------------------
# 5. Make in India / Local Content Mock API
# ---------------------------------------------------------------------------
@app.get("/mock/makeinindia/verify", tags=["Make in India"])
def verify_local_content(bidder_id: str = Query(...)):
    bidder = BY_BIDDER_ID.get(bidder_id)
    if not bidder:
        not_found("bidder_id", bidder_id)
    check = get_check(bidder, "MAKE_IN_INDIA_LOCAL_CONTENT")
    return {
        "source": "MOCK_MAKE_IN_INDIA_API",
        "bidder_id": bidder_id,
        "status": check["status"],
        "details": check["details"],
        "checked_at": now_iso()
    }


# ---------------------------------------------------------------------------
# 6. Blacklist / Debarment Mock API
# ---------------------------------------------------------------------------
@app.get("/mock/blacklist/verify", tags=["Blacklist / Debarment"])
def verify_blacklist(bidder_id: str = Query(...)):
    bidder = BY_BIDDER_ID.get(bidder_id)
    if not bidder:
        not_found("bidder_id", bidder_id)
    check = get_check(bidder, "BLACKLIST_DEBARMENT")
    return {
        "source": "MOCK_BLACKLIST_REGISTRY_API",
        "bidder_id": bidder_id,
        "status": check["status"],
        "details": check["details"],
        "checked_at": now_iso()
    }


# ---------------------------------------------------------------------------
# 7. Combined convenience endpoint — fetch ALL portal checks for one bidder
#    in a single call (this is what your compliance engine will mainly use)
# ---------------------------------------------------------------------------
@app.get("/mock/verify-all/{bidder_id}", tags=["Combined"])
def verify_all(bidder_id: str):
    bidder = BY_BIDDER_ID.get(bidder_id)
    if not bidder:
        not_found("bidder_id", bidder_id)

    results = {}
    for check in bidder["compliance_checks"]:
        results[check["check_type"]] = {
            "status": check["status"],
            "details": check["details"]
        }

    return {
        "bidder_id": bidder_id,
        "company_name": bidder["company_name"],
        "gstin": bidder["gstin"],
        "pan": bidder["pan"],
        "udyam_number": bidder["udyam_number"],
        "checks": results,
        "checked_at": now_iso()
    }


# ---------------------------------------------------------------------------
# 8. Utility: list all bidders (so your frontend/dropdown can populate itself)
# ---------------------------------------------------------------------------
@app.get("/mock/bidders", tags=["Utility"])
def list_bidders(limit: int = 20, offset: int = 0):
    subset = BIDDERS[offset: offset + limit]
    return {
        "total": len(BIDDERS),
        "count": len(subset),
        "bidders": [
            {
                "bidder_id": b["bidder_id"],
                "company_name": b["company_name"],
                "gstin": b["gstin"],
                "pan": b["pan"],
                "udyam_number": b["udyam_number"],
                "bid_id": b["bid_id"]
            } for b in subset
        ]
    }


@app.get("/", tags=["Utility"])
def root():
    return {
        "message": "Mock Government Portal APIs are running.",
        "docs": "/docs",
        "endpoints": [
            "/mock/gst/verify?gstin=...",
            "/mock/pan/verify?pan=...",
            "/mock/udyam/verify?udyam_number=...",
            "/mock/epfo/verify?bidder_id=...",
            "/mock/makeinindia/verify?bidder_id=...",
            "/mock/blacklist/verify?bidder_id=...",
            "/mock/verify-all/{bidder_id}",
            "/mock/bidders?limit=20&offset=0"
        ]
    }