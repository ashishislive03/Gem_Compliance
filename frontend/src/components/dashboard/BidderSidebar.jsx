import React from "react";
import { Search, ChevronRight, AlertTriangle } from "lucide-react";
import Skeleton from "../Skeleton";

export default function BidderSidebar({
  bidders, loading, error, query, onQueryChange, selectedId, onSelect,
}) {
  const filtered = React.useMemo(() => {
    if (!query.trim()) return bidders;
    const q = query.toLowerCase();
    return bidders.filter(
      (b) => b.company_name.toLowerCase().includes(q) || b.bidder_id.toLowerCase().includes(q)
    );
  }, [query, bidders]);

  return (
    <aside className="w-80 border-r border-[#E2DFD5] bg-white flex flex-col shrink-0">
      <div className="p-4 border-b border-[#E2DFD5]">
        <p className="font-mono text-[11px] tracking-widest text-[#16213E]/40 mb-2">BIDDER REGISTER</p>
        <div className="relative">
          <Search size={15} className="absolute left-2.5 top-2.5 text-[#16213E]/30" />
          <input
            value={query}
            onChange={(e) => onQueryChange(e.target.value)}
            placeholder="Search company or bidder ID"
            className="w-full pl-8 pr-3 py-2 text-sm border border-[#E2DFD5] rounded-sm bg-[#F7F6F1]/50 focus:outline-none focus:ring-1 focus:ring-[#16213E]/30 focus:bg-white transition-colors"
          />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        {error && (
          <div className="p-4 text-sm text-[#B3261E] flex items-start gap-2">
            <AlertTriangle size={15} className="shrink-0 mt-0.5" />
            {error}. Is the backend running on port 8000?
          </div>
        )}
        {loading && !error && (
          <div className="p-4 space-y-3">
            {[...Array(6)].map((_, i) => <Skeleton key={i} className="h-14 w-full" />)}
          </div>
        )}
        {!loading && !error && filtered.length === 0 && (
          <p className="p-4 text-sm text-[#16213E]/40">No bidders match "{query}"</p>
        )}
        {!loading && filtered.map((b) => {
          const isActive = b.bidder_id === selectedId;
          return (
            <button
              key={b.bidder_id}
              onClick={() => onSelect(b.bidder_id)}
              className={`w-full text-left px-4 py-3 border-b border-[#E2DFD5]/70 flex items-center justify-between transition-colors ${
                isActive ? "bg-[#16213E]/[0.04]" : "hover:bg-[#F7F6F1]"
              }`}
            >
              <div className="min-w-0">
                <p className="text-sm font-medium text-[#16213E] truncate">{b.company_name}</p>
                <p className="font-mono text-[11px] text-[#16213E]/40 mt-0.5">{b.bidder_id}</p>
              </div>
              <ChevronRight size={15} className={isActive ? "text-[#A8681E]" : "text-[#16213E]/20"} />
            </button>
          );
        })}
      </div>
    </aside>
  );
}