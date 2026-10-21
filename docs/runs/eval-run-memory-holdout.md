# Step 33 eval — `run-memory-holdout` (`job-1792386159-a4933c`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (219/219) | ≥ 95% |
| evidence resolvability | 100.0% (11721/11721) | ≥ 90% |
| hallucinated paths | 0 of 2300 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 428 checked | = 0 |

## Confidence score

**0.0%** — weakest component C4; 4 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 98.28% | schema valid after repair 219/219 (LB 98.28%); evidence ids resolve 11721/11721 (LB 99.97%); cited paths exist 2300/2300 (LB 99.83%); A9 function names exist 428/428 (LB 99.11%) |
| C2 Factual accuracy | 79.27% | golden facts agree 376/453 (LB 79.27%) |
| C3 Claim support | 58.49% | cited claims entailed by their evidence 1472/2435 (LB 58.49%) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 97.93% | 1 - ECE at bootstrap 95%: 153 fact confidences, ECE 0.013, 95th percentile 0.0207 |
| C7 Execution proof | not assessed | P5 runtime differential NOT_RUN; sandbox deferred (decision 1) |
| C8 Robustness | 94.42% | adversarial cases pass 65/65 (LB 94.42%) |
| C9 Human acceptance | not assessed | all reviews were by scripted actors |

## Agreement with golden facts (`evals/golden/facts/`)

453 tool-derived facts over 10 repos; 0 human-reviewed.

| fact type | agreement | n | misses (first 5) |
|---|---|---|---|
| build_manifest | 100.0% | 15 | — |
| capability_route | 80.0% | 10 | spring-framework-petclinic capability_route (got API_ONLY, want UI), cargotracker capability_route (got HEADLESS_BATCH, want UI) |
| ci | 100.0% | 10 | — |
| containerized | 100.0% | 10 | — |
| datastore | 100.0% | 20 | — |
| dependency | 100.0% | 150 | — |
| entity | 62.65% | 83 | saleor CustomSchedule (got False, want True), saleor CustomerEvent (got False, want True), saleor GiftCardTag (got False, want True), saleor Group (got False, want True), saleor InvoiceEvent (got False, want True) |
| framework | 100.0% | 13 | — |
| has_data_layer | 90.0% | 10 | angular-phonecat has_data_layer (got True, want False) |
| has_tests | 100.0% | 10 | — |
| license | 100.0% | 10 | — |
| primary_language | 100.0% | 10 | — |
| route | 50.57% | 87 | eshop-modernizing /api (got False, want True), eshop-modernizing /api/[controller] (got False, want True), eshop-modernizing /items/*/pic (got False, want True), eshop-modernizing /uploadimage (got False, want True), saleor /static (got False, want True) |
| runtime_version | 100.0% | 9 | — |
| test_framework | 100.0% | 6 | — |

## Assurance of released items (`appmod/kernel/assurance.py`)

4675 items released through 23 G2 gates: coverage 100.0%, of which 37.93% without scripted confirmation (tool-measured, entailed or human-confirmed).

| class | items | share |
|---|---|---|
| tool-measured | 301 | 6.44% |
| entailed | 1472 | 31.49% |
| scripted-confirmed | 2902 | 62.07% |

## Evidence mix (model items: OBSERVED + DOCUMENTED share)

| phase | share | observed+documented | total |
|---|---|---|---|
| P1 | 51.32% | 1184 | 2307 |
| P2 | 15.15% | 20 | 132 |
| P3 | 13.63% | 170 | 1247 |
| P4 | 16.1% | 99 | 615 |

## Claim support (`appmod/agents/verifier.py`)

2435 cited OBSERVED/DOCUMENTED model claims. NOT_ENTAILED and INSUFFICIENT were published as INFERRED. UNCHECKED: no checkable text behind the ids or no verdict; NO_RECORD: published without a verifier verdict.

| verdict | claims | share |
|---|---|---|
| ENTAILED | 1472 | 60.45% |
| INSUFFICIENT | 882 | 36.22% |
| NOT_ENTAILED | 80 | 3.29% |
| UNCHECKED | 1 | 0.04% |

Human audit sample: 112 claims (`verifier-audit-<label>.jsonl`).

## Calibration of model confidence

153 fact confidences checked against golden facts: ECE 0.013 (bootstrap 95th percentile 0.0207). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.9-1.0 | 153 | 0.981 | 0.993 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 9 | 0.933 | 0.889 |
| datastore | 20 | 0.978 | 1.0 |
| entity | 49 | 0.99 | 1.0 |
| framework | 13 | 0.98 | 1.0 |
| license | 10 | 0.988 | 1.0 |
| route | 44 | 0.981 | 1.0 |
| runtime_version | 8 | 0.968 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 9 | 0.933 | 0.9 | 1.0 | 0 |
| P1 A11 risk scores | 30 | 0.939 | 0.83 | 0.99 | 0 |
| P2 A6 dispositions | 10 | 0.795 | 0.66 | 0.88 | 0 |
| P3 A2 boundaries | 54 | 0.942 | 0.85 | 0.98 | 0 |
| P4 A3 task estimates | 43 | 0.812 | 0.72 | 0.89 | 0 |

## Variation with evidence

- P2 dispositions: {'Retire': 2, 'Retain': 2, 'Refactor': 5, 'Replatform': 1}
- P3 decomposition: 6 distinct boundary sets across 6 apps
