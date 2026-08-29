import React from "react";
import SealBadge from "./SealBadge";

export default function Footer() {
  return (
    <footer className="border-t border-[#E2DFD5]">
      <div className="max-w-6xl mx-auto px-6 py-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
        <div className="flex items-center gap-3">
          <SealBadge size={30} />
          <div>
            <p className="text-sm font-medium text-[#16213E]">GeM Compliance Verification</p>
            <p className="text-xs text-[#16213E]/50 mt-0.5">
              Prototype for Smart India Hackathon 2026 — uses simulated portal data.
            </p>
          </div>
        </div>
        <p className="font-mono text-xs text-[#16213E]/40">
          AI-assisted decision support · Final decisions rest with the Procurement Officer
        </p>
      </div>
    </footer>
  );
}