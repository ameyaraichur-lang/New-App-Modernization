# Step 33 eval — `run9-tune` (`job-1792048590-b4f6f6`)

**Release gate: FAIL**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (516/516) | ≥ 95% |
| evidence resolvability | 100.0% (27149/27149) | ≥ 90% |
| hallucinated paths | 3 of 3051 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 632 checked | = 0 |

## Confidence score

**0.0%** — weakest component C4; 5 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 99.26% | schema valid after repair 516/516 (LB 99.26%); evidence ids resolve 27149/27149 (LB 99.99%); cited paths exist 3048/3051 (LB 99.71%); A9 function names exist 632/632 (LB 99.4%) |
| C2 Factual accuracy | 91.84% | golden facts agree 580/617 (LB 91.84%) |
| C3 Claim support | 56.73% | cited claims entailed by their evidence 2976/5123 (LB 56.73%) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 98.1% | 1 - ECE at bootstrap 95%: 212 fact confidences, ECE 0.0069, 95th percentile 0.019 |
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
| entity | 95.12% | 41 | django-realworld-example-app TimestampedModel (got False, want True), webgoat WebWolfUser (got False, want True) |
| framework | 100.0% | 23 | — |
| has_data_layer | 80.0% | 20 | sinatra has_data_layer (got True, want False), todomvc has_data_layer (got True, want False), react-redux-realworld has_data_layer (got True, want False), struts-examples has_data_layer (got True, want False) |
| has_tests | 90.0% | 20 | microblog has_tests (got True, want False), bugzilla has_tests (got False, want True) |
| license | 100.0% | 14 | — |
| primary_language | 100.0% | 20 | — |
| route | 78.18% | 110 | eshop-on-web /[controller] (got False, want True), eshop-on-web /[controller]/[action] (got False, want True), eshop-on-web /api/[controller]/[action] (got False, want True), ofbiz /*/openapi.* (got False, want True), webgoat /challenge/7 (got False, want True) |
| runtime_version | 100.0% | 11 | — |
| test_framework | 100.0% | 7 | — |

## Claim support (`appmod/agents/verifier.py`)

5123 cited OBSERVED/DOCUMENTED model claims. NOT_ENTAILED and INSUFFICIENT were published as INFERRED. UNCHECKED: no checkable text behind the ids or no verdict; NO_RECORD: published without a verifier verdict.

| verdict | claims | share |
|---|---|---|
| ENTAILED | 2976 | 58.09% |
| INSUFFICIENT | 1729 | 33.75% |
| NOT_ENTAILED | 418 | 8.16% |

Human audit sample: 233 claims (`verifier-audit-<label>.jsonl`).

## Calibration of model confidence

212 fact confidences checked against golden facts: ECE 0.0069 (bootstrap 95th percentile 0.019). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.9-1.0 | 212 | 0.979 | 0.986 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 19 | 0.939 | 0.842 |
| datastore | 23 | 0.981 | 1.0 |
| entity | 39 | 0.991 | 1.0 |
| framework | 23 | 0.977 | 1.0 |
| license | 14 | 0.988 | 1.0 |
| route | 84 | 0.981 | 1.0 |
| runtime_version | 10 | 0.972 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 19 | 0.939 | 0.9 | 0.95 | 0 |
| P1 A11 risk scores | 60 | 0.934 | 0.75 | 0.99 | 0 |
| P2 A6 dispositions | 20 | 0.817 | 0.75 | 0.93 | 0 |
| P3 A2 boundaries | 118 | 0.949 | 0.84 | 0.98 | 0 |
| P4 A3 task estimates | 126 | 0.836 | 0.7 | 0.94 | 0 |

## Variation with evidence

- P2 dispositions: {'Refactor': 10, 'Retain': 3, 'Replatform': 7}
- P3 decomposition: 17 distinct boundary sets across 17 apps

## Hallucinated paths

- `{"artifact": "P1/flask-tutorial/A1", "path": "auth.py/blog.py/db.py"}`
- `{"artifact": "P1/microblog/A3", "path": "migrations/script.py"}`
- `{"artifact": "P3/laravel58/A1", "path": "package.json/composer.json"}`
