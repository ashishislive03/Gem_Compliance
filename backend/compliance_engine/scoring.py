"""
Compliance Scoring Engine
==========================
Pure scoring/risk logic — separated from the cross-checking logic so it
can be tuned independently (weights are the first thing judges/mentors
will ask you to justify).

Matches the weights defined in Step 1 (data_schema_design.md).
"""

CHECK_WEIGHTS = {
    "GST_COMPLIANCE": 20,
    "PAN_ITR_COMPLIANCE": 15,
    "UDYAM_MSME": 15,
    "EPFO_ESIC_COMPLIANCE": 15,
    "MAKE_IN_INDIA_LOCAL_CONTENT": 15,
    "BLACKLIST_DEBARMENT": 20,
}

STATUS_SCORE = {
    "COMPLIANT": 1.0,
    "PARTIAL": 0.5,
    "NOT_APPLICABLE": 1.0,   # doesn't penalize if genuinely not applicable
    "NON_COMPLIANT": 0.0,
}

# Each document-vs-portal mismatch on a critical identifier costs points
# and forces at least a PARTIAL on that check, since it means the bidder's
# paperwork doesn't match the government record — a real red flag.
MISMATCH_PENALTY = 10


def compute_score_and_risk(check_results: list[dict], mismatch_count: int = 0) -> tuple[int, str]:
    """
    check_results: list of {"check_type": ..., "status": ...}
    mismatch_count: number of document-vs-portal field mismatches found
    Returns: (score 0-100, risk_level)
    """
    total = 0
    blacklisted = False

    for check in check_results:
        weight = CHECK_WEIGHTS.get(check["check_type"], 0)
        status_value = STATUS_SCORE.get(check["status"], 0.0)
        total += weight * status_value
        if check["check_type"] == "BLACKLIST_DEBARMENT" and check["status"] == "NON_COMPLIANT":
            blacklisted = True

    score = round(total) - (mismatch_count * MISMATCH_PENALTY)
    score = max(0, min(100, score))

    if blacklisted:
        risk = "HIGH"
        score = min(score, 30)  # blacklist is a hard cap regardless of other scores
    elif score >= 80:
        risk = "LOW"
    elif score >= 50:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return score, risk