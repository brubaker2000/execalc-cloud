import { WorkspaceShell } from "@/components/shell/workspace-shell";

const decisionItems = [
  {
    title: "Draft trade-down",
    objective: "cut_payroll",
    confidence: "medium",
    summary:
      "Trade down can improve flexibility if surplus value is preserved and fixed commitments do not increase.",
  },
  {
    title: "ClaimCheck positioning",
    objective: "preserve_optionality",
    confidence: "medium",
    summary:
      "Lender-aligned claims stewardship appears structurally stronger when authority, sequencing, and restoration standards are unified.",
  },
  {
    title: "Bank partner thesis",
    objective: "maximize_strategic_fit",
    confidence: "unknown",
    summary:
      "Partnership logic is promising, but more concrete institutional requirements are needed before underwriting conviction increases.",
  },
];

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
          This surface will become the durable system of record for governed
          decision artifacts.
        </div>
      </div>

      <div>
        <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
          Next Build Target
        </div>
        <div className="mt-2 text-sm text-zinc-200">
          Replace placeholder rows with persisted artifacts from the decision
          journal and retrieval endpoints.
        </div>
      </div>
    </div>
  </div>
);

export default function DecisionsPage() {
  const selected = decisionItems[0];

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
          Structured decision artifacts will live here so the organization can
          revisit, inspect, and compare its prior judgment instead of losing it
          in chat history.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
          <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-zinc-500">
            Recent Decision Artifacts
          </div>

          <div className="space-y-3">
            {decisionItems.map((item, idx) => (
              <div
                key={item.title}
                className={`rounded-xl border px-4 py-3 ${
                  idx === 0
                    ? "border-zinc-600 bg-zinc-100 text-zinc-950"
                    : "border-zinc-800 bg-zinc-950 text-zinc-300"
                }`}
              >
                <div className="text-sm font-semibold">{item.title}</div>
                <div className="mt-1 text-xs opacity-80">
                  Objective: {item.objective}
                </div>
                <div className="mt-1 text-xs opacity-80">
                  Confidence: {item.confidence}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-5">
          <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">
            Artifact Detail
          </div>

          <div className="space-y-4">
            <div>
              <h2 className="text-lg font-semibold text-zinc-100">
                {selected.title}
              </h2>
              <p className="mt-2 text-sm text-zinc-400">
                Objective: {selected.objective}
              </p>
              <p className="mt-1 text-sm text-zinc-400">
                Confidence: {selected.confidence}
              </p>
            </div>

            <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                Summary
              </div>
              <p className="mt-2 text-sm leading-6 text-zinc-300">
                {selected.summary}
              </p>
            </div>

            <div className="grid gap-4 lg:grid-cols-2">
              <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                  Why this surface matters
                </div>
                <p className="mt-2 text-sm leading-6 text-zinc-300">
                  Decisions should become durable artifacts rather than
                  disappearing back into conversational history.
                </p>
              </div>

              <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                  What comes next
                </div>
                <p className="mt-2 text-sm leading-6 text-zinc-300">
                  Retrieval, comparison, and persistence-backed artifact browsing
                  will turn this from a placeholder into real decision memory.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </WorkspaceShell>
  );
}
