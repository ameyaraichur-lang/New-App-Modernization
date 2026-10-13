import { useEffect, useMemo, useState } from 'react';
import { api, can, getToken, setToken, type Me } from '../api';
import { fmt, ms, percentile, useLiveRun, type AgentRun, type Ev } from '../live';

interface RunRow { job_id: string; repo: string; status: string; started_at: string | null; progress: number; apps: string[] }
interface JobSnap {
  job_id: string; status: string; stage_detail: string | null; progress: number; apps: string[];
  started_at: string | null; finished_at: string | null;
  llm: { enabled: boolean; calls: number; input_tokens: number; output_tokens: number; failovers: number; cached: number; tool_calls: number };
}
interface Health {
  astra: { configured: boolean; llm_mode: string; cache: string; tiers: Record<string, string>; embedding: string };
  analyzers: { tools: Record<string, { available: boolean; version?: string; error?: string }> };
  tools: { name: string; needs_repo: boolean; description: string }[];
  mcp: { configured: string[]; connected: string[]; tools: string[]; errors: Record<string, string> };
}
interface ProbeResult {
  kind: string; deployment: string; tiers: string[]; ok: boolean; latency_ms: number; model?: string;
  reply?: string; input_tokens?: number; output_tokens?: number; reasoning_tokens?: number; dimensions?: number; error?: string;
}
interface Probe { configured: boolean; endpoint_host: string | null; api_version: string; probed_at: string; results: ProbeResult[] }

type Tab = 'live' | 'agent' | 'analysis' | 'connectivity';
const ACTIVE = ['PENDING', 'QUEUED', 'RUNNING', 'AWAITING_REVIEW'];
const TERMINAL_NODE = ['COMPLETE', 'PARTIAL', 'FAILED', 'NOT_ASSESSED', 'SKIPPED_APPROVED', 'AWAITING_REVIEW', 'BLOCKED'];

const stage = (a: AgentRun) =>
  TERMINAL_NODE.includes(a.status) ? a.status
    : a.done ? 'CHECKING'
      : a.rejections.length && a.rejections[a.rejections.length - 1].seq > (a.modelCalls[a.modelCalls.length - 1]?.seq ?? 0) ? 'REPAIRING'
        : a.modelCalls.length ? 'INVESTIGATING' : a.status;

const STAGE_COLOR: Record<string, string> = {
  INVESTIGATING: 'blue', REPAIRING: 'amber', CHECKING: 'purple', COMPLETE: 'green', PARTIAL: 'amber',
  FAILED: 'red', BLOCKED: 'red', AWAITING_REVIEW: 'amber', SKIPPED_APPROVED: '', NOT_ASSESSED: 'amber',
};

