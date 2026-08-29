import React, { useState } from "react";
import { History, ChevronDown } from "lucide-react";

export default function AuditTrail({ logs }) {
  const [open, setOpen] = useState(false);
  if (!logs.length) return null;

  return (
    <div className="bg-white rounded-sm border border-[#E2DFD5]">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-5 py-3.5"
      >
        <span className="flex items-center gap-2 font-mono text-[11px] tracking-widest text-[#16213E]/40">
          <History size={13} />
          AUDIT TRAIL ({logs.length})
        </span>
        <ChevronDown size={15} className={`text-[#16213E]/30 transition-transform ${open ? "rotate-180" : ""}`} />
      </button>
      {open && (
        <div className="border-t border-[#E2DFD5]">
          {logs.map((log, i) => (
            <div
              key={log.log_id}
              className={`px-5 py-3 ${i !== logs.length - 1 ? "border-b border-[#E2DFD5]/70" : ""}`}
            >
              <div className="flex justify-between items-baseline gap-3">
                <span className="text-sm font-medium text-[#16213E]">
                  {log.action.replaceAll("_", " ")}
                </span>
                <span className="font-mono text-[10.5px] text-[#16213E]/35 shrink-0">
                  {new Date(log.timestamp).toLocaleString()}
                </span>
              </div>
              <p className="text-sm text-[#16213E]/55 mt-0.5">
                by {log.performed_by} — {log.details}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}