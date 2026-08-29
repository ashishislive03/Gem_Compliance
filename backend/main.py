"""
Main Backend API — Day 6
==========================
This is the single backend your React frontend talks to. It ties together:
  - Mock Government Portal APIs (Step 2)
  - Compliance Engine (Step 4)
  - Audit Trail logging (new, this step)

Endpoints the frontend uses:
  GET  /api/bidders                    -> list of bidders (for sidebar)
  GET  /api/bidders/{bidder_id}/assessment  -> full compliance assessment (for main panel)
  POST /api/bidders/{bidder_id}/decision    -> officer records Qualify/Disqualify/Clarify
  GET  /api/bidders/{bidder_id}/audit-log   -> audit trail for that bidder

Run:
    cd backend
    uvicorn main:app --reload --port 8000

CORS is open so your Vite frontend (usually http://localhost:5173) can call it directly.
"""

import sys
import os
import json
import sqlite3
import importlib.util
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


def _load_module(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_engine_path = os.path.join(os.path.dirname(__file__), "compliance_engine", "engine.py")
engine_module = _load_module("compliance_engine_module", _engine_path)
run_compliance_check = engine_module.run_compliance_check
BIDDERS = engine_module.mock_apis.BIDDERS

app = FastAPI(title="GeM Bid Compliance Platform — Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "audit_trail.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bidder_id TEXT,
            action TEXT,
            performed_by TEXT,
            details TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


def log_action(bidder_id: str, action: str, performed_by: str, details: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO audit_logs (bidder_id, action, performed_by, details, timestamp) VALUES (?, ?, ?, ?, ?)",
        (bidder_id, action, performed_by, details, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    )
    conn.commit()
    conn.close()


init_db()


class DecisionRequest(BaseModel):
    decision: str  # "Qualified" | "Disqualified" | "Clarification requested"
    officer_name: str = "Procurement Officer"
    remarks: Optional[str] = None


@app.get("/api/bidders")
def list_bidders(limit: int = 50, offset: int = 0):
    subset = BIDDERS[offset: offset + limit]
    return {
        "total": len(BIDDERS),
        "bidders": [
            {
                "bidder_id": b["bidder_id"],
                "company_name": b["company_name"],
                "bid_id": b["bid_id"],
            } for b in subset
        ]
    }


@app.get("/api/bidders/{bidder_id}/assessment")
def get_assessment(bidder_id: str, inject_mismatch: bool = False):
    try:
        assessment = run_compliance_check(bidder_id, inject_mismatch_for_demo=inject_mismatch)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Bidder {bidder_id} not found")

    log_action(
        bidder_id, "COMPLIANCE_CHECK_PERFORMED", "SYSTEM_AI",
        f"Score={assessment['compliance_score']}, Risk={assessment['risk_level']}, "
        f"Mismatches={len(assessment['document_portal_mismatches'])}"
    )
    return assessment


@app.post("/api/bidders/{bidder_id}/decision")
def record_decision(bidder_id: str, req: DecisionRequest):
    if req.decision not in ("Qualified", "Disqualified", "Clarification requested"):
        raise HTTPException(status_code=400, detail="Invalid decision value")

    log_action(
        bidder_id, f"OFFICER_DECISION_{req.decision.upper().replace(' ', '_')}",
        req.officer_name, req.remarks or "No remarks provided"
    )
    return {
        "bidder_id": bidder_id,
        "decision": req.decision,
        "recorded_by": req.officer_name,
        "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }


@app.get("/api/bidders/{bidder_id}/audit-log")
def get_audit_log(bidder_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM audit_logs WHERE bidder_id = ? ORDER BY timestamp DESC", (bidder_id,)
    ).fetchall()
    conn.close()
    return {"bidder_id": bidder_id, "logs": [dict(r) for r in rows]}


@app.get("/")
def root():
    return {"message": "GeM Bid Compliance Backend running.", "docs": "/docs"}