import { useEffect, useRef, useState } from 'react';
import { api, can, getToken, setToken, withToken, type Me } from '../api';
import { AgentTrace, Approvals, Questions } from './RunPanels';

interface NodeStatus { id: string; status: string; reused?: boolean }
interface PhaseState { phase: number; app: string; status: string; nodes: NodeStatus[]; decision: string | null; note: string }
interface GateEntry { phase: number; app?: string; gate: string; decision: string }
interface LogEntry { ts: string; msg: string; level: string }
interface LlmStats { enabled: boolean; calls: number; input_tokens: number; output_tokens: number;
  reasoning_tokens: number; failovers: number; cached: number; tool_calls: number }
interface JobState {
  job_id: string; repo: string; repos: string[]; apps: string[]; app_id: string | null; owner: string;
  status: string; stage: string; stage_detail: string | null; current_phase: number | null;
  progress: number; log: LogEntry[]; started_at: string | null; finished_at: string | null;
  error: string | null; phases: PhaseState[]; gate_chain: GateEntry[];
  facts: Record<string, string | number>; app_facts: Record<string, Record<string, unknown>>;
  review_mode: string; llm: LlmStats; pending_reviews: number; open_questions: number;
}
interface RunRow { job_id: string; repo: string; status: string; started_at: string | null; progress: number; review_mode: string }

const STATUS_COLOR: Record<string, string> = {
  PUBLISHED: 'green', COMPLETE: 'green', COMPLETED: 'green', PARTIAL: 'amber', RUNNING: 'blue',
  AWAITING_REVIEW: 'amber', AWAITING_INPUT: 'amber', PENDING: '', FAILED: 'red', BLOCKED: 'red',
  CANCELLED: 'red',
  INTERRUPTED: 'amber', NOT_ADMITTED: '', FAILED_RETRY_EXHAUSTED: 'red', SKIPPED_APPROVED: '',
  'N/A': '', SKIPPED: '', RETRY_SCHEDULED: 'amber',
};
const ACTIVE = ['PENDING', 'QUEUED', 'RUNNING', 'AWAITING_REVIEW', 'AWAITING_INPUT'];
const phaseName = (p: number) =>
  ({ 1: 'Discovery', 2: 'Portfolio decision', 3: 'Target architecture',
     4: 'Planning', 5: 'Code modernization', 6: 'Data modernization' } as Record<number, string>)[p] ?? `P${p}`;

function elapsed(from: string | null, to: string | null): string {
  if (!from) return '—';
  const secs = Math.max(0, Math.round(((to ? Date.parse(to) : Date.now()) - Date.parse(from)) / 1000));
  return secs < 60 ? `${secs}s` : secs < 3600 ? `${Math.floor(secs / 60)}m ${secs % 60}s`
    : `${Math.floor(secs / 3600)}h ${Math.floor((secs % 3600) / 60)}m`;
}

const input: React.CSSProperties = {
  background: 'var(--panel2)', color: 'var(--text)', border: '1px solid var(--border)',
  borderRadius: 6, padding: '8px 10px', fontFamily: 'inherit', fontSize: 13,
};

type Tab = 'overview' | 'approvals' | 'questions' | 'trace' | 'artifacts';

