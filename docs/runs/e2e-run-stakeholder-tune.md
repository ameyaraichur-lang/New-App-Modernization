# E2E agentic acceptance run `run-stakeholder-tune`

- **Job**: `job-1792395473-494e4a` — **FAILED** (error: `AttributeError: partially initialized module 'httpx' has no attribute 'Response' (most likely due to a circular import)`)
- **Repositories**: `spring-petclinic`, `flask-tutorial`, `django-realworld-example-app`, `microblog`, `node-express-realworld-example-app`, `musicstore`, `laravel58`, `sinatra`, `golang-example`, `todomvc`, `react-redux-realworld`, `eshop-on-web`, `orchard`, `struts-examples`, `ofbiz`, `webgoat`, `carddemo`, `mantisbt`, `bugzilla`, `juice-shop`
- **Elapsed**: 104 min 18 s; LLM cache mode `record` (record = every call live, responses recorded for replay)
- **Astra tiers**: {'reasoning': 'gpt-6-astra', 'coding': 'gpt-5.3-codex-PlayWright', 'fast': 'gpt-4.1-mini', 'fallback': 'gpt-5.4'}
- **Human surfaces**: review_mode=human; release-gate approvals and stakeholder answers were submitted over the API by a **scripted** reviewer/stakeholder (labelled as automation in every record).

## Result

**Agent success rate: 18.52%** (105/567 P1–P4 agent dispatches; threshold > 97.0%).

Success = artifact not FAILED **and** enriched by the live Astra agent loop (not seed fallback) **and** passes ContractValidator (envelope + payload schema + content hash).

| phase | ok / total |
|---|---|
| P1 Discovery | 105 / 220 |
| P2 Portfolio | 0 / 7 |
| P3 Architecture | 0 / 160 |
| P4 Planning | 0 / 180 |

- Tool calls: 1863; evidence ids cited: 1191; LLM findings: 624; repair rounds: 3; failovers: 0
- Tokens: {'input': 8195617, 'output': 414300, 'reasoning': 13942}

## Release gates

Assurance is per released item: model items that were neither entailed by the claim-support verifier nor tool-measured were confirmed by the approving reviewer (scripted here).

| phase | app | phase status | decision | assurance (before review) | confirmed by review |
|---|---|---|---|---|---|
| P1 | django-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 113 · scripted-confirmed 26 · unverified 121 | 121 |
| P1 | flask-tutorial | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 133 · scripted-confirmed 27 · unverified 66 | 66 |
| P1 | microblog | RUNNING | — | — | 0 |
| P1 | spring-petclinic | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 20 · entailed 143 · scripted-confirmed 26 · unverified 95 | 95 |
| P1 | node-express-realworld-example-app | RUNNING | — | — | 0 |
| P1 | laravel58 | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 117 · scripted-confirmed 24 · unverified 88 | 88 |
| P1 | musicstore | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 102 · scripted-confirmed 21 · unverified 136 | 136 |
| P1 | sinatra | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 113 · scripted-confirmed 27 · unverified 89 | 89 |
| P1 | golang-example | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 20 · entailed 104 · scripted-confirmed 26 · unverified 126 | 126 |
| P1 | todomvc | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 121 · scripted-confirmed 30 · unverified 102 | 102 |

Reviews: 29 (decided by `scripted-reviewer`); stakeholder questions: 260 (260 answered).

## Per-agent results

| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| P1.A1 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 45 | 25 | ✅ |  |
| P1.A2 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 24 | 22 | ✅ |  |
| P1.A3 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 28 | 19 | ✅ |  |
| P1.A4 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 10 | 8 | ✅ |  |
| P1.A5 | spring-petclinic | PARTIAL | yes | fast | 7 | 1 | 9 | 9 | ✅ |  |
| P1.A6 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 25 | 13 | ✅ |  |
| P1.A7 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P1.A8 | spring-petclinic | PARTIAL | yes | reasoning | 3 | 0 | 2 | 4 | ✅ |  |
| P1.A9 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 24 | 16 | ✅ |  |
| P1.A10 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 24 | 15 | ✅ |  |
| P1.A11 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 15 | 12 | ✅ |  |
| P1.A1 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 24 | 17 | ✅ |  |
| P1.A2 | flask-tutorial | PARTIAL | yes | reasoning | 3 | 0 | 12 | 11 | ✅ |  |
| P1.A3 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 11 | 8 | ✅ |  |
| P1.A4 | flask-tutorial | PARTIAL | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P1.A5 | flask-tutorial | PARTIAL | yes | fast | 6 | 0 | 10 | 11 | ✅ |  |
| P1.A6 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 16 | 15 | ✅ |  |
| P1.A7 | flask-tutorial | PARTIAL | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P1.A8 | flask-tutorial | PARTIAL | yes | reasoning | 3 | 0 | 4 | 4 | ✅ |  |
| P1.A9 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 0 | 23 | 11 | ✅ |  |
| P1.A10 | flask-tutorial | PARTIAL | yes | reasoning | 7 | 0 | 19 | 10 | ✅ |  |
| P1.A11 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 12 | 8 | ✅ |  |
| P1.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 35 | 15 | ✅ |  |
| P1.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 27 | 17 | ✅ |  |
| P1.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 39 | 23 | ✅ |  |
| P1.A4 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P1.A5 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 9 | 7 | ✅ |  |
| P1.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 16 | 18 | ✅ |  |
| P1.A7 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P1.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 2 | ✅ |  |
| P1.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 38 | 18 | ✅ |  |
| P1.A10 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 20 | 10 | ✅ |  |
| P1.A11 | django-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 12 | 10 | ✅ |  |
| P1.A1 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 43 | 16 | ✅ |  |
| P1.A2 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 23 | 18 | ✅ |  |
| P1.A3 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 23 | 18 | ✅ |  |
| P1.A4 | microblog | PARTIAL | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P1.A5 | microblog | PARTIAL | yes | fast | 6 | 0 | 9 | 7 | ✅ |  |
| P1.A6 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 26 | 21 | ✅ |  |
| P1.A7 | microblog | PARTIAL | yes | fast | 6 | 0 | 10 | 8 | ✅ |  |
| P1.A8 | microblog | PARTIAL | yes | reasoning | 7 | 0 | 6 | 7 | ✅ |  |
| P1.A9 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A10 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A11 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A1 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 47 | 29 | ✅ |  |
| P1.A2 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 27 | 20 | ✅ |  |
| P1.A3 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 29 | 20 | ✅ |  |
| P1.A4 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P1.A5 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P1.A6 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 20 | 19 | ✅ |  |
| P1.A7 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 5 | ✅ |  |
| P1.A8 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 3 | 5 | ✅ |  |
| P1.A9 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 24 | 11 | ✅ |  |
| P1.A10 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A11 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A1 | musicstore | PARTIAL | yes | reasoning | 9 | 0 | 55 | 23 | ✅ |  |
| P1.A2 | musicstore | PARTIAL | yes | reasoning | 7 | 0 | 30 | 15 | ✅ |  |
| P1.A3 | musicstore | PARTIAL | yes | reasoning | 8 | 0 | 31 | 15 | ✅ |  |
| P1.A4 | musicstore | PARTIAL | yes | fast | 6 | 0 | 11 | 6 | ✅ |  |
| P1.A5 | musicstore | PARTIAL | yes | fast | 7 | 0 | 11 | 7 | ✅ |  |
| P1.A6 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 30 | 18 | ✅ |  |
| P1.A7 | musicstore | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A8 | musicstore | PARTIAL | yes | reasoning | 2 | 0 | 3 | 5 | ✅ |  |
| P1.A9 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 24 | 19 | ✅ |  |
| P1.A10 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 20 | 11 | ✅ |  |
| P1.A11 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 17 | 11 | ✅ |  |
| P1.A1 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 32 | 16 | ✅ |  |
| P1.A2 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 28 | 20 | ✅ |  |
| P1.A3 | laravel58 | PARTIAL | yes | reasoning | 6 | 0 | 33 | 15 | ✅ |  |
| P1.A4 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P1.A5 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 10 | 6 | ✅ |  |
| P1.A6 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 23 | 22 | ✅ |  |
| P1.A7 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A8 | laravel58 | PARTIAL | yes | reasoning | 2 | 0 | 3 | 7 | ✅ |  |
| P1.A9 | laravel58 | PARTIAL | yes | reasoning | 6 | 0 | 29 | 16 | ✅ |  |
| P1.A10 | laravel58 | PARTIAL | yes | reasoning | 7 | 0 | 22 | 10 | ✅ |  |
| P1.A11 | laravel58 | PARTIAL | yes | reasoning | 6 | 0 | 18 | 11 | ✅ |  |
| P1.A1 | sinatra | PARTIAL | yes | reasoning | 5 | 0 | 26 | 16 | ✅ |  |
| P1.A2 | sinatra | PARTIAL | yes | reasoning | 5 | 1 | 12 | 11 | ✅ |  |
| P1.A3 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 15 | 11 | ✅ |  |
| P1.A4 | sinatra | PARTIAL | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P1.A5 | sinatra | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A6 | sinatra | PARTIAL | yes | reasoning | 3 | 0 | 12 | 13 | ✅ |  |
| P1.A7 | sinatra | PARTIAL | yes | fast | 7 | 1 | 6 | 2 | ✅ |  |
| P1.A8 | sinatra | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 10 | 10 | ✅ |  |
| P1.A10 | sinatra | PARTIAL | yes | reasoning | 5 | 0 | 15 | 10 | ✅ |  |
| P1.A11 | sinatra | PARTIAL | yes | reasoning | 5 | 0 | 18 | 13 | ✅ |  |
| P1.A1 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 35 | 19 | ✅ |  |
| P1.A2 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 20 | 15 | ✅ |  |
| P1.A3 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 22 | 12 | ✅ |  |
| P1.A4 | golang-example | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A5 | golang-example | PARTIAL | yes | fast | 6 | 0 | 5 | 5 | ✅ |  |
| P1.A6 | golang-example | PARTIAL | yes | reasoning | 4 | 0 | 16 | 14 | ✅ |  |
| P1.A7 | golang-example | PARTIAL | yes | fast | 6 | 0 | 5 | 5 | ✅ |  |
| P1.A8 | golang-example | PARTIAL | yes | reasoning | 3 | 0 | 2 | 2 | ✅ |  |
| P1.A9 | golang-example | PARTIAL | yes | reasoning | 4 | 0 | 19 | 13 | ✅ |  |
| P1.A10 | golang-example | PARTIAL | yes | reasoning | 7 | 0 | 17 | 12 | ✅ |  |
| P1.A11 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 18 | 12 | ✅ |  |
| P1.A1 | todomvc | PARTIAL | yes | reasoning | 8 | 0 | 55 | 18 | ✅ |  |
| P1.A2 | todomvc | PARTIAL | yes | reasoning | 7 | 0 | 34 | 20 | ✅ |  |
| P1.A3 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 27 | 16 | ✅ |  |
| P1.A4 | todomvc | PARTIAL | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P1.A5 | todomvc | PARTIAL | yes | fast | 7 | 0 | 9 | 5 | ✅ |  |
| P1.A6 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 25 | 17 | ✅ |  |
| P1.A7 | todomvc | PARTIAL | yes | fast | 7 | 0 | 7 | 2 | ✅ |  |
| P1.A8 | todomvc | PARTIAL | yes | reasoning | 3 | 0 | 4 | 3 | ✅ |  |
| P1.A9 | todomvc | PARTIAL | yes | reasoning | 7 | 0 | 27 | 20 | ✅ |  |
| P1.A10 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 20 | 12 | ✅ |  |
| P1.A11 | todomvc | PARTIAL | yes | reasoning | 5 | 0 | 14 | 10 | ✅ |  |
| P1.A1 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A2 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A3 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A4 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A5 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A6 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A7 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A8 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A9 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A10 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A11 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A1 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A2 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A3 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A4 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A5 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A6 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A7 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A8 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A9 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A10 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A11 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A1 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A2 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A3 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A4 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A5 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A6 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A7 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A8 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A9 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A10 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A11 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A1 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A2 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A3 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A4 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A5 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A6 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A7 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A8 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A9 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A10 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A11 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A1 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A2 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A3 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A4 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A5 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A6 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A7 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A8 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A9 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A10 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A11 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A1 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A2 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A3 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A4 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A5 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A6 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A7 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A8 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A9 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A10 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A11 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A1 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A2 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A3 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A4 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A5 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A6 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A7 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A8 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A9 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A10 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A11 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A1 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A2 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A3 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A4 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A5 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A6 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A7 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A8 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A9 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A10 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A11 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A1 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A2 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A3 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A4 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A5 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A6 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A7 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A8 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A9 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A10 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A11 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A1 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A2 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A3 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A4 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A5 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A6 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A7 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A8 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A9 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A10 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P1.A11 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P2.A1 | PF1 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P2.A2 | PF1 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P2.A3 | PF1 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P2.A4 | PF1 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P2.A5 | PF1 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P2.A6 | PF1 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P2.A7 | PF1 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A2 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | spring-petclinic | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | flask-tutorial | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | django-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | microblog | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | node-express-realworld-example-app | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | musicstore | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | laravel58 | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | sinatra | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | golang-example | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | todomvc | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | react-redux-realworld | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | eshop-on-web | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | orchard | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | ofbiz | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | webgoat | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | carddemo | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A1 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A2 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A3 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A4 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A5 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A6 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A7 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A8 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P4.A9 | juice-shop | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |

