import React from "react";
import { ChevronLeft } from "lucide-react";
import SealBadge from "../SealBadge";

export default function DashboardHeader({ onBack, bidderCount }) {
  return (
    <header className="bg-[#16213E] text-[#F7F6F1]">
      <div className="max-w-[1400px] mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-4">
          {onBack && (
            <button
              onClick={onBack}
              className="flex items-center gap-1 text-xs text-[#F7F6F1]/50 hover:text-[#F7F6F1] transition-colors"
            >
              <ChevronLeft size={14} />
              Home
            </button>
          )}
          <div className="w-px h-5 bg-[#F7F6F1]/15 hidden sm:block" />
          <div className="flex items-center gap-2.5">
            <SealBadge size={28} />
            <span className="font-serif text-[15px] tracking-tight">GeM Compliance Verification</span>
          </div>
        </div>
        <p className="font-mono text-[11px] text-[#F7F6F1]/45 tracking-wide hidden sm:block">
          {bidderCount ? `${bidderCount} BIDDERS · TENDER GEM/2026/B/••••` : "LOADING TENDER DATA"}
        </p>
      </div>
    </header>
  );
}