import React, { useState } from "react";
import { CheckCircle2, Loader2, Clock } from "lucide-react";
import { postDecision } from "../../hooks/useCompliance";

export default function DecisionPanel({ bidderId, onDecisionRecorded }) {
  const [decision, setDecision] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  async function handleDecision(value) {
    setSubmitting(true);
    setError(null);
    try {
      await postDecision(bidderId, value);
      setDecision(value);
      onDecisionRecorded?.();
    } catch (e) {
      setError(e.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="bg-white rounded-sm border border-[#E2DFD5] p-5">
      <p className="font-mono text-[11px] tracking-widest text-[#16213E]/40 mb-3">
        PROCUREMENT OFFICER DECISION
      </p>

      {decision ? (
        <div className="rounded-sm border border-[#E2DFD5] bg-[#F7F6F1] p-4 text-sm text-[#16213E]/80 flex items-center gap-2">
          <CheckCircle2 size={16} className="text-[#1B7F5C] shrink-0" />
          Decision recorded: <span className="font-medium text-[#16213E]">{decision}</span> — added to the audit log.
        </div>
      ) : (
        <div>
          <div className="flex flex-col sm:flex-row gap-2">
            <button
              disabled={submitting}
              onClick={() => handleDecision("Qualified")}
              className="flex-1 px-4 py-2.5 rounded-sm bg-[#1B7F5C] text-white text-sm font-medium hover:bg-[#166a4c] transition-colors disabled:opacity-60 flex items-center justify-center gap-2"
            >
              {submitting && <Loader2 size={14} className="animate-spin" />}
              Qualify bidder
            </button>
            <button
              disabled={submitting}
              onClick={() => handleDecision("Clarification requested")}
              className="flex-1 px-4 py-2.5 rounded-sm border border-[#16213E]/25 text-[#16213E] text-sm font-medium hover:bg-[#F7F6F1] transition-colors disabled:opacity-60"
            >
              Request clarification
            </button>
            <button
              disabled={submitting}
              onClick={() => handleDecision("Disqualified")}
              className="flex-1 px-4 py-2.5 rounded-sm border border-[#B3261E]/35 text-[#B3261E] text-sm font-medium hover:bg-[#B3261E]/[0.05] transition-colors disabled:opacity-60"
            >
              Disqualify bidder
            </button>
          </div>
          {error && <p className="text-sm text-[#B3261E] mt-2">{error}</p>}
        </div>
      )}

      <p className="text-xs text-[#16213E]/40 mt-3 flex items-center gap-1.5">
        <Clock size={12} />
        The AI provides decision support only — final qualification decision rests with the officer.
      </p>
    </div>
  );
}