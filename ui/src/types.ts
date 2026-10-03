export interface AgentSpec {
  id: string;
  local_id: string;
  name: string;
  tier: number | null;
  tier_label: string;
  lane: string;
  prerequisites: string[];
  execution_raw: string;
  activities: string;
  inputs: string;
  outputs: string;
  origin: string;
  contract_rule: string;
  merge_tuning: string;
  responsibility: string;
}

export interface GateSpec {
  id: string;
  kind: string;
  node_type: string;
  entry: string;
  output: string;
  blocking_rule: string;
  meaning: string;
}

export interface EdgeSpec {
  from: string;
  to: string;
  from_kind: string;
  to_kind: string;
  type: string;
  required_artifact: string;
  failure_behavior: string;
  external: boolean;
}

export interface PhaseRegistry {
  phase: number;
  name: string;
  schema_version: string;
  freeze_recommendation: string;
  agents: AgentSpec[];
  gates: GateSpec[];
  hard_edges: EdgeSpec[];
  run_controls: { stage: string; control: string; when: string; behavior: string; accountable: string; failure: string }[];
  activation_matrix: Record<string, string>[];
  execution_routes: Record<string, string>[];
  artifact_contracts: {
    envelope_fields: { field: string; type: string; required: string; definition: string; failure: string }[];
    agent_payloads: Record<string, { fields: { name: string; type: string; nullable: boolean }[]; raw: string; rule: string }>;
    named_objects: Record<string, { type: string; required: string; definition: string; fields: { name: string; type: string }[]; failure: string }>;
  };
}

export interface MasterLink {
  id: string;
  from: string;
  to: string;
  type: string;
  handoff: string;
  label: string;
}

export interface MasterRegistry {
  phases: { phase: number; name: string; roles: { id: string; name: string }[]; freeze_recommendation: string }[];
  links: MasterLink[];
  open_findings: { id: string; severity: string; category: string; title: string }[];
}
