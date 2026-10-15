# Step 33 eval — `s1-r4` (`job-1791950641-ffb627`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (482/482) | ≥ 95% |
| evidence resolvability | 100.0% (27114/27114) | ≥ 90% |
| hallucinated paths | 0 of 2774 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 650 checked | = 0 |

## Confidence score

**0.0%** — weakest component C3; 6 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 99.21% | schema valid after repair 482/482 (LB 99.21%); evidence ids resolve 27114/27114 (LB 99.99%); cited paths exist 2774/2774 (LB 99.86%); A9 function names exist 650/650 (LB 99.41%) |
| C2 Factual accuracy | 89.29% | golden facts agree 566/617 (LB 89.29%) |
| C3 Claim support | not assessed | claim-support verifier not built (stack PR 6) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | 0.0% | P1 A5 capability route identical across runs 20/20 (LB 83.89%); P2 A6 disposition identical across runs 10/20 (LB 29.93%); P3 A2 boundary Jaccard >= 0.8 0/16 (LB 0.0%); P1 A11 risk score spread <= 1 59/60 (LB 91.14%) |
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
| entity | 97.56% | 41 | django-realworld-example-app TimestampedModel (got False, want True) |
| framework | 100.0% | 23 | — |
| has_data_layer | 80.0% | 20 | sinatra has_data_layer (got True, want False), todomvc has_data_layer (got True, want False), react-redux-realworld has_data_layer (got True, want False), struts-examples has_data_layer (got True, want False) |
| has_tests | 90.0% | 20 | microblog has_tests (got True, want False), bugzilla has_tests (got False, want True) |
| license | 64.29% | 14 | microblog license (got None, want mit), golang-example license (got None, want mit), todomvc license (got None, want mit), eshop-on-web license (got None, want mit), bugzilla license (got None, want lgpl) |
| primary_language | 90.0% | 20 | carddemo primary_language (got shell, want cobol), bugzilla primary_language (got javascript, want perl) |
| route | 76.36% | 110 | eshop-on-web /[controller] (got False, want True), eshop-on-web /[controller]/[action] (got False, want True), eshop-on-web /api/[controller]/[action] (got False, want True), ofbiz /*/openapi.* (got False, want True), webgoat /challenge/7 (got False, want True) |
| runtime_version | 72.73% | 11 | golang-example runtime (got None, want go 1.21), orchard runtime (got None, want net4.8), juice-shop runtime (got None, want node 22) |
| test_framework | 100.0% | 7 | — |

## Variation with evidence

- P2 dispositions: {'Refactor': 10, 'Retain': 4, 'Replatform': 5, 'Retire': 1}
- P3 decomposition: 15 distinct boundary sets across 15 apps
