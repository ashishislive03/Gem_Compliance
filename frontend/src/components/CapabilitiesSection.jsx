import React from "react";
import { Receipt, IdCard, Factory, Users, Globe2, ShieldBan } from "lucide-react";

const CAPABILITIES = [
  {
    icon: Receipt,
    title: "GST registration & filing",
    desc: "Confirms GSTIN validity, registration status, and recent return-filing history against GSTN.",
  },
  {
    icon: IdCard,
    title: "PAN & income tax",
    desc: "Verifies PAN validity and whether the latest ITR was filed on time.",
  },
  {
    icon: Factory,
    title: "Udyam / MSME registration",
    desc: "Checks Udyam number validity, enterprise category, and active status.",
  },
  {
    icon: Users,
    title: "EPFO / ESIC",
    desc: "Confirms establishment registration and contribution status, where applicable.",
  },
  {
    icon: Globe2,
    title: "Make in India / local content",
    desc: "Compares declared local-content percentage against the tender's required threshold.",
  },
  {
    icon: ShieldBan,
    title: "Blacklist / debarment",
    desc: "Screens against debarment records — a hard disqualifier when flagged.",
  },
];

export default function CapabilitiesSection() {
  return (
    <section id="capabilities" className="max-w-6xl mx-auto px-6 py-20">
      <div className="max-w-lg mb-12">
        <p className="font-mono text-xs tracking-[0.2em] text-[#A8681E] mb-3">WHAT GETS CHECKED</p>
        <h2 className="font-serif text-3xl text-[#16213E]">
          Six statutory checks, run the same way every time.
        </h2>
      </div>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-px bg-[#E2DFD5] border border-[#E2DFD5]">
        {CAPABILITIES.map(({ icon: Icon, title, desc }) => (
          <div key={title} className="bg-[#F7F6F1] p-6">
            <Icon size={20} className="text-[#A8681E] mb-4" strokeWidth={1.75} />
            <h3 className="text-[#16213E] font-medium text-[15px] mb-1.5">{title}</h3>
            <p className="text-sm text-[#16213E]/60 leading-relaxed">{desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}