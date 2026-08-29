import React from "react";
import { ShieldCheck, ShieldAlert, ShieldX } from "lucide-react";

const RISK_STYLES = {
  LOW: { color: "#1B7F5C", bg: "bg-[#1B7F5C]/[0.06]", border: "border-[#1B7F5C]/25", text: "text-[#1B7F5C]", icon: ShieldCheck },
  MEDIUM: { color: "#A8681E", bg: "bg-[#A8681E]/[0.06]", border: "border-[#A8681E]/25", text: "text-[#A8681E]", icon: ShieldAlert },
  HIGH: { color: "#B3261E", bg: "bg-[#B3261E]/[0.06]", border: "border-[#B3261E]/25", text: "text-[#B3261E]", icon: ShieldX },
};

function ScoreRing({ score, strokeColor }) {
  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="relative w-32 h-32 flex items-center justify-center shrink-0">
      <svg className="w-32 h-32 -rotate-90">
        <circle cx="64" cy="64" r="54" stroke="#E2DFD5" strokeWidth="8" fill="none" />
        <circle
          cx="64" cy="64" r="54" stroke={strokeColor} strokeWidth="8" fill="none"
          strokeDasharray={circumference} strokeDashoffset={offset} strokeLinecap="round"
          style={{ transition: "stroke-dashoffset 0.6s ease" }}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="font-serif text-3xl text-[#16213E]">{score}</span>
        <span className="font-mono text-[10px] text-[#16213E]/40">/ 100</span>
      </div>
    </div>
  );
}

export default function ScoreCard({ score, riskLevel }) {
  const style = RISK_STYLES[riskLevel];
  const Icon = style.icon;

  return (
    <div className={`rounded-sm border ${style.border} ${style.bg} p-6 flex items-center gap-6`}>
      <ScoreRing score={score} strokeColor={style.color} />
      <div>
        <div className={`inline-flex items-center gap-1.5 font-mono text-xs tracking-widest ${style.text} mb-2`}>
          <Icon size={16} />
          {riskLevel} RISK
        </div>
        <p className="text-sm text-[#16213E]/60 max-w-sm leading-relaxed">
          Compliance score reflects weighted results across six statutory checks,
          with document-to-portal cross-verification.
        </p>
      </div>
    </div>
  );
}