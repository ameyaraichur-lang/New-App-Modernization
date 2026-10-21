# Step 33 eval — `run-analyzers-tune` (`job-1792312730-11eca1`)

**Release gate: FAIL**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (414/414) | ≥ 95% |
| evidence resolvability | 100.0% (21838/21838) | ≥ 90% |
| hallucinated paths | 3 of 3050 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 663 checked | = 0 |

## Confidence score

**0.0%** — weakest component C4; 4 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 99.08% | schema valid after repair 414/414 (LB 99.08%); evidence ids resolve 21838/21838 (LB 99.98%); cited paths exist 3047/3050 (LB 99.71%); A9 function names exist 663/663 (LB 99.42%) |
| C2 Factual accuracy | 91.29% | golden facts agree 577/617 (LB 91.29%) |
| C3 Claim support | 59.44% | cited claims entailed by their evidence 2754/4524 (LB 59.44%) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 97.92% | 1 - ECE at bootstrap 95%: 207 fact confidences, ECE 0.0111, 95th percentile 0.0208 |
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
| entity | 90.24% | 41 | django-realworld-example-app TimestampedModel (got False, want True), webgoat AssignmentProgress (got False, want True), webgoat LessonProgress (got False, want True), webgoat UserProgress (got False, want True) |
| framework | 100.0% | 23 | — |
| has_data_layer | 80.0% | 20 | sinatra has_data_layer (got True, want False), todomvc has_data_layer (got True, want False), react-redux-realworld has_data_layer (got True, want False), struts-examples has_data_layer (got True, want False) |
| has_tests | 90.0% | 20 | microblog has_tests (got True, want False), bugzilla has_tests (got False, want True) |
| license | 100.0% | 14 | — |
| primary_language | 100.0% | 20 | — |
| route | 77.27% | 110 | eshop-on-web /[controller] (got False, want True), eshop-on-web /[controller]/[action] (got False, want True), eshop-on-web /api/[controller]/[action] (got False, want True), ofbiz /*/openapi.* (got False, want True), webgoat /challenge/7 (got False, want True) |
| runtime_version | 100.0% | 11 | — |
| test_framework | 100.0% | 7 | — |

## Assurance of released items (`appmod/kernel/assurance.py`)

8600 items released through 43 G2 gates: coverage 100.0%, of which 38.72% without scripted confirmation (tool-measured, entailed or human-confirmed).

| class | items | share |
|---|---|---|
| tool-measured | 576 | 6.7% |
| entailed | 2754 | 32.02% |
| scripted-confirmed | 5270 | 61.28% |

## Evidence mix (model items: OBSERVED + DOCUMENTED share)

| phase | share | observed+documented | total |
|---|---|---|---|
| P1 | 50.09% | 2193 | 4378 |
| P2 | 13.99% | 20 | 143 |
| P3 | 14.32% | 318 | 2221 |
| P4 | 19.54% | 223 | 1141 |

## Claim support (`appmod/agents/verifier.py`)

4524 cited OBSERVED/DOCUMENTED model claims. NOT_ENTAILED and INSUFFICIENT were published as INFERRED. UNCHECKED: no checkable text behind the ids or no verdict; NO_RECORD: published without a verifier verdict.

| verdict | claims | share |
|---|---|---|
| ENTAILED | 2754 | 60.88% |
| INSUFFICIENT | 1535 | 33.93% |
| NOT_ENTAILED | 235 | 5.19% |

Human audit sample: 198 claims (`verifier-audit-<label>.jsonl`).

## Calibration of model confidence

207 fact confidences checked against golden facts: ECE 0.0111 (bootstrap 95th percentile 0.0208). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.9-1.0 | 207 | 0.979 | 0.99 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 19 | 0.945 | 0.895 |
| datastore | 23 | 0.979 | 1.0 |
| entity | 36 | 0.99 | 1.0 |
| framework | 23 | 0.981 | 1.0 |
| license | 14 | 0.989 | 1.0 |
| route | 82 | 0.981 | 1.0 |
| runtime_version | 10 | 0.974 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 19 | 0.945 | 0.9 | 0.95 | 0 |
| P1 A11 risk scores | 59 | 0.938 | 0.78 | 0.99 | 0 |
| P2 A6 dispositions | 20 | 0.795 | 0.6 | 0.87 | 0 |
| P3 A2 boundaries | 73 | 0.936 | 0.73 | 0.98 | 0 |
| P4 A3 task estimates | 81 | 0.814 | 0.63 | 0.93 | 0 |

## Variation with evidence

- P2 dispositions: {'Retain': 8, 'Replatform': 7, 'Refactor': 3, 'Retire': 1, 'Replace': 1}
- P3 decomposition: 11 distinct boundary sets across 11 apps

## Hallucinated paths

- `{"artifact": "P1/spring-petclinic/A2", "path": "pom.xml/build.gradle"}`
- `{"artifact": "P1/microblog/A2", "path": "search.py/translate.py/email.py"}`
- `{"artifact": "P1/struts-examples/A2", "path": "data/order...json"}`
