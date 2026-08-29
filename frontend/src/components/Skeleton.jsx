import React from "react";

export default function Skeleton({ className = "" }) {
  return <div className={`bg-[#E2DFD5]/60 rounded-sm animate-pulse ${className}`} />;
}