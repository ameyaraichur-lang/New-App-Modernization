# Step 33 eval — `run5-facts` (`job-1791792319-d40469`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (253/253) | ≥ 95% |
| evidence resolvability | 100.0% (14169/14169) | ≥ 90% |
| hallucinated paths | 0 of 888 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 370 checked | = 0 |

## Confidence score

**0.0%** — weakest component C3; 7 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 98.5% | schema valid after repair 253/253 (LB 98.5%); evidence ids resolve 14169/14169 (LB 99.97%); cited paths exist 888/888 (LB 99.57%); A9 function names exist 370/370 (LB 98.97%) |
| C2 Factual accuracy | 94.24% | golden facts agree 304/314 (LB 94.24%) |
| C3 Claim support | not assessed | claim-support verifier not built (stack PR 6) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no repeated runs (stack PR 4) |
| C6 Calibration | not assessed | no confidence field on decisions (stack PR 5) |
| C7 Execution proof | not assessed | P5 runtime differential NOT_RUN; sandbox deferred (decision 1) |
| C8 Robustness | not assessed | adversarial suite not built (stack PR 8) |
| C9 Human acceptance | not assessed | all reviews were by scripted actors |

## Agreement with golden facts (`evals/golden/facts/`)

314 tool-derived facts over 10 repos; 0 human-reviewed.

| fact type | agreement | n | misses (first 5) |
|---|---|---|---|
| build_manifest | 100.0% | 13 | — |
| capability_route | 90.0% | 10 | golang-example capability_route (got HEADLESS_BATCH, want API_ONLY) |
| ci | 80.0% | 10 | musicstore ci (got False, want True), todomvc ci (got False, want True) |
| containerized | 100.0% | 10 | — |
| datastore | 100.0% | 9 | — |
| dependency | 100.0% | 123 | — |
| entity | 95.83% | 24 | django-realworld-example-app TimestampedModel (got False, want True) |
| framework | 100.0% | 15 | — |
| has_data_layer | 70.0% | 10 | sinatra has_data_layer (got True, want False), todomvc has_data_layer (got True, want False), react-redux-realworld has_data_layer (got True, want False) |
| has_tests | 100.0% | 10 | — |
| license | 66.67% | 6 | golang-example license (got None, want mit), todomvc license (got None, want mit) |
| primary_language | 100.0% | 10 | — |
| route | 100.0% | 56 | — |
| runtime_version | 80.0% | 5 | golang-example runtime (got None, want go 1.21) |
| test_framework | 100.0% | 3 | — |

## Variation with evidence

- P2 dispositions: {'Refactor': 4, 'Replatform': 4, 'Retain': 2}
- P3 decomposition: 8 distinct boundary sets across 8 apps
