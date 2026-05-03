"use client";

import { useMemo, useState } from "react";
import { LiveExecutiveBrief, type ExecutiveArtifact, type RailNugget } from "@/components/shell/live-executive-brief";
import { WorkspaceShell } from "@/components/shell/workspace-shell";

const IDLE_ARTIFACT: ExecutiveArtifact = {
  label: "Live Executive Brief",
  updatedAt: "Idle",
  sourceSurface: "Execalc Workspace",
  status: "Idle",
  coreThesis:
    "The executive rail becomes most credible when it reflects live governed runtime state, and remains explicit about being idle before any decision has been formed.",
  executiveBrief:
    "No live decision artifact is loaded yet. Use the workspace to run a governed decision, and the rail will switch from idle posture to runtime-derived signal.",
  keyInsights: [
    "The rail should stay truthful even before a decision exists.",
    "Idle state is more honest than mock state.",
    "Live runtime output should replace idle copy as soon as a decision is formed.",
  ],
  decisionSignal:
    "No decision loaded yet. Submit a prompt to generate a governed decision artifact.",
};

type DecisionRunResponse = {
  ok: boolean;
  report?: {
    executive_summary?: string;
    confidence?: string;
    confidence_rationale?: string[];
    governing_objective?: string;
    tradeoffs?: {
      upside?: string[];
      downside?: string[];
      key_tradeoffs?: string[];
      asymmetry?: string[];
    };
    sensitivity?: { name: string; impact: string }[];
    next_actions?: string[];
    value_assessment?: string;
    risk_reward_assessment?: string;
    supply_demand_assessment?: string;
    asset_assessment?: string;
    liability_assessment?: string;
    actors?: string[];
    incentives?: string[];
    asymmetries?: string[];
  };
  audit?: {
    envelope_id?: string;
    scenario_type?: string;
    tenant_id?: string;
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
  error?: string;
};

type OrchestrationRunResponse = {
  ok: boolean;
  turn_class?: string;
  assistant_message?: string;
  rail_state?: { mode?: string };
  decision_result?: unknown;
  action_proposal?: unknown;
  execution_boundary_result?: { status?: string; reason?: string } | null;
  error?: string;
};

export default function ExecalcPage() {
  const [prompt, setPrompt] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [decision, setDecision] = useState<DecisionRunResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [chatPrompt, setChatPrompt] = useState("");
  const [isOrchestrating, setIsOrchestrating] = useState(false);
  const [orchestrationResult, setOrchestrationResult] = useState<OrchestrationRunResponse | null>(null);
  const [orchestrationError, setOrchestrationError] = useState<string | null>(null);

  const canSubmit = useMemo(
    () => prompt.trim().length > 0 && !isSubmitting,
    [prompt, isSubmitting]
  );

  async function convertToDecision() {
    if (!canSubmit) return;

    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch("/api/decision/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-User-Id": "test_user",
          "X-Role": "operator",
          "X-Tenant-Id": "tenant_test_001",
        },
        body: JSON.stringify({
          scenario: {
            scenario_type: "general",
            governing_objective: "unspecified",
            prompt,
            facts: {},
            constraints: {},
            requested_depth: "standard",
            workspace_id: "workspace_execalc",
            project_id: "project_execalc",
            chat_id: "chat_execalc",
            thread_id: decision?.audit?.envelope_id ?? null,
          },
        }),
      });

      const body = (await response.json()) as DecisionRunResponse;

      if (!response.ok || !body.ok) {
        setDecision(null);
        setError(body.error || "Decision run failed");
        return;
      }

      setDecision(body);
    } catch (err) {
      setDecision(null);
      setError(err instanceof Error ? err.message : "Network error");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function sendToOrchestration() {
    if (!chatPrompt.trim() || isOrchestrating) return;

    setIsOrchestrating(true);
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
          user_text: chatPrompt,
          scenario_type: "general",
          governing_objective: "unspecified",
          navigation: {
            workspace_id: "workspace_execalc",
            project_id: "project_execalc",
            chat_id: "chat_execalc",
            thread_id: decision?.audit?.envelope_id ?? null,
          },
        }),
      });

      const body = (await response.json()) as OrchestrationRunResponse;

      if (!response.ok || !body.ok) {
        setOrchestrationResult(null);
        setOrchestrationError(body.error || "Orchestration failed");
        return;
      }

      setOrchestrationResult(body);
    } catch (err) {
      setOrchestrationResult(null);
      setOrchestrationError(err instanceof Error ? err.message : "Network error");
    } finally {
      setIsOrchestrating(false);
    }
  }

  const liveInsights = [
    decision?.report?.value_assessment,
    decision?.report?.risk_reward_assessment,
    decision?.report?.supply_demand_assessment,
    decision?.report?.asset_assessment,
    decision?.report?.liability_assessment,
    ...(decision?.report?.tradeoffs?.key_tradeoffs || []),
    ...(decision?.report?.next_actions || [])
      .slice(0, 2)
      .map((action) => "Next action: " + action),
    ...(decision?.report?.sensitivity || [])
      .slice(0, 2)
      .map((item) => "Sensitivity: " + item.name + " (" + item.impact + ")"),
  ].filter((value): value is string => Boolean(value));

    const observedAnomalies = [
      ...(decision?.audit?.stability?.anomalies || []).map(
        (item) => "Stability anomaly: " + item
      ),
      ...(decision?.audit?.drift?.anomalies || []).map(
        (item) => "Drift anomaly: " + item
      ),
    ];

      const stabilitySignals = (decision?.audit?.stability?.signals || []).map(
        (item) => "Stability signal: " + item
      );

      const driftSignals = (decision?.audit?.drift?.signals || []).map(
        (item) => "Drift signal: " + item
      );

    const boundaryInsight = decision?.execution_boundary?.status
      ? "Execution boundary: " +
        decision.execution_boundary.status +
        (decision.execution_boundary.reason
          ? " - " + decision.execution_boundary.reason
          : "")
      : null;

    const runtimeNuggets: RailNugget[] = [
      ...(boundaryInsight
        ? [{
            id: "boundary",
            label: "Execution Boundary",
            body: boundaryInsight,
            kind: "boundary" as const,
            priority: 100,
          }]
        : []),
      ...(decision?.audit?.stability?.anomalies || []).slice(0, 2).map((item, index) => ({
        id: "stability-" + index,
        label: "Stability Anomaly",
        body: item,
        kind: "anomaly" as const,
        priority: 88,
      })),
      ...(decision?.audit?.drift?.anomalies || []).slice(0, 2).map((item, index) => ({
        id: "drift-" + index,
        label: "Drift Anomaly",
        body: item,
        kind: "drift_anomaly" as const,
        priority: 92,
      })),
        ...((decision?.audit?.stability?.anomalies || []).length === 0
          ? stabilitySignals.slice(0, 1).map((item, index) => ({
              id: "stability-signal-" + index,
              label: "Stability Signal",
              body: item,
              kind: "signal" as const,
              priority: 68,
            }))
          : []),
        ...((decision?.audit?.drift?.anomalies || []).length === 0
          ? driftSignals.slice(0, 1).map((item, index) => ({
              id: "drift-signal-" + index,
              label: "Drift Signal",
              body: item,
              kind: "signal" as const,
              priority: 66,
            }))
          : []),
      ...liveInsights.slice(0, 3).map((item, index) => ({
        id: "insight-" + index,
        label: index === 0 ? "Primary Insight" : "Supporting Insight",
        body: item,
        kind: item.startsWith("Next action:") ? ("action" as const) : ("insight" as const),
        priority: item.startsWith("Next action:") ? 80 : (index === 0 ? 70 : 60),
      })),
    ];

  const artifact: ExecutiveArtifact = decision?.report
    ? {
        label: "Live Executive Brief",
        updatedAt: isSubmitting ? "Refreshing" : "Decision generated",
        sourceSurface: "Execalc Workspace",
        status: isSubmitting ? "Converting" : "Live",
        coreThesis:
          decision.report.executive_summary ||
          "Decision generated from governed runtime output.",
        executiveBrief:
          (decision.audit?.scenario_type
            ? "Scenario: " + decision.audit.scenario_type
            : "Live decision artifact") +
          (decision.report.governing_objective
            ? ". Governing objective: " + decision.report.governing_objective
            : "") +
          (decision.report.confidence
            ? ". Confidence: " + decision.report.confidence
            : ""),
        keyInsights:
          [boundaryInsight, ...observedAnomalies, ...liveInsights].filter(
            (value): value is string => Boolean(value)
          ).length > 0
            ? [boundaryInsight, ...observedAnomalies, ...liveInsights]
                .filter((value): value is string => Boolean(value))
                .slice(0, 3)
            : [
                "Decision artifact available, but no additional governed insights have been surfaced yet.",
              ],
        railNuggets: runtimeNuggets,
        decisionSignal: isSubmitting
          ? "Decision conversion in progress"
          : boundaryInsight
            ? boundaryInsight
            : decision.report.confidence
              ? "Decision ready: " + decision.report.confidence + " confidence"
              : "Decision ready",
      }
    : {
        ...IDLE_ARTIFACT,
        status: isSubmitting ? "Converting" : error ? "Error" : IDLE_ARTIFACT.status,
        updatedAt: isSubmitting
          ? "Updating"
          : error
            ? "Execution failed"
            : IDLE_ARTIFACT.updatedAt,
        decisionSignal: error
          ? "Decision failed: " + error
          : isSubmitting
            ? "Decision conversion in progress"
            : IDLE_ARTIFACT.decisionSignal,
      };

  const rightRail = <LiveExecutiveBrief artifact={artifact} />;

    const recentDecisionItems = decision?.audit?.envelope_id
      ? [{
          label: "Current: " + decision.audit.envelope_id,
          active: true,
        }]
      : [{
          label: "No decision yet",
          active: true,
        }];

  return (
    <WorkspaceShell
        activeTab="Execalc"
        rightRail={rightRail}
        workspaceLabel="Execalc Workspace"
        projects={[{ label: "Stage 8 UI Shell", active: true }]}
        chats={[{
          label: decision?.audit?.envelope_id
            ? "Thread: " + decision.audit.envelope_id
            : "Thread not established yet",
          active: true,
        }]}
        recentDecisions={recentDecisionItems}
      >
      <div className="mb-6">
        <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
          Workbench Mode
        </div>
        <h1 className="mt-2 text-2xl font-semibold tracking-tight">
          Execalc Chat Workspace
        </h1>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-400">
          A governed executive workbench for discussion, structured reasoning,
          decision formation, and continuity across live organizational work.
        </p>
      </div>

      <div className="space-y-4">
        <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
          <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">
            Operator
          </div>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="min-h-32 w-full resize-y rounded-xl border border-zinc-700 bg-zinc-950 px-3 py-3 text-sm leading-6 text-zinc-200 outline-none focus:border-zinc-500"
          />
        </div>

        <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
          <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">
            Execalc
          </div>
          <p className="text-sm leading-6 text-zinc-200">
            The central surface should remain conversational, but the surrounding
            workspace should support decisions, diagnostics, planning,
            monitoring, and role-governed organizational synthesis.
          </p>

          <div className="mt-4 flex flex-wrap gap-2">
            {["Refine", "Summarize", "Formalize", "Pressure Test"].map(
              (action) => (
                <button
                  key={action}
                  type="button"
                  disabled
                  className="rounded-full border border-zinc-800 bg-zinc-950 px-3 py-1.5 text-xs font-medium text-zinc-600 cursor-not-allowed"
                >
                  {action}
                </button>
              )
            )}
            <button
              type="button"
              onClick={convertToDecision}
              disabled={!canSubmit}
              className="rounded-full border border-zinc-500 bg-zinc-100 px-3 py-1.5 text-xs font-semibold text-zinc-950 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSubmitting ? "Converting..." : "Convert to Decision"}
            </button>
          </div>
        </div>

        {error ? (
          <div className="rounded-2xl border border-red-900 bg-red-950/40 p-4">
            <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-red-300">
              Error
            </div>
            <p className="text-sm text-red-200">{error}</p>
          </div>
        ) : null}

        {decision?.report ? (
          <div className="rounded-2xl border border-zinc-700 bg-zinc-900 p-5">
            <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">
              Decision Artifact
            </div>

            <div className="space-y-4">
              <div>
                <h2 className="text-lg font-semibold text-zinc-100">
                  {decision.report.executive_summary || "Executive Summary"}
                </h2>
                <p className="mt-2 text-sm text-zinc-400">
                  Objective:{" "}
                  {decision.report.governing_objective || "unspecified_objective"}
                </p>
                <p className="mt-1 text-sm text-zinc-400">
                  Confidence: {decision.report.confidence || "unknown"}
                </p>
                {decision.audit?.envelope_id ? (
                  <p className="mt-1 text-xs text-zinc-500">
                    Envelope ID: {decision.audit.envelope_id}
                  </p>
                ) : null}
              </div>

              <div className="grid gap-4 lg:grid-cols-2">
                <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                  <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                    Value Assessment
                  </div>
                  <p className="mt-2 text-sm leading-6 text-zinc-300">
                    {decision.report.value_assessment}
                  </p>
                </div>

                <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                  <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                    Risk / Reward
                  </div>
                  <p className="mt-2 text-sm leading-6 text-zinc-300">
                    {decision.report.risk_reward_assessment}
                  </p>
                </div>
              </div>

              <div className="grid gap-4 lg:grid-cols-2">
                <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                  <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                    Tradeoffs
                  </div>
                  <ul className="mt-2 space-y-2 text-sm text-zinc-300">
                    {(decision.report.tradeoffs?.key_tradeoffs || []).map(
                      (item) => (
                        <li key={item}>- {item}</li>
                      )
                    )}
                  </ul>
                </div>

                <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                  <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                    Next Actions
                  </div>
                  <ul className="mt-2 space-y-2 text-sm text-zinc-300">
                    {(decision.report.next_actions || []).map((item) => (
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
                  {(decision.report.sensitivity || []).length > 0 ? (
                    (decision.report.sensitivity || []).map((item) => (
                      <li key={item.name}>
                        <span className="font-medium text-zinc-100">
                          {item.name}:
                        </span>{" "}
                        {item.impact}
                      </li>
                    ))
                  ) : (
                    <li>No sensitivity variables surfaced.</li>
                  )}
                </ul>
              </div>
            </div>
          </div>
        ) : null}
      </div>

      <div className="mt-6 border-t border-zinc-800 bg-zinc-950 px-0 py-4">
        <div className="flex w-full gap-3">
          <textarea
            value={chatPrompt}
            onChange={(e) => setChatPrompt(e.target.value)}
            placeholder="Ask a question or describe a situation..."
            rows={1}
            className="flex-1 resize-none rounded-2xl border border-zinc-700 bg-zinc-900 px-4 py-3 text-sm text-zinc-200 outline-none placeholder:text-zinc-500 focus:border-zinc-500"
          />
          <button
            type="button"
            onClick={sendToOrchestration}
            disabled={!chatPrompt.trim() || isOrchestrating}
            className="rounded-2xl bg-zinc-100 px-5 py-3 text-sm font-semibold text-zinc-950 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isOrchestrating ? "..." : "Send"}
          </button>
        </div>
        {orchestrationResult ? (
          <div className="mt-3 rounded-xl border border-zinc-800 bg-zinc-900 p-4">
            <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-zinc-500">
              Response
            </div>
            <p className="text-sm leading-6 text-zinc-300">{orchestrationResult.assistant_message}</p>
            {orchestrationResult.turn_class ? (
              <p className="mt-2 text-xs text-zinc-500">
                Turn: {orchestrationResult.turn_class} · Mode: {orchestrationResult.rail_state?.mode}
              </p>
            ) : null}
          </div>
        ) : orchestrationError ? (
          <div className="mt-3 rounded-xl border border-red-900 bg-red-950/40 p-4">
            <p className="text-sm text-red-200">{orchestrationError}</p>
          </div>
        ) : null}
      </div>
    </WorkspaceShell>
  );
}
