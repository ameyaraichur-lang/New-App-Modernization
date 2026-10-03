import { useMemo, useState } from 'react';
import {
  ReactFlow, Background, Controls, MiniMap,
  type Edge, type Node,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import type { MasterLink, MasterRegistry } from '../types';

const TYPE_COLOR: Record<string, string> = {
  HANDOFF: 'var(--handoff)',
  BRANCH: 'var(--branch)',
  CONDITIONAL: 'var(--conditional)',
  REFERENCE: 'var(--reference)',
  ACTIVATE: 'var(--activate)',
  PROPOSED: 'var(--proposed)',
};

const POSITIONS: Record<string, { x: number; y: number }> = {
  P1: { x: 0, y: 120 },
  P2: { x: 230, y: 120 },
  R: { x: 460, y: 300 },
  P3: { x: 460, y: 40 },
  P4: { x: 700, y: 40 },
  P5: { x: 930, y: 40 },
  P6: { x: 1180, y: 140 },
  P8: { x: 1180, y: -60 },
  P9: { x: 1420, y: -60 },
  C: { x: 1650, y: -60 },
  E: { x: 1180, y: 340 },
};

const NODE_META: Record<string, { title: string; sub: string; future?: boolean; ghost?: boolean }> = {
  P1: { title: 'P1', sub: 'Discovery' },
  P2: { title: 'P2', sub: 'Portfolio' },
  R: { title: 'R', sub: 'Retain / Retire / HOLD', ghost: true },
  P3: { title: 'P3', sub: 'Target architecture' },
  P4: { title: 'P4', sub: 'Modernization planning' },
  P5: { title: 'P5', sub: 'Code & app modernization' },
  P6: { title: 'P6', sub: 'Data modernization' },
  P8: { title: 'P8', sub: 'Deploy & cutover', future: true },
  P9: { title: 'P9', sub: 'Post-mod operations', future: true },
  C: { title: 'C', sub: 'Program closure', future: true },
  E: { title: 'E', sub: 'Environment (AH01)', ghost: true },
};

export function MasterMap({
  master,
  onOpenPhase,
}: {
  master: MasterRegistry;
  onOpenPhase: (phase: number) => void;
}) {
  const [selectedLink, setSelectedLink] = useState<MasterLink | null>(null);

  const nodes: Node[] = useMemo(() => {
    return Object.entries(POSITIONS).map(([id, pos]) => {
      const meta = NODE_META[id];
      const phaseNum = id.match(/^P(\d+)$/);
      const roles = phaseNum
        ? master.phases.find((p) => p.phase === Number(phaseNum[1]))?.roles.length
        : undefined;
      return {
        id,
        position: pos,
        data: {
          label: (
            <div
              style={{
                opacity: meta.ghost ? 0.6 : meta.future ? 0.55 : 1,
                cursor: phaseNum && Number(phaseNum[1]) !== 7 ? 'pointer' : 'default',
              }}
              onClick={() => phaseNum && onOpenPhase(Number(phaseNum[1]))}
            >
              <div className="node-label" style={{ fontWeight: 700, fontSize: 13 }}>{meta.title}</div>
              <div className="node-sub">{meta.sub}</div>
              {roles !== undefined && <div className="node-sub">{roles} roles</div>}
            </div>
          ),
        },
        style: {
          background: meta.ghost ? '#21262d' : 'var(--panel2)',
          border: `1px solid ${meta.future ? '#6e768166' : 'var(--border)'}`,
          borderRadius: 8,
          width: 168,
          padding: 8,
        },
      };
    });
  }, [master, onOpenPhase]);

  const edges: Edge[] = useMemo(() => {
    return master.links.map((link) => ({
      id: link.id,
      source: link.from,
      target: link.to,
      label: `${link.id} · ${link.type.toLowerCase()}`,
      animated: link.type === 'PROPOSED',
      style: {
        stroke: TYPE_COLOR[link.type] ?? 'var(--border)',
        strokeWidth: link.type === 'HANDOFF' ? 2 : 1.5,
        strokeDasharray: link.type === 'PROPOSED' ? '5 4' : undefined,
      },
      labelStyle: { fill: '#c9d1d9', fontSize: 10, fontWeight: 600 },
      labelBgStyle: { fill: '#161b22', fillOpacity: 0.9 },
      labelBgPadding: [4, 2] as [number, number],
    }));
  }, [master]);

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onEdgeClick={(_, edge) => {
          const link = master.links.find((l) => l.id === edge.id);
          if (link) setSelectedLink(link);
        }}
        fitView
        proOptions={{ hideAttribution: true }}
      >
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
        {Object.entries(TYPE_COLOR).map(([type, color]) => (
          <div className="row" key={type}>
            <div className="swatch" style={{ background: color }} />
            {type}
          </div>
        ))}
      </div>

      {selectedLink && (
        <div
          style={{
            position: 'absolute', top: 12, right: 12, zIndex: 10, width: 330,
            background: 'var(--panel)', border: '1px solid var(--border)',
            borderRadius: 8, padding: 14,
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <b>{selectedLink.id} · {selectedLink.handoff}</b>
            <button className="nav-btn" style={{ padding: '0 8px' }} onClick={() => setSelectedLink(null)}>×</button>
          </div>
          <p style={{ fontSize: 12, color: 'var(--muted)', margin: '8px 0 4px' }}>
            {selectedLink.from} → {selectedLink.to} · <span style={{ color: TYPE_COLOR[selectedLink.type] }}>{selectedLink.type}</span>
          </p>
          <p style={{ fontSize: 12, margin: 0 }}>{selectedLink.label}</p>
        </div>
      )}

      <div style={{ position: 'absolute', top: 12, left: 12, zIndex: 10, maxWidth: 430 }}>
        <div className="card">
          <h3>Master pipeline topology</h3>
          <p className="body" style={{ color: 'var(--muted)', fontSize: 12 }}>
            Generated from Master_Registry.json — 17 typed connections, 78 roles, 8 active
            phases (1–6, 8, 9), Phase 7 intentionally skipped. Click a phase node to open
            its DAG; click a link for its handoff contract (H01–H18).
          </p>
        </div>
      </div>
    </div>
  );
}
