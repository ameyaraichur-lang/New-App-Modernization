# Step 33 eval — `run7-tune` (`job-1791958928-42cb2d`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (499/499) | ≥ 95% |
| evidence resolvability | 100.0% (27428/27428) | ≥ 90% |
| hallucinated paths | 0 of 2813 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 653 checked | = 0 |

## Confidence score

**0.0%** — weakest component C3; 6 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 99.24% | schema valid after repair 499/499 (LB 99.24%); evidence ids resolve 27428/27428 (LB 99.99%); cited paths exist 2813/2813 (LB 99.86%); A9 function names exist 653/653 (LB 99.42%) |
| C2 Factual accuracy | 89.47% | golden facts agree 567/617 (LB 89.47%) |
| C3 Claim support | not assessed | claim-support verifier not built (stack PR 6) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 98.21% | 1 - ECE at bootstrap 95%: 203 fact confidences, ECE 0.0051, 95th percentile 0.0179 |
| C7 Execution proof | not assessed | P5 runtime differential NOT_RUN; sandbox deferred (decision 1) |
| C8 Robustness | not assessed | adversarial suite not built (stack PR 8) |
| C9 Human acceptance | not assessed | all reviews were by scripted actors |

## Agreement with golden facts (`evals/golden/facts/`)

617 tool-derived facts over 20 repos; 0 human-reviewed.

| fact type | agreement | n | misses (first 5) |
|---|---|---|---|
| build_manifest | 100.0% | 25 | — |
| capability_route | 75.0% | 20 | golang-example capability_route (got HEADLESS_BATCH, want API_ONLY), struts-examples capability_route (got API_ONLY, want UI), carddemo capability_route (got HEADLESS_BATCH, want HEADLESS), mantisbt capability_route (got API_ONLY, want UI), bugzilla capability_route (got API_ONLY, want UI) |
| ci | 90.0% | 20 | musicstore ci (got False, want True), todomvc ci (got False, want True) |
| containerized | 100.0% | 20 | — |
| datastore | 95.83% | 24 | carddemo postgresql (got False, want True) |
| dependency | 100.0% | 242 | — |
| entity | 97.56% | 41 | django-realworld-example-app TimestampedModel (got False, want True) |
| framework | 100.0% | 23 | — |
| has_data_layer | 80.0% | 20 | sinatra has_data_layer (got True, want False), todomvc has_data_layer (got True, want False), react-redux-realworld has_data_layer (got True, want False), struts-examples has_data_layer (got True, want False) |
| has_tests | 90.0% | 20 | microblog has_tests (got True, want False), bugzilla has_tests (got False, want True) |
| license | 71.43% | 14 | microblog license (got None, want mit), eshop-on-web license (got None, want mit), bugzilla license (got None, want lgpl), juice-shop license (got None, want mit) |
| primary_language | 90.0% | 20 | carddemo primary_language (got shell, want cobol), bugzilla primary_language (got javascript, want perl) |
| route | 77.27% | 110 | eshop-on-web /[controller] (got False, want True), eshop-on-web /[controller]/[action] (got False, want True), eshop-on-web /api/[controller]/[action] (got False, want True), ofbiz /*/openapi.* (got False, want True), webgoat /challenge/7 (got False, want True) |
| runtime_version | 63.64% | 11 | spring-petclinic runtime (got None, want java 17), orchard runtime (got None, want net4.8), ofbiz runtime (got None, want java 17), mantisbt runtime (got None, want php 8.1) |
| test_framework | 100.0% | 7 | — |

## Calibration of model confidence

203 fact confidences checked against golden facts: ECE 0.0051 (bootstrap 95th percentile 0.0179). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.9-1.0 | 203 | 0.98 | 0.985 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 18 | 0.944 | 0.833 |
| datastore | 23 | 0.981 | 1.0 |
| entity | 39 | 0.99 | 1.0 |
| framework | 21 | 0.977 | 1.0 |
| license | 10 | 0.988 | 1.0 |
| route | 82 | 0.982 | 1.0 |
| runtime_version | 10 | 0.986 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 18 | 0.944 | 0.9 | 0.99 | 0 |
| P1 A11 risk scores | 60 | 0.941 | 0.76 | 0.99 | 0 |
| P2 A6 dispositions | 20 | 0.774 | 0.58 | 0.92 | 0 |
| P3 A2 boundaries | 114 | 0.952 | 0.85 | 0.99 | 0 |
| P4 A3 task estimates | 117 | 0.851 | 0.62 | 0.93 | 0 |

## Variation with evidence

- P2 dispositions: {'Refactor': 11, 'Retain': 3, 'Replatform': 5, 'Retire': 1}
- P3 decomposition: 16 distinct boundary sets across 16 apps
