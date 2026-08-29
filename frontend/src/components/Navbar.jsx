import React from "react";
import SealBadge from "./SealBadge";

export default function Navbar({ onLaunch }) {
  return (
    <header className="sticky top-0 z-30 bg-[#F7F6F1]/90 backdrop-blur border-b border-[#E2DFD5]">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <SealBadge size={34} />
          <span className="font-serif text-[17px] text-[#16213E] tracking-tight">
            GeM Compliance Verification
          </span>
        </div>
        <nav className="hidden md:flex items-center gap-8 text-sm text-[#16213E]/70">
          <a href="#capabilities" className="hover:text-[#16213E] transition-colors">Capabilities</a>
          <a href="#how-it-works" className="hover:text-[#16213E] transition-colors">How it works</a>
          <a href="#impact" className="hover:text-[#16213E] transition-colors">Impact</a>
        </nav>
        <button
          onClick={onLaunch}
          className="px-4 py-2 rounded-md bg-[#16213E] text-[#F7F6F1] text-sm font-medium hover:bg-[#22315A] transition-colors"
        >
          Open dashboard
        </button>
      </div>
    </header>
  );
}