import { useEffect, useRef, useState } from 'react';
import { api, withToken } from './api';

export type Kind = 'NODE' | 'MODEL_CALL' | 'TOOL_CALL' | 'SUBMISSION_REJECTED' | 'AGENT_LLM_DONE' | 'CONNECTIVITY';
export const KINDS: Kind[] = ['NODE', 'MODEL_CALL', 'TOOL_CALL', 'SUBMISSION_REJECTED', 'AGENT_LLM_DONE', 'CONNECTIVITY'];

export interface Ev {
  seq: number; ts: string; kind: Kind; phase?: number; app?: string; node?: string; agent?: string;
  [k: string]: unknown;
}

export interface AgentRun {
  key: string; phase: number; app: string; node: string;
  status: string; startedAt: string | null; lastAt: string | null;
  turns: number; modelCalls: Ev[]; toolCalls: Ev[]; rejections: Ev[]; done: Ev | null;
  tokensIn: number; tokensOut: number; tokensReasoning: number; latencyMs: number;
  failovers: number; cached: number; errors: number; deployments: Set<string>;
}

export const agentKey = (e: { phase?: number; app?: string; node?: string }) => `P${e.phase}/${e.app}/${e.node}`;

function blank(e: Ev): AgentRun {
  return { key: agentKey(e), phase: Number(e.phase ?? 0), app: String(e.app ?? ''), node: String(e.node ?? ''),
    status: 'PENDING', startedAt: null, lastAt: null, turns: 0, modelCalls: [], toolCalls: [], rejections: [],
    done: null, tokensIn: 0, tokensOut: 0, tokensReasoning: 0, latencyMs: 0, failovers: 0, cached: 0, errors: 0,
    deployments: new Set() };
}

const num = (v: unknown) => (typeof v === 'number' ? v : 0);

/** Fold one event into the per-agent table. */
export function fold(agents: Map<string, AgentRun>, e: Ev): void {
  if (e.node === undefined || e.phase === undefined) return;
  const k = agentKey(e);
  const a = agents.get(k) ?? blank(e);
  agents.set(k, a);
  a.lastAt = e.ts;
  switch (e.kind) {
    case 'NODE':
      a.status = String(e.status ?? a.status);
      if (a.status === 'RUNNING' && !a.startedAt) a.startedAt = e.ts;
      break;
    case 'MODEL_CALL':
      a.startedAt ??= e.ts;
      if (a.status === 'PENDING') a.status = 'RUNNING';
      a.modelCalls.push(e);
      a.turns = Math.max(a.turns, num(e.turn));
      a.tokensIn += e.cached ? 0 : num(e.input_tokens);
      a.tokensOut += e.cached ? 0 : num(e.output_tokens);
      a.tokensReasoning += e.cached ? 0 : num(e.reasoning_tokens);
      a.latencyMs += num(e.latency_ms);
      a.failovers += e.failover ? 1 : 0;
      a.cached += e.cached ? 1 : 0;
      a.errors += e.error ? 1 : 0;
      if (e.deployment) a.deployments.add(String(e.deployment));
      break;
    case 'TOOL_CALL':
      a.toolCalls.push(e);
      break;
    case 'SUBMISSION_REJECTED':
      a.rejections.push(e);
      break;
    case 'AGENT_LLM_DONE':
      a.done = e;
      break;
  }
}

export interface LiveState { events: Ev[]; agents: Map<string, AgentRun>; version: number; connected: boolean; loading: boolean }

/** Backfill a run's agent events, then follow its SSE stream. Re-renders at most every 400 ms. */
export function useLiveRun(jobId: string | null): LiveState {
  const events = useRef<Ev[]>([]);
  const agents = useRef(new Map<string, AgentRun>());
  const [version, setVersion] = useState(0);
  const [connected, setConnected] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    events.current = [];
    agents.current = new Map();
    setVersion((v) => v + 1);
    if (!jobId) return;
    let closed = false;
    let es: EventSource | null = null;
    let pending: number | null = null;
    const bump = () => {
      if (pending !== null) return;
      pending = window.setTimeout(() => { pending = null; setVersion((v) => v + 1); }, 400);
    };
    const push = (e: Ev) => {
      if (!KINDS.includes(e.kind)) return;
      const last = events.current[events.current.length - 1];
      if (last && e.seq <= last.seq) return;
      events.current.push(e);
      fold(agents.current, e);
      bump();
    };
    (async () => {
      setLoading(true);
      let after = 0;
      for (;;) {
        const page = await api<Ev[]>(`/api/runs/${jobId}/events?after=${after}&limit=5000&kinds=${KINDS.join(',')}`)
          .catch(() => [] as Ev[]);
        if (closed) return;
        page.forEach(push);
        if (page.length < 5000) break;
        after = page[page.length - 1].seq;
      }
      setLoading(false);
      const from = events.current.length ? events.current[events.current.length - 1].seq : 0;
      es = new EventSource(withToken(`/api/runs/${jobId}/stream?after=${from}`));
      es.onopen = () => setConnected(true);
      es.onerror = () => setConnected(false);
      KINDS.forEach((k) => es!.addEventListener(k, (m) => push(JSON.parse((m as MessageEvent).data) as Ev)));
      es.addEventListener('END', () => { setConnected(false); es?.close(); });
    })();
    return () => { closed = true; es?.close(); if (pending !== null) window.clearTimeout(pending); setConnected(false); };
  }, [jobId]);

  return { events: events.current, agents: agents.current, version, connected, loading };
}

export function percentile(values: number[], p: number): number {
  if (!values.length) return 0;
  const s = [...values].sort((a, b) => a - b);
  return s[Math.min(s.length - 1, Math.floor((p / 100) * s.length))];
}

export const fmt = (n: number) => (n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e3 ? `${(n / 1e3).toFixed(1)}k` : String(Math.round(n)));
export const ms = (n: number) => (n >= 60000 ? `${(n / 60000).toFixed(1)} min` : n >= 1000 ? `${(n / 1000).toFixed(1)} s` : `${n} ms`);
