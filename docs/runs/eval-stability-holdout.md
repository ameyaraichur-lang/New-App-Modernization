# Step 33 eval — `stability-holdout` (`job-1792176354-be3f2b`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (253/253) | ≥ 95% |
| evidence resolvability | 100.0% (14899/14899) | ≥ 90% |
| hallucinated paths | 0 of 2130 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 432 checked | = 0 |

## Confidence score

**0.0%** — weakest component C3; 7 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 98.5% | schema valid after repair 253/253 (LB 98.5%); evidence ids resolve 14899/14899 (LB 99.97%); cited paths exist 2130/2130 (LB 99.82%); A9 function names exist 432/432 (LB 99.12%) |
| C2 Factual accuracy | 77.15% | golden facts agree 367/453 (LB 77.15%) |
| C3 Claim support | not assessed | claim-support verifier not built (stack PR 6) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | not assessed | no confidence field on decisions (stack PR 5) |
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
| license | 60.0% | 10 | eshop-modernizing license (got None, want mit), angular-phonecat license (got None, want mit), human-essentials license (got None, want mit), gitea license (got None, want mit) |
| primary_language | 100.0% | 10 | — |
| route | 54.02% | 87 | eshop-modernizing /api/[controller] (got False, want True), eshop-modernizing /items/*/pic (got False, want True), saleor /static (got False, want True), djangoproject /.well-known/security.txt (got False, want True), djangoproject /403 (got False, want True) |
| runtime_version | 66.67% | 9 | eshop-modernizing runtime (got None, want net4.7.2), opencart runtime (got None, want php 8.0), gitea runtime (got None, want go 1.27) |
| test_framework | 100.0% | 6 | — |

## Variation with evidence

- P2 dispositions: {'Replatform': 2, 'Retain': 1, 'Refactor': 6, 'Retire': 1}
- P3 decomposition: 8 distinct boundary sets across 8 apps
