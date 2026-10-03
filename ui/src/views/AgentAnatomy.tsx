import type { AgentSpec, PhaseRegistry } from '../types';

/**
 * The "exact work anatomy" view: every field comes verbatim from the compiled
 * workbook registry — activities, inputs, outputs, execution/prerequisites,
 * origin (merge lineage) and the evidence & safety contract.
 */
export function AgentAnatomy({
  agent,
  reg,
  onClose,
}: {
  agent: AgentSpec;
  reg: PhaseRegistry;
  onClose: () => void;
}) {
  const payload = reg.artifact_contracts.agent_payloads[agent.local_id];
  const controls = reg.run_controls.filter((rc) =>
    rc.stage.includes(agent.local_id) || rc.stage === 'RUN' || rc.stage === 'All',
  );

  return (
    <div className="agent-anatomy">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
        <div>
          <h2>{agent.id}</h2>
          <div style={{ color: 'var(--muted)', fontSize: 13 }}>{agent.name}</div>
          <div style={{ marginTop: 6 }}>
            <span className="chip blue">
              {agent.lane === 'async' ? 'async lane' : `Tier ${agent.tier ?? '—'}`}
            </span>
            <span className="chip">{agent.tier_label}</span>
            {agent.prerequisites.length > 0 && (
              <span className="chip amber">requires {agent.prerequisites.join(' + ')}</span>
            )}
          </div>
        </div>
        <button className="nav-btn" style={{ padding: '0 8px' }} onClick={onClose}>×</button>
      </div>

      <div className="section">
        <h4>Activities & responsibility</h4>
        <p>{agent.activities}</p>
      </div>

      <div className="section">
        <h4>Inputs</h4>
        <p>{agent.inputs}</p>
      </div>

      <div className="section">
        <h4>Outputs</h4>
        <p>{agent.outputs}</p>
      </div>

      <div className="section">
        <h4>Execution & prerequisites</h4>
        <p>{agent.execution_raw}</p>
      </div>

      <div className="section">
        <h4>Origin · merge lineage</h4>
        <p>{agent.origin || '—'}</p>
        {agent.merge_tuning && <p style={{ color: 'var(--muted)' }}>{agent.merge_tuning}</p>}
      </div>

      <div className="section">
        <h4>Evidence & safety contract</h4>
        <div className="guardrail">
          <p>{agent.contract_rule}</p>
        </div>
      </div>

      {payload && (
        <div className="section">
          <h4>Artifact payload contract</h4>
          <table className="table field-table">
            <thead>
              <tr><th>field</th><th>type</th><th>nullable</th></tr>
            </thead>
            <tbody>
              {payload.fields.map((f) => (
                <tr key={f.name}>
                  <td><code>{f.name}</code></td>
                  <td>{f.type}</td>
                  <td>{f.nullable ? 'yes' : 'no'}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {payload.rule && (
            <p style={{ color: 'var(--muted)', marginTop: 6, fontSize: 11 }}>{payload.rule}</p>
          )}
        </div>
      )}

      {controls.length > 0 && (
        <div className="section">
          <h4>Binding run controls</h4>
          {controls.slice(0, 6).map((rc, i) => (
            <div className="card" key={i}>
              <h3>{rc.control} <span className="chip">{rc.stage}</span></h3>
              <p className="body">{rc.behavior}</p>
              {rc.failure && (
                <div className="kv"><b>On failure:</b> {rc.failure}</div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