export function RunnerView() {
  const [me, setMe] = useState<Me | null>(null);
  const [tokenDraft, setTokenDraft] = useState('');
  const [authErr, setAuthErr] = useState<string | null>(null);
  const [repos, setRepos] = useState('');
  const [decisionMode, setDecisionMode] = useState(true);
  const [includeP6, setIncludeP6] = useState(true);
  const [reviewMode, setReviewMode] = useState<'simulated' | 'human'>('simulated');
  const [runs, setRuns] = useState<RunRow[]>([]);
  const [jobId, setJobId] = useState<string | null>(null);
  const [job, setJob] = useState<JobState | null>(null);
  const [tab, setTab] = useState<Tab>('overview');
  const [tick, setTick] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [artifacts, setArtifacts] = useState<{ artifact_id: string; producer_id: string; status: string; phase_id: number }[]>([]);
  const [artifact, setArtifact] = useState<Record<string, unknown> | null>(null);
  const logRef = useRef<HTMLDivElement | null>(null);

  async function login(tok?: string) {
    if (tok !== undefined) setToken(tok);
    try {
      setMe(await api<Me>('/api/me'));
      setAuthErr(null);
      setRuns(await api<RunRow[]>('/api/runs'));
    } catch (e) {
      setMe(null);
      setAuthErr(getToken() ? String(e) : null);
    }
  }
  useEffect(() => { login(); }, []);

  // live updates: SSE event stream -> debounced snapshot refresh (+ slow poll fallback)
  useEffect(() => {
    if (!jobId || !me) return;
    let timer: number | null = null;
    const refresh = () => {
      if (timer) return;
      timer = window.setTimeout(async () => {
        timer = null;
        try {
          const s = await api<JobState>(`/api/runs/${jobId}`);
          setJob(s);
          setTick((t) => t + 1);
          if (!ACTIVE.includes(s.status)) setArtifacts(await api(`/api/runs/${jobId}/artifacts`));
        } catch { /* transient */ }
      }, 700);
    };
    refresh();
    const es = new EventSource(withToken(`/api/runs/${jobId}/stream`));
    ['NODE', 'PHASE', 'LOG', 'REVIEW_PENDING', 'JOB', 'AGENT_LLM_DONE'].forEach((k) => es.addEventListener(k, refresh));
    es.addEventListener('END', () => { refresh(); es.close(); });
    const poll = window.setInterval(refresh, 5000);
    return () => { es.close(); window.clearInterval(poll); if (timer) window.clearTimeout(timer); };
  }, [jobId, me]);

  const logLen = job?.log?.length ?? 0;
  useEffect(() => {
    const el = logRef.current;
    if (el && el.scrollHeight - el.scrollTop - el.clientHeight < 60) el.scrollTop = el.scrollHeight;
  }, [logLen]);

  async function start() {
    setError(null); setJob(null); setArtifacts([]); setArtifact(null); setTab('overview');
    const list = repos.split(/\n|,/).map((r) => r.trim()).filter(Boolean);
    try {
      const body = await api<{ job_id: string }>('/api/runs', {
        method: 'POST',
        body: JSON.stringify({ repos: list, decision_mode: decisionMode, include_p6: includeP6, review_mode: reviewMode }),
      });
      setJobId(body.job_id);
      setRuns(await api<RunRow[]>('/api/runs'));
    } catch (e) { setError(String(e)); }
  }

  async function control(action: 'cancel' | 'resume') {
    try { await api(`/api/runs/${jobId}/${action}`, { method: 'POST' }); setTick((t) => t + 1); }
    catch (e) { setError(String(e)); }
  }

  async function openArtifact(id: string) {
    setArtifact(await api(`/api/runs/${jobId}/artifacts/${id}`));
  }

  if (!me) {
    return (
      <div style={{ padding: 20, maxWidth: 700 }}>
        <div className="card">
          <h3>Sign in</h3>
          <p className="body">
            Paste an API token. Tokens come from <code>APPMOD_API_TOKENS</code>; with none configured the
            server generates an admin token in <code>runs/.admin_token</code> on the server host.
          </p>
          <div style={{ display: 'flex', gap: 8 }}>
            <input type="password" style={{ ...input, flex: 1 }} value={tokenDraft} placeholder="bearer token"
                   onChange={(e) => setTokenDraft(e.target.value)}
                   onKeyDown={(e) => { if (e.key === 'Enter') login(tokenDraft.trim()); }} />
            <button className="btn-primary" onClick={() => login(tokenDraft.trim())}>Sign in</button>
          </div>
          {authErr && <div style={{ color: 'var(--red)', fontSize: 12, marginTop: 6 }}>{authErr}</div>}
        </div>
      </div>
    );
  }

  const running = !!job && ACTIVE.includes(job.status);
  const apps = job?.apps?.length ? job.apps : [];
  const byPhase = (phase: number) => (job?.phases ?? []).filter((p) => p.phase === phase);

  return (
    <div style={{ padding: 20, maxWidth: 1200 }}>
      <div className="card sticky-form">
        <h3>
          Repositories under test
          <span style={{ float: 'right', fontSize: 11, color: 'var(--muted)', fontWeight: 400 }}>
            {me.user} · {me.roles.join(', ')}{' '}
            <a href="#" style={{ color: 'var(--accent)' }} onClick={(e) => { e.preventDefault(); setToken(''); setMe(null); }}>sign out</a>
          </span>
        </h3>
        <div style={{ display: 'flex', gap: 8 }}>
          <textarea value={repos} rows={2} onChange={(e) => setRepos(e.target.value)}
                    placeholder={'one per line: /path/to/legacy-repo  or  https://github.com/org/repo.git\n(several repos = one portfolio run: P1 per app → one P2 → P3/P4 per authorized app)'}
                    style={{ ...input, flex: 1, resize: 'vertical' }} />
          <button className="btn-primary" onClick={start}
                  disabled={!repos.trim() || !can(me, 'operator') || running}>
            {running ? 'Running…' : 'Run pipeline'}
          </button>
        </div>
        <div style={{ marginTop: 10, fontSize: 12, color: 'var(--muted)', display: 'flex', gap: 18, flexWrap: 'wrap' }}>
          <label>review mode{' '}
            <select value={reviewMode} onChange={(e) => setReviewMode(e.target.value as 'simulated' | 'human')} style={{ ...input, padding: '2px 6px' }}>
              <option value="simulated">simulated (gates auto-release, labelled simulated)</option>
              <option value="human">human (gates wait for reviewer approval; A8 uses recorded answers)</option>
            </select>
          </label>
          <label><input type="checkbox" checked={decisionMode} onChange={(e) => setDecisionMode(e.target.checked)} /> decision mode</label>
          <label><input type="checkbox" checked={includeP6} onChange={(e) => setIncludeP6(e.target.checked)} /> include Phase 6 (single repo)</label>
        </div>
        {error && <div style={{ color: 'var(--red)', marginTop: 8, fontSize: 12 }}>{error}</div>}
        {runs.length > 0 && (
          <div style={{ marginTop: 10, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {runs.slice(0, 8).map((r) => (
              <button key={r.job_id} className={`chip ${STATUS_COLOR[r.status] || ''}`}
                      style={{ cursor: 'pointer', background: r.job_id === jobId ? 'var(--panel2)' : 'transparent' }}
                      title={r.repo} onClick={() => { setJobId(r.job_id); setTab('overview'); }}>
                {r.job_id.slice(-6)} · {r.status} · {r.progress}%
              </button>
            ))}
          </div>
        )}
      </div>

      {job && (
        <>
          <div className="card" style={{ borderColor: running ? 'var(--accent)' : undefined }}>
            <h3>
              Run {job.job_id}{' '}
              <span className={`chip ${STATUS_COLOR[job.status] || ''}`}>{job.status}</span>{' '}
              {job.stage_detail && <span className={`chip ${running ? 'blue pulse' : ''}`}>{job.stage_detail}</span>}{' '}
              <span className="chip purple">{job.review_mode}</span>
              <span style={{ float: 'right', color: 'var(--muted)', fontSize: 11 }}>
                ⏱ {elapsed(job.started_at, job.finished_at)}{' '}
                {can(me, 'operator') && running && <button className="btn-secondary" onClick={() => control('cancel')}>Cancel</button>}
                {can(me, 'operator') && ['INTERRUPTED', 'FAILED', 'CANCELLED'].includes(job.status) &&
                  <button className="btn-secondary" onClick={() => control('resume')}>Resume (reuses finished nodes)</button>}
              </span>
            </h3>
            <div className="progress-track"><div className="progress-fill" style={{ width: `${job.progress}%` }} /></div>
            <div className="kv" style={{ marginTop: 6 }}>
              <span style={{ marginRight: 14 }}><b>LLM</b>: {job.llm.enabled ? 'Astra' : 'off'}</span>
              <span style={{ marginRight: 14 }}><b>model calls</b>: {job.llm.calls}</span>
              <span style={{ marginRight: 14 }}><b>tool calls</b>: {job.llm.tool_calls}</span>
              <span style={{ marginRight: 14 }}><b>tokens in/out</b>: {job.llm.input_tokens.toLocaleString()} / {job.llm.output_tokens.toLocaleString()}</span>
              <span style={{ marginRight: 14 }}><b>failovers</b>: {job.llm.failovers}</span>
              {job.pending_reviews > 0 && <span className="chip amber">{job.pending_reviews} awaiting review</span>}{' '}
              {job.open_questions > 0 && <span className="chip amber">{job.open_questions} open questions</span>}
            </div>
            {job.error && <div style={{ color: 'var(--red)', fontSize: 12, marginTop: 6 }}>{job.error}</div>}
            <div style={{ display: 'flex', gap: 6, marginTop: 10 }}>
              {(['overview', 'approvals', 'questions', 'trace', 'artifacts'] as Tab[]).map((t) => (
                <button key={t} className={`chip ${tab === t ? 'blue' : ''}`} style={{ cursor: 'pointer', background: 'transparent' }}
                        onClick={() => setTab(t)}>
                  {t}{t === 'approvals' && job.pending_reviews ? ` (${job.pending_reviews})` : ''}
                  {t === 'questions' && job.open_questions ? ` (${job.open_questions})` : ''}
                </button>
              ))}
            </div>
          </div>

          {tab === 'approvals' && jobId && <Approvals jobId={jobId} me={me} tick={tick} />}
          {tab === 'questions' && jobId && <Questions jobId={jobId} me={me} tick={tick} />}
          {tab === 'trace' && jobId && <AgentTrace jobId={jobId} tick={tick} />}

          {tab === 'overview' && (
            <>
              {Object.keys(job.app_facts ?? {}).length > 0 && (
                <div className="card">
                  <h3>Applications ({apps.length})</h3>
                  <table className="table">
                    <thead><tr><th>app</th><th>language</th><th>code LOC</th><th>deps</th><th>route</th><th>P1 release</th><th>disposition</th></tr></thead>
                    <tbody>
                      {Object.entries(job.app_facts).map(([a, f]) => (
                        <tr key={a}>
                          <td>{a}</td><td>{String(f.primary_language ?? '')}</td><td>{String(f.code_loc ?? f.loc ?? '')}</td>
                          <td>{String(f.dependencies ?? '')}</td><td>{String(f.route ?? '')}</td>
                          <td>{String(f.p1_release ?? '')}</td>
                          <td>{f.disposition ? <span className={`chip ${f.authorized ? 'green' : ''}`}>{String(f.disposition)}</span> : '…'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {[1, 2, 3, 4, 5, 6].map((ph) => byPhase(ph).length > 0 && (
                <div className="card" key={ph}>
                  <h3>Phase {ph} — {phaseName(ph)}</h3>
                  {byPhase(ph).map((p) => (
                    <div key={`${p.phase}-${p.app}`} style={{ borderTop: '1px solid var(--border)', padding: '6px 0' }}>
                      <div>
                        <span className={`chip ${STATUS_COLOR[p.status] || ''}${p.status === 'RUNNING' ? ' pulse' : ''}`}>{p.status}</span>{' '}
                        <b>{p.app}</b> {p.decision && <span className="chip blue">{p.decision}</span>}
                        {p.note && <span className="kv"> {p.note}</span>}
                      </div>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 4 }}>
                        {p.nodes.map((n) => (
                          <span key={n.id} title={n.status}
                                className={`chip ${STATUS_COLOR[n.status] ?? ''}${n.status === 'RUNNING' ? ' pulse' : ''}`}>
                            {n.id}{n.reused ? ' ↺' : ''} · {n.status}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              ))}

              {job.status === 'COMPLETED' && (
                <div className="card" style={{ borderColor: 'var(--green)' }}>
                  <h3>✅ Outcome ready</h3>
                  <div style={{ display: 'flex', gap: 10 }}>
                    <a className="btn-primary" href={withToken(`/api/runs/${jobId}/outcome`)} download>⬇ Outcome bundle (.zip)</a>
                    <a className="btn-secondary" href={withToken(`/api/runs/${jobId}/outcome?format=md`)} download>⬇ Report (.md)</a>
                  </div>
                </div>
              )}

              {job.log?.length > 0 && (
                <div className="card">
                  <h3>Activity log <span style={{ color: 'var(--muted)', fontWeight: 400 }}>(live)</span></h3>
                  <div className="runner-log" ref={logRef}>
                    {job.log.map((l, i) => (
                      <div key={i} className={`log-line ${l.level}`}><span className="log-ts">{l.ts.slice(11, 19)}</span> {l.msg}</div>
                    ))}
                    {running && <div className="log-line info log-cursor">▌</div>}
                  </div>
                </div>
              )}
            </>
          )}

          {tab === 'artifacts' && (
            <div className="card">
              <h3>Artifacts ({artifacts.length})</h3>
              {artifacts.length === 0 && <div className="kv">Artifacts are listed once the run finishes.</div>}
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {artifacts.map((a) => (
                  <button key={a.artifact_id} className={`chip ${STATUS_COLOR[a.status] ?? ''}`}
                          style={{ cursor: 'pointer', background: 'transparent' }} onClick={() => openArtifact(a.artifact_id)}>
                    {a.artifact_id} · {a.status}
                  </button>
                ))}
              </div>
              {artifact && (
                <pre style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: 8, padding: 12,
                              marginTop: 10, maxHeight: 520, overflow: 'auto', fontSize: 11 }}>
                  {JSON.stringify(artifact, null, 2)}
                </pre>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}
