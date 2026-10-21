# Step 33 eval — `run-stakeholder-tune` (`job-1792395473-494e4a`)

**Release gate: PASS**

| metric | value | threshold |
|---|---|---|
| schema-valid after repair | 100.0% (105/105) | ≥ 95% |
| evidence resolvability | 99.28% (5621/5662) | ≥ 90% |
| hallucinated paths | 0 of 943 checked | = 0 |
| hallucinated symbols (A9 functions) | 0 of 334 checked | = 0 |

## Confidence score

**0.0%** — weakest component C4; 4 of 9 components not assessed (each counts as 0). Every value is a 95% Wilson lower bound.

| component | lower bound | basis |
|---|---|---|
| C1 Integrity | 96.47% | schema valid after repair 105/105 (LB 96.47%); evidence ids resolve 5621/5662 (LB 99.02%); cited paths exist 943/943 (LB 99.59%); A9 function names exist 334/334 (LB 98.86%) |
| C2 Factual accuracy | 51.0% | golden facts agree 339/617 (LB 51.0%) |
| C3 Claim support | 70.08% | cited claims entailed by their evidence 1133/1566 (LB 70.08%) |
| C4 Decision correctness | not assessed | no expert decision labels (decision 2: skipped) |
| C5 Stability | not assessed | no stability report given (scripts/stability_run.py) |
| C6 Calibration | 97.51% | 1 - ECE at bootstrap 95%: 141 fact confidences, ECE 0.0226, 95th percentile 0.0249 |
| C7 Execution proof | not assessed | P5 runtime differential NOT_RUN; sandbox deferred (decision 1) |
| C8 Robustness | 94.42% | adversarial cases pass 65/65 (LB 94.42%) |
| C9 Human acceptance | not assessed | all reviews were by scripted actors |

## Agreement with golden facts (`evals/golden/facts/`)

617 tool-derived facts over 20 repos; 0 human-reviewed.

| fact type | agreement | n | misses (first 5) |
|---|---|---|---|
| build_manifest | 52.0% | 25 | react-redux-realworld package.json (got False, want True), eshop-on-web *.csproj (got False, want True), orchard package.json (got False, want True), orchard *.csproj (got False, want True), struts-examples pom.xml (got False, want True) |
| capability_route | 50.0% | 20 | react-redux-realworld capability_route (got None, want UI), eshop-on-web capability_route (got None, want UI), orchard capability_route (got None, want UI), struts-examples capability_route (got None, want UI), ofbiz capability_route (got None, want UI) |
| ci | 60.0% | 20 | eshop-on-web ci (got False, want True), orchard ci (got False, want True), struts-examples ci (got False, want True), ofbiz ci (got False, want True), webgoat ci (got False, want True) |
| containerized | 70.0% | 20 | eshop-on-web containerized (got False, want True), ofbiz containerized (got False, want True), webgoat containerized (got False, want True), mantisbt containerized (got False, want True), bugzilla containerized (got False, want True) |
| datastore | 45.83% | 24 | eshop-on-web sqlserver (got False, want True), orchard mysql (got False, want True), orchard postgresql (got False, want True), orchard redis (got False, want True), ofbiz postgresql (got False, want True) |
| dependency | 50.83% | 242 | react-redux-realworld cross-env (got False, want True), react-redux-realworld history (got False, want True), react-redux-realworld marked (got False, want True), react-redux-realworld react (got False, want True), react-redux-realworld react-dom (got False, want True) |
| entity | 60.98% | 41 | spring-petclinic PetType (got False, want True), django-realworld-example-app TimestampedModel (got False, want True), eshop-on-web Basket (got False, want True), eshop-on-web BasketItem (got False, want True), eshop-on-web CatalogBrand (got False, want True) |
| framework | 65.22% | 23 | react-redux-realworld react (got None, want react), eshop-on-web aspnetcore (got None, want microsoft.aspnetcore.mvc.testing), eshop-on-web entity-framework (got None, want microsoft.entityframeworkcore.inmemory), orchard aspnet-mvc (got None, want microsoft.aspnet.mvc), struts-examples struts2 (got None, want org.apache.struts:struts2-core) |
| has_data_layer | 50.0% | 20 | sinatra has_data_layer (got True, want False), todomvc has_data_layer (got True, want False), eshop-on-web has_data_layer (got False, want True), orchard has_data_layer (got False, want True), ofbiz has_data_layer (got False, want True) |
| has_tests | 55.0% | 20 | microblog has_tests (got True, want False), eshop-on-web has_tests (got False, want True), orchard has_tests (got False, want True), struts-examples has_tests (got False, want True), ofbiz has_tests (got False, want True) |
| license | 42.86% | 14 | react-redux-realworld license (got None, want mit), eshop-on-web license (got None, want mit), orchard license (got None, want bsd), ofbiz license (got None, want apache), webgoat license (got None, want gpl) |
| primary_language | 50.0% | 20 | react-redux-realworld primary_language (got None, want javascript), eshop-on-web primary_language (got None, want csharp), orchard primary_language (got None, want csharp), struts-examples primary_language (got None, want java), ofbiz primary_language (got None, want java) |
| route | 64.55% | 110 | eshop-on-web /[controller] (got False, want True), eshop-on-web /[controller]/[action] (got False, want True), eshop-on-web /api/[controller]/[action] (got False, want True), eshop-on-web /api/authenticate (got False, want True), eshop-on-web /logout (got False, want True) |
| runtime_version | 45.45% | 11 | orchard runtime (got None, want net4.8), struts-examples runtime (got None, want java 17), ofbiz runtime (got None, want java 17), webgoat runtime (got None, want java 25), mantisbt runtime (got None, want php 8.1) |
| test_framework | 42.86% | 7 | eshop-on-web mstest.testadapter (got False, want True), orchard nunit (got False, want True), struts-examples junit:junit (got False, want True), mantisbt phpunit/phpunit (got False, want True) |

