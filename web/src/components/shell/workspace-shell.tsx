type WorkspaceShellItem = {
  label: string;
  active?: boolean;
};

type WorkspaceShellProps = {
  activeTab: "Execalc" | "Decisions" | "Diagnostics" | "Planning" | "Signals" | "Admin";
  children: React.ReactNode;
  rightRail?: React.ReactNode;
  workspaceLabel?: string;
  projects?: WorkspaceShellItem[];
  chats?: WorkspaceShellItem[];
  recentDecisions?: WorkspaceShellItem[];
};

const surfaceTabs = [
  "Execalc",
  "Decisions",
  "Diagnostics",
  "Planning",
  "Signals",
  "Admin",
] as const;

const defaultProjects: WorkspaceShellItem[] = [
  { label: "PCG Workspace", active: true },
  { label: "Athlete Equity" },
  { label: "ClaimCheck" },
  { label: "Wells Fargo" },
];

const defaultChats: WorkspaceShellItem[] = [
  { label: "Nick lender thesis" },
  { label: "Bow River model" },
  { label: "Org cognition notes" },
  { label: "Stage 8 UI shell" },
];

const defaultRecentDecisions: WorkspaceShellItem[] = [
  { label: "Draft trade-down" },
  { label: "ClaimCheck positioning" },
  { label: "Bank partner thesis" },
];

export function WorkspaceShell({
  activeTab,
  children,
  rightRail,
  workspaceLabel = "PCG Workspace",
  projects = defaultProjects,
  chats = defaultChats,
  recentDecisions = defaultRecentDecisions,
}: WorkspaceShellProps) {
  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100">
      <div className="flex min-h-screen flex-col">
        <header className="border-b border-zinc-800 bg-zinc-950/95">
          <div className="flex h-14 items-center justify-between px-4">
            <div className="flex items-center gap-3">
              <div className="rounded-md border border-zinc-700 bg-zinc-900 px-2 py-1 text-sm font-semibold">
                Execalc
              </div>
              <div className="text-sm text-zinc-400">{workspaceLabel}</div>
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
            {surfaceTabs.map((tab) => {
              const href = tab === "Execalc" ? "/execalc" : `/${tab.toLowerCase()}`;
              const active = tab === activeTab;

              return (
                <a
                  key={tab}
                  href={href}
                  className={`rounded-md border px-3 py-1.5 text-sm ${
                    active
                      ? "border-zinc-600 bg-zinc-100 text-zinc-950"
                      : "border-zinc-800 bg-zinc-900 text-zinc-300"
                  }`}
                >
                  {tab}
                </a>
              );
            })}
          </div>
        </header>

        <div className="flex flex-1 overflow-hidden">
          <aside className="hidden w-72 shrink-0 border-r border-zinc-800 bg-zinc-900 md:flex md:flex-col">
            <div className="border-b border-zinc-800 px-4 py-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                Projects
              </div>
              <div className="mt-3 space-y-2">
                {projects.map((project) => (
                  <div
                    key={project.label}
                    className={
                      project.active
                        ? "rounded-md bg-zinc-100 px-3 py-2 text-sm text-zinc-950"
                        : "rounded-md bg-zinc-800 px-3 py-2 text-sm text-zinc-300"
                    }
                  >
                    {project.label}
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
                    key={chat.label}
                    className={
                      chat.active
                        ? "rounded-md bg-zinc-100 px-3 py-2 text-sm text-zinc-950"
                        : "rounded-md bg-zinc-800 px-3 py-2 text-sm text-zinc-300"
                    }
                  >
                    {chat.label}
                  </div>
                ))}
              </div>
            </div>

            <div className="px-4 py-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
                Recent Decisions
              </div>
              <div className="mt-3 space-y-2">
                {recentDecisions.map((decisionItem) => (
                  <div
                    key={decisionItem.label}
                    className={
                      decisionItem.active
                        ? "rounded-md bg-zinc-100 px-3 py-2 text-sm text-zinc-950"
                        : "rounded-md bg-zinc-800 px-3 py-2 text-sm text-zinc-300"
                    }
                  >
                    {decisionItem.label}
                  </div>
                ))}
              </div>
            </div>
          </aside>

          <section className="flex min-w-0 flex-1 flex-col">
            <div className="flex-1 overflow-y-auto px-4 py-6 md:px-6">
              <div className="mx-auto flex h-full w-full max-w-5xl gap-6">
                <div className="flex min-w-0 flex-1 flex-col">{children}</div>

                {rightRail ? (
                  <aside className="hidden w-80 shrink-0 lg:block">{rightRail}</aside>
                ) : null}
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}
