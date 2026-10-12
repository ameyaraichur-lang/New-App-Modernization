# Step 33 eval — `run4` (`job-1791780230-52f08d`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (270/270) | ≥ 95% |
| evidence resolvability | 100.0% (14988/14988) | ≥ 90% |
| hallucinated paths | 0 of 860 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 351 checked | = 0 |

## Confidence score

**0.0%** — weakest component C3; 7 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 98.6% | schema valid after repair 270/270 (LB 98.6%); evidence ids resolve 14988/14988 (LB 99.97%); cited paths exist 860/860 (LB 99.56%); A9 function names exist 351/351 (LB 98.92%) |
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

- P2 dispositions: {'Refactor': 5, 'Replatform': 4, 'Retain': 1}
- P3 decomposition: 9 distinct boundary sets across 9 apps