## Assurance of released items (`appmod/kernel/assurance.py`)

2158 items released through 8 G2 gates: coverage 100.0%, of which 50.6% without scripted confirmation (tool-measured, entailed or human-confirmed).

| class | items | share |
|---|---|---|
| tool-measured | 154 | 7.14% |
| entailed | 938 | 43.47% |
| scripted-confirmed | 1066 | 49.4% |

## Evidence mix (model items: OBSERVED + DOCUMENTED share)

| phase | share | observed+documented | total |
|---|---|---|---|
| P1 | 53.47% | 1133 | 2119 |
| P2 | 100.0% | 0 | 0 |
| P3 | 100.0% | 0 | 0 |
| P4 | 100.0% | 0 | 0 |

## Claim support (`appmod/agents/verifier.py`)

1566 cited OBSERVED/DOCUMENTED model claims. NOT_ENTAILED and INSUFFICIENT were published as INFERRED. UNCHECKED: no checkable text behind the ids or no verdict; NO_RECORD: published without a verifier verdict.

| verdict | claims | share |
|---|---|---|
| ENTAILED | 1133 | 72.35% |
| INSUFFICIENT | 419 | 26.76% |
| NOT_ENTAILED | 14 | 0.89% |

Human audit sample: 75 claims (`verifier-audit-<label>.jsonl`).

## Calibration of model confidence

141 fact confidences checked against golden facts: ECE 0.0226 (bootstrap 95th percentile 0.0249). Only facts a model item states are checkable, so wrong items that contradict a tool fact are not counted yet.

| confidence | n | mean confidence | accuracy |
|---|---|---|---|
| 0.9-1.0 | 141 | 0.977 | 1.0 |

| fact type | n | mean confidence | accuracy |
|---|---|---|---|
| capability_route | 10 | 0.94 | 1.0 |
| datastore | 11 | 0.982 | 1.0 |
| entity | 25 | 0.99 | 1.0 |
| framework | 15 | 0.98 | 1.0 |
| license | 5 | 0.99 | 1.0 |
| route | 70 | 0.976 | 1.0 |
| runtime_version | 5 | 0.979 | 1.0 |

Decision confidence (uncalibrated: no labels exist for these decisions):

| decision | n | mean | min | max | items without confidence |
|---|---|---|---|---|---|
| P1 A5 capability route review | 10 | 0.94 | 0.9 | 0.95 | 0 |
| P1 A11 risk scores | 24 | 0.937 | 0.82 | 0.99 | 0 |
| P2 A6 dispositions | 0 | None | None | None | 0 |
| P3 A2 boundaries | 0 | None | None | None | 0 |
| P4 A3 task estimates | 0 | None | None | None | 0 |

## Variation with evidence

- P2 dispositions: {}
- P3 decomposition: 0 distinct boundary sets across 0 apps

## Unresolved evidence ids (sample)

- `{"artifact": "P1/spring-petclinic/A8", "id": "human:q-78138674ac"}`
- `{"artifact": "P1/spring-petclinic/A8", "id": "human:q-71558910aa"}`
- `{"artifact": "P1/spring-petclinic/A9", "id": "human:q-65b917d55a"}`
- `{"artifact": "P1/spring-petclinic/A9", "id": "human:q-84f608ed5b"}`
- `{"artifact": "P1/spring-petclinic/A11", "id": "human:q-2e3b1cd71d"}`
- `{"artifact": "P1/spring-petclinic/A11", "id": "human:q-09e63f5eee"}`
- `{"artifact": "P1/spring-petclinic/A11", "id": "human:q-09e63f5eee"}`
- `{"artifact": "P1/flask-tutorial/A6", "id": "human:q-4fb82e8b57"}`
- `{"artifact": "P1/flask-tutorial/A6", "id": "human:q-bff6321003"}`
- `{"artifact": "P1/flask-tutorial/A9", "id": "human:q-612ab3ff8a"}`
- `{"artifact": "P1/flask-tutorial/A9", "id": "human:q-a3d4329f6f"}`
- `{"artifact": "P1/flask-tutorial/A9", "id": "human:q-612ab3ff8a"}`
- `{"artifact": "P1/django-realworld-example-app/A9", "id": "human:q-e23567b83a"}`
- `{"artifact": "P1/musicstore/A8", "id": "human:q-08f6f8672b"}`
- `{"artifact": "P1/musicstore/A8", "id": "human:q-68220e3001"}`
- `{"artifact": "P1/musicstore/A9", "id": "human:q-3a23907e17"}`
- `{"artifact": "P1/musicstore/A9", "id": "human:q-7dc4cc0f16"}`
- `{"artifact": "P1/laravel58/A6", "id": "human:q-6c4bf3004a"}`
- `{"artifact": "P1/laravel58/A6", "id": "human:q-e0fcf811e9"}`
- `{"artifact": "P1/laravel58/A8", "id": "human:q-2d0f8fb7bd"}`
- `{"artifact": "P1/laravel58/A8", "id": "human:q-359274fc44"}`
- `{"artifact": "P1/laravel58/A8", "id": "human:q-f2283d3e97"}`
- `{"artifact": "P1/laravel58/A9", "id": "human:q-66461c39ea"}`
- `{"artifact": "P1/laravel58/A9", "id": "human:q-0f1e87b358"}`
- `{"artifact": "P1/sinatra/A3", "id": "human:q-77ad2ef6ec"}`
- `{"artifact": "P1/sinatra/A3", "id": "human:q-376ae10219"}`
- `{"artifact": "P1/sinatra/A6", "id": "human:q-59e5eaff0e"}`
- `{"artifact": "P1/sinatra/A6", "id": "human:q-72b10556ca"}`
- `{"artifact": "P1/sinatra/A9", "id": "human:q-79cd2c5906"}`
- `{"artifact": "P1/sinatra/A9", "id": "human:q-f34f08e992"}`
- `{"artifact": "P1/sinatra/A10", "id": "human:q-4112b0ab42"}`
- `{"artifact": "P1/sinatra/A10", "id": "human:q-4112b0ab42"}`
- `{"artifact": "P1/golang-example/A9", "id": "human:q-87b5858679"}`
- `{"artifact": "P1/golang-example/A9", "id": "human:q-c6370ee6ea"}`
- `{"artifact": "P1/golang-example/A9", "id": "human:q-2aa4ee1e48"}`
- `{"artifact": "P1/todomvc/A6", "id": "human:q-2208c85b96"}`
- `{"artifact": "P1/todomvc/A6", "id": "human:q-86f8a7085c"}`
- `{"artifact": "P1/todomvc/A6", "id": "human:q-bcfa9fa1cb"}`
- `{"artifact": "P1/todomvc/A9", "id": "human:q-10cbe4c778"}`
- `{"artifact": "P1/todomvc/A9", "id": "human:q-e0ee93ee9a"}`
