import React from "react";
import { CheckCircle2, MinusCircle, XCircle } from "lucide-react";

const CHECK_LABELS = {
  GST_COMPLIANCE: "GST registration & filing",
  PAN_ITR_COMPLIANCE: "PAN & income tax",
  UDYAM_MSME: "Udyam / MSME registration",
  EPFO_ESIC_COMPLIANCE: "EPFO / ESIC",
  MAKE_IN_INDIA_LOCAL_CONTENT: "Make in India / local content",
  BLACKLIST_DEBARMENT: "Blacklist / debarment",
};

const STATUS_STYLES = {
  COMPLIANT: { icon: CheckCircle2, color: "text-[#1B7F5C]", label: "Compliant" },
  PARTIAL: { icon: MinusCircle, color: "text-[#A8681E]", label: "Partial" },
  NON_COMPLIANT: { icon: XCircle, color: "text-[#B3261E]", label: "Non-compliant" },
  NOT_APPLICABLE: { icon: MinusCircle, color: "text-[#16213E]/30", label: "Not applicable" },
};

export default function CheckBreakdown({ checks }) {
  return (
    <div className="bg-white rounded-sm border border-[#E2DFD5]">
      <div className="px-5 pt-4 pb-3 border-b border-[#E2DFD5]">
        <p className="font-mono text-[11px] tracking-widest text-[#16213E]/40">COMPLIANCE CHECK BREAKDOWN</p>
      </div>
      <div>
        {checks.map((c, i) => {
          const style = STATUS_STYLES[c.status];
          const Icon = style.icon;
          return (
            <div
              key={c.check_type}
              className={`flex items-center justify-between px-5 py-3 ${i !== checks.length - 1 ? "border-b border-[#E2DFD5]/70" : ""}`}
            >
              <span className="text-sm text-[#16213E]">{CHECK_LABELS[c.check_type] || c.check_type}</span>
              <span className={`flex items-center gap-1.5 text-sm font-medium ${style.color}`}>
                <Icon size={16} />
                {style.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}