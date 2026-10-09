import { useCallback, useEffect, useState } from 'react';
import { api, can, type Me } from '../api';

interface Review {
  review_id: string; job_id: string; phase: number; app: string; gate: string;
  candidate_hash: string; status: string; decision: string | null; reviewer: string | null;
  comment: string | null; created_at: string; decided_at: string | null;
  proposal: Record<string, unknown>;
}

interface Question {
  question_id: string; app: string; question: string; why: string; target_role: string;
  source: string; status: string; answer: string | null; respondent: string | null; answered_at: string | null;
}

interface TraceCall { seq: number; ts: string; [k: string]: unknown }
interface AgentTraceRow {
  phase: number; app: string; node: string;
  model_calls: TraceCall[]; tool_calls: TraceCall[]; rejections: TraceCall[]; done: TraceCall | null;
}

const box: React.CSSProperties = {
  background: 'var(--panel2)', color: 'var(--text)', border: '1px solid var(--border)',
  borderRadius: 6, padding: '6px 8px', fontFamily: 'inherit', fontSize: 12, width: '100%',
};

const PROPOSAL_KEYS = ['status', 'authorized_apps', 'conditions', 'scope', 'blockers', 'unresolved',
  'risk_summary', 'candidate_hash', 'manifest_hash'];

export function Approvals({ jobId, me, tick }: { jobId: string; me: Me | null; tick: number }) {
  const [rows, setRows] = useState<Review[]>([]);
  const [comment, setComment] = useState<Record<string, string>>({});
  const [err, setErr] = useState<string | null>(null);
  const load = useCallback(() => {
    api<Review[]>(`/api/reviews?job_id=${jobId}`).then(setRows).catch((e) => setErr(String(e)));
  }, [jobId]);
  useEffect(load, [load, tick]);

  async function decide(r: Review, decision: 'approve' | 'reject') {
    setErr(null);
    try {
      await api(`/api/reviews/${r.review_id}/decision`, {
        method: 'POST',
        body: JSON.stringify({ decision, candidate_hash: r.candidate_hash, comment: comment[r.review_id] ?? '' }),
      });
      load();
    } catch (e) { setErr(String(e)); load(); }
  }

  const pending = rows.filter((r) => r.status === 'PENDING');
  const past = rows.filter((r) => r.status !== 'PENDING');
  return (
    <div className="card">
      <h3>Release-gate approvals <span className="chip">{pending.length} pending</span></h3>
      {!can(me, 'reviewer') && <div className="kv">Your token lacks the <b>reviewer</b> role — read-only.</div>}
      {err && <div style={{ color: 'var(--red)', fontSize: 12 }}>{err}</div>}
      {pending.length === 0 && <div className="kv">Nothing awaiting review.</div>}
      {pending.map((r) => (
        <div key={r.review_id} className="card" style={{ borderColor: 'var(--amber)' }}>
          <h3>P{r.phase} · {r.app} · {r.gate} <span className="chip amber">proposed {String(r.proposal.status)}</span></h3>
          <div className="kv">candidate <code>{r.candidate_hash.slice(0, 16)}…</code> · {r.review_id}</div>
          <pre style={{ fontSize: 11, maxHeight: 220, overflow: 'auto' }}>
            {JSON.stringify(Object.fromEntries(Object.entries(r.proposal).filter(([k]) => PROPOSAL_KEYS.includes(k))), null, 2)}
          </pre>
          {can(me, 'reviewer') && (
            <div style={{ display: 'flex', gap: 8 }}>
              <input style={box} placeholder="comment / reason (recorded with your identity)"
                     value={comment[r.review_id] ?? ''}
                     onChange={(e) => setComment({ ...comment, [r.review_id]: e.target.value })} />
              <button className="btn-primary" onClick={() => decide(r, 'approve')}>Approve</button>
              <button className="btn-secondary" onClick={() => decide(r, 'reject')}>Reject</button>
            </div>
          )}
        </div>
      ))}
      {past.length > 0 && (
        <table className="table">
          <thead><tr><th>gate</th><th>app</th><th>status</th><th>decision</th><th>by</th><th>comment</th></tr></thead>
          <tbody>
            {past.map((r) => (
              <tr key={r.review_id}>
                <td>P{r.phase}.{r.gate}</td><td>{r.app}</td><td>{r.status}</td>
                <td>{r.decision ?? '—'}</td><td>{r.reviewer ?? '—'}</td><td>{r.comment ?? ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export function Questions({ jobId, me, tick }: { jobId: string; me: Me | null; tick: number }) {
  const [rows, setRows] = useState<Question[]>([]);
  const [draft, setDraft] = useState<Record<string, string>>({});
  const [err, setErr] = useState<string | null>(null);
  const load = useCallback(() => {
    api<Question[]>(`/api/runs/${jobId}/questions`).then(setRows).catch((e) => setErr(String(e)));
  }, [jobId]);
  useEffect(load, [load, tick]);

  async function submit(q: Question) {
    setErr(null);
    try {
      await api(`/api/questions/${q.question_id}/answer`, {
        method: 'POST', body: JSON.stringify({ answer: draft[q.question_id] ?? '' }),
      });
      setDraft({ ...draft, [q.question_id]: '' });
      load();
    } catch (e) { setErr(String(e)); }
  }

  return (
    <div className="card">
      <h3>Stakeholder questionnaire <span className="chip">{rows.filter((q) => q.status === 'OPEN').length} open</span></h3>
      <div className="kv">
        Recorded answers are the only source of HUMAN_CONFIRMED evidence (P1.A8). Answering re-runs the
        affected discovery nodes and supersedes any pending P1 approval.
      </div>
      {!can(me, 'stakeholder') && <div className="kv">Your token lacks the <b>stakeholder</b> role — read-only.</div>}
      {err && <div style={{ color: 'var(--red)', fontSize: 12 }}>{err}</div>}
      {rows.map((q) => (
        <div key={q.question_id} style={{ borderTop: '1px solid var(--border)', padding: '8px 0' }}>
          <div>
            <span className={`chip ${q.status === 'ANSWERED' ? 'green' : 'amber'}`}>{q.status}</span>{' '}
            <span className="chip">{q.app}</span> <span className="chip">{q.source}</span>{' '}
            <b>{q.question}</b>
          </div>
          {q.why && <div className="kv">why: {q.why}{q.target_role ? ` · ask: ${q.target_role}` : ''}</div>}
          {q.answer && <div className="kv">answer by <b>{q.respondent}</b>: {q.answer}</div>}
          {can(me, 'stakeholder') && (
            <div style={{ display: 'flex', gap: 8, marginTop: 4 }}>
              <input style={box} placeholder={q.answer ? 'revise answer' : 'your answer'}
                     value={draft[q.question_id] ?? ''}
                     onChange={(e) => setDraft({ ...draft, [q.question_id]: e.target.value })} />
              <button className="btn-primary" disabled={!(draft[q.question_id] ?? '').trim()}
                      onClick={() => submit(q)}>Record</button>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export function AgentTrace({ jobId, tick }: { jobId: string; tick: number }) {
  const [rows, setRows] = useState<AgentTraceRow[]>([]);
  const [open, setOpen] = useState<string | null>(null);
  useEffect(() => { api<AgentTraceRow[]>(`/api/runs/${jobId}/trace`).then(setRows).catch(() => {}); }, [jobId, tick]);
  const key = (r: AgentTraceRow) => `P${r.phase}/${r.app}/${r.node}`;
  return (
    <div className="card">
      <h3>Agent trace <span className="chip">{rows.length} agents</span></h3>
      <table className="table">
        <thead><tr><th>agent</th><th>app</th><th>model calls</th><th>tools</th><th>rejected</th><th>tokens in/out</th><th>result</th></tr></thead>
        <tbody>
          {rows.map((r) => {
            const tin = r.model_calls.reduce((n, c) => n + Number((c.input_tokens as number) ?? 0), 0);
            const tout = r.model_calls.reduce((n, c) => n + Number((c.output_tokens as number) ?? 0), 0);
            const done = r.done as Record<string, unknown> | null;
            return (
              <tr key={key(r)} style={{ cursor: 'pointer' }} onClick={() => setOpen(open === key(r) ? null : key(r))}>
                <td>P{r.phase}.{r.node}</td><td>{r.app}</td><td>{r.model_calls.length}</td>
                <td>{r.tool_calls.length}</td><td>{r.rejections.length}</td><td>{tin} / {tout}</td>
                <td>{done ? <span className={`chip ${done.enriched ? 'green' : 'amber'}`}>{String(done.mode ?? (done.enriched ? 'enriched' : 'seed'))}</span> : '…'}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
      {open && (() => {
        const r = rows.find((x) => key(x) === open);
        if (!r) return null;
        return (
          <div className="card">
            <h3>{open}</h3>
            {r.done && <div className="kv">{String((r.done as Record<string, unknown>).summary ?? '')}</div>}
            <div className="label">Tool calls</div>
            {r.tool_calls.map((t) => (
              <div key={t.seq} className="log-line info">
                <span className="log-ts">{String(t.ts).slice(11, 19)}</span> <b>{String(t.tool ?? t.name)}</b>{' '}
                <code>{JSON.stringify(t.args)}</code> → {String(t.evidence_id ?? t.eid ?? '')}
                {t.error ? <span style={{ color: 'var(--red)' }}> {String(t.error)}</span> : null}
              </div>
            ))}
            <div className="label" style={{ marginTop: 8 }}>Model calls</div>
            {r.model_calls.map((m) => (
              <div key={m.seq} className="log-line info">
                <span className="log-ts">{String(m.ts).slice(11, 19)}</span> {String(m.deployment)} · turn {String(m.turn ?? '')}
                {' '}· {String(m.latency_ms ?? '')} ms{m.cached ? ' · cached' : ''}{m.failover ? ' · failover' : ''}
                {m.error ? <span style={{ color: 'var(--red)' }}> {String(m.error)}</span> : null}
              </div>
            ))}
            {r.rejections.length > 0 && <div className="label" style={{ marginTop: 8 }}>Rejected submissions</div>}
            {r.rejections.map((x) => (
              <div key={x.seq} className="log-line error">{JSON.stringify(x.problems ?? x)}</div>
            ))}
          </div>
        );
      })()}
    </div>
  );
}
