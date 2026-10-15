# Step 33 eval — `run8-tune` (`job-1791977827-353a3d`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (499/499) | ≥ 95% |
| evidence resolvability | 100.0% (27767/27767) | ≥ 90% |
| hallucinated paths | 0 of 2778 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 601 checked | = 0 |

## Confidence score

**0.0%** — weakest component C3; 6 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 99.24% | schema valid after repair 499/499 (LB 99.24%); evidence ids resolve 27767/27767 (LB 99.99%); cited paths exist 2778/2778 (LB 99.86%); A9 function names exist 601/601 (LB 99.36%) |
| C2 Factual accuracy | 91.29% | golden facts agree 577/617 (LB 91.29%) |
| C3 Claim support | not assessed | claim-support verifier not built (stack PR 6) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 97.86% | 1 - ECE at bootstrap 95%: 207 fact confidences, ECE 0.0092, 95th percentile 0.0214 |
| C7 Execution proof | not assessed | P5 runtime differential NOT_RUN; sandbox deferred (decision 1) |
| C8 Robustness | not assessed | adversarial suite not built (stack PR 8) |
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
| primary_language | 90.0% | 20 | carddemo primary_language (got shell, want cobol), bugzilla primary_language (got javascript, want perl) |
| route | 76.36% | 110 | eshop-on-web /[controller] (got False, want True), eshop-on-web /[controller]/[action] (got False, want True), eshop-on-web /api/[controller]/[action] (got False, want True), ofbiz /*/openapi.* (got False, want True), webgoat /challenge/7 (got False, want True) |
| runtime_version | 100.0% | 11 | — |
| test_framework | 100.0% | 7 | — |

## Calibration of model confidence

207 fact confidences checked against golden facts: ECE 0.0092 (bootstrap 95th percentile 0.0214). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.7-0.8 | 1 | 0.7 | 1.0 |
| 0.9-1.0 | 206 | 0.978 | 0.985 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 19 | 0.927 | 0.842 |
| datastore | 23 | 0.98 | 1.0 |
| entity | 40 | 0.99 | 1.0 |
| framework | 22 | 0.978 | 1.0 |
| license | 11 | 0.989 | 1.0 |
| route | 82 | 0.978 | 1.0 |
| runtime_version | 10 | 0.978 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 19 | 0.927 | 0.7 | 0.99 | 0 |
| P1 A11 risk scores | 60 | 0.94 | 0.82 | 0.99 | 0 |
| P2 A6 dispositions | 20 | 0.833 | 0.77 | 0.9 | 0 |
| P3 A2 boundaries | 117 | 0.953 | 0.8 | 0.99 | 0 |
| P4 A3 task estimates | 122 | 0.84 | 0.66 | 0.96 | 0 |

## Variation with evidence

- P2 dispositions: {'Refactor': 9, 'Retain': 3, 'Replatform': 7, 'Retire': 1}
- P3 decomposition: 16 distinct boundary sets across 16 apps
