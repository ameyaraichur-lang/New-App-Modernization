import type { MasterRegistry, PhaseRegistry } from './types';

export const PHASE_IDS = [1, 2, 3, 4, 5, 6, 8, 9];

export async function loadMaster(): Promise<MasterRegistry> {
  const res = await fetch('/registry/master.json');
  return res.json();
}

export async function loadPhase(phase: number): Promise<PhaseRegistry> {
  const res = await fetch(`/registry/phase_${phase}.json`);
  return res.json();
}

/** Layered layout: x by tier/gate stage, y by order within column. */
export function layoutPhase(reg: PhaseRegistry) {
  type Pos = { x: number; y: number };
  const COL_WIDTH = 300;
  const ROW_HEIGHT = 140;

  const nodes = [
    ...reg.agents.map((a) => ({ id: a.local_id, kind: 'agent' as const, tier: a.tier, lane: a.lane })),
    ...reg.gates.map((g) => ({ id: g.id, kind: g.kind as string, tier: null, lane: 'normal' })),
  ];

  // Column key: gates keep their id (G0 < Tier0 < ... < G1 < ...); use a
  // synthetic order index derived from topological position.
  const incoming: Record<string, string[]> = {};
  for (const e of reg.hard_edges) {
    (incoming[e.to] ||= []).push(e.from);
  }
  // compute depth via longest-path over agents+gates
  const depth: Record<string, number> = {};
  const resolve = (id: string, guard: Set<string> = new Set()): number => {
    if (id in depth) return depth[id];
    if (guard.has(id)) return 0;
    guard.add(id);
    const preds = incoming[id] || [];
    depth[id] = preds.length ? Math.max(...preds.map((p) => resolve(p, guard))) + 1 : 0;
    return depth[id];
  };
  nodes.forEach((n) => resolve(n.id));

  const byCol: Record<number, typeof nodes> = {};
  for (const n of nodes) {
    const col = n.kind === 'intake' ? 0 : depth[n.id];
    (byCol[col] ||= []).push(n);
  }
  const positions: Record<string, Pos> = {};
  for (const [col, items] of Object.entries(byCol)) {
    const x = Number(col) * COL_WIDTH;
    const sorted = [...items].sort((a, b) => a.id.localeCompare(b.id, undefined, { numeric: true }));
    sorted.forEach((n, i) => {
      positions[n.id] = { x, y: i * ROW_HEIGHT };
    });
  }
  return { positions, depth };
}
