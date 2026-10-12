# Step 33 eval — `run5` (`job-1791792319-d40469`)

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
| C2 Factual accuracy | 86.82% | golden facts agree 38/39 (LB 86.82%) |
| C3 Claim support | not assessed | claim-support verifier not built (stack PR 6) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no repeated runs (stack PR 4) |
| C6 Calibration | not assessed | no confidence field on decisions (stack PR 5) |
| C7 Execution proof | not assessed | P5 runtime differential NOT_RUN; sandbox deferred (decision 1) |
| C8 Robustness | not assessed | adversarial suite not built (stack PR 8) |
| C9 Human acceptance | not assessed | all reviews were by scripted actors |

## Agreement with golden labels (`evals/golden/corpus.json`)

| fact | agreement | misses |
|---|---|---|
| primary_language | 100.0% | — |
| framework | 100.0% | — |
| has_tests | 100.0% | — |
| has_data_layer | 90.0% | todomvc (got True, want False) |

## Variation with evidence

- P2 dispositions: {'Refactor': 4, 'Replatform': 4, 'Retain': 2}
- P3 decomposition: 8 distinct boundary sets across 8 apps
