# Step 33 eval — `run4` (`job-1791780230-52f08d`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (270/270) | ≥ 95% |
| evidence resolvability | 100.0% (14988/14988) | ≥ 90% |
| hallucinated paths | 0 of 860 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 351 checked | = 0 |

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
