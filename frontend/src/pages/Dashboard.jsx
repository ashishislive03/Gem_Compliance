import React, { useState } from "react";
import { AlertTriangle } from "lucide-react";
import { useBidders, useAssessment, useAuditLog } from "../hooks/useCompliance";
import Skeleton from "../components/Skeleton";
import DashboardHeader from "../components/dashboard/DashboardHeader";
import BidderSidebar from "../components/dashboard/BidderSidebar";
import ScoreCard from "../components/dashboard/ScoreCard";
import CheckBreakdown from "../components/dashboard/CheckBreakdown";
import MismatchAlert from "../components/dashboard/MismatchAlert";
import RecommendationCard from "../components/dashboard/RecommendationCard";
import DecisionPanel from "../components/dashboard/DecisionPanel";
import AuditTrail from "../components/dashboard/AuditTrail";

export default function ComplianceDashboard({ onBack }) {
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState("BID-00001");
  const [refreshKey, setRefreshKey] = useState(0);

  const { bidders, loading: biddersLoading, error: biddersError } = useBidders();
  const { assessment, loading: assessmentLoading, error: assessmentError } = useAssessment(selectedId);
  const auditLogs = useAuditLog(selectedId, refreshKey);

  return (
    <div className="min-h-screen bg-[#F7F6F1]">
      <DashboardHeader onBack={onBack} bidderCount={bidders.length} />

      <div className="flex" style={{ minHeight: "calc(100vh - 64px)" }}>
        <BidderSidebar
          bidders={bidders}
          loading={biddersLoading}
          error={biddersError}
          query={query}
          onQueryChange={setQuery}
          selectedId={selectedId}
          onSelect={setSelectedId}
        />

        <main className="flex-1 p-8 max-w-3xl mx-auto w-full">
          {assessmentError && (
            <div className="rounded-sm border border-[#B3261E]/30 bg-[#B3261E]/[0.05] p-4 flex items-center gap-2 text-sm text-[#B3261E]">
              <AlertTriangle size={16} className="shrink-0" />
              {assessmentError}. Is the backend running and is this bidder ID valid?
            </div>
          )}

          {assessmentLoading && !assessmentError && (
            <div className="space-y-6">
              <Skeleton className="h-6 w-48" />
              <Skeleton className="h-36 w-full" />
              <Skeleton className="h-48 w-full" />
            </div>
          )}

          {assessment && !assessmentLoading && (
            <>
              <div className="mb-6">
                <h2 className="font-serif text-2xl text-[#16213E] mb-1">{assessment.company_name}</h2>
                <p className="font-mono text-[12px] text-[#16213E]/45">
                  {assessment.bidder_id}
                  {assessment.bid_id ? ` · BID ${assessment.bid_id}` : ""}
                </p>
              </div>

              <div className="space-y-6">
                <ScoreCard score={assessment.compliance_score} riskLevel={assessment.risk_level} />
                <MismatchAlert mismatches={assessment.document_portal_mismatches} />
                <CheckBreakdown checks={assessment.check_summary} />
                <RecommendationCard
                  recommendation={assessment.ai_recommendation}
                  pendingItems={assessment.pending_requirements}
                />
                <DecisionPanel
                  bidderId={assessment.bidder_id}
                  onDecisionRecorded={() => setRefreshKey((k) => k + 1)}
                />
                <AuditTrail logs={auditLogs} />
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  );
}