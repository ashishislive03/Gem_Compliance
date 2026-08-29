import React from "react";

const STEPS = [
  {
    n: "01",
    title: "Bidder submits documents",
    desc: "GST certificate, PAN, Udyam certificate and other statutory documents are uploaded against the tender.",
  },
  {
    n: "02",
    title: "AI reads the documents",
    desc: "An extraction model pulls GSTIN, PAN, Udyam number and other fields from the uploaded certificates — regardless of layout.",
  },
  {
    n: "03",
    title: "Portals are queried",
    desc: "The same identifiers are checked against GSTN, Udyam, PAN, EPFO and other government records.",
  },
  {
    n: "04",
    title: "Document and portal are cross-checked",
    desc: "Any mismatch between what was submitted and what the government record actually shows is flagged immediately.",
  },
  {
    n: "05",
    title: "Officer reviews and decides",
    desc: "A compliance score, risk level and plain-English recommendation are shown — the officer makes the final call.",
  },
];

export default function HowItWorksSection() {
  return (
    <section id="how-it-works" className="max-w-6xl mx-auto px-6 py-20">
      <div className="max-w-lg mb-14">
        <p className="font-mono text-xs tracking-[0.2em] text-[#A8681E] mb-3">THE PIPELINE</p>
        <h2 className="font-serif text-3xl text-[#16213E]">How a bidder gets verified</h2>
      </div>

      <div className="relative max-w-2xl">
        <div className="absolute left-[27px] top-2 bottom-2 w-px bg-[#E2DFD5]" aria-hidden="true" />
        <div className="space-y-10">
          {STEPS.map((s) => (
            <div key={s.n} className="relative flex gap-6">
              <span className="relative z-10 font-mono text-sm text-[#A8681E] bg-[#F7F6F1] w-14 shrink-0 pt-0.5">
                {s.n}
              </span>
              <div className="pb-1">
                <h3 className="text-[#16213E] font-medium text-[15px] mb-1">{s.title}</h3>
                <p className="text-sm text-[#16213E]/60 leading-relaxed max-w-md">{s.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}