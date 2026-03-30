"use client";

import { useEffect, useState } from "react";
import { LiveExecutiveBrief, type ExecutiveArtifact, type RailNugget } from "@/components/shell/live-executive-brief";
import { WorkspaceShell } from "@/components/shell/workspace-shell";

type DecisionListRecord = {
  created_at: string;
  envelope_id: string;
  ok: boolean;
  tenant_id: string;
};

type RecentResponse = {
  ok: boolean;
  persist_enabled?: boolean;
  records?: DecisionListRecord[];
  error?: string;
};

type DecisionDetailResponse = {
  ok: boolean;
  envelope_id?: string;
  created_at?: string;
  result?: {
    ok?: boolean;
    report?: {
      executive_summary?: string;
      confidence?: string;
      governing_objective?: string;
      value_assessment?: string;
      risk_reward_assessment?: string;
      tradeoffs?: {
        key_tradeoffs?: string[];
      };
      next_actions?: string[];
      sensitivity?: { name: string; impact: string }[];
    };
    audit?: {
      envelope_id?: string;
      tenant_id?: string;
      scenario_type?: string;
      user_id?: string;
      workspace_id?: string;
      project_id?: string;
      chat_id?: string;
      thread_id?: string | null;
      stability?: {
        mode?: string;
        status?: string;
        signals?: string[];
        anomalies?: string[];
      };
      drift?: {
        mode?: string;
        status?: string;
        signals?: string[];
        anomalies?: string[];
      };
    };
      execution_boundary?: {
        status?: string;
        reason?: string;
      };
  };
  error?: string;
};

type OrchestrationResponse = {
  ok: boolean;
  turn_class?: string;
  assistant_message?: string;
  rail_state?: {
    mode?: string;
  };
  action_proposal?: {
    action_type?: string;
    tenant_id?: string;
    user_id?: string;
    requires_human_review?: boolean;
    risk_level?: string;
  } | null;
  execution_boundary_result?: {
    status?: string;
    reason?: string;
  } | null;
  error?: string;
};


export default function DecisionsPage() {
  const [records, setRecords] = useState<DecisionListRecord[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<DecisionDetailResponse | null>(null);
  const [loadingList, setLoadingList] = useState(true);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [orchestrationInput, setOrchestrationInput] = useState("What should we do?");
  const [orchestrationLoading, setOrchestrationLoading] = useState(false);
  const [orchestrationResult, setOrchestrationResult] =
    useState<OrchestrationResponse | null>(null);
  const [orchestrationError, setOrchestrationError] = useState<string | null>(null);

  useEffect(() => {
    async function loadRecent() {
      setLoadingList(true);
      setError(null);

      try {
        const response = await fetch("/api/decision/recent?limit=10", {
          headers: {
            "X-User-Id": "test_user",
            "X-Role": "operator",
            "X-Tenant-Id": "tenant_test_001",
          },
          cache: "no-store",
        });

        const body = (await response.json()) as RecentResponse;

        if (!response.ok || !body.ok) {
          setError(body.error || "Failed to load recent decisions");
          setRecords([]);
          return;
        }

        const rows = body.records || [];
        setRecords(rows);

        if (rows.length > 0) {
          setSelectedId(rows[0].envelope_id);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Network error");
        setRecords([]);
      } finally {
        setLoadingList(false);
      }
    }

    loadRecent();
  }, []);

  useEffect(() => {
    async function loadDetail(envelopeId: string) {
      setLoadingDetail(true);
      setError(null);

      try {
        const response = await fetch(`/api/decision/${envelopeId}`, {
          headers: {
            "X-User-Id": "test_user",
            "X-Role": "operator",
            "X-Tenant-Id": "tenant_test_001",
          },
          cache: "no-store",
        });

        const body = (await response.json()) as DecisionDetailResponse;

        if (!response.ok || !body.ok) {
          setDetail(null);
          setError(body.error || "Failed to load decision detail");
          return;
        }

        setDetail(body);
      } catch (err) {
        setDetail(null);
        setError(err instanceof Error ? err.message : "Network error");
      } finally {
        setLoadingDetail(false);
      }
    }

    if (selectedId) {
      loadDetail(selectedId);
    }
  }, [selectedId]);

  const report = detail?.result?.report;

  const railInsights = [
    report?.value_assessment,
    report?.risk_reward_assessment,
    ...(report?.tradeoffs?.key_tradeoffs || []),
    ...(report?.next_actions || []).slice(0, 2).map((action) => "Next action: " + action),
    ...(report?.sensitivity || [])
      .slice(0, 2)
      .map((item) => "Sensitivity: " + item.name + " (" + item.impact + ")"),
    orchestrationResult?.execution_boundary_result?.status
      ? "Boundary: " +
        orchestrationResult.execution_boundary_result.status +
        (orchestrationResult.execution_boundary_result.reason
          ? " - " + orchestrationResult.execution_boundary_result.reason
          : "")
      : null,
    orchestrationResult?.action_proposal?.action_type
      ? "Action proposal: " +
        orchestrationResult.action_proposal.action_type +
        (orchestrationResult.action_proposal.risk_level
          ? " (" + orchestrationResult.action_proposal.risk_level + ")"
          : "")
      : null,
  ].filter((value): value is string => Boolean(value));

    const detailAudit = detail?.result?.audit;
      const stabilityAnomalies = (detailAudit?.stability?.anomalies || []).slice(0, 2);

      const driftAnomalies = (detailAudit?.drift?.anomalies || []).slice(0, 2);

      const stabilitySignals = (detailAudit?.stability?.signals || []).map(
        (item) => "Stability signal: " + item
      );

      const driftSignals = (detailAudit?.drift?.signals || []).map(
        (item) => "Drift signal: " + item
      );

    const detailBoundaryInsight = detail?.result?.execution_boundary?.status
      ? "Decision boundary: " +
        detail.result.execution_boundary.status +
        (detail.result.execution_boundary.reason
          ? " - " + detail.result.execution_boundary.reason
          : "")
      : null;

    const runtimeNuggets: RailNugget[] = [
      ...(detailBoundaryInsight
        ? [{
            id: "detail-boundary",
            label: "Decision Boundary",
            body: detailBoundaryInsight,
            kind: "boundary" as const,
            priority: 100,
          }]
        : []),
        ...stabilityAnomalies.map((item, index) => ({
          id: "stability-" + index,
          label: "Stability Anomaly",
          body: item,
          kind: "anomaly" as const,
          priority: 90,
        })),
        ...driftAnomalies.map((item, index) => ({
          id: "drift-" + index,
          label: "Drift Anomaly",
          body: item,
          kind: "anomaly" as const,
          priority: 90,
        })),
        ...((detailAudit?.stability?.anomalies || []).length === 0
          ? stabilitySignals.slice(0, 1).map((item, index) => ({
              id: "stability-signal-" + index,
              label: "Stability Signal",
              body: item,
              kind: "signal" as const,
              priority: 68,
            }))
          : []),
        ...((detailAudit?.drift?.anomalies || []).length === 0
          ? driftSignals.slice(0, 1).map((item, index) => ({
              id: "drift-signal-" + index,
              label: "Drift Signal",
              body: item,
              kind: "signal" as const,
              priority: 66,
            }))
          : []),
      ...railInsights.slice(0, 3).map((item, index) => ({
        id: "insight-" + index,
        label: index === 0 ? "Primary Insight" : "Supporting Insight",
        body: item,
        kind: item.startsWith("Action proposal:") ? ("action" as const) : ("insight" as const),
        priority: item.startsWith("Action proposal:") ? 80 : (index === 0 ? 70 : 60),
      })),
    ];

  const artifact: ExecutiveArtifact = {
    label: "Decision Rail",
    updatedAt: detail?.created_at,
    sourceSurface: "Decisions Workspace",
    status: error
      ? "Error"
      : orchestrationError
        ? "Probe error"
        : orchestrationLoading
          ? "Probe running"
          : loadingDetail
            ? "Loading detail"
            : selectedId
            ? "Decision loaded"
            : loadingList
                ? "Loading list"
                : "Idle",
    coreThesis:
      report?.executive_summary ||
      (loadingDetail
        ? "Loading selected decision artifact from persisted decision memory."
        : records.length > 0
          ? "A persisted decision is available for inspection; the rail should surface governed state from the selected artifact rather than placeholder copy."
          : "No persisted decisions are available yet. The rail will populate once decision artifacts exist."),
    executiveBrief: detail?.result?.audit?.scenario_type
      ? "Selected scenario: " +
        detail.result.audit.scenario_type +
        (report?.governing_objective
          ? ". Governing objective: " + report.governing_objective
          : "") +
        (report?.confidence ? ". Confidence: " + report.confidence : "")
      : orchestrationResult?.assistant_message ||
        "The rail reflects governed decision and orchestration state instead of placeholder narrative.",
      keyInsights:
        [detailBoundaryInsight, ...stabilityAnomalies, ...driftAnomalies, ...railInsights].filter(
          (value): value is string => Boolean(value)
        ).length > 0
          ? [detailBoundaryInsight, ...stabilityAnomalies, ...driftAnomalies, ...railInsights]
              .filter((value): value is string => Boolean(value))
              .slice(0, 3)
          : ["No governed signals surfaced yet from the selected decision or orchestration probe."],
        railNuggets: runtimeNuggets,
      decisionSignal: orchestrationError
        ? "Orchestration probe failed: " + orchestrationError
        : orchestrationLoading
          ? "Running orchestration probe"
          : detailBoundaryInsight
            ? detailBoundaryInsight
            : orchestrationResult?.execution_boundary_result?.status
              ? "Execution boundary status: " +
                orchestrationResult.execution_boundary_result.status +
                (orchestrationResult.execution_boundary_result.reason
                  ? " - " + orchestrationResult.execution_boundary_result.reason
                  : "")
              : report?.confidence
                ? "Selected decision confidence: " + report.confidence
                : selectedId
                  ? "Decision detail loaded; more governed signals appear as runtime outputs expand."
                  : "Select a persisted decision to populate the rail.",
  };

  const rightRail = <LiveExecutiveBrief artifact={artifact} />;

    const recentDecisionItems = records.map((record) => ({
      label: record.envelope_id === selectedId
        ? "Selected: " + record.envelope_id
        : record.envelope_id,
      active: record.envelope_id === selectedId,
    }));

  async function runOrchestrationProbe() {
    setOrchestrationLoading(true);
    setOrchestrationError(null);

    try {
      const response = await fetch("/api/orchestration/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-User-Id": "test_user",
          "X-Role": "operator",
          "X-Tenant-Id": "tenant_test_001",
        },
        body: JSON.stringify({
          user_text: orchestrationInput,
          scenario_type: "general",
          governing_objective: "workspace_probe",
          navigation: {
            workspace_id: "workspace_decisions",
            project_id: "project_decision_memory",
            chat_id: "chat_decisions_probe",
            thread_id: selectedId || null,
          },
        }),
      });

      const body = (await response.json()) as OrchestrationResponse;

      if (!response.ok || !body.ok) {
        setOrchestrationResult(null);
        setOrchestrationError(body.error || "Failed to run orchestration");
        return;
      }

      setOrchestrationResult(body);
    } catch (err) {
      setOrchestrationResult(null);
      setOrchestrationError(err instanceof Error ? err.message : "Network error");
    } finally {
      setOrchestrationLoading(false);
    }
  }

  return (
    <WorkspaceShell
        activeTab="Decisions"
        rightRail={rightRail}
        workspaceLabel="Decisions Workspace"
        projects={[{ label: "Decision Memory", active: true }]}
        chats={[{
          label: selectedId ? "Selected thread: " + selectedId : "Decision list view",
          active: true,
        }]}
        recentDecisions={recentDecisionItems}
      >
      <div className="mb-6">
        <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
          Decision Memory
        </div>
        <h1 className="mt-2 text-2xl font-semibold tracking-tight">
          Decisions
        </h1>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-400">
          Structured decision artifacts live here so the organization can
          revisit, inspect, and compare prior judgment instead of losing it in
          chat history.
        </p>
      </div>

      {error ? (
        <div className="mb-6 rounded-2xl border border-red-900 bg-red-950/40 p-4">
          <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-red-300">
            Error
          </div>
          <p className="text-sm text-red-200">{error}</p>
        </div>
      ) : null}

      <div className="mb-6 rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
        <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">
          Orchestration Probe
        </div>
        <p className="mb-4 max-w-2xl text-sm text-zinc-400">
          Narrow end-to-end proof for the thin chat orchestration layer. This sends one
          executive turn through the new orchestration API and shows the returned runtime envelope.
        </p>

        <div className="flex flex-col gap-3">
          <textarea
            value={orchestrationInput}
            onChange={(e) => setOrchestrationInput(e.target.value)}
            className="min-h-[96px] rounded-xl border border-zinc-800 bg-zinc-950 px-4 py-3 text-sm text-zinc-100 outline-none"
          />
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={runOrchestrationProbe}
              disabled={orchestrationLoading || !orchestrationInput.trim()}
              className="rounded-lg border border-zinc-700 bg-zinc-100 px-4 py-2 text-sm font-semibold text-zinc-950 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {orchestrationLoading ? "Running..." : "Run orchestration"}
            </button>

            {orchestrationError ? (
              <span className="text-sm text-red-300">{orchestrationError}</span>
            ) : null}
          </div>

          {orchestrationResult ? (
            <div className="mt-2 rounded-xl border border-zinc-800 bg-zinc-950 p-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                    Turn Class
                  </div>
                  <div className="mt-1 text-sm text-zinc-200">
                    {orchestrationResult.turn_class || "unknown"}
                  </div>
                </div>
                <div>
                  <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                    Rail Mode
                  </div>
                  <div className="mt-1 text-sm text-zinc-200">
                    {orchestrationResult.rail_state?.mode || "unknown"}
                  </div>
                </div>
                <div className="md:col-span-2">
                  <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                    Assistant Message
                  </div>
                  <div className="mt-1 text-sm text-zinc-200">
                    {orchestrationResult.assistant_message || "No message returned."}
                  </div>
                </div>

                {orchestrationResult.action_proposal ? (
                  <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
                    <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                      Action Proposal
                    </div>
                    <div className="mt-2 space-y-1 text-sm text-zinc-200">
                      <div>Type: {orchestrationResult.action_proposal.action_type || "unknown"}</div>
                      <div>Tenant: {orchestrationResult.action_proposal.tenant_id || "unknown"}</div>
                      <div>User: {orchestrationResult.action_proposal.user_id || "unknown"}</div>
                      <div>
                        Human Review: {orchestrationResult.action_proposal.requires_human_review ? "yes" : "no"}
                      </div>
                      <div>Risk: {orchestrationResult.action_proposal.risk_level || "unknown"}</div>
                    </div>
                  </div>
                ) : null}

                {orchestrationResult.execution_boundary_result ? (
                  <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
                    <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                      Boundary Result
                    </div>
                    <div className="mt-2 space-y-1 text-sm text-zinc-200">
                      <div>Status: {orchestrationResult.execution_boundary_result.status || "unknown"}</div>
                      <div>Reason: {orchestrationResult.execution_boundary_result.reason || "none"}</div>
                    </div>
                  </div>
                ) : null}
              </div>
            </div>
          ) : null}
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
          <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-zinc-500">
            Recent Decision Artifacts
          </div>

          {loadingList ? (
            <div className="text-sm text-zinc-400">Loading recent decisions...</div>
          ) : records.length === 0 ? (
            <div className="text-sm text-zinc-400">No persisted decisions found.</div>
          ) : (
            <div className="space-y-3">
              {records.map((item) => {
                const active = item.envelope_id === selectedId;
                return (
                  <button
                    key={item.envelope_id}
                    type="button"
                    onClick={() => setSelectedId(item.envelope_id)}
                    className={`block w-full rounded-xl border px-4 py-3 text-left ${
                      active
                        ? "border-zinc-600 bg-zinc-100 text-zinc-950"
                        : "border-zinc-800 bg-zinc-950 text-zinc-300"
                    }`}
                  >
                    <div className="text-sm font-semibold">{item.envelope_id}</div>
                    <div className="mt-1 text-xs opacity-80">
                      Created: {item.created_at}
                    </div>
                    <div className="mt-1 text-xs opacity-80">
                      Tenant: {item.tenant_id}
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
          <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">
            Artifact Detail
          </div>

          {loadingDetail ? (
            <div className="text-sm text-zinc-400">Loading decision detail...</div>
          ) : !report ? (
            <div className="text-sm text-zinc-400">
              Select a decision artifact to inspect its contents.
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <h2 className="text-lg font-semibold text-zinc-100">
                  {report.executive_summary || "Executive Summary"}
                </h2>
                <p className="mt-2 text-sm text-zinc-400">
                  Objective: {report.governing_objective || "unspecified_objective"}
                </p>
                <p className="mt-1 text-sm text-zinc-400">
                  Confidence: {report.confidence || "unknown"}
                </p>
                {detail?.envelope_id ? (
                  <p className="mt-1 text-xs text-zinc-500">
                    Envelope ID: {detail.envelope_id}
                  </p>
                ) : null}
              </div>

              <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                  Value Assessment
                </div>
                <p className="mt-2 text-sm leading-6 text-zinc-300">
                  {report.value_assessment}
                </p>
              </div>

              <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                  Risk / Reward
                </div>
                <p className="mt-2 text-sm leading-6 text-zinc-300">
                  {report.risk_reward_assessment}
                </p>
              </div>

              <div className="grid gap-4 lg:grid-cols-2">
                <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                  <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                    Tradeoffs
                  </div>
                  <ul className="mt-2 space-y-2 text-sm text-zinc-300">
                    {(report.tradeoffs?.key_tradeoffs || []).map((item) => (
                      <li key={item}>- {item}</li>
                    ))}
                  </ul>
                </div>

                <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                  <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                    Next Actions
                  </div>
                  <ul className="mt-2 space-y-2 text-sm text-zinc-300">
                    {(report.next_actions || []).map((item) => (
                      <li key={item}>- {item}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                  Sensitivity
                </div>
                <ul className="mt-2 space-y-2 text-sm text-zinc-300">
                  {(report.sensitivity || []).length > 0 ? (
                    (report.sensitivity || []).map((item) => (
                      <li key={item.name}>
                        <span className="font-medium text-zinc-100">{item.name}:</span>{" "}
                        {item.impact}
                      </li>
                    ))
                  ) : (
                    <li>No sensitivity variables surfaced.</li>
                  )}
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </WorkspaceShell>
  );
}
