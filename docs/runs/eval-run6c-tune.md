# Step 33 eval — `run6c-tune` (`job-1791800144-cd8327`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (414/414) | ≥ 95% |
| evidence resolvability | 100.0% (23641/23641) | ≥ 90% |
| hallucinated paths | 0 of 2786 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 659 checked | = 0 |

## Confidence score

**0.0%** — weakest component C3; 7 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 99.08% | schema valid after repair 414/414 (LB 99.08%); evidence ids resolve 23641/23641 (LB 99.98%); cited paths exist 2786/2786 (LB 99.86%); A9 function names exist 659/659 (LB 99.42%) |
| C2 Factual accuracy | 89.66% | golden facts agree 568/617 (LB 89.66%) |
| C3 Claim support | not assessed | claim-support verifier not built (stack PR 6) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no repeated runs (stack PR 4) |
| C6 Calibration | not assessed | no confidence field on decisions (stack PR 5) |
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
| entity | 95.12% | 41 | django-realworld-example-app TimestampedModel (got False, want True), webgoat WebWolfUser (got False, want True) |
| framework | 100.0% | 23 | — |
| has_data_layer | 80.0% | 20 | sinatra has_data_layer (got True, want False), todomvc has_data_layer (got True, want False), react-redux-realworld has_data_layer (got True, want False), struts-examples has_data_layer (got True, want False) |
| has_tests | 90.0% | 20 | microblog has_tests (got True, want False), bugzilla has_tests (got False, want True) |
| license | 64.29% | 14 | microblog license (got None, want mit), golang-example license (got None, want mit), todomvc license (got None, want mit), eshop-on-web license (got None, want mit), juice-shop license (got None, want mit) |
| primary_language | 90.0% | 20 | carddemo primary_language (got shell, want cobol), bugzilla primary_language (got javascript, want perl) |
| route | 80.0% | 110 | eshop-on-web /[controller] (got False, want True), eshop-on-web /[controller]/[action] (got False, want True), eshop-on-web /api/[controller]/[action] (got False, want True), ofbiz /*/openapi.* (got False, want True), webgoat /challenge/7 (got False, want True) |
| runtime_version | 63.64% | 11 | golang-example runtime (got None, want go 1.21), orchard runtime (got None, want net4.8), mantisbt runtime (got None, want php 8.1), juice-shop runtime (got None, want node 22) |
| test_framework | 100.0% | 7 | — |

## Variation with evidence

- P2 dispositions: {'Retain': 9, 'Retire': 1, 'Replatform': 7, 'Refactor': 3}
- P3 decomposition: 11 distinct boundary sets across 11 apps
