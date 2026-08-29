import React from "react";
import { ArrowRight } from "lucide-react";
import SealBadge from "./SealBadge";

function DocumentMock() {
  return (
    <div className="relative w-full max-w-sm mx-auto">
      <div className="bg-white border border-[#E2DFD5] rounded-sm shadow-[0_1px_0_#E2DFD5,0_12px_32px_-16px_rgba(22,33,62,0.25)] p-6 rotate-[-1.5deg]">
        <p className="font-mono text-[10px] tracking-widest text-[#16213E]/40 mb-4">
          GEM/2026/B/5437923 · BIDDER RECORD
        </p>
        <div className="h-3 w-3/4 bg-[#16213E]/10 rounded-sm mb-2.5" />
        <div className="h-3 w-full bg-[#16213E]/10 rounded-sm mb-2.5" />
        <div className="h-3 w-5/6 bg-[#16213E]/10 rounded-sm mb-5" />
        <div className="grid grid-cols-2 gap-2">
          {["GSTIN", "PAN", "UDYAM", "EPFO"].map((f) => (
            <div key={f} className="border border-[#E2DFD5] rounded-sm px-2 py-1.5">
              <p className="font-mono text-[9px] text-[#16213E]/40">{f}</p>
              <div className="h-2 w-3/4 bg-[#16213E]/10 rounded-sm mt-1" />
            </div>
          ))}
        </div>
      </div>
      {/* Seal stamps onto the corner of the document */}
      <div className="absolute -right-6 -bottom-6 sm:-right-10 sm:-bottom-8">
        <SealBadge size={104} animate />
      </div>
    </div>
  );
}

export default function Hero({ onLaunch }) {
  return (
    <section className="max-w-6xl mx-auto px-6 pt-16 pb-10 md:pt-24 md:pb-16">
      <div className="grid md:grid-cols-2 gap-14 items-center">
        <div>
          <p className="font-mono text-xs tracking-[0.2em] text-[#A8681E] mb-5">
            GeM PROCUREMENT · AI VERIFICATION
          </p>
          <h1 className="font-serif text-4xl sm:text-5xl leading-[1.08] text-[#16213E] mb-6">
            One verified record.
            <br />
            Six government portals.
            <br />
            Zero manual cross-checking.
          </h1>
          <p className="text-[#16213E]/70 text-base leading-relaxed max-w-md mb-8">
            Every bidder's GST, PAN, Udyam, EPFO, local-content and blacklist status —
            checked against the actual portal records and the documents they submitted,
            in the time it takes to open one dashboard.
          </p>
          <div className="flex flex-wrap items-center gap-4">
            <button
              onClick={onLaunch}
              className="inline-flex items-center gap-2 px-5 py-3 rounded-md bg-[#16213E] text-[#F7F6F1] text-sm font-medium hover:bg-[#22315A] transition-colors"
            >
              Open the compliance dashboard
              <ArrowRight size={16} />
            </button>
            <a
              href="#how-it-works"
              className="text-sm font-medium text-[#16213E]/70 hover:text-[#16213E] transition-colors"
            >
              See how it works
            </a>
          </div>
        </div>

        <DocumentMock />
      </div>

      {/* Ledger-style stats strip — real figures, not decorative */}
      <div className="mt-20 border-t border-b border-[#E2DFD5] py-5 flex flex-wrap gap-x-10 gap-y-3 justify-center sm:justify-between text-center sm:text-left">
        {[
          ["6", "statutory checks per bidder"],
          ["150", "bidders in this demo dataset"],
          ["1", "dashboard instead of 6 portals"],
        ].map(([n, label]) => (
          <div key={label}>
            <span className="font-serif text-2xl text-[#16213E]">{n}</span>
            <span className="block font-mono text-[11px] tracking-wide text-[#16213E]/50 mt-0.5">
              {label}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}