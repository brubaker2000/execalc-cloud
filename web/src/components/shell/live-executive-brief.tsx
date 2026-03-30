type RailNugget = {
  id: string;
  label: string;
  body: string;
  kind?: "boundary" | "anomaly" | "signal" | "insight" | "action" | "memory";
  priority?: number;
};

type ExecutiveArtifact = {
  label?: string;
  updatedAt?: string;
  sourceSurface?: string;
  status?: string;
  coreThesis: string;
  executiveBrief: string;
  keyInsights: string[];
  decisionSignal: string;
  railNuggets?: RailNugget[];
};

type LiveExecutiveBriefProps = {
  artifact: ExecutiveArtifact;
};

const nuggetTone: Record<NonNullable<RailNugget["kind"]>, string> = {
  boundary: "border-amber-700/40 bg-amber-950/20",
  anomaly: "border-red-800/40 bg-red-950/20",
    signal: "border-violet-800/40 bg-violet-950/20",
  insight: "border-zinc-800 bg-zinc-900",
  action: "border-emerald-800/40 bg-emerald-950/20",
  memory: "border-sky-800/40 bg-sky-950/20",
};

export function LiveExecutiveBrief({
  artifact,
}: LiveExecutiveBriefProps) {
  const runtimeNuggets = [...(artifact.railNuggets || [])].sort(
    (a, b) => (b.priority || 0) - (a.priority || 0)
  );
  const sectionTitle = runtimeNuggets.length > 0 ? "Runtime Nuggets" : "Key Insights";

  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
      <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
        {artifact.label || "Live Executive Brief"}
      </div>

      {artifact.updatedAt || artifact.sourceSurface || artifact.status ? (
        <div className="mt-3 flex flex-wrap gap-2 text-xs text-zinc-400">
          {artifact.updatedAt ? (
            <div className="rounded-full border border-zinc-800 bg-zinc-950 px-2 py-1">
              Updated: {artifact.updatedAt}
            </div>
          ) : null}
          {artifact.sourceSurface ? (
            <div className="rounded-full border border-zinc-800 bg-zinc-950 px-2 py-1">
              Surface: {artifact.sourceSurface}
            </div>
          ) : null}
          {artifact.status ? (
            <div className="rounded-full border border-zinc-800 bg-zinc-950 px-2 py-1">
              Status: {artifact.status}
            </div>
          ) : null}
        </div>
      ) : null}

      <div className="mt-4 space-y-4">
        <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
          <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
            Core Thesis
          </div>
          <p className="mt-2 text-sm leading-6 text-zinc-200">
            {artifact.coreThesis}
          </p>
        </div>

        <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
          <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
            Executive Brief
          </div>
          <p className="mt-2 text-sm leading-6 text-zinc-300">
            {artifact.executiveBrief}
          </p>
        </div>

        <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
          <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
            {sectionTitle}
          </div>
          <div className="mt-2 space-y-2">
            {runtimeNuggets.length > 0
              ? runtimeNuggets.map((nugget) => (
                  <div
                    key={nugget.id}
                    className={`rounded-lg border px-3 py-3 ${nugget.kind ? nuggetTone[nugget.kind] : "border-zinc-800 bg-zinc-900"}`}
                  >
                    <div className="text-[11px] font-semibold uppercase tracking-wide text-zinc-400">
                      {nugget.label}
                    </div>
                    <div className="mt-1 text-sm leading-6 text-zinc-200">
                      {nugget.body}
                    </div>
                  </div>
                ))
              : artifact.keyInsights.map((insight) => (
                  <div
                    key={insight}
                    className="rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm leading-6 text-zinc-300"
                  >
                    {insight}
                  </div>
                ))}
          </div>
        </div>

        <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">
          <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
            Decision Signal
          </div>
          <p className="mt-2 text-sm leading-6 text-zinc-200">
            {artifact.decisionSignal}
          </p>
        </div>
      </div>
    </div>
  );
}

export type { ExecutiveArtifact, RailNugget };
