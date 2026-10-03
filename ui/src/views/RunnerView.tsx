import { useEffect, useRef, useState } from 'react';

interface NodeStatus { id: string; status: string }
interface PhaseState { phase: number; status: string; nodes: NodeStatus[]; decision: string | null; note: string }
interface GateEntry { phase: number; gate: string; decision: string }
interface LogEntry { ts: string; msg: string; level: string }
interface JobState {
  job_id: string; repo: string; app_id: string | null;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  stage: string; stage_detail: string | null; current_phase: number | null;
  progress: number; log: LogEntry[];
  started_at: string | null; finished_at: string | null;
  error: string | null;
  phases: PhaseState[]; gate_chain: GateEntry[];
  facts: Record<string, string | number>;
}

const STATUS_COLOR: Record<string, string> = {
  PUBLISHED: 'green', COMPLETE: 'green', COMPLETED: 'green',
  PARTIAL: 'amber', RUNNING: 'blue', PENDING: '',
  FAILED: 'red', BLOCKED: 'red', NOT_READY: 'red', FAILED_RETRY_EXHAUSTED: 'red',
  SKIPPED_APPROVED: '', N_A: '', 'N/A': '', SKIPPED: '', RETRY_SCHEDULED: 'amber',
};

const phaseName = (p: number) =>
  ({ 1: 'Discovery', 2: 'Portfolio decision', 3: 'Target architecture',
     4: 'Planning', 5: 'Code modernization', 6: 'Data modernization' } as Record<number, string>)[p] ?? `P${p}`;

function elapsed(from: string | null, to: string | null): string {
  if (!from) return '—';
  const end = to ? Date.parse(to) : Date.now();
  const secs = Math.max(0, Math.round((end - Date.parse(from)) / 1000));
  return secs < 60 ? `${secs}s` : `${Math.floor(secs / 60)}m ${secs % 60}s`;
}

