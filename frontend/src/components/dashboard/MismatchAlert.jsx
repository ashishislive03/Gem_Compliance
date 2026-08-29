import React from "react";
import { FileWarning } from "lucide-react";

export default function MismatchAlert({ mismatches }) {
  if (!mismatches || mismatches.length === 0) return null;

  return (
    <div className="rounded-sm border border-[#B3261E]/30 bg-[#B3261E]/[0.05] p-4 flex gap-3">
      <FileWarning size={18} className="text-[#B3261E] shrink-0 mt-0.5" />
      <div>
        <p className="text-sm font-medium text-[#B3261E] mb-1.5">Document-portal mismatch detected</p>
        {mismatches.map((m, i) => (
          <p key={i} className="font-mono text-[12.5px] text-[#B3261E]/85 leading-relaxed">{m}</p>
        ))}
      </div>
    </div>
  );
}