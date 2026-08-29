import React from "react";
import SealBadge from "./SealBadge";
import { ArrowRight } from "lucide-react";

const IMPACT = [
  ["60–80%", "reduction in manual verification effort"],
  ["6", "portals replaced by one dashboard"],
  ["100%", "of checks logged to an audit trail"],
];

export default function ImpactSection({ onLaunch }) {
  return (
    <section id="impact" className="bg-[#16213E] text-[#F7F6F1]">
      <div className="max-w-6xl mx-auto px-6 py-20">
        <p className="font-mono text-xs tracking-[0.2em] text-[#C99A54] mb-3">EXPECTED IMPACT</p>
        <h2 className="font-serif text-3xl mb-12 max-w-lg">
          Less time verifying paperwork, more time evaluating bids.
        </h2>

        <div className="grid sm:grid-cols-3 gap-10 mb-16">
          {IMPACT.map(([n, label]) => (
            <div key={label} className="border-t border-[#F7F6F1]/15 pt-5">
              <span className="font-serif text-4xl">{n}</span>
              <p className="text-sm text-[#F7F6F1]/60 mt-2 leading-relaxed">{label}</p>
            </div>
          ))}
        </div>

        <div className="flex flex-col sm:flex-row items-center gap-6 sm:gap-10 border-t border-[#F7F6F1]/15 pt-10">
          <SealBadge size={72} />
          <div className="flex-1">
            <p className="text-[#F7F6F1]/90 font-medium mb-1">AI recommends. Officers decide.</p>
            <p className="text-sm text-[#F7F6F1]/55 max-w-md">
              The platform verifies and flags — the qualification decision always
              stays with the Procurement Officer.
            </p>
          </div>
          <button
            onClick={onLaunch}
            className="inline-flex items-center gap-2 px-5 py-3 rounded-md bg-[#F7F6F1] text-[#16213E] text-sm font-medium hover:bg-white transition-colors shrink-0"
          >
            Open the dashboard
            <ArrowRight size={16} />
          </button>
        </div>
      </div>
    </section>
  );
}