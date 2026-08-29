import React from "react";
import { Check } from "lucide-react";

/**
 * SealBadge — the visual signature of the site.
 * A circular verification seal with a dashed rotating ring and curved label
 * text, echoing an official government stamp. Reused at 3 sizes across the
 * page (navbar mark, hero centerpiece, CTA accent) since the product itself
 * is about stamping bidders "verified" across government portals.
 */
export default function SealBadge({ size = 96, animate = false, label = "GEM COMPLIANCE • VERIFIED •" }) {
  const id = React.useId();
  const r = size / 2 - 4;
  const cx = size / 2;
  const cy = size / 2;

  return (
    <div
      className={animate ? "seal-stamp-in" : ""}
      style={{ width: size, height: size }}
    >
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <defs>
          <path
            id={`sealpath-${id}`}
            d={`M ${cx - r},${cy} a ${r},${r} 0 1,1 ${r * 2},0 a ${r},${r} 0 1,1 -${r * 2},0`}
          />
        </defs>
        <circle
          cx={cx} cy={cy} r={r}
          fill="none" stroke="#A8681E" strokeWidth="1.5"
          strokeDasharray="3 4"
          className={animate ? "seal-ring-spin" : ""}
        />
        <circle cx={cx} cy={cy} r={r - 8} fill="none" stroke="#A8681E" strokeWidth="1" />
        <text fontSize={size * 0.072} letterSpacing="2" fill="#A8681E" fontFamily="IBM Plex Mono, monospace">
          <textPath href={`#sealpath-${id}`} startOffset="0%">
            {label}
          </textPath>
        </text>
        <circle cx={cx} cy={cy} r={size * 0.18} fill="#16213E" />
        <foreignObject x={cx - size * 0.11} y={cy - size * 0.11} width={size * 0.22} height={size * 0.22}>
          <div className="w-full h-full flex items-center justify-center">
            <Check color="#F7F6F1" size={size * 0.16} strokeWidth={2.5} />
          </div>
        </foreignObject>
      </svg>
    </div>
  );
}