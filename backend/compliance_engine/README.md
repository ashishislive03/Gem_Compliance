# Compliance Engine — Step 4 (Day 4)

## What this does
For a given bidder, this engine:
1. Fetches portal/mock-API data for all 6 checks (calls Step 2's mock APIs)
2. Fetches AI-extracted document data (calls Step 3's extraction module)
3. **Cross-checks** document values against portal records (catches GSTIN/PAN/Udyam mismatches)
4. Computes overall **Compliance Score** and **Risk Level** (`scoring.py`)
5. Generates a plain-English **AI Recommendation** for the officer
6. Returns the final assessment object matching the Step 1 schema

## Files
| File | Purpose |
|---|---|
| `scoring.py` | Pure weighted scoring + risk classification logic |
| `engine.py` | Main engine: fetches data, cross-checks, scores, recommends |

## Setup
Place this folder alongside `mock_apis/` and `bidders.json` (or copy them
in, as done here):
```
compliance_engine/
├── engine.py
├── scoring.py
├── mock_apis/main.py     (copy from Step 2)
└── bidders.json          (copy from Step 2)
```

## Run it
```bash
python3 engine.py BID-00001                    # clean bidder
python3 engine.py BID-00011                    # blacklisted bidder
python3 engine.py BID-00001 --inject-mismatch  # demo: forces a fake GSTIN mismatch
```

## Tested results (already verified in this sandbox)

| Bidder | Profile | Score | Risk | Notes |
|---|---|---|---|---|
| BID-00001 | Clean | 100 | LOW | All 6 checks compliant |
| BID-00005 | Minor issues | 78 | MEDIUM | ITR delay + local content below threshold, correctly flagged |
| BID-00011 | Blacklisted | 15 | HIGH | Score hard-capped due to blacklist, regardless of other checks |
| BID-00001 + injected mismatch | Clean docs, tampered GSTIN | 90 | LOW→MEDIUM | Engine catches the exact mismatch and shows both values |

**This last test is your strongest demo moment** — it proves the platform
catches a bidder submitting a document that doesn't match the government
record, which is exactly the kind of error/fraud manual review is prone to
miss.

## Important note on this sandbox
`simulate_document_extraction()` in `engine.py` currently **simulates** what
real AI document extraction (Step 3) would return, since this sandbox has
no live `ANTHROPIC_API_KEY`. Once your team has a key, replace that function
with an actual call to `extract_document.py`'s `extract_document()` — the
rest of the engine (cross-check, scoring, recommendation) needs **zero
changes**, since it just expects a dict with `gstin`, `pan`, `udyam_number`.

## Next Step (Day 5)
Build the **Dashboard (frontend)**: a React UI where the officer sees
the compliance score, risk level badge, the check-by-check breakdown,
any document-portal mismatches highlighted, the AI recommendation text,
and a final "Qualify / Disqualify / Request Clarification" decision button.