"""
Compliance Engine
===================
Step 4 of the pipeline. For a given bidder, this engine:

  1. Fetches portal/mock-API data for all 6 checks (Step 2)
  2. Fetches AI-extracted document data (Step 3)
  3. CROSS-CHECKS extracted document fields against portal records
     (e.g. does the GSTIN on the uploaded certificate match GSTN's record?)
  4. Flags any mismatches or missing information
  5. Computes the overall Compliance Score + Risk Level (scoring.py)
  6. Generates a plain-English AI recommendation for the Procurement Officer
  7. Returns the final "Compliance Assessment" object (matches Step 1 schema)

This is where genuine AI/compliance value is added — simply calling 6 APIs
and averaging scores would just be a dashboard. Cross-checking documents
against portals to CATCH DISCREPANCIES is the actual decision-support value.
"""

import sys
import os
import json
from datetime import datetime, timezone
import importlib.util


def _load_module(module_name: str, file_path: str):
    """Load a module from an explicit file path under a unique name,
    avoiding collisions with other files also named 'main.py'."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

_mock_apis_path = os.path.join(_THIS_DIR, "mock_apis", "main.py")
mock_apis = _load_module("mock_apis_server", _mock_apis_path)

_scoring_path = os.path.join(_THIS_DIR, "scoring.py")
scoring_module = _load_module("scoring_module", _scoring_path)
compute_score_and_risk = scoring_module.compute_score_and_risk

mock_app = mock_apis.app
BY_BIDDER_ID = mock_apis.BY_BIDDER_ID
from fastapi.testclient import TestClient

mock_client = TestClient(mock_app)


# ---------------------------------------------------------------------------
# 1. Fetch portal data (calls the mock APIs from Step 2)
# ---------------------------------------------------------------------------
def fetch_portal_data(bidder_id: str) -> dict:
    r = mock_client.get(f"/mock/verify-all/{bidder_id}")
    if r.status_code != 200:
        raise ValueError(f"Bidder {bidder_id} not found in portal records")
    return r.json()


# ---------------------------------------------------------------------------
# 2. Fetch AI-extracted document data
#
# NOTE: In production this calls extract_document.py (Step 3) on the
# bidder's actual uploaded PDFs via the Claude API. This sandbox has no
# live ANTHROPIC_API_KEY, so we simulate realistic extraction output here
# — including occasionally injecting a mismatch, exactly like a real
# bidder submitting a slightly outdated or mistyped document would.
# Swap this function for real extract_document.py calls once your team
# has an API key configured — the rest of the engine does not change.
# ---------------------------------------------------------------------------
def simulate_document_extraction(bidder_id: str, inject_mismatch: bool = False) -> dict:
    bidder = BY_BIDDER_ID.get(bidder_id)
    if not bidder:
        raise ValueError(f"Bidder {bidder_id} not found")

    gstin = bidder["gstin"]
    pan = bidder["pan"]
    udyam = bidder["udyam_number"]

    if inject_mismatch:
        # simulate a bidder uploading a certificate with a typo / outdated GSTIN
        gstin = gstin[:-1] + ("9" if gstin[-1] != "9" else "8")

    return {
        "gstin": gstin,
        "pan": pan,
        "udyam_number": udyam,
        "legal_name": bidder["company_name"],
        "extraction_confidence": 0.95,
        "extraction_status": "SUCCESS",
    }


# ---------------------------------------------------------------------------
# 3. Cross-check extracted document fields vs portal records
# ---------------------------------------------------------------------------
def cross_check(document_data: dict, portal_data: dict) -> list[str]:
    flags = []

    if document_data.get("gstin") != portal_data.get("gstin"):
        flags.append(
            f"GSTIN mismatch: document shows '{document_data.get('gstin')}', "
            f"GSTN portal record shows '{portal_data.get('gstin')}'"
        )

    if document_data.get("pan") != portal_data.get("pan"):
        flags.append(
            f"PAN mismatch: document shows '{document_data.get('pan')}', "
            f"portal record shows '{portal_data.get('pan')}'"
        )

    if document_data.get("udyam_number") != portal_data.get("udyam_number"):
        flags.append(
            f"Udyam number mismatch: document shows '{document_data.get('udyam_number')}', "
            f"portal record shows '{portal_data.get('udyam_number')}'"
        )

    return flags


# ---------------------------------------------------------------------------
# 4. Generate a plain-English AI recommendation
#    (template-based here; swap for an LLM call for more natural language
#     once you have an API key — same idea as extract_document.py)
# ---------------------------------------------------------------------------
def generate_recommendation(check_results: list[dict], mismatch_flags: list[str], risk_level: str) -> str:
    non_compliant = [c["check_type"].replace("_", " ").title() for c in check_results if c["status"] == "NON_COMPLIANT"]
    partial = [c["check_type"].replace("_", " ").title() for c in check_results if c["status"] == "PARTIAL"]

    if risk_level == "LOW" and not non_compliant and not mismatch_flags:
        return ("Bidder appears fully compliant across all verified statutory and eligibility "
                "requirements. No document-portal mismatches detected. Recommended for qualification, "
                "subject to Procurement Officer's final review.")

    parts = []
    if non_compliant:
        parts.append(f"Non-compliant on: {', '.join(non_compliant)}")
    if partial:
        parts.append(f"Partial compliance flagged on: {', '.join(partial)}")
    if mismatch_flags:
        parts.append(f"{len(mismatch_flags)} document-vs-portal discrepancy(ies) found")

    detail = "; ".join(parts)

    if risk_level == "HIGH":
        return (f"HIGH RISK — {detail}. Recommend detailed manual review before qualification; "
                f"one or more issues may be disqualifying under GeM terms.")
    else:
        return (f"MEDIUM RISK — {detail}. Bidder may still qualify but these items need "
                f"Procurement Officer clarification/verification before final decision.")


# ---------------------------------------------------------------------------
# 5. Main entry point — runs the full engine for one bidder
# ---------------------------------------------------------------------------
def run_compliance_check(bidder_id: str, inject_mismatch_for_demo: bool = False) -> dict:
    portal_data = fetch_portal_data(bidder_id)
    document_data = simulate_document_extraction(bidder_id, inject_mismatch=inject_mismatch_for_demo)

    mismatch_flags = cross_check(document_data, portal_data)

    check_results = [
        {"check_type": ct, "status": info["status"], "details": info["details"]}
        for ct, info in portal_data["checks"].items()
    ]

    score, risk = compute_score_and_risk(check_results, mismatch_count=len(mismatch_flags))
    recommendation = generate_recommendation(check_results, mismatch_flags, risk)

    pending = [f for f in mismatch_flags]
    for c in check_results:
        if c["status"] in ("NON_COMPLIANT", "PARTIAL"):
            pending.append(f"{c['check_type'].replace('_', ' ').title()} needs review ({c['status']})")

    assessment = {
        "bidder_id": bidder_id,
        "company_name": portal_data["company_name"],
        "bid_id": None,
        "compliance_score": score,
        "risk_level": risk,
        "check_summary": [{"check_type": c["check_type"], "status": c["status"]} for c in check_results],
        "document_portal_mismatches": mismatch_flags,
        "ai_recommendation": recommendation,
        "pending_requirements": pending,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    return assessment


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 engine.py <bidder_id> [--inject-mismatch]")
        sys.exit(1)

    bidder_id = sys.argv[1]
    inject = "--inject-mismatch" in sys.argv

    result = run_compliance_check(bidder_id, inject_mismatch_for_demo=inject)
    print(json.dumps(result, indent=2))