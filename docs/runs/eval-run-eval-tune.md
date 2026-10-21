# Step 33 eval — `run-eval-tune` (`job-1792182753-d8acb4`)

**Release gate: FAIL**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (499/499) | ≥ 95% |
| evidence resolvability | 100.0% (26352/26352) | ≥ 90% |
| hallucinated paths | 2 of 3027 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 606 checked | = 0 |

## Confidence score

**0.0%** — weakest component C4; 4 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 99.24% | schema valid after repair 499/499 (LB 99.24%); evidence ids resolve 26352/26352 (LB 99.99%); cited paths exist 3025/3027 (LB 99.76%); A9 function names exist 606/606 (LB 99.37%) |
| C2 Factual accuracy | 91.84% | golden facts agree 580/617 (LB 91.84%) |
| C3 Claim support | 55.44% | cited claims entailed by their evidence 2789/4908 (LB 55.44%) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 98.14% | 1 - ECE at bootstrap 95%: 209 fact confidences, ECE 0.0076, 95th percentile 0.0186 |
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
| route | 77.27% | 110 | eshop-on-web /[controller] (got False, want True), eshop-on-web /[controller]/[action] (got False, want True), eshop-on-web /api/[controller]/[action] (got False, want True), ofbiz /*/openapi.* (got False, want True), webgoat /challenge/7 (got False, want True) |
| runtime_version | 100.0% | 11 | — |
| test_framework | 100.0% | 7 | — |

## Assurance of released items (`appmod/kernel/assurance.py`)

10244 items released through 53 G2 gates: coverage 100.0%, of which 33.68% without scripted confirmation (tool-measured, entailed or human-confirmed).

| class | items | share |
|---|---|---|
| tool-measured | 661 | 6.45% |
| entailed | 2789 | 27.23% |
| scripted-confirmed | 6794 | 66.32% |

## Claim support (`appmod/agents/verifier.py`)

4908 cited OBSERVED/DOCUMENTED model claims. NOT_ENTAILED and INSUFFICIENT were published as INFERRED. UNCHECKED: no checkable text behind the ids or no verdict; NO_RECORD: published without a verifier verdict.

| verdict | claims | share |
|---|---|---|
| ENTAILED | 2789 | 56.83% |
| INSUFFICIENT | 1832 | 37.33% |
| NOT_ENTAILED | 279 | 5.68% |
| UNCHECKED | 8 | 0.16% |

Human audit sample: 216 claims (`verifier-audit-<label>.jsonl`).

## Calibration of model confidence

209 fact confidences checked against golden facts: ECE 0.0076 (bootstrap 95th percentile 0.0186). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.9-1.0 | 209 | 0.978 | 0.986 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 19 | 0.926 | 0.842 |
| datastore | 23 | 0.982 | 1.0 |
| entity | 40 | 0.991 | 1.0 |
| framework | 23 | 0.978 | 1.0 |
| license | 13 | 0.99 | 1.0 |
| route | 81 | 0.981 | 1.0 |
| runtime_version | 10 | 0.974 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 19 | 0.926 | 0.9 | 0.95 | 0 |
| P1 A11 risk scores | 60 | 0.931 | 0.65 | 0.99 | 0 |
| P2 A6 dispositions | 20 | 0.803 | 0.67 | 0.91 | 0 |
| P3 A2 boundaries | 115 | 0.95 | 0.84 | 0.98 | 0 |
| P4 A3 task estimates | 115 | 0.84 | 0.69 | 0.93 | 0 |

## Variation with evidence

- P2 dispositions: {'Refactor': 12, 'Replatform': 4, 'Retire': 1, 'Retain': 3}
- P3 decomposition: 16 distinct boundary sets across 16 apps

## Hallucinated paths

- `{"artifact": "P1/node-express-realworld-example-app/A1", "path": "listing/package.json"}`
- `{"artifact": "P4/golang-example/A3", "path": "users/articles/common/scripts/api/doc.go"}`