export function LiveAgents() {
  const [me, setMe] = useState<Me | null>(null);
  const [checking, setChecking] = useState(() => !!getToken());
  const [tokenDraft, setTokenDraft] = useState('');
  const [runs, setRuns] = useState<RunRow[]>([]);
  const [jobId, setJobId] = useState<string | null>(null);
  const [job, setJob] = useState<JobSnap | null>(null);
  const [tab, setTab] = useState<Tab>('live');
  const [selected, setSelected] = useState<string | null>(null);
  const live = useLiveRun(me ? jobId : null);

  async function login(tok?: string) {
    if (tok !== undefined) setToken(tok);
    try {
      setMe(await api<Me>('/api/me'));
      const rows = await api<RunRow[]>('/api/runs');
      setRuns(rows);
      setJobId((cur) => cur ?? rows.find((r) => ACTIVE.includes(r.status))?.job_id ?? rows[0]?.job_id ?? null);
    } catch { setMe(null); }
    setChecking(false);
  }
  useEffect(() => { login(); }, []);

  useEffect(() => {
    if (!jobId || !me) return;
    let stop = false;
    const tick = async () => {
      try { const s = await api<JobSnap>(`/api/runs/${jobId}`); if (!stop) setJob(s); } catch { /* transient */ }
    };
    tick();
    const t = window.setInterval(tick, 3000);
    return () => { stop = true; window.clearInterval(t); };
  }, [jobId, me]);

  if (!me && checking) return <div className="live"><div className="kv muted">Checking sign-in…</div></div>;
  if (!me) {
    return (
      <div className="live">
        <div className="card" style={{ maxWidth: 620 }}>
          <h3>Sign in to watch agents</h3>
          <p className="body">Paste an API token (viewer is enough to watch; the connectivity probe needs operator).</p>
          <div style={{ display: 'flex', gap: 8 }}>
            <input className="input" type="password" style={{ flex: 1 }} value={tokenDraft} placeholder="bearer token"
                   onChange={(e) => setTokenDraft(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') login(tokenDraft.trim()); }} />
            <button className="btn-primary" onClick={() => login(tokenDraft.trim())}>Sign in</button>
          </div>
          {getToken() && <div className="kv" style={{ color: 'var(--red)' }}>Stored token was rejected.</div>}
        </div>
      </div>
    );
  }

  const agents = [...live.agents.values()];
  const running = !!job && ACTIVE.includes(job.status);
  const lastConn = [...live.events].reverse().find((e) => e.kind === 'CONNECTIVITY');
  const paused = running && lastConn?.status === 'LOST';

  return (
    <div className="live">
      <div className="live-head">
        <div>
          <div className="live-title">Live agentic operation</div>
          <div className="kv">Watch each agent investigate with tools, submit, get checked by the kernel and publish.</div>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span className={`dot ${live.connected ? 'on' : running ? 'warn' : ''}`} />
          <span className="kv">{live.loading ? 'loading history…' : live.connected ? 'streaming' : running ? 'reconnecting' : 'not live'}</span>
          <select className="input" value={jobId ?? ''} onChange={(e) => { setJobId(e.target.value); setSelected(null); }}>
            {runs.map((r) => (
              <option key={r.job_id} value={r.job_id}>
                {r.job_id.slice(-12)} · {r.status} · {r.apps?.length || 1} app{(r.apps?.length || 1) > 1 ? 's' : ''} · {r.progress}%
              </option>
            ))}
          </select>
          <button className="btn-secondary" onClick={() => login()}>Refresh</button>
        </div>
      </div>

      {job && (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <span className={`chip ${running ? 'blue pulse' : job.status === 'COMPLETED' ? 'green' : 'amber'}`}>{job.status}</span>
              <span className="kv">{job.stage_detail}</span>
            </div>
            <span className="kv">{job.apps?.length} apps · {job.progress}%</span>
          </div>
          <div className="progress-track"><div className="progress-fill" style={{ width: `${job.progress}%` }} /></div>
          {paused && (
            <div className="outage-banner">
              ⚡ Astra has been unreachable since {lastConn.ts.slice(11, 19)} UTC. Model work is paused and
              agent retries are not being spent; agents resume on their own once the endpoint answers.
            </div>
          )}
        </div>
      )}

      <LoopExplainer agents={agents} />

      <div className="tabs">
        {([['live', 'Live operation'], ['agent', 'Agent loop'], ['analysis', 'LLM analysis'], ['connectivity', 'Connectivity']] as [Tab, string][])
          .map(([t, label]) => (
            <button key={t} className={`tab ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>{label}</button>
          ))}
      </div>

      {tab === 'live' && <LiveTab agents={agents} events={live.events} onOpen={(k) => { setSelected(k); setTab('agent'); }} />}
      {tab === 'agent' && <AgentTab agents={agents} selected={selected} onSelect={setSelected} />}
      {tab === 'analysis' && <AnalysisTab agents={agents} events={live.events} />}
      {tab === 'connectivity' && <ConnectivityTab me={me} />}
    </div>
  );
}

// -- how an agent works -------------------------------------------------------------------

function LoopExplainer({ agents }: { agents: AgentRun[] }) {
  const tools = agents.reduce((n, a) => n + a.toolCalls.length, 0);
  const turns = agents.reduce((n, a) => n + a.modelCalls.length, 0);
  const rejected = agents.reduce((n, a) => n + a.rejections.length, 0);
  const done = agents.filter((a) => a.done).length;
  const published = agents.filter((a) => TERMINAL_NODE.includes(a.status)).length;
  const steps = [
    { n: '1', title: 'Seed', body: 'Deterministic tools measure the repo first (scan, LOC, SBOM, analyzers). The seed is never rewritten by the model.',
      stat: `${agents.length} agents seen` },
    { n: '2', title: 'Investigate', body: 'The model calls allowlisted tools (read_file, grep, search_code, scanners). Every result gets an evidence id.',
      stat: `${fmt(turns)} model turns · ${fmt(tools)} tool calls` },
    { n: '3', title: 'Submit', body: 'It finishes with a strict submit_outcome: findings, gaps and payload items, each citing evidence ids, with a confidence.',
      stat: `${done} submissions accepted` },
    { n: '4', title: 'Kernel checks', body: 'Unknown evidence ids, invented paths or symbols and schema errors bounce the submission back for repair (up to 2).',
      stat: `${rejected} bounced for repair` },
    { n: '5', title: 'Merge & gate', body: 'Only the agent\u2019s own fields merge into the seed; status can only get stricter. Gates are deterministic; humans approve releases.',
      stat: `${published} published` },
  ];
  return (
    <div className="loop">
      {steps.map((s, i) => (
        <div key={s.n} className="loop-step">
          <div className="loop-n">{s.n}</div>
          <div className="loop-title">{s.title}</div>
          <div className="loop-body">{s.body}</div>
          <div className="loop-stat">{s.stat}</div>
          {i < steps.length - 1 && <div className="loop-arrow">→</div>}
        </div>
      ))}
    </div>
  );
}

// -- live operation -----------------------------------------------------------------------

function LiveTab({ agents, events, onOpen }: { agents: AgentRun[]; events: Ev[]; onOpen: (k: string) => void }) {
  const [filter, setFilter] = useState<'all' | 'MODEL_CALL' | 'TOOL_CALL' | 'SUBMISSION_REJECTED' | 'AGENT_LLM_DONE'>('all');
  const active = agents.filter((a) => !TERMINAL_NODE.includes(a.status) && a.modelCalls.length)
    .sort((x, y) => (y.lastAt ?? '').localeCompare(x.lastAt ?? ''));
  const feed = events.filter((e) => e.kind !== 'NODE' && (filter === 'all' || e.kind === filter)).slice(-150).reverse();
  return (
    <div className="grid2">
      <div className="card">
        <h3>Working now <span className="chip blue">{active.length}</span></h3>
        {active.length === 0 && <div className="kv">No agent is mid-loop. Pick a running job, or open a finished agent from the Agent loop tab.</div>}
        <div className="agent-cards">
          {active.map((a) => {
            const lastTool = a.toolCalls[a.toolCalls.length - 1];
            const st = stage(a);
            return (
              <button key={a.key} className="agent-card" onClick={() => onOpen(a.key)}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <b>P{a.phase}.{a.node}</b>
                  <span className={`chip ${STAGE_COLOR[st] ?? ''} ${st === 'INVESTIGATING' ? 'pulse' : ''}`}>{st.toLowerCase()}</span>
                </div>
                <div className="kv">{a.app}</div>
                <div className="kv">turn {a.turns} · {a.toolCalls.length} tools · {fmt(a.tokensIn + a.tokensOut)} tokens</div>
                {lastTool && <div className="kv mono">↳ {String(lastTool.tool)}({argsBrief(lastTool.args)})</div>}
              </button>
            );
          })}
        </div>
      </div>
      <div className="card">
        <h3>
          Event feed
          <select className="input small" style={{ float: 'right' }} value={filter} onChange={(e) => setFilter(e.target.value as typeof filter)}>
            <option value="all">all</option><option value="MODEL_CALL">model calls</option><option value="TOOL_CALL">tool calls</option>
            <option value="SUBMISSION_REJECTED">rejections</option><option value="AGENT_LLM_DONE">agent done</option>
            <option value="CONNECTIVITY">connectivity</option>
          </select>
        </h3>
        <div className="feed">
          {feed.map((e) => <FeedLine key={e.seq} e={e} onOpen={onOpen} />)}
          {feed.length === 0 && <div className="kv">No events yet.</div>}
        </div>
      </div>
    </div>
  );
}

function FeedLine({ e, onOpen }: { e: Ev; onOpen: (k: string) => void }) {
  if (e.kind === 'CONNECTIVITY') {
    const text = e.status === 'LOST' ? 'Astra unreachable — model work paused, retries not spent'
      : e.status === 'RESTORED' ? `Astra reachable again after ${String(e.waited_s)} s — model work resumed`
        : `stopped waiting for Astra (${String(e.reason)})`;
    return (
      <div className="feed-line CONNECTIVITY">
        <span className="muted">{e.ts.slice(11, 19)}</span> <span className="feed-icon">⚡</span>{' '}
        <span className={e.status === 'RESTORED' ? '' : 'err'}>{text}</span>
      </div>
    );
  }
  const who = `P${e.phase}.${e.node} ${e.app}`;
  const open = () => onOpen(`P${e.phase}/${e.app}/${e.node}`);
  let body: React.ReactNode;
  if (e.kind === 'MODEL_CALL') {
    const asks = Array.isArray(e.tool_calls) ? (e.tool_calls as string[]) : [];
    body = <>turn {String(e.turn)} · {String(e.deployment)} · {ms(Number(e.latency_ms ?? 0))} · {fmt(Number(e.input_tokens ?? 0))}→{fmt(Number(e.output_tokens ?? 0))} tok
      {e.cached ? ' · cached' : ''}{e.failover ? ' · failover' : ''}{asks.length ? ` · asks ${asks.join(', ')}` : ''}
      {e.error ? <span className="err"> {String(e.error)}</span> : null}</>;
  } else if (e.kind === 'TOOL_CALL') {
    body = <><span className="mono">{String(e.tool)}({argsBrief(e.args)})</span> · {String(e.status)} · {String(e.ms ?? '')} ms
      {e.evidence_id ? <span className="mono muted"> → {String(e.evidence_id)}</span> : null}</>;
  } else if (e.kind === 'SUBMISSION_REJECTED') {
    body = <span className="err">submission bounced: {(e.problems as string[] | undefined)?.[0] ?? ''}</span>;
  } else {
    body = <>done · {String(e.status)} · {String(e.turns)} turns · {String(e.tool_calls)} tools{e.repairs ? ` · ${String(e.repairs)} repairs` : ''}</>;
  }
  const icon = { MODEL_CALL: '◆', TOOL_CALL: '⚙', SUBMISSION_REJECTED: '↺', AGENT_LLM_DONE: '✓', NODE: '·' }[e.kind];
  return (
    <div className={`feed-line ${e.kind}`} onClick={open}>
      <span className="muted">{e.ts.slice(11, 19)}</span> <span className="feed-icon">{icon}</span> <b>{who}</b> · {body}
    </div>
  );
}

function argsBrief(args: unknown): string {
  if (!args || typeof args !== 'object') return '';
  return Object.entries(args as Record<string, unknown>).map(([k, v]) => `${k}=${String(v).slice(0, 40)}`).join(', ').slice(0, 90);
}

// -- one agent's loop ---------------------------------------------------------------------

function AgentTab({ agents, selected, onSelect }: { agents: AgentRun[]; selected: string | null; onSelect: (k: string) => void }) {
  const [q, setQ] = useState('');
  const list = agents.filter((a) => a.modelCalls.length && `${a.key} ${a.app}`.toLowerCase().includes(q.toLowerCase()))
    .sort((x, y) => x.phase - y.phase || x.app.localeCompare(y.app) || x.node.localeCompare(y.node, undefined, { numeric: true }));
  const a = agents.find((x) => x.key === selected) ?? null;
  return (
    <div className="split-agent">
      <div className="card agent-list">
        <input className="input" placeholder="filter agents or apps" value={q} onChange={(e) => setQ(e.target.value)} style={{ width: '100%' }} />
        {list.map((x) => {
          const st = stage(x);
          return (
            <button key={x.key} className={`agent-row ${x.key === selected ? 'active' : ''}`} onClick={() => onSelect(x.key)}>
              <span><b>P{x.phase}.{x.node}</b> <span className="muted">{x.app}</span></span>
              <span className={`chip ${STAGE_COLOR[st] ?? ''}`}>{st.toLowerCase()}</span>
            </button>
          );
        })}
      </div>
      <div>{a ? <Timeline a={a} /> : <div className="card kv">Select an agent to replay its loop turn by turn.</div>}</div>
    </div>
  );
}

function Timeline({ a }: { a: AgentRun }) {
  const steps = [...a.modelCalls, ...a.toolCalls, ...a.rejections, ...(a.done ? [a.done] : [])].sort((x, y) => x.seq - y.seq);
  const done = a.done;
  return (
    <>
      <div className="card">
        <h3>P{a.phase}.{a.node} · {a.app} <span className={`chip ${STAGE_COLOR[stage(a)] ?? ''}`}>{stage(a).toLowerCase()}</span></h3>
        <div className="kpis">
          <Kpi label="model turns" value={String(a.modelCalls.length)} />
          <Kpi label="tool calls" value={String(a.toolCalls.length)} />
          <Kpi label="repairs" value={String(a.rejections.length)} />
          <Kpi label="tokens in / out" value={`${fmt(a.tokensIn)} / ${fmt(a.tokensOut)}`} />
          <Kpi label="model time" value={ms(a.latencyMs)} />
          <Kpi label="models" value={[...a.deployments].join(', ') || '—'} />
        </div>
        {done?.summary ? <p className="body">{String(done.summary)}</p> : null}
      </div>
      <div className="card">
        <h3>Loop replay <span className="chip">{steps.length} steps</span></h3>
        <div className="timeline">
          {steps.map((e) => (
            <div key={e.seq} className={`tl ${e.kind}`}>
              <div className="tl-dot" />
              <div className="tl-body">
                <div className="tl-head">
                  <b>{{ MODEL_CALL: `Model turn ${String(e.turn ?? '')}`, TOOL_CALL: `Tool · ${String(e.tool)}`,
                        SUBMISSION_REJECTED: 'Kernel bounced the submission', AGENT_LLM_DONE: 'Submission accepted', NODE: '',
                        CONNECTIVITY: '' }[e.kind]}</b>
                  <span className="muted">{e.ts.slice(11, 19)}</span>
                </div>
                {e.kind === 'MODEL_CALL' && (
                  <div className="kv">{String(e.deployment)} · {ms(Number(e.latency_ms ?? 0))} · in {fmt(Number(e.input_tokens ?? 0))} · out {fmt(Number(e.output_tokens ?? 0))}
                    {Number(e.reasoning_tokens ?? 0) ? ` · reasoning ${fmt(Number(e.reasoning_tokens))}` : ''}{e.cached ? ' · cached' : ''}{e.failover ? ' · failover' : ''}
                    {Array.isArray(e.tool_calls) && (e.tool_calls as string[]).length ? <> · requested <span className="mono">{(e.tool_calls as string[]).join(', ')}</span></> : null}
                    {e.error ? <div className="err">{String(e.error)}</div> : null}</div>
                )}
                {e.kind === 'TOOL_CALL' && (
                  <div className="kv"><span className="mono">{argsBrief(e.args)}</span> · {String(e.status)} · {String(e.ms ?? '')} ms · {fmt(Number(e.bytes ?? 0))} bytes
                    {e.evidence_id ? <> · evidence <span className="mono">{String(e.evidence_id)}</span></> : null}</div>
                )}
                {e.kind === 'SUBMISSION_REJECTED' && (
                  <ul className="problems">{((e.problems as string[]) ?? []).map((p, i) => <li key={i}>{p}</li>)}</ul>
                )}
                {e.kind === 'AGENT_LLM_DONE' && (
                  <div className="kv">status {String(e.status)} · {String(e.mode)} · {String(e.turns)} turns · {String(e.tool_calls)} tool calls
                    {Number(e.incidents ?? 0) ? <span className="err"> · {String(e.incidents)} prompt-injection incidents recorded</span> : null}</div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

function Kpi({ label, value, hint }: { label: string; value: string; hint?: string }) {
  return <div className="kpi" title={hint}><div className="kpi-v">{value}</div><div className="kpi-l">{label}</div></div>;
}

// -- LLM analysis ---------------------------------------------------------------------------

function AnalysisTab({ agents, events }: { agents: AgentRun[]; events: Ev[] }) {
  const s = useMemo(() => {
    const calls = events.filter((e) => e.kind === 'MODEL_CALL');
    const tools = events.filter((e) => e.kind === 'TOOL_CALL');
    const done = agents.filter((a) => a.done);
    const byDep = new Map<string, Ev[]>();
    calls.forEach((c) => { const k = String(c.deployment); byDep.set(k, [...(byDep.get(k) ?? []), c]); });
    const byTool = new Map<string, Ev[]>();
    tools.forEach((t) => { const k = String(t.tool); byTool.set(k, [...(byTool.get(k) ?? []), t]); });
    const byPhase = new Map<number, number>();
    agents.forEach((a) => byPhase.set(a.phase, (byPhase.get(a.phase) ?? 0) + a.tokensIn + a.tokensOut));
    const reasons = new Map<string, number>();
    events.filter((e) => e.kind === 'SUBMISSION_REJECTED').forEach((e) => ((e.problems as string[]) ?? []).forEach((p) => {
      const k = p.split(/[:(\[]/)[0].trim().slice(0, 60);
      reasons.set(k, (reasons.get(k) ?? 0) + 1);
    }));
    const live = calls.filter((c) => !c.cached);
    return {
      calls, tools, done, byDep, byTool, byPhase, reasons,
      tin: live.reduce((n, c) => n + Number(c.input_tokens ?? 0), 0),
      tout: live.reduce((n, c) => n + Number(c.output_tokens ?? 0), 0),
      treason: live.reduce((n, c) => n + Number(c.reasoning_tokens ?? 0), 0),
      cached: calls.filter((c) => c.cached).length, failovers: calls.filter((c) => c.failover).length,
      errors: calls.filter((c) => c.error).length, enriched: done.filter((a) => a.done?.enriched).length,
      repaired: done.filter((a) => a.rejections.length).length,
    };
  }, [agents, events]);
  const maxTool = Math.max(1, ...[...s.byTool.values()].map((v) => v.length));
  const maxPhase = Math.max(1, ...s.byPhase.values());
  return (
    <>
      <div className="card">
        <h3>Model usage</h3>
        <div className="kpis">
          <Kpi label="model calls" value={fmt(s.calls.length)} />
          <Kpi label="tokens in" value={fmt(s.tin)} />
          <Kpi label="tokens out" value={fmt(s.tout)} hint={`of which reasoning ${fmt(s.treason)}`} />
          <Kpi label="cache hits" value={`${s.calls.length ? Math.round((100 * s.cached) / s.calls.length) : 0}%`} />
          <Kpi label="failovers" value={String(s.failovers)} />
          <Kpi label="model errors" value={String(s.errors)} />
          <Kpi label="agents enriched" value={`${s.enriched} / ${s.done.length}`} hint="accepted model submission merged into the seed" />
          <Kpi label="needed repair" value={`${s.done.length ? Math.round((100 * s.repaired) / s.done.length) : 0}%`} />
          <Kpi label="turns per agent" value={s.done.length ? (s.done.reduce((n, a) => n + a.modelCalls.length, 0) / s.done.length).toFixed(1) : '—'} />
          <Kpi label="tools per agent" value={s.done.length ? (s.done.reduce((n, a) => n + a.toolCalls.length, 0) / s.done.length).toFixed(1) : '—'} />
        </div>
      </div>
      <div className="grid2">
        <div className="card">
          <h3>Per model deployment</h3>
          <table className="table">
            <thead><tr><th>deployment</th><th>calls</th><th>p50</th><th>p95</th><th>tokens in / out</th><th>errors</th></tr></thead>
            <tbody>
              {[...s.byDep.entries()].map(([d, cs]) => {
                const lat = cs.filter((c) => !c.cached).map((c) => Number(c.latency_ms ?? 0));
                return (
                  <tr key={d}><td className="mono">{d}</td><td>{cs.length}</td><td>{ms(percentile(lat, 50))}</td><td>{ms(percentile(lat, 95))}</td>
                    <td>{fmt(cs.reduce((n, c) => n + Number(c.input_tokens ?? 0), 0))} / {fmt(cs.reduce((n, c) => n + Number(c.output_tokens ?? 0), 0))}</td>
                    <td>{cs.filter((c) => c.error).length}</td></tr>
                );
              })}
            </tbody>
          </table>
          <h3 style={{ marginTop: 14 }}>Tokens by phase</h3>
          {[...s.byPhase.entries()].sort((a, b) => a[0] - b[0]).map(([p, n]) => (
            <div key={p} className="bar-row"><span className="bar-label">Phase {p}</span>
              <span className="bar"><span style={{ width: `${(100 * n) / maxPhase}%` }} /></span><span className="bar-v">{fmt(n)}</span></div>
          ))}
        </div>
        <div className="card">
          <h3>Tool usage</h3>
          {[...s.byTool.entries()].sort((a, b) => b[1].length - a[1].length).map(([t, cs]) => {
            const bad = cs.filter((c) => c.status !== 'OK').length;
            const avg = cs.reduce((n, c) => n + Number(c.ms ?? 0), 0) / cs.length;
            return (
              <div key={t} className="bar-row" title={`${bad} not OK · avg ${Math.round(avg)} ms`}>
                <span className="bar-label mono">{t}</span>
                <span className="bar"><span style={{ width: `${(100 * cs.length) / maxTool}%` }} /></span>
                <span className="bar-v">{cs.length}{bad ? <span className="err"> ({bad})</span> : null}</span>
              </div>
            );
          })}
          <h3 style={{ marginTop: 14 }}>Why submissions bounced</h3>
          {s.reasons.size === 0 && <div className="kv">No rejected submissions.</div>}
          {[...s.reasons.entries()].sort((a, b) => b[1] - a[1]).map(([r, n]) => (
            <div key={r} className="kv">{n} × {r}</div>
          ))}
        </div>
      </div>
    </>
  );
}

// -- connectivity -------------------------------------------------------------------------

function ConnectivityTab({ me }: { me: Me }) {
  const [health, setHealth] = useState<Health | null>(null);
  const [probe, setProbe] = useState<Probe | null>(null);
  const [probing, setProbing] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  useEffect(() => { api<Health>('/api/health/tools').then(setHealth).catch((e) => setErr(String(e))); }, []);
  async function runProbe() {
    setProbing(true); setErr(null);
    try { setProbe(await api<Probe>('/api/health/llm/probe', { method: 'POST' })); } catch (e) { setErr(String(e)); }
    setProbing(false);
  }
  const tiers = health?.astra.tiers ?? {};
  const resultFor = (dep: string, kind: string) => probe?.results.find((r) => r.deployment === dep && r.kind === kind);
  return (
    <>
      <div className="card">
        <h3>
          Astra model connectivity
          <span style={{ float: 'right' }}>
            <button className="btn-primary" onClick={runProbe} disabled={probing || !can(me, 'operator')}
                    title={can(me, 'operator') ? 'one tiny live request per deployment' : 'needs the operator role'}>
              {probing ? 'Probing…' : 'Run live probe'}
            </button>
          </span>
        </h3>
        {!health && !err && <div className="kv muted">Checking tiers, tools and analyzer versions…</div>}
        {health && (
          <div className="kv">
            {health.astra.configured ? <span className="chip green">configured</span> : <span className="chip red">not configured</span>}
            llm mode <b>{health.astra.llm_mode}</b> · response cache <b>{health.astra.cache}</b>
            {probe?.endpoint_host && <> · endpoint <b>{probe.endpoint_host}</b> · api {probe.api_version}</>}
          </div>
        )}
        <p className="body muted">The probe sends “Reply with OK.” to every deployment directly (no cache, no retries) and reports what came back.
          Agents pick a tier per role: reasoning for analysis, coding for task DAGs, fast for descriptor work; fallback takes over on transient errors.</p>
        <div className="tier-grid">
          {[...Object.entries(tiers).map(([t, d]) => ({ t, d, kind: 'responses' })), ...(health ? [{ t: 'embedding', d: health.astra.embedding, kind: 'embeddings' }] : [])]
            .map(({ t, d, kind }) => {
              const r = resultFor(d, kind);
              return (
                <div key={t} className={`tier ${r ? (r.ok ? 'ok' : 'bad') : ''}`}>
                  <div className="tier-head"><span className={`dot ${r ? (r.ok ? 'on' : 'bad') : ''}`} /> <b>{t}</b></div>
                  <div className="mono">{d}</div>
                  {r?.ok && (
                    <div className="kv">{ms(r.latency_ms)} · {kind === 'embeddings' ? `${r.dimensions} dims` : <>model {r.model} · “{r.reply}” · {r.input_tokens}→{r.output_tokens} tok</>}</div>
                  )}
                  {r && !r.ok && <div className="err">{r.error}</div>}
                  {!r && <div className="kv">not probed yet</div>}
                </div>
              );
            })}
        </div>
        {probe && <div className="kv">probed {probe.probed_at.slice(11, 19)} UTC</div>}
        {err && <div className="err">{err}</div>}
      </div>
      {health && (
        <div className="grid2">
          <div className="card">
            <h3>Agent tools <span className="chip">{health.tools.length}</span></h3>
            <div className="kv">Deny-by-default: each agent gets an allowlist of these. Results are recorded as evidence the model must cite.</div>
            <div className="tool-chips">{health.tools.map((t) => <span key={t.name} className="chip" title={t.description}>{t.name}</span>)}</div>
          </div>
          <div className="card">
            <h3>Analyzers & MCP</h3>
            {Object.entries(health.analyzers.tools ?? {}).map(([k, v]) => (
              <div key={k} className="kv"><span className={`dot ${v.available ? 'on' : 'bad'}`} /> <b>{k}</b>{' '}
                <span className="muted">{v.available ? v.version : v.error ?? 'not installed'}</span></div>
            ))}
            <div className="kv" style={{ marginTop: 10 }}>
              MCP servers: {health.mcp.configured.length ? `${health.mcp.connected.length} of ${health.mcp.configured.length} connected · ${health.mcp.tools.length} tools` : 'none configured'}
              {Object.entries(health.mcp.errors).map(([k, v]) => <div key={k} className="err">{k}: {v}</div>)}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
