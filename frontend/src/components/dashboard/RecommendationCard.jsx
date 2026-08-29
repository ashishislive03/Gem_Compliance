import React from "react";

export default function RecommendationCard({ recommendation, pendingItems }) {
  return (
    <div className="bg-white rounded-sm border border-[#E2DFD5] p-5">
      <p className="font-mono text-[11px] tracking-widest text-[#A8681E] mb-2">AI RECOMMENDATION</p>
      <p className="text-sm text-[#16213E]/80 leading-relaxed">{recommendation}</p>
      {pendingItems?.length > 0 && (
        <div className="mt-4 pt-4 border-t border-[#E2DFD5]">
          <p className="font-mono text-[10.5px] tracking-widest text-[#16213E]/40 mb-2">PENDING ITEMS</p>
          <ul className="space-y-1.5">
            {pendingItems.map((p, i) => (
              <li key={i} className="text-sm text-[#16213E]/70 flex gap-2">
                <span className="text-[#A8681E]">·</span>{p}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}