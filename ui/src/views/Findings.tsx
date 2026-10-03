import type { MasterRegistry, PhaseRegistry } from '../types';

export function Findings({
  master,
  phaseReqs,
}: {
  master: MasterRegistry;
  phaseReqs: Record<number, PhaseRegistry>;
}) {
  const sevColor = (sev: string) =>
    sev === 'High' ? 'red' : 'amber';
  const catColor = (cat: string) =>
    cat.includes('ROUTE GAP') ? 'red' : cat.includes('CLARIFICATION') ? 'amber' : 'blue';

  return (
    <div style={{ padding: 20, maxWidth: 980 }}>
      <h2 style={{ marginTop: 0 }}>Open findings — blueprint audit (AH01–AH06)</h2>
      <p style={{ color: 'var(--muted)', fontSize: 13 }}>
        From Integrated_Handoff_Audit.md. Each finding carries its build-side resolution
        from the build plan (§1.5): AH01 pilot-scope environment option, AH02 disposition
        register, AH03 release-identity chain, AH04 = this build's contract layer,
        AH05 pilot-default policy bundle, AH06 invalidation engine.
      </p>

      {master.open_findings.map((f) => (
        <div className="card" key={f.id}>
          <h3>
            {f.id} — {f.title}{' '}
            <span className={`chip ${sevColor(f.severity)}`}>{f.severity}</span>{' '}
            <span className={`chip ${catColor(f.category)}`}>{f.category}</span>
          </h3>
        </div>
      ))}

      <h2>Freeze status per phase</h2>
      <table className="table">
        <thead>
          <tr>
            <th>Phase</th><th>Name</th><th>Roles</th><th>Gates</th><th>Freeze recommendation</th>
          </tr>
        </thead>
        <tbody>
          {master.phases.map((p) => {
            const reg = phaseReqs[p.phase];
            return (
              <tr key={p.phase} style={{ opacity: p.phase >= 8 ? 0.55 : 1 }}>
                <td><b>P{p.phase}</b></td>
                <td>{p.name}</td>
                <td>{p.roles.length}</td>
                <td className="small">{reg ? reg.gates.map((g) => g.id).join(', ') : '—'}</td>
                <td>
                  <span className={`chip ${p.freeze_recommendation === 'FREEZE CORE STRUCTURE' ? 'green' : 'blue'}`}>
                    {p.freeze_recommendation}
                  </span>
                </td>
              </tr>
            );
          })}
          <tr>
            <td><b>P7</b></td>
            <td colSpan={4} className="small">Intentionally skipped — assurance mapped to active phases (IA05)</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
