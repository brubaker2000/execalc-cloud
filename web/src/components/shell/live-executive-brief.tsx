type ExecutiveArtifact = {
  coreThesis: string;
  executiveBrief: string;
  keyInsights: string[];
  decisionSignal: string;
};

type LiveExecutiveBriefProps = {
  artifact: ExecutiveArtifact;
};

export function LiveExecutiveBrief({
  artifact,
}: LiveExecutiveBriefProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
      <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
        Live Executive Brief
      </div>

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
            Key Insights
          </div>
          <div className="mt-2 space-y-2">
            {artifact.keyInsights.map((insight) => (
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

export type { ExecutiveArtifact };