## Failures

- `P1/microblog/A9`: no artifact published
- `P1/microblog/A10`: no artifact published
- `P1/microblog/A11`: no artifact published
- `P1/node-express-realworld-example-app/A10`: no artifact published
- `P1/node-express-realworld-example-app/A11`: no artifact published
- `P1/react-redux-realworld/A1`: no artifact published
- `P1/react-redux-realworld/A2`: no artifact published
- `P1/react-redux-realworld/A3`: no artifact published
- `P1/react-redux-realworld/A4`: no artifact published
- `P1/react-redux-realworld/A5`: no artifact published
- `P1/react-redux-realworld/A6`: no artifact published
- `P1/react-redux-realworld/A7`: no artifact published
- `P1/react-redux-realworld/A8`: no artifact published
- `P1/react-redux-realworld/A9`: no artifact published
- `P1/react-redux-realworld/A10`: no artifact published
- `P1/react-redux-realworld/A11`: no artifact published
- `P1/eshop-on-web/A1`: no artifact published
- `P1/eshop-on-web/A2`: no artifact published
- `P1/eshop-on-web/A3`: no artifact published
- `P1/eshop-on-web/A4`: no artifact published
- `P1/eshop-on-web/A5`: no artifact published
- `P1/eshop-on-web/A6`: no artifact published
- `P1/eshop-on-web/A7`: no artifact published
- `P1/eshop-on-web/A8`: no artifact published
- `P1/eshop-on-web/A9`: no artifact published
- `P1/eshop-on-web/A10`: no artifact published
- `P1/eshop-on-web/A11`: no artifact published
- `P1/orchard/A1`: no artifact published
- `P1/orchard/A2`: no artifact published
- `P1/orchard/A3`: no artifact published
- `P1/orchard/A4`: no artifact published
- `P1/orchard/A5`: no artifact published
- `P1/orchard/A6`: no artifact published
- `P1/orchard/A7`: no artifact published
- `P1/orchard/A8`: no artifact published
- `P1/orchard/A9`: no artifact published
- `P1/orchard/A10`: no artifact published
- `P1/orchard/A11`: no artifact published
- `P1/struts-examples/A1`: no artifact published
- `P1/struts-examples/A2`: no artifact published
- `P1/struts-examples/A3`: no artifact published
- `P1/struts-examples/A4`: no artifact published
- `P1/struts-examples/A5`: no artifact published
- `P1/struts-examples/A6`: no artifact published
- `P1/struts-examples/A7`: no artifact published
- `P1/struts-examples/A8`: no artifact published
- `P1/struts-examples/A9`: no artifact published
- `P1/struts-examples/A10`: no artifact published
- `P1/struts-examples/A11`: no artifact published
- `P1/ofbiz/A1`: no artifact published
- `P1/ofbiz/A2`: no artifact published
- `P1/ofbiz/A3`: no artifact published
- `P1/ofbiz/A4`: no artifact published
- `P1/ofbiz/A5`: no artifact published
- `P1/ofbiz/A6`: no artifact published
- `P1/ofbiz/A7`: no artifact published
- `P1/ofbiz/A8`: no artifact published
- `P1/ofbiz/A9`: no artifact published
- `P1/ofbiz/A10`: no artifact published
- `P1/ofbiz/A11`: no artifact published
- `P1/webgoat/A1`: no artifact published
- `P1/webgoat/A2`: no artifact published
- `P1/webgoat/A3`: no artifact published
- `P1/webgoat/A4`: no artifact published
- `P1/webgoat/A5`: no artifact published
- `P1/webgoat/A6`: no artifact published
- `P1/webgoat/A7`: no artifact published
- `P1/webgoat/A8`: no artifact published
- `P1/webgoat/A9`: no artifact published
- `P1/webgoat/A10`: no artifact published
- `P1/webgoat/A11`: no artifact published
- `P1/carddemo/A1`: no artifact published
- `P1/carddemo/A2`: no artifact published
- `P1/carddemo/A3`: no artifact published
- `P1/carddemo/A4`: no artifact published
- `P1/carddemo/A5`: no artifact published
- `P1/carddemo/A6`: no artifact published
- `P1/carddemo/A7`: no artifact published
- `P1/carddemo/A8`: no artifact published
- `P1/carddemo/A9`: no artifact published
- `P1/carddemo/A10`: no artifact published
- `P1/carddemo/A11`: no artifact published
- `P1/mantisbt/A1`: no artifact published
- `P1/mantisbt/A2`: no artifact published
- `P1/mantisbt/A3`: no artifact published
- `P1/mantisbt/A4`: no artifact published
- `P1/mantisbt/A5`: no artifact published
- `P1/mantisbt/A6`: no artifact published
- `P1/mantisbt/A7`: no artifact published
- `P1/mantisbt/A8`: no artifact published
- `P1/mantisbt/A9`: no artifact published
- `P1/mantisbt/A10`: no artifact published
- `P1/mantisbt/A11`: no artifact published
- `P1/bugzilla/A1`: no artifact published
- `P1/bugzilla/A2`: no artifact published
- `P1/bugzilla/A3`: no artifact published
- `P1/bugzilla/A4`: no artifact published
- `P1/bugzilla/A5`: no artifact published
- `P1/bugzilla/A6`: no artifact published
- `P1/bugzilla/A7`: no artifact published
- `P1/bugzilla/A8`: no artifact published
- `P1/bugzilla/A9`: no artifact published
- `P1/bugzilla/A10`: no artifact published
- `P1/bugzilla/A11`: no artifact published
- `P1/juice-shop/A1`: no artifact published
- `P1/juice-shop/A2`: no artifact published
- `P1/juice-shop/A3`: no artifact published
- `P1/juice-shop/A4`: no artifact published
- `P1/juice-shop/A5`: no artifact published
- `P1/juice-shop/A6`: no artifact published
- `P1/juice-shop/A7`: no artifact published
- `P1/juice-shop/A8`: no artifact published
- `P1/juice-shop/A9`: no artifact published
- `P1/juice-shop/A10`: no artifact published
- `P1/juice-shop/A11`: no artifact published
- `P2/PF1/A1`: no artifact published
- `P2/PF1/A2`: no artifact published
- `P2/PF1/A3`: no artifact published
- `P2/PF1/A4`: no artifact published
- `P2/PF1/A5`: no artifact published
- `P2/PF1/A6`: no artifact published
- `P2/PF1/A7`: no artifact published
- `P3/spring-petclinic/A1`: no artifact published
- `P3/spring-petclinic/A2`: no artifact published
- `P3/spring-petclinic/A3`: no artifact published
- `P3/spring-petclinic/A4`: no artifact published
- `P3/spring-petclinic/A5`: no artifact published
- `P3/spring-petclinic/A6`: no artifact published
- `P3/spring-petclinic/A7`: no artifact published
- `P3/spring-petclinic/A8`: no artifact published
- `P3/flask-tutorial/A1`: no artifact published
- `P3/flask-tutorial/A2`: no artifact published
- `P3/flask-tutorial/A3`: no artifact published
- `P3/flask-tutorial/A4`: no artifact published
- `P3/flask-tutorial/A5`: no artifact published
- `P3/flask-tutorial/A6`: no artifact published
- `P3/flask-tutorial/A7`: no artifact published
- `P3/flask-tutorial/A8`: no artifact published
- `P3/django-realworld-example-app/A1`: no artifact published
- `P3/django-realworld-example-app/A2`: no artifact published
- `P3/django-realworld-example-app/A3`: no artifact published
- `P3/django-realworld-example-app/A4`: no artifact published
- `P3/django-realworld-example-app/A5`: no artifact published
- `P3/django-realworld-example-app/A6`: no artifact published
- `P3/django-realworld-example-app/A7`: no artifact published
- `P3/django-realworld-example-app/A8`: no artifact published
- `P3/microblog/A1`: no artifact published
- `P3/microblog/A2`: no artifact published
- `P3/microblog/A3`: no artifact published
- `P3/microblog/A4`: no artifact published
- `P3/microblog/A5`: no artifact published
- `P3/microblog/A6`: no artifact published
- `P3/microblog/A7`: no artifact published
- `P3/microblog/A8`: no artifact published
- `P3/node-express-realworld-example-app/A1`: no artifact published
- `P3/node-express-realworld-example-app/A2`: no artifact published
- `P3/node-express-realworld-example-app/A3`: no artifact published
- `P3/node-express-realworld-example-app/A4`: no artifact published
- `P3/node-express-realworld-example-app/A5`: no artifact published
- `P3/node-express-realworld-example-app/A6`: no artifact published
- `P3/node-express-realworld-example-app/A7`: no artifact published
- `P3/node-express-realworld-example-app/A8`: no artifact published
- `P3/musicstore/A1`: no artifact published
- `P3/musicstore/A2`: no artifact published
- `P3/musicstore/A3`: no artifact published
- `P3/musicstore/A4`: no artifact published
- `P3/musicstore/A5`: no artifact published
- `P3/musicstore/A6`: no artifact published
- `P3/musicstore/A7`: no artifact published
- `P3/musicstore/A8`: no artifact published
- `P3/laravel58/A1`: no artifact published
- `P3/laravel58/A2`: no artifact published
- `P3/laravel58/A3`: no artifact published
- `P3/laravel58/A4`: no artifact published
- `P3/laravel58/A5`: no artifact published
- `P3/laravel58/A6`: no artifact published
- `P3/laravel58/A7`: no artifact published
- `P3/laravel58/A8`: no artifact published
- `P3/sinatra/A1`: no artifact published
- `P3/sinatra/A2`: no artifact published
- `P3/sinatra/A3`: no artifact published
- `P3/sinatra/A4`: no artifact published
- `P3/sinatra/A5`: no artifact published
- `P3/sinatra/A6`: no artifact published
- `P3/sinatra/A7`: no artifact published
- `P3/sinatra/A8`: no artifact published
- `P3/golang-example/A1`: no artifact published
- `P3/golang-example/A2`: no artifact published
- `P3/golang-example/A3`: no artifact published
- `P3/golang-example/A4`: no artifact published
- `P3/golang-example/A5`: no artifact published
- `P3/golang-example/A6`: no artifact published
- `P3/golang-example/A7`: no artifact published
- `P3/golang-example/A8`: no artifact published
- `P3/todomvc/A1`: no artifact published
- `P3/todomvc/A2`: no artifact published
- `P3/todomvc/A3`: no artifact published
- `P3/todomvc/A4`: no artifact published
- `P3/todomvc/A5`: no artifact published
- `P3/todomvc/A6`: no artifact published
- `P3/todomvc/A7`: no artifact published
- `P3/todomvc/A8`: no artifact published
- `P3/react-redux-realworld/A1`: no artifact published
- `P3/react-redux-realworld/A2`: no artifact published
- `P3/react-redux-realworld/A3`: no artifact published
- `P3/react-redux-realworld/A4`: no artifact published
- `P3/react-redux-realworld/A5`: no artifact published
- `P3/react-redux-realworld/A6`: no artifact published
- `P3/react-redux-realworld/A7`: no artifact published
- `P3/react-redux-realworld/A8`: no artifact published
- `P3/eshop-on-web/A1`: no artifact published
- `P3/eshop-on-web/A2`: no artifact published
- `P3/eshop-on-web/A3`: no artifact published
- `P3/eshop-on-web/A4`: no artifact published
- `P3/eshop-on-web/A5`: no artifact published
- `P3/eshop-on-web/A6`: no artifact published
- `P3/eshop-on-web/A7`: no artifact published
- `P3/eshop-on-web/A8`: no artifact published
- `P3/orchard/A1`: no artifact published
- `P3/orchard/A2`: no artifact published
- `P3/orchard/A3`: no artifact published
- `P3/orchard/A4`: no artifact published
- `P3/orchard/A5`: no artifact published
- `P3/orchard/A6`: no artifact published
- `P3/orchard/A7`: no artifact published
- `P3/orchard/A8`: no artifact published
- `P3/struts-examples/A1`: no artifact published
- `P3/struts-examples/A2`: no artifact published
- `P3/struts-examples/A3`: no artifact published
- `P3/struts-examples/A4`: no artifact published
- `P3/struts-examples/A5`: no artifact published
- `P3/struts-examples/A6`: no artifact published
- `P3/struts-examples/A7`: no artifact published
- `P3/struts-examples/A8`: no artifact published
- `P3/ofbiz/A1`: no artifact published
- `P3/ofbiz/A2`: no artifact published
- `P3/ofbiz/A3`: no artifact published
- `P3/ofbiz/A4`: no artifact published
- `P3/ofbiz/A5`: no artifact published
- `P3/ofbiz/A6`: no artifact published
- `P3/ofbiz/A7`: no artifact published
- `P3/ofbiz/A8`: no artifact published
- `P3/webgoat/A1`: no artifact published
- `P3/webgoat/A2`: no artifact published
- `P3/webgoat/A3`: no artifact published
- `P3/webgoat/A4`: no artifact published
- `P3/webgoat/A5`: no artifact published
- `P3/webgoat/A6`: no artifact published
- `P3/webgoat/A7`: no artifact published
- `P3/webgoat/A8`: no artifact published
- `P3/carddemo/A1`: no artifact published
- `P3/carddemo/A2`: no artifact published
- `P3/carddemo/A3`: no artifact published
- `P3/carddemo/A4`: no artifact published
- `P3/carddemo/A5`: no artifact published
- `P3/carddemo/A6`: no artifact published
- `P3/carddemo/A7`: no artifact published
- `P3/carddemo/A8`: no artifact published
- `P3/mantisbt/A1`: no artifact published
- `P3/mantisbt/A2`: no artifact published
- `P3/mantisbt/A3`: no artifact published
- `P3/mantisbt/A4`: no artifact published
- `P3/mantisbt/A5`: no artifact published
- `P3/mantisbt/A6`: no artifact published
- `P3/mantisbt/A7`: no artifact published
- `P3/mantisbt/A8`: no artifact published
- `P3/bugzilla/A1`: no artifact published
- `P3/bugzilla/A2`: no artifact published
- `P3/bugzilla/A3`: no artifact published
- `P3/bugzilla/A4`: no artifact published
- `P3/bugzilla/A5`: no artifact published
- `P3/bugzilla/A6`: no artifact published
- `P3/bugzilla/A7`: no artifact published
- `P3/bugzilla/A8`: no artifact published
- `P3/juice-shop/A1`: no artifact published
- `P3/juice-shop/A2`: no artifact published
- `P3/juice-shop/A3`: no artifact published
- `P3/juice-shop/A4`: no artifact published
- `P3/juice-shop/A5`: no artifact published
- `P3/juice-shop/A6`: no artifact published
- `P3/juice-shop/A7`: no artifact published
- `P3/juice-shop/A8`: no artifact published
- `P4/spring-petclinic/A1`: no artifact published
- `P4/spring-petclinic/A2`: no artifact published
- `P4/spring-petclinic/A3`: no artifact published
- `P4/spring-petclinic/A4`: no artifact published
- `P4/spring-petclinic/A5`: no artifact published
- `P4/spring-petclinic/A6`: no artifact published
- `P4/spring-petclinic/A7`: no artifact published
- `P4/spring-petclinic/A8`: no artifact published
- `P4/spring-petclinic/A9`: no artifact published
- `P4/flask-tutorial/A1`: no artifact published
- `P4/flask-tutorial/A2`: no artifact published
- `P4/flask-tutorial/A3`: no artifact published
- `P4/flask-tutorial/A4`: no artifact published
- `P4/flask-tutorial/A5`: no artifact published
- `P4/flask-tutorial/A6`: no artifact published
- `P4/flask-tutorial/A7`: no artifact published
- `P4/flask-tutorial/A8`: no artifact published
- `P4/flask-tutorial/A9`: no artifact published
- `P4/django-realworld-example-app/A1`: no artifact published
- `P4/django-realworld-example-app/A2`: no artifact published
- `P4/django-realworld-example-app/A3`: no artifact published
- `P4/django-realworld-example-app/A4`: no artifact published
- `P4/django-realworld-example-app/A5`: no artifact published
- `P4/django-realworld-example-app/A6`: no artifact published
- `P4/django-realworld-example-app/A7`: no artifact published
- `P4/django-realworld-example-app/A8`: no artifact published
- `P4/django-realworld-example-app/A9`: no artifact published
- `P4/microblog/A1`: no artifact published
- `P4/microblog/A2`: no artifact published
- `P4/microblog/A3`: no artifact published
- `P4/microblog/A4`: no artifact published
- `P4/microblog/A5`: no artifact published
- `P4/microblog/A6`: no artifact published
- `P4/microblog/A7`: no artifact published
- `P4/microblog/A8`: no artifact published
- `P4/microblog/A9`: no artifact published
- `P4/node-express-realworld-example-app/A1`: no artifact published
- `P4/node-express-realworld-example-app/A2`: no artifact published
- `P4/node-express-realworld-example-app/A3`: no artifact published
- `P4/node-express-realworld-example-app/A4`: no artifact published
- `P4/node-express-realworld-example-app/A5`: no artifact published
- `P4/node-express-realworld-example-app/A6`: no artifact published
- `P4/node-express-realworld-example-app/A7`: no artifact published
- `P4/node-express-realworld-example-app/A8`: no artifact published
- `P4/node-express-realworld-example-app/A9`: no artifact published
- `P4/musicstore/A1`: no artifact published
- `P4/musicstore/A2`: no artifact published
- `P4/musicstore/A3`: no artifact published
- `P4/musicstore/A4`: no artifact published
- `P4/musicstore/A5`: no artifact published
- `P4/musicstore/A6`: no artifact published
- `P4/musicstore/A7`: no artifact published
- `P4/musicstore/A8`: no artifact published
- `P4/musicstore/A9`: no artifact published
- `P4/laravel58/A1`: no artifact published
- `P4/laravel58/A2`: no artifact published
- `P4/laravel58/A3`: no artifact published
- `P4/laravel58/A4`: no artifact published
- `P4/laravel58/A5`: no artifact published
- `P4/laravel58/A6`: no artifact published
- `P4/laravel58/A7`: no artifact published
- `P4/laravel58/A8`: no artifact published
- `P4/laravel58/A9`: no artifact published
- `P4/sinatra/A1`: no artifact published
- `P4/sinatra/A2`: no artifact published
- `P4/sinatra/A3`: no artifact published
- `P4/sinatra/A4`: no artifact published
- `P4/sinatra/A5`: no artifact published
- `P4/sinatra/A6`: no artifact published
- `P4/sinatra/A7`: no artifact published
- `P4/sinatra/A8`: no artifact published
- `P4/sinatra/A9`: no artifact published
- `P4/golang-example/A1`: no artifact published
- `P4/golang-example/A2`: no artifact published
- `P4/golang-example/A3`: no artifact published
- `P4/golang-example/A4`: no artifact published
- `P4/golang-example/A5`: no artifact published
- `P4/golang-example/A6`: no artifact published
- `P4/golang-example/A7`: no artifact published
- `P4/golang-example/A8`: no artifact published
- `P4/golang-example/A9`: no artifact published
- `P4/todomvc/A1`: no artifact published
- `P4/todomvc/A2`: no artifact published
- `P4/todomvc/A3`: no artifact published
- `P4/todomvc/A4`: no artifact published
- `P4/todomvc/A5`: no artifact published
- `P4/todomvc/A6`: no artifact published
- `P4/todomvc/A7`: no artifact published
- `P4/todomvc/A8`: no artifact published
- `P4/todomvc/A9`: no artifact published
- `P4/react-redux-realworld/A1`: no artifact published
- `P4/react-redux-realworld/A2`: no artifact published
- `P4/react-redux-realworld/A3`: no artifact published
- `P4/react-redux-realworld/A4`: no artifact published
- `P4/react-redux-realworld/A5`: no artifact published
- `P4/react-redux-realworld/A6`: no artifact published
- `P4/react-redux-realworld/A7`: no artifact published
- `P4/react-redux-realworld/A8`: no artifact published
- `P4/react-redux-realworld/A9`: no artifact published
- `P4/eshop-on-web/A1`: no artifact published
- `P4/eshop-on-web/A2`: no artifact published
- `P4/eshop-on-web/A3`: no artifact published
- `P4/eshop-on-web/A4`: no artifact published
- `P4/eshop-on-web/A5`: no artifact published
- `P4/eshop-on-web/A6`: no artifact published
- `P4/eshop-on-web/A7`: no artifact published
- `P4/eshop-on-web/A8`: no artifact published
- `P4/eshop-on-web/A9`: no artifact published
- `P4/orchard/A1`: no artifact published
- `P4/orchard/A2`: no artifact published
- `P4/orchard/A3`: no artifact published
- `P4/orchard/A4`: no artifact published
- `P4/orchard/A5`: no artifact published
- `P4/orchard/A6`: no artifact published
- `P4/orchard/A7`: no artifact published
- `P4/orchard/A8`: no artifact published
- `P4/orchard/A9`: no artifact published
- `P4/struts-examples/A1`: no artifact published
- `P4/struts-examples/A2`: no artifact published
- `P4/struts-examples/A3`: no artifact published
- `P4/struts-examples/A4`: no artifact published
- `P4/struts-examples/A5`: no artifact published
- `P4/struts-examples/A6`: no artifact published
- `P4/struts-examples/A7`: no artifact published
- `P4/struts-examples/A8`: no artifact published
- `P4/struts-examples/A9`: no artifact published
- `P4/ofbiz/A1`: no artifact published
- `P4/ofbiz/A2`: no artifact published
- `P4/ofbiz/A3`: no artifact published
- `P4/ofbiz/A4`: no artifact published
- `P4/ofbiz/A5`: no artifact published
- `P4/ofbiz/A6`: no artifact published
- `P4/ofbiz/A7`: no artifact published
- `P4/ofbiz/A8`: no artifact published
- `P4/ofbiz/A9`: no artifact published
- `P4/webgoat/A1`: no artifact published
- `P4/webgoat/A2`: no artifact published
- `P4/webgoat/A3`: no artifact published
- `P4/webgoat/A4`: no artifact published
- `P4/webgoat/A5`: no artifact published
- `P4/webgoat/A6`: no artifact published
- `P4/webgoat/A7`: no artifact published
- `P4/webgoat/A8`: no artifact published
- `P4/webgoat/A9`: no artifact published
- `P4/carddemo/A1`: no artifact published
- `P4/carddemo/A2`: no artifact published
- `P4/carddemo/A3`: no artifact published
- `P4/carddemo/A4`: no artifact published
- `P4/carddemo/A5`: no artifact published
- `P4/carddemo/A6`: no artifact published
- `P4/carddemo/A7`: no artifact published
- `P4/carddemo/A8`: no artifact published
- `P4/carddemo/A9`: no artifact published
- `P4/mantisbt/A1`: no artifact published
- `P4/mantisbt/A2`: no artifact published
- `P4/mantisbt/A3`: no artifact published
- `P4/mantisbt/A4`: no artifact published
- `P4/mantisbt/A5`: no artifact published
- `P4/mantisbt/A6`: no artifact published
- `P4/mantisbt/A7`: no artifact published
- `P4/mantisbt/A8`: no artifact published
- `P4/mantisbt/A9`: no artifact published
- `P4/bugzilla/A1`: no artifact published
- `P4/bugzilla/A2`: no artifact published
- `P4/bugzilla/A3`: no artifact published
- `P4/bugzilla/A4`: no artifact published
- `P4/bugzilla/A5`: no artifact published
- `P4/bugzilla/A6`: no artifact published
- `P4/bugzilla/A7`: no artifact published
- `P4/bugzilla/A8`: no artifact published
- `P4/bugzilla/A9`: no artifact published
- `P4/juice-shop/A1`: no artifact published
- `P4/juice-shop/A2`: no artifact published
- `P4/juice-shop/A3`: no artifact published
- `P4/juice-shop/A4`: no artifact published
- `P4/juice-shop/A5`: no artifact published
- `P4/juice-shop/A6`: no artifact published
- `P4/juice-shop/A7`: no artifact published
- `P4/juice-shop/A8`: no artifact published
- `P4/juice-shop/A9`: no artifact published