export function RunnerView() {
  const [repo, setRepo] = useState('');
  const [decisionMode, setDecisionMode] = useState(true);
  const [includeP6, setIncludeP6] = useState(true);
  const [jobId, setJobId] = useState<string | null>(null);
  const [job, setJob] = useState<JobState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);
  const [artifacts, setArtifacts] = useState<{ artifact_id: string; producer_id: string; status: string }[]>([]);
  const [artifact, setArtifact] = useState<Record<string, unknown> | null>(null);
  const pollRef = useRef<number | null>(null);
  const logRef = useRef<HTMLDivElement | null>(null);
  const phaseRefs = useRef<Record<number, HTMLDivElement | null>>({});

  useEffect(() => {
    fetch('/api/runs').then(r => setApiOnline(r.ok)).catch(() => setApiOnline(false));
    return () => { if (pollRef.current) window.clearInterval(pollRef.current); };
  }, []);

  useEffect(() => {
    if (!jobId) return;
    if (pollRef.current) window.clearInterval(pollRef.current);
    pollRef.current = window.setInterval(async () => {
      const r = await fetch(`/api/runs/${jobId}`);
      if (!r.ok) return;
      const state: JobState = await r.json();
      setJob(state);
      if (state.status === 'COMPLETED' || state.status === 'FAILED') {
        if (pollRef.current) window.clearInterval(pollRef.current);
        const ar = await fetch(`/api/runs/${jobId}/artifacts`);
        if (ar.ok) setArtifacts(await ar.json());
      }
    }, 1200);
  }, [jobId]);

  // live log: keep pinned to the newest line unless the user scrolled up
  const logLen = job?.log?.length ?? 0;
  useEffect(() => {
    const el = logRef.current;
    if (!el) return;
    const nearBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 60;
    if (nearBottom) el.scrollTop = el.scrollHeight;
  }, [logLen]);

  // follow the simulation: scroll to the phase currently executing
  const activePhase = job?.stage === 'RUNNING' ? job.current_phase : null;
  useEffect(() => {
    if (activePhase == null) return;
    const el = phaseRefs.current[activePhase];
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, [activePhase]);

  async function start() {
    setError(null);
    setJob(null); setArtifacts([]); setArtifact(null);
    try {
      const r = await fetch('/api/runs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo, decision_mode: decisionMode, include_p6: includeP6 }),
      });
      if (!r.ok) {
        const body = await r.json().catch(() => ({ detail: r.statusText }));
        throw new Error(body.detail || `HTTP ${r.status}`);
      }
      const body = await r.json();
      setJobId(body.job_id);
    } catch (e) {
      setError(String(e));
    }
  }

  async function openArtifact(id: string) {
    const r = await fetch(`/api/runs/${jobId}/artifacts/${id}`);
    if (r.ok) setArtifact(await r.json());
  }

  const stageLabel = (j: JobState) => {
    if (j.stage === 'QUEUED') return 'Queued';
    if (j.stage === 'CLONING') return 'Cloning repository…';
    if (j.stage === 'RUNNING')
      return j.current_phase != null ? `Phase ${j.current_phase}/6 — ${phaseName(j.current_phase)}` : 'Preparing';
    return j.status;
  };

  const running = job?.status === 'RUNNING' || job?.status === 'PENDING';

  return (
    <div style={{ padding: 20, maxWidth: 1100 }}>
      {apiOnline === false && (
        <div className="card" style={{ borderColor: 'var(--amber)' }}>
          <h3>API offline</h3>
          <p className="body">
            The runner API is not reachable from this server. Start it with{' '}
            <code>python -m appmod.server</code> and open{' '}
            <a href="http://localhost:8600" style={{ color: 'var(--accent)' }}>http://localhost:8600</a>{' '}
            (this static preview cannot execute runs).
          </p>
        </div>
      )}

      {/* ---- user input — always pinned at the top ---- */}
      <div className="card sticky-form">
        <h3>Repository under test</h3>
        <div style={{ display: 'flex', gap: 8 }}>
          <input
            value={repo}
            onChange={(e) => setRepo(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter' && repo.trim()) start(); }}
            placeholder="C:/path/to/legacy-repo   or   https://github.com/org/repo.git"
            style={{
              flex: 1, background: 'var(--panel2)', color: 'var(--text)',
              border: '1px solid var(--border)', borderRadius: 6, padding: '8px 10px',
              fontFamily: 'inherit', fontSize: 13,
            }}
          />
          <button
            onClick={start}
            disabled={!repo.trim() || apiOnline === false || running}
            style={{
              background: '#1f6feb', color: 'white', border: 'none', borderRadius: 6,
              padding: '8px 18px', fontSize: 13, fontWeight: 600, cursor: 'pointer',
            }}
          >
            {running ? 'Running…' : 'Run pipeline'}
          </button>
        </div>
        <div style={{ marginTop: 10, fontSize: 12, color: 'var(--muted)', display: 'flex', gap: 18 }}>
          <label style={{ cursor: 'pointer' }}>
            <input type="checkbox" checked={decisionMode}
                   onChange={(e) => setDecisionMode(e.target.checked)} />{' '}
            decision mode (simulated stakeholder evidence → P2 can authorize)
          </label>
          <label style={{ cursor: 'pointer' }}>
            <input type="checkbox" checked={includeP6}
                   onChange={(e) => setIncludeP6(e.target.checked)} />{' '}
            include Phase 6 (data migration when seed data exists)
          </label>
        </div>
        {error && <div style={{ color: 'var(--red)', marginTop: 8, fontSize: 12 }}>{error}</div>}
      </div>

      {job && (
        <>
          {/* ---- live status: stage, progress, facts ---- */}
          <div className="card" style={{ borderColor: running ? 'var(--accent)' : undefined }}>
            <h3>
              Run {job.job_id}{' '}
              <span className={`chip ${STATUS_COLOR[job.status] || ''}`}>{job.status}</span>{' '}
              <span className={`chip ${running ? 'blue pulse' : ''}`}>{stageLabel(job)}</span>{' '}
              {job.app_id && <span className="chip purple">{job.app_id}</span>}
              <span style={{ float: 'right', color: 'var(--muted)', fontSize: 11 }}>
                ⏱ {elapsed(job.started_at ?? null, job.finished_at ?? null)}
              </span>
            </h3>
            <div className="progress-track">
              <div className="progress-fill" style={{ width: `${job.progress}%` }} />
            </div>
            <div style={{ fontSize: 11, color: 'var(--muted)', marginTop: 4 }}>
              {job.stage === 'CLONING'
                ? 'Shallow git clone in progress — large repos can take a few minutes. Watch the activity log below.'
                : `${job.progress}% of the pipeline complete`}
            </div>
            {Object.keys(job.facts).length > 0 && (
              <div className="kv" style={{ marginTop: 8 }}>
                {Object.entries(job.facts).filter(([k]) => k !== 'store_path').map(([k, v]) => (
                  <span key={k} style={{ marginRight: 14 }}><b>{k}</b>: {String(v)}</span>
                ))}
              </div>
            )}
            {job.error && <div style={{ color: 'var(--red)', fontSize: 12, marginTop: 6 }}>{job.error}</div>}
          </div>

          {/* ---- live activity log ---- */}
          {job.log && job.log.length > 0 && (
            <div className="card">
              <h3>Activity log <span style={{ color: 'var(--muted)', fontWeight: 400 }}>(live)</span></h3>
              <div className="runner-log" ref={logRef}>
                {job.log.map((l, i) => (
                  <div key={i} className={`log-line ${l.level}`}>
                    <span className="log-ts">{l.ts.slice(11, 19)}</span> {l.msg}
                  </div>
                ))}
                {running && <div className="log-line info log-cursor">▌</div>}
              </div>
            </div>
          )}

          {/* ---- phases: live simulation, follows the active phase ---- */}
          {job.phases.map((p) => {
            const isActive = p.phase === activePhase;
            return (
              <div className={`card ${isActive ? 'phase-active' : ''}`} key={p.phase}
                   ref={(el) => { phaseRefs.current[p.phase] = el; }}>
                <h3>
                  <span className={`chip ${STATUS_COLOR[p.status] || ''}`}>{p.status}</span>{' '}
                  Phase {p.phase} — {phaseName(p.phase)}
                  {p.decision && <span className="chip blue">{p.decision}</span>}
                  {isActive && <span className="chip blue pulse">executing…</span>}
                </h3>
                {p.note && <div className="kv">{p.note}</div>}
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 6 }}>
                  {p.nodes.map((n) => (
                    <span key={n.id}
                          className={`chip ${STATUS_COLOR[n.status] ?? ''}${n.status === 'RUNNING' ? ' pulse' : ''}`}
                          title={n.status}>
                      {n.id} · {n.status}
                    </span>
                  ))}
                </div>
              </div>
            );
          })}

          {/* ---- outcome download once the run finishes ---- */}
          {job.status === 'COMPLETED' && (
            <div className="card" style={{ borderColor: 'var(--green)' }}>
              <h3>✅ Outcome ready</h3>
              <p className="body">
                The pipeline finished. Download the outcome bundle — it contains the
                run report (markdown), the complete run state, and every published
                artifact envelope from the immutable store.
              </p>
              <div style={{ display: 'flex', gap: 10, marginTop: 6 }}>
                <a className="btn-primary" href={`/api/runs/${jobId}/outcome`} download>
                  ⬇ Download outcome bundle (.zip)
                </a>
                <a className="btn-secondary" href={`/api/runs/${jobId}/outcome?format=md`} download>
                  ⬇ Report only (.md)
                </a>
              </div>
            </div>
          )}

          {job.gate_chain.length > 0 && (
            <div className="card">
              <h3>Gate chain</h3>
              <table className="table">
                <thead><tr><th>Phase</th><th>Gate</th><th>Decision</th></tr></thead>
                <tbody>
                  {job.gate_chain.map((g, i) => (
                    <tr key={i}>
                      <td>P{g.phase}</td><td>{g.gate}</td>
                      <td><span className={`chip ${/READY|AUTHORIZED|PASS/.test(g.decision) ? 'green' : /LIMITED|N\/A|SCOPED/.test(g.decision) ? 'amber' : 'red'}`}>
                        {g.decision}
                      </span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {artifacts.length > 0 && (
            <div className="card">
              <h3>Artifacts ({artifacts.length})</h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {artifacts.map((a) => (
                  <button key={a.artifact_id} className="chip blue"
                          style={{ cursor: 'pointer', background: 'transparent' }}
                          onClick={() => openArtifact(a.artifact_id)}>
                    {a.producer_id} · {a.status}
                  </button>
                ))}
              </div>
              {artifact && (
                <pre style={{
                  background: 'var(--bg)', border: '1px solid var(--border)',
                  borderRadius: 8, padding: 12, marginTop: 10, maxHeight: 420,
                  overflow: 'auto', fontSize: 11,
                }}>
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
