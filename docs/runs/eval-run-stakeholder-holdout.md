# Step 33 eval — `run-stakeholder-holdout` (`job-1792401717-7d7e76`)

**Release gate: FAIL**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (202/202) | ≥ 95% |
| evidence resolvability | 99.11% (11105/11205) | ≥ 90% |
| hallucinated paths | 3 of 2323 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 398 checked | = 0 |

## Confidence score

**0.0%** — weakest component C4; 4 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 98.13% | schema valid after repair 202/202 (LB 98.13%); evidence ids resolve 11105/11205 (LB 98.92%); cited paths exist 2320/2323 (LB 99.62%); A9 function names exist 398/398 (LB 99.04%) |
| C2 Factual accuracy | 79.51% | golden facts agree 377/453 (LB 79.51%) |
| C3 Claim support | 59.18% | cited claims entailed by their evidence 1494/2444 (LB 59.18%) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 97.86% | 1 - ECE at bootstrap 95%: 150 fact confidences, ECE 0.0137, 95th percentile 0.0214 |
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
| entity | 61.45% | 83 | saleor CheckoutDelivery (got False, want True), saleor CustomSchedule (got False, want True), saleor CustomerEvent (got False, want True), saleor GiftCardTag (got False, want True), saleor Group (got False, want True) |
| framework | 100.0% | 13 | — |
| has_data_layer | 90.0% | 10 | angular-phonecat has_data_layer (got True, want False) |
| has_tests | 100.0% | 10 | — |
| license | 100.0% | 10 | — |
| primary_language | 100.0% | 10 | — |
| route | 52.87% | 87 | eshop-modernizing /api (got False, want True), eshop-modernizing /api/[controller] (got False, want True), eshop-modernizing /items/*/pic (got False, want True), saleor /static (got False, want True), djangoproject /.well-known/security.txt (got False, want True) |
| runtime_version | 100.0% | 9 | — |
| test_framework | 100.0% | 6 | — |

## Assurance of released items (`appmod/kernel/assurance.py`)

4680 items released through 21 G2 gates: coverage 100.0%, of which 38.01% without scripted confirmation (tool-measured, entailed or human-confirmed).

| class | items | share |
|---|---|---|
| tool-measured | 285 | 6.09% |
| entailed | 1494 | 31.92% |
| scripted-confirmed | 2901 | 61.99% |

## Evidence mix (model items: OBSERVED + DOCUMENTED share)

| phase | share | observed+documented | total |
|---|---|---|---|
| P1 | 51.4% | 1214 | 2362 |
| P2 | 14.93% | 20 | 134 |
| P3 | 13.45% | 145 | 1078 |
| P4 | 22.37% | 115 | 514 |

## Claim support (`appmod/agents/verifier.py`)

2444 cited OBSERVED/DOCUMENTED model claims. NOT_ENTAILED and INSUFFICIENT were published as INFERRED. UNCHECKED: no checkable text behind the ids or no verdict; NO_RECORD: published without a verifier verdict.

| verdict | claims | share |
|---|---|---|
| ENTAILED | 1494 | 61.13% |
| INSUFFICIENT | 830 | 33.96% |
| NOT_ENTAILED | 120 | 4.91% |

Human audit sample: 131 claims (`verifier-audit-<label>.jsonl`).

## Calibration of model confidence

150 fact confidences checked against golden facts: ECE 0.0137 (bootstrap 95th percentile 0.0214). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.9-1.0 | 150 | 0.98 | 0.993 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 9 | 0.922 | 0.889 |
| datastore | 20 | 0.981 | 1.0 |
| entity | 45 | 0.99 | 1.0 |
| framework | 13 | 0.979 | 1.0 |
| license | 9 | 0.989 | 1.0 |
| route | 46 | 0.98 | 1.0 |
| runtime_version | 8 | 0.971 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 9 | 0.922 | 0.9 | 0.95 | 0 |
| P1 A11 risk scores | 30 | 0.948 | 0.85 | 0.99 | 0 |
| P2 A6 dispositions | 10 | 0.78 | 0.7 | 0.82 | 0 |
| P3 A2 boundaries | 43 | 0.934 | 0.86 | 0.98 | 0 |
| P4 A3 task estimates | 38 | 0.83 | 0.68 | 0.91 | 0 |

## Variation with evidence

- P2 dispositions: {'Retain': 5, 'Refactor': 5}
- P3 decomposition: 5 distinct boundary sets across 5 apps

## Unresolved evidence ids (sample)

- `{"artifact": "P1/eshop-modernizing/A6", "id": "human:q-e0ffb387cc"}`
- `{"artifact": "P1/eshop-modernizing/A6", "id": "human:q-5270ebbe3f"}`
- `{"artifact": "P1/eshop-modernizing/A8", "id": "human:q-45b1952d7a"}`
- `{"artifact": "P1/eshop-modernizing/A8", "id": "human:q-036cf7b1af"}`
- `{"artifact": "P1/eshop-modernizing/A9", "id": "human:q-6e7b1bbe65"}`
- `{"artifact": "P1/eshop-modernizing/A9", "id": "human:q-2241e4c54e"}`
- `{"artifact": "P1/eshop-modernizing/A11", "id": "human:q-06aa9f6171"}`
- `{"artifact": "P1/eshop-modernizing/A11", "id": "human:q-e0ee0cf6c4"}`
- `{"artifact": "P1/spring-framework-petclinic/A6", "id": "human:q-f00c00034f"}`
- `{"artifact": "P1/spring-framework-petclinic/A6", "id": "human:q-2f95160f44"}`
- `{"artifact": "P1/spring-framework-petclinic/A8", "id": "human:q-56a4f370f5"}`
- `{"artifact": "P1/spring-framework-petclinic/A8", "id": "human:q-b05fdd58fa"}`
- `{"artifact": "P1/spring-framework-petclinic/A8", "id": "human:q-b05fdd58fa"}`
- `{"artifact": "P1/spring-framework-petclinic/A8", "id": "human:q-e88a71dc29"}`
- `{"artifact": "P1/spring-framework-petclinic/A8", "id": "human:q-80ee849619"}`
- `{"artifact": "P1/spring-framework-petclinic/A8", "id": "human:q-393eef5367"}`
- `{"artifact": "P1/spring-framework-petclinic/A9", "id": "human:q-2e8fc713d9"}`
- `{"artifact": "P1/spring-framework-petclinic/A9", "id": "human:q-00f53cd1d4"}`
- `{"artifact": "P1/spring-framework-petclinic/A9", "id": "human:q-bd6800690f"}`
- `{"artifact": "P1/spring-framework-petclinic/A9", "id": "human:q-2e8fc713d9"}`
- `{"artifact": "P1/spring-framework-petclinic/A9", "id": "human:q-00f53cd1d4"}`
- `{"artifact": "P1/cargotracker/A6", "id": "human:q-06fd9110ca"}`
- `{"artifact": "P1/cargotracker/A6", "id": "human:q-7d19941865"}`
- `{"artifact": "P1/cargotracker/A8", "id": "human:q-0fff1f456b"}`
- `{"artifact": "P1/cargotracker/A8", "id": "human:q-b2e83a6dd2"}`
- `{"artifact": "P1/cargotracker/A8", "id": "human:q-0fff1f456b"}`
- `{"artifact": "P1/cargotracker/A8", "id": "human:q-b2e83a6dd2"}`
- `{"artifact": "P1/cargotracker/A9", "id": "human:q-4ddd87af67"}`
- `{"artifact": "P1/cargotracker/A9", "id": "human:q-4120394aa3"}`
- `{"artifact": "P1/cargotracker/A11", "id": "human:q-80044ce9bf"}`
- `{"artifact": "P1/cargotracker/A11", "id": "human:q-96a838824b"}`
- `{"artifact": "P1/cargotracker/A11", "id": "human:q-80044ce9bf"}`
- `{"artifact": "P1/cargotracker/A11", "id": "human:q-96a838824b"}`
- `{"artifact": "P1/jhipster-sample-app/A9", "id": "human:q-193a211168"}`
- `{"artifact": "P1/jhipster-sample-app/A9", "id": "human:q-ed3547fc6d"}`
- `{"artifact": "P1/jhipster-sample-app/A11", "id": "human:q-416d82e6d2"}`
- `{"artifact": "P1/jhipster-sample-app/A11", "id": "human:q-416d82e6d2"}`
- `{"artifact": "P1/jhipster-sample-app/A11", "id": "human:q-416d82e6d2"}`
- `{"artifact": "P1/saleor/A6", "id": "human:q-aeb51cd730"}`
- `{"artifact": "P1/saleor/A6", "id": "human:q-c3fd28d0b7"}`

## Hallucinated paths

- `{"artifact": "P1/gitea/A6", "path": "tests/pgsql.ini"}`
- `{"artifact": "P1/gitea/A6", "path": "tests/mssql.ini"}`
- `{"artifact": "P1/gitea/A6", "path": "tests/mysql.ini"}`
