# Step 33 eval — `run-memory-tune` (`job-1792340613-81baff`)

**Release gate: FAIL**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (295/295) | ≥ 95% |
| evidence resolvability | 100.0% (15468/15468) | ≥ 90% |
| hallucinated paths | 2 of 3065 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 625 checked | = 0 |

## Confidence score

**0.0%** — weakest component C4; 4 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 98.71% | schema valid after repair 295/295 (LB 98.71%); evidence ids resolve 15468/15468 (LB 99.98%); cited paths exist 3063/3065 (LB 99.76%); A9 function names exist 625/625 (LB 99.39%) |
| C2 Factual accuracy | 92.21% | golden facts agree 582/617 (LB 92.21%) |
| C3 Claim support | 64.97% | cited claims entailed by their evidence 2499/3758 (LB 64.97%) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 97.62% | 1 - ECE at bootstrap 95%: 213 fact confidences, ECE 0.0099, 95th percentile 0.0238 |
| C7 Execution proof | not assessed | P5 runtime differential NOT_RUN; sandbox deferred (decision 1) |
| C8 Robustness | 94.42% | adversarial cases pass 65/65 (LB 94.42%) |
| C9 Human acceptance | not assessed | all reviews were by scripted actors |

## Agreement with golden facts (`evals/golden/facts/`)

617 tool-derived facts over 20 repos; 0 human-reviewed.

| fact type | agreement | n | misses (first 5) |
|---|---|---|---|
| build_manifest | 100.0% | 25 | — |
| capability_route | 80.0% | 20 | struts-examples capability_route (got API_ONLY, want UI), carddemo capability_route (got HEADLESS_BATCH, want HEADLESS), mantisbt capability_route (got API_ONLY, want UI), bugzilla capability_route (got API_ONLY, want UI) |
| ci | 100.0% | 20 | — |
| containerized | 100.0% | 20 | — |
| datastore | 95.83% | 24 | carddemo postgresql (got False, want True) |
| dependency | 100.0% | 242 | — |
| entity | 97.56% | 41 | django-realworld-example-app TimestampedModel (got False, want True) |
| framework | 100.0% | 23 | — |
| has_data_layer | 80.0% | 20 | sinatra has_data_layer (got True, want False), todomvc has_data_layer (got True, want False), react-redux-realworld has_data_layer (got True, want False), struts-examples has_data_layer (got True, want False) |
| has_tests | 90.0% | 20 | microblog has_tests (got True, want False), bugzilla has_tests (got False, want True) |
| license | 100.0% | 14 | — |
| primary_language | 100.0% | 20 | — |
| route | 79.09% | 110 | eshop-on-web /[controller] (got False, want True), eshop-on-web /[controller]/[action] (got False, want True), eshop-on-web /api/[controller]/[action] (got False, want True), ofbiz /*/openapi.* (got False, want True), webgoat /challenge/7 (got False, want True) |
| runtime_version | 100.0% | 11 | — |
| test_framework | 100.0% | 7 | — |

## Assurance of released items (`appmod/kernel/assurance.py`)

6388 items released through 29 G2 gates: coverage 100.0%, of which 46.27% without scripted confirmation (tool-measured, entailed or human-confirmed).

| class | items | share |
|---|---|---|
| tool-measured | 457 | 7.15% |
| entailed | 2499 | 39.12% |
| scripted-confirmed | 3432 | 53.73% |

## Evidence mix (model items: OBSERVED + DOCUMENTED share)

| phase | share | observed+documented | total |
|---|---|---|---|
| P1 | 51.26% | 2282 | 4452 |
| P2 | 16.79% | 23 | 137 |
| P3 | 15.25% | 120 | 787 |
| P4 | 18.23% | 74 | 406 |

## Claim support (`appmod/agents/verifier.py`)

3758 cited OBSERVED/DOCUMENTED model claims. NOT_ENTAILED and INSUFFICIENT were published as INFERRED. UNCHECKED: no checkable text behind the ids or no verdict; NO_RECORD: published without a verifier verdict.

| verdict | claims | share |
|---|---|---|
| ENTAILED | 2499 | 66.5% |
| INSUFFICIENT | 1156 | 30.76% |
| NOT_ENTAILED | 102 | 2.71% |
| UNCHECKED | 1 | 0.03% |

Human audit sample: 206 claims (`verifier-audit-<label>.jsonl`).

## Calibration of model confidence

213 fact confidences checked against golden facts: ECE 0.0099 (bootstrap 95th percentile 0.0238). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.8-0.9 | 1 | 0.85 | 0.0 |
| 0.9-1.0 | 212 | 0.98 | 0.986 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 19 | 0.937 | 0.789 |
| datastore | 23 | 0.98 | 1.0 |
| entity | 40 | 0.989 | 1.0 |
| framework | 23 | 0.981 | 1.0 |
| license | 14 | 0.989 | 1.0 |
| route | 84 | 0.982 | 1.0 |
| runtime_version | 10 | 0.976 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 19 | 0.937 | 0.85 | 0.95 | 0 |
| P1 A11 risk scores | 60 | 0.93 | 0.7 | 0.99 | 0 |
| P2 A6 dispositions | 20 | 0.781 | 0.64 | 0.89 | 0 |
| P3 A2 boundaries | 24 | 0.953 | 0.9 | 0.97 | 0 |
| P4 A3 task estimates | 29 | 0.844 | 0.78 | 0.93 | 0 |

## Variation with evidence

- P2 dispositions: {'Retain': 15, 'Replatform': 3, 'Retire': 1, 'Refactor': 1}
- P3 decomposition: 4 distinct boundary sets across 4 apps

## Hallucinated paths

- `{"artifact": "P1/flask-tutorial/A3", "path": "auth.py/blog.py"}`
- `{"artifact": "P1/microblog/A1", "path": "Dockerfile/boot.sh"}`
