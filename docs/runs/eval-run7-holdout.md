# Step 33 eval — `run7-holdout` (`job-1791970992-f5f3cf`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (253/253) | ≥ 95% |
| evidence resolvability | 100.0% (14730/14730) | ≥ 90% |
| hallucinated paths | 0 of 2124 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 450 checked | = 0 |

## Confidence score

**0.0%** — weakest component C3; 6 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 98.5% | schema valid after repair 253/253 (LB 98.5%); evidence ids resolve 14730/14730 (LB 99.97%); cited paths exist 2124/2124 (LB 99.82%); A9 function names exist 450/450 (LB 99.15%) |
| C2 Factual accuracy | 77.38% | golden facts agree 368/453 (LB 77.38%) |
| C3 Claim support | not assessed | claim-support verifier not built (stack PR 6) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 97.71% | 1 - ECE at bootstrap 95%: 146 fact confidences, ECE 0.0146, 95th percentile 0.0229 |
| C7 Execution proof | not assessed | P5 runtime differential NOT_RUN; sandbox deferred (decision 1) |
| C8 Robustness | not assessed | adversarial suite not built (stack PR 8) |
| C9 Human acceptance | not assessed | all reviews were by scripted actors |

## Agreement with golden facts (`evals/golden/facts/`)

453 tool-derived facts over 10 repos; 0 human-reviewed.

| fact type | agreement | n | misses (first 5) |
|---|---|---|---|
| build_manifest | 100.0% | 15 | — |
| capability_route | 80.0% | 10 | spring-framework-petclinic capability_route (got API_ONLY, want UI), cargotracker capability_route (got HEADLESS_BATCH, want UI) |
| ci | 90.0% | 10 | angular-phonecat ci (got False, want True) |
| containerized | 100.0% | 10 | — |
| datastore | 100.0% | 20 | — |
| dependency | 100.0% | 150 | — |
| entity | 57.83% | 83 | saleor CustomSchedule (got False, want True), saleor CustomerEvent (got False, want True), saleor GiftCardTag (got False, want True), saleor Group (got False, want True), saleor InvoiceEvent (got False, want True) |
| framework | 100.0% | 13 | — |
| has_data_layer | 90.0% | 10 | angular-phonecat has_data_layer (got True, want False) |
| has_tests | 100.0% | 10 | — |
| license | 70.0% | 10 | eshop-modernizing license (got None, want mit), angular-phonecat license (got None, want mit), gitea license (got None, want mit) |
| primary_language | 100.0% | 10 | — |
| route | 52.87% | 87 | eshop-modernizing /api (got False, want True), eshop-modernizing /api/[controller] (got False, want True), eshop-modernizing /items/*/pic (got False, want True), saleor /static (got False, want True), djangoproject /.well-known/security.txt (got False, want True) |
| runtime_version | 77.78% | 9 | eshop-modernizing runtime (got None, want net4.7.2), gitea runtime (got None, want go 1.27) |
| test_framework | 100.0% | 6 | — |

## Calibration of model confidence

146 fact confidences checked against golden facts: ECE 0.0146 (bootstrap 95th percentile 0.0229). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.8-0.9 | 1 | 0.8 | 1.0 |
| 0.9-1.0 | 145 | 0.98 | 0.993 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 9 | 0.911 | 0.889 |
| datastore | 20 | 0.982 | 1.0 |
| entity | 43 | 0.989 | 1.0 |
| framework | 13 | 0.977 | 1.0 |
| license | 7 | 0.988 | 1.0 |
| route | 46 | 0.98 | 1.0 |
| runtime_version | 8 | 0.972 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 9 | 0.911 | 0.8 | 0.95 | 0 |
| P1 A11 risk scores | 30 | 0.947 | 0.87 | 0.99 | 0 |
| P2 A6 dispositions | 10 | 0.825 | 0.69 | 0.92 | 0 |
| P3 A2 boundaries | 70 | 0.946 | 0.77 | 0.99 | 0 |
| P4 A3 task estimates | 60 | 0.84 | 0.76 | 0.93 | 0 |

## Variation with evidence

- P2 dispositions: {'Replatform': 1, 'Retain': 1, 'Refactor': 7, 'Retire': 1}
- P3 decomposition: 8 distinct boundary sets across 8 apps
