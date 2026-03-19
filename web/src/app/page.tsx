const surfaceTabs = [
  "Execalc",
  "Decisions",
  "Diagnostics",
  "Planning",
  "Signals",
  "Admin",
];

const projects = [
  "PCG Workspace",
  "Athlete Equity",
  "ClaimCheck",
  "Wells Fargo",
];

const chats = [
  "Nick lender thesis",
  "Bow River model",
  "Org cognition notes",
  "Stage 8 UI shell",
];

const recentDecisions = [
  "Draft trade-down",
  "ClaimCheck positioning",
  "Bank partner thesis",
];

const signals = [
  "Rising disagreement around pricing language",
  "Emerging lender outreach opportunity",
  "Cross-thread concern about execution burden",
];

export default function Home() {
  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100">
      <div className="flex min-h-screen flex-col">
        <header className="border-b border-zinc-800 bg-zinc-950/95">
          <div className="flex h-14 items-center justify-between px-4">
            <div className="flex items-center gap-3">
              <div className="rounded-md border border-zinc-700 bg-zinc-900 px-2 py-1 text-sm font-semibold">
                Execalc
              </div>
              <div className="text-sm text-zinc-400">PCG Workspace</div>
            </div>

            <div className="hidden flex-1 justify-center px-8 md:flex">
              <div className="w-full max-w-md rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm text-zinc-400">
                Search workspace
              </div>
            </div>

            <div className="flex items-center gap-3 text-sm text-zinc-400">
              <div className="rounded-md border border-zinc-800 bg-zinc-900 px-3 py-1.5">
                Alerts
              </div>
              <div className="rounded-md border border-zinc-800 bg-zinc-900 px-3 py-1.5">
                Profile
              </div>
            </div>
          </div>

          <div className="flex gap-2 overflow-x-auto px-4 py-3">
            {surfaceTabs.map((tab) => (
              <div
                key={tab}
                className={`rounded-md border px-3 py-1.5 text-sm ${
                  tab === "Execalc"
                    ? "border-zinc-600 bg-zinc-100 text-zinc-950"
                    : "border-zinc-800 bg-zinc-900 text-zinc-300"
                }`}
              >
                {tab}
              </div>
            ))}
          </div>
        </header>

        <div className="flex flex-1 overflow-hidden">
          <aside className="hidden w-72 shrink-0 border-r border-zinc-800 bg-zinc-900 md:flex md:flex-col">
            <div className="border-b border-zinc-800 px-4 py-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                Projects
              </div>
              <div className="mt-3 space-y-2">
                {projects.map((project, idx) => (
                  <div
                    key={project}
                    className={`rounded-md px-3 py-2 text-sm ${
                      idx === 0
                        ? "bg-zinc-100 text-zinc-950"
                        : "bg-zinc-800 text-zinc-300"
                    }`}
                  >
                    {project}
                  </div>
                ))}
              </div>
            </div>

            <div className="border-b border-zinc-800 px-4 py-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                Chats
              </div>
              <div className="mt-3 space-y-2">
                {chats.map((chat) => (
                  <div
                    key={chat}
                    className="rounded-md bg-zinc-800 px-3 py-2 text-sm text-zinc-300"
                  >
                    {chat}
                  </div>
                ))}
              </div>
            </div>

            <div className="px-4 py-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                Recent Decisions
              </div>
              <div className="mt-3 space-y-2">
                {recentDecisions.map((decision) => (
                  <div
                    key={decision}
                    className="rounded-md bg-zinc-800 px-3 py-2 text-sm text-zinc-300"
                  >
                    {decision}
                  </div>
                ))}
              </div>
            </div>
          </aside>

          <section className="flex min-w-0 flex-1 flex-col">
            <div className="flex-1 overflow-y-auto px-4 py-6 md:px-6">
              <div className="mx-auto flex h-full w-full max-w-5xl gap-6">
                <div className="flex min-w-0 flex-1 flex-col">
                  <div className="mb-6">
                    <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                      Workbench Mode
                    </div>
                    <h1 className="mt-2 text-2xl font-semibold tracking-tight">
                      Execalc Chat Workspace
                    </h1>
                    <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-400">
                      A governed executive workbench for discussion, structured
                      reasoning, decision formation, and continuity across live
                      organizational work.
                    </p>
                  </div>

                  <div className="space-y-4">
                    <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
                      <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">
                        Operator
                      </div>
                      <p className="text-sm leading-6 text-zinc-200">
                        We think this design will make Execalc very sticky. I
                        want the workspace to feel familiar like a browser, but
                        actually function like a governed operating system for
                        executive cognition.
                      </p>
                    </div>

                    <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
                      <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">
                        Execalc
                      </div>
                      <p className="text-sm leading-6 text-zinc-200">
                        The central surface should remain conversational, but the
                        surrounding workspace should support decisions,
                        diagnostics, planning, monitoring, and role-governed
                        organizational synthesis.
                      </p>

                      <div className="mt-4 flex flex-wrap gap-2">
                        {[
                          "Refine",
                          "Summarize",
                          "Formalize",
                          "Pressure Test",
                          "Convert to Decision",
                        ].map((action) => (
                          <button
                            key={action}
                            type="button"
                            className="rounded-full border border-zinc-700 bg-zinc-950 px-3 py-1.5 text-xs font-medium text-zinc-200"
                          >
                            {action}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                <aside className="hidden w-80 shrink-0 lg:block">
                  <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
                    <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                      Context
                    </div>

                    <div className="mt-4 space-y-4">
                      <div>
                        <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                          Active Project
                        </div>
                        <div className="mt-2 text-sm text-zinc-200">
                          PCG Workspace
                        </div>
                      </div>

                      <div>
                        <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                          Current Thread
                        </div>
                        <div className="mt-2 text-sm text-zinc-200">
                          Stage 8 UI shell scaffold
                        </div>
                      </div>

                      <div>
                        <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                          Organizational Signals
                        </div>
                        <div className="mt-2 space-y-2">
                          {signals.map((signal) => (
                            <div
                              key={signal}
                              className="rounded-xl border border-zinc-800 bg-zinc-950 px-3 py-2 text-sm text-zinc-300"
                            >
                              {signal}
                            </div>
                          ))}
                        </div>
                      </div>

                      <div>
                        <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                          Current Objective
                        </div>
                        <div className="mt-2 text-sm text-zinc-200">
                          Establish the first executable UI shell for the
                          strategic operating system.
                        </div>
                      </div>
                    </div>
                  </div>
                </aside>
              </div>
            </div>

            <div className="border-t border-zinc-800 bg-zinc-950 px-4 py-4 md:px-6">
              <div className="mx-auto flex w-full max-w-5xl gap-3">
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
          </section>
        </div>
      </div>
    </main>
  );
}
