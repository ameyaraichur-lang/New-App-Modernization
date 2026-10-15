import { useEffect, useState } from 'react';
import { loadMaster, loadPhase, PHASE_IDS } from './data';
import type { MasterRegistry, PhaseRegistry, AgentSpec } from './types';
import { MasterMap } from './views/MasterMap';
import { PhaseView } from './views/PhaseView';
import { AgentAnatomy } from './views/AgentAnatomy';
import { Findings } from './views/Findings';
import { RunnerView } from './views/RunnerView';
import { LiveAgents } from './views/LiveAgents';

type View =
  | { kind: 'master' }
  | { kind: 'phase'; phase: number }
  | { kind: 'findings' }
  | { kind: 'runner' }
  | { kind: 'live' };

export default function App() {
  const [master, setMaster] = useState<MasterRegistry | null>(null);
  const [phaseReqs, setPhaseReqs] = useState<Record<number, PhaseRegistry>>({});
  const [view, setView] = useState<View>({ kind: 'master' });
  const [selectedAgent, setSelectedAgent] = useState<{ phase: number; agent: AgentSpec } | null>(null);

  useEffect(() => {
    loadMaster().then(setMaster);
  }, []);

  async function openPhase(phase: number) {
    if (!phaseReqs[phase]) {
      const reg = await loadPhase(phase);
      setPhaseReqs((prev) => ({ ...prev, [phase]: reg }));
    }
    setView({ kind: 'phase', phase });
    setSelectedAgent(null);
  }

  const roleCount = (phase: number) =>
    master?.phases.find((p) => p.phase === phase)?.roles.length;

  const isFuture = (phase: number) => phase >= 8;

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>Pipeline Console</h1>
        <div className="subtitle">
          App Modernization · blueprint v3 Review · {master ? `${master.phases.reduce((n, p) => n + p.roles.length, 0)} roles` : '…'}
        </div>

        <div className="nav-section">
          <div className="label">Pipeline</div>
          <button
            className={`nav-btn ${view.kind === 'master' ? 'active' : ''}`}
            onClick={() => setView({ kind: 'master' })}
          >
            Master pipeline map
            <span className="meta">{master ? `${master.links.length} typed links` : ''}</span>
          </button>
        </div>

        <div className="nav-section">
          <div className="label">Phases 1–6 · build scope</div>
          {PHASE_IDS.filter((p) => p <= 6).map((p) => (
            <button
              key={p}
              className={`nav-btn ${view.kind === 'phase' && view.phase === p ? 'active' : ''}`}
              onClick={() => openPhase(p)}
            >
              Phase {p}
              <span className="meta">
                {nameFor(master, p)} · {roleCount(p) ?? '…'} roles
              </span>
            </button>
          ))}
        </div>

        <div className="nav-section">
          <div className="label">Future phases</div>
          {PHASE_IDS.filter((p) => p > 6).map((p) => (
            <button
              key={p}
              className={`nav-btn future ${view.kind === 'phase' && view.phase === p ? 'active' : ''}`}
              onClick={() => openPhase(p)}
            >
              Phase {p}
              <span className="meta">{nameFor(master, p)} · {roleCount(p) ?? '…'} roles</span>
            </button>
          ))}
          <div className="label" style={{ marginTop: 10 }}>Phase 7</div>
          <div style={{ fontSize: 11, color: 'var(--muted)', padding: '2px 10px' }}>
            Intentionally skipped — assurance mapped to active phases (IA05)
          </div>
        </div>

        <div className="nav-section">
          <div className="label">Execute</div>
          <button
            className={`nav-btn ${view.kind === 'runner' ? 'active' : ''}`}
            onClick={() => setView({ kind: 'runner' })}
          >
            Run pipeline on repos
            <span className="meta">Astra agents P1–P4 · approvals · trace</span>
          </button>
          <button
            className={`nav-btn ${view.kind === 'live' ? 'active' : ''}`}
            onClick={() => setView({ kind: 'live' })}
          >
            Live agents
            <span className="meta">agent loop · LLM analysis · connectivity</span>
          </button>
        </div>

        <div className="nav-section">
          <div className="label">Review</div>
          <button
            className={`nav-btn ${view.kind === 'findings' ? 'active' : ''}`}
            onClick={() => setView({ kind: 'findings' })}
          >
            Open findings & freeze status
          </button>
        </div>
      </aside>

      <div className="main">
        <div className="topbar">
          <span className="crumb">{crumb(view, master, phaseReqs)}</span>
        </div>
        <div className="split">
          <div className="content" style={{ padding: 0 }}>
            {!master ? (
              <div style={{ padding: 20, color: 'var(--muted)' }}>Loading registry…</div>
            ) : view.kind === 'master' ? (
              <MasterMap master={master} onOpenPhase={openPhase} />
            ) : view.kind === 'findings' ? (
              <Findings master={master} phaseReqs={phaseReqs} />
            ) : view.kind === 'runner' ? (
              <RunnerView />
            ) : view.kind === 'live' ? (
              <LiveAgents />
            ) : (
              <PhaseView
                reg={phaseReqs[view.phase]}
                onSelectAgent={(agent) =>
                  setSelectedAgent({ phase: view.phase, agent })
                }
                selectedAgent={selectedAgent?.phase === view.phase ? selectedAgent?.agent.local_id : undefined}
              />
            )}
          </div>
          {selectedAgent && (
            <div className="detail-panel">
              <AgentAnatomy
                agent={selectedAgent.agent}
                reg={phaseReqs[selectedAgent.phase]}
                onClose={() => setSelectedAgent(null)}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function nameFor(master: MasterRegistry | null, phase: number): string {
  return master?.phases.find((p) => p.phase === phase)?.name ?? '';
}

function crumb(
  view: View,
  master: MasterRegistry | null,
  phaseReqs: Record<number, PhaseRegistry>,
): string {
  if (view.kind === 'master') return 'Master pipeline — 17 typed links, 78 roles, Phase 7 skipped';
  if (view.kind === 'findings') return 'Open findings (AH01–AH06) · freeze recommendations';
  if (view.kind === 'live') return 'Live agents — how each agent investigates, submits and is checked; model usage and connectivity';
  if (view.kind === 'runner') return 'Pipeline runner — one or many repositories, live agents, human release gates';
  const reg = phaseReqs[view.phase];
  return reg ? `P${reg.phase} · ${reg.name} · ${reg.schema_version} · ${reg.freeze_recommendation}` : `Phase ${view.phase}`;
}
