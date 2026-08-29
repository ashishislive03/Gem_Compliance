import { useState, useEffect } from "react";

const API_BASE = "http://localhost:8000/api";

export function useBidders() {
  const [bidders, setBidders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`${API_BASE}/bidders`)
      .then((r) => {
        if (!r.ok) throw new Error("Failed to load bidders");
        return r.json();
      })
      .then((d) => setBidders(d.bidders))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return { bidders, loading, error };
}

export function useAssessment(bidderId) {
  const [assessment, setAssessment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!bidderId) return;
    setLoading(true);
    setError(null);
    fetch(`${API_BASE}/bidders/${bidderId}/assessment`)
      .then((r) => {
        if (!r.ok) throw new Error("Could not load compliance assessment");
        return r.json();
      })
      .then(setAssessment)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [bidderId]);

  return { assessment, loading, error };
}

export function useAuditLog(bidderId, refreshKey) {
  const [logs, setLogs] = useState([]);
  useEffect(() => {
    if (!bidderId) return;
    fetch(`${API_BASE}/bidders/${bidderId}/audit-log`)
      .then((r) => r.json())
      .then((d) => setLogs(d.logs || []))
      .catch(() => setLogs([]));
  }, [bidderId, refreshKey]);
  return logs;
}

export async function postDecision(bidderId, decision, officerName = "Procurement Officer") {
  const res = await fetch(`${API_BASE}/bidders/${bidderId}/decision`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ decision, officer_name: officerName }),
  });
  if (!res.ok) throw new Error("Could not record decision");
  return res.json();
}