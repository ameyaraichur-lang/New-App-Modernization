import { useMemo } from 'react';
import type React from 'react';
import {
  ReactFlow, Background, Controls, MiniMap, MarkerType,
  type Edge, type Node,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import type { AgentSpec, PhaseRegistry } from '../types';
import { layoutPhase } from '../data';

export function PhaseView({
  reg,
  onSelectAgent,
  selectedAgent,
}: {
  reg: PhaseRegistry;
  onSelectAgent: (agent: AgentSpec) => void;
  selectedAgent?: string;
}) {
  const { nodes, edges } = useMemo(() => buildGraph(reg, onSelectAgent, selectedAgent),
    [reg, onSelectAgent, selectedAgent]);
  if (!reg) return <div style={{ padding: 20, color: 'var(--muted)' }}>Loading…</div>;

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <ReactFlow nodes={nodes} edges={edges} fitView proOptions={{ hideAttribution: true }}>
        <Background color="#21262d" gap={20} />
        <Controls />
        <MiniMap
          pannable
          zoomable
          nodeColor="#30363d"
          nodeStrokeColor="#8b949e"
          maskColor="#0d1117cc"
          style={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }}
        />
      </ReactFlow>
      <div className="legend">
        <div className="row"><span className="chip blue">agent</span> tier-ordered hard edges</div>
        <div className="row"><span className="chip amber">gate</span> deterministic service · never an agent</div>
        <div className="row"><span className="chip purple">execution</span> X-services (deterministic runner)</div>
        <div className="row"><span className="chip">dashed</span> async lane — never blocks fan-in</div>
      </div>
      <div style={{ position: 'absolute', top: 12, left: 12, zIndex: 10 }}>
        <div className="card" style={{ maxWidth: 380 }}>
          <h3>P{reg.phase} — {reg.name}</h3>
          <div className="kv">
            <b>{reg.agents.length}</b> agents · <b>{reg.gates.length}</b> gates ·{' '}
            <b>{reg.hard_edges.filter((e) => !e.external).length}</b> hard edges ·{' '}
            <b>{reg.hard_edges.filter((e) => e.external).length}</b> external routes
          </div>
          <div className="kv" style={{ marginTop: 6 }}>
            <span className={`chip ${reg.freeze_recommendation === 'FREEZE CORE STRUCTURE' ? 'green' : 'blue'}`}>
              {reg.freeze_recommendation}
            </span>
            {reg.schema_version}
          </div>
          <p className="body" style={{ color: 'var(--muted)', fontSize: 12, marginTop: 8 }}>
            Click any agent node to open its full work anatomy. Layout mirrors the workbook
            Execution DAG (topological tiers left → right).
          </p>
        </div>
      </div>
    </div>
  );
}

function buildGraph(
  reg: PhaseRegistry,
  onSelectAgent: (a: AgentSpec) => void,
  selectedAgent?: string,
): { nodes: Node[]; edges: Edge[] } {
  if (!reg) return { nodes: [], edges: [] };
  const { positions } = layoutPhase(reg);

  const nodes: Node[] = [];
  for (const agent of reg.agents) {
    nodes.push({
      id: agent.local_id,
      position: positions[agent.local_id] ?? { x: 0, y: 0 },
      data: {
        label: (
          <div onClick={() => onSelectAgent(agent)} style={{ cursor: 'pointer' }}>
            <div className="node-label">
              <span className="badge-tier">{agent.lane === 'async' ? 'async' : `T${agent.tier ?? '·'}`}</span>
              <b>{agent.local_id}</b>
            </div>
            <div className="node-sub">{agent.name}</div>
          </div>
        ),
      },
      style: {
        background: agent.local_id === selectedAgent ? '#1f6feb44' : 'var(--panel2)',
        border: `1px solid ${agent.local_id === selectedAgent ? '#1f6feb' : 'var(--border)'}`,
        borderRadius: 8, width: 205, padding: 9,
        borderStyle: agent.lane === 'async' ? 'dashed' : 'solid',
      },
    });
  }
  for (const gate of reg.gates) {
    nodes.push({
      id: gate.id,
      position: positions[gate.id] ?? { x: 0, y: 0 },
      data: {
        label: (
          <div className="node-label" style={{ textAlign: 'center' }}>
            <b style={{ color: gate.node_type === 'execution' ? 'var(--purple)' : 'var(--amber)' }}>
              {gate.id}
            </b>
            <div className="node-sub">{gate.kind}</div>
          </div>
        ),
      },
      style: {
        background: '#21262d',
        border: `1.5px solid ${gate.node_type === 'execution' ? 'var(--purple)' : 'var(--amber)'}'`,
        borderRadius: 20, width: 90, padding: 6,
      },
    });
  }

  const edges: Edge[] = reg.hard_edges
    .filter((e) => !e.external)
    .map((e) => ({
      id: `${e.from}->${e.to}`,
      source: e.from,
      target: e.to,
      animated: false,
      markerEnd: { type: MarkerType.ArrowClosed, color: '#58a6ff88' },
      style: { stroke: '#58a6ff66', strokeWidth: 1.5 },
    }));

  // external routes shown as stub labels on their source node
  const externals: Record<string, string[]> = {};
  for (const e of reg.hard_edges.filter((x) => x.external)) {
    (externals[e.from] ||= []).push(e.to);
  }
  for (const node of nodes) {
    const ext = externals[node.id];
    if (ext) {
      const base = node.data.label as React.ReactNode;
      node.data = {
        ...node.data,
        label: (
          <div>
            {base}
            <div className="node-sub" style={{ color: 'var(--green)', marginTop: 2 }}>
              → {ext.join(', ')}
            </div>
          </div>
        ),
      };
    }
  }
  return { nodes, edges };
}
