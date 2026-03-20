"use client";

import { useEffect, useState } from "react";
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
    };
  };
  error?: string;
};

const rightRail = (
  <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
    <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
      Decisions Surface
    </div>

    <div className="mt-4 space-y-4">
      <div>
        <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
          Purpose
        </div>
        <div className="mt-2 text-sm text-zinc-200">
          This surface now reads from the persisted decision journal instead of
          placeholder data.
        </div>
      </div>

      <div>
        <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
          Next Build Target
        </div>
        <div className="mt-2 text-sm text-zinc-200">
          Add comparison, filters, and richer artifact inspection across stored
          decisions.
        </div>
      </div>
    </div>
  </div>
);

export default function DecisionsPage() {
  const [records, setRecords] = useState<DecisionListRecord[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<DecisionDetailResponse | null>(null);
  const [loadingList, setLoadingList] = useState(true);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [error, setError] = useState<string | null>(null);

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

  return (
    <WorkspaceShell activeTab="Decisions" rightRail={rightRail}>
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
