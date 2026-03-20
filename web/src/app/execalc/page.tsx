"use client";

import { useMemo, useState } from "react";
import { LiveExecutiveBrief, type ExecutiveArtifact } from "@/components/shell/live-executive-brief";
import { WorkspaceShell } from "@/components/shell/workspace-shell";

const MOCK_ARTIFACT: ExecutiveArtifact = {
  label: "Live Executive Brief",
  updatedAt: "Stage 8",
  sourceSurface: "Execalc Workspace",
  status: "Mocked",
  coreThesis:
    "Execalc becomes materially more valuable when the interface preserves high-signal thinking in real time instead of forcing the operator to recover it from scrollback.",
  executiveBrief:
    "The current shell already supports a right-side rail, which makes it the cleanest place to prove the Real-Time Decision Artifact Engine in product. Instead of showing passive context only, the rail should act as a live executive layer that tracks what the conversation has actually concluded, what matters, and where judgment is heading.",
  keyInsights: [
    "The right rail is the first visible proof of Execalc's cognition layer.",
    "The operator should be able to think from the rail while the chat is still unfolding.",
    "This stub should be deterministic first, then wired to live scenario and decision logic.",
  ],
  decisionSignal:
    "Structurally correct next move. Keep the first implementation mocked and visible, then wire it to live cognition after the UI shape is proven.",
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
  };
  error?: string;
};

const INITIAL_PROMPT =
  "We think this design will make Execalc very sticky. I want the workspace to feel familiar like a browser, but actually function like a governed operating system for executive cognition.";

export default function ExecalcPage() {
  const [prompt, setPrompt] = useState(INITIAL_PROMPT);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [decision, setDecision] = useState<DecisionRunResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

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
            scenario_type: "strategic_ui_shell",
            governing_objective: "preserve_optionality",
            prompt,
            facts: {
              source_surface: "execalc_workbench",
              current_focus: "ui_shell_scaffold",
            },
            constraints: {
              stage: "stage8",
            },
            requested_depth: "standard",
            decision_horizon: "current build cycle",
            stakeholder_scope: "operator, future executive users",
            risk_surface: "medium",
            assumptions:
              "A familiar shell will increase usability and stickiness.",
            decision_notes:
              "Initial UI shell should remain governed, minimal, and extensible.",
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

  const artifact: ExecutiveArtifact = {
    ...MOCK_ARTIFACT,
    status: isSubmitting
      ? "Converting"
      : error
        ? "Error"
        : decision?.report
          ? "Live"
          : MOCK_ARTIFACT.status,
    updatedAt: decision?.report
      ? "Decision generated"
      : isSubmitting
        ? "Updating"
        : MOCK_ARTIFACT.updatedAt,
    coreThesis: decision?.report?.executive_summary || MOCK_ARTIFACT.coreThesis,
    executiveBrief:
      decision?.report?.value_assessment || MOCK_ARTIFACT.executiveBrief,
    decisionSignal: error
      ? `Decision failed: ${error}`
      : decision?.report
        ? `Decision ready: ${decision.report.confidence || "unknown"} confidence`
        : isSubmitting
          ? "Decision conversion in progress"
          : MOCK_ARTIFACT.decisionSignal,
  };

  const rightRail = <LiveExecutiveBrief artifact={artifact} />;

  return (
    <WorkspaceShell activeTab="Execalc" rightRail={rightRail}>
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
                  className="rounded-full border border-zinc-700 bg-zinc-950 px-3 py-1.5 text-xs font-medium text-zinc-200"
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
          <div className="flex-1 rounded-2xl border border-zinc-700 bg-zinc-900 px-4 py-3 text-sm text-zinc-400">
            Describe the decision or idea...
          </div>
          <button
            type="button"
            className="rounded-2xl bg-zinc-100 px-5 py-3 text-sm font-semibold text-zinc-950"
          >
            Send
          </button>
        </div>
      </div>
    </WorkspaceShell>
  );
}
