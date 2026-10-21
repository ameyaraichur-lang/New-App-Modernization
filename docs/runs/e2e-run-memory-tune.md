# E2E agentic acceptance run `run-memory-tune`

- **Job**: `job-1792340613-81baff` — **COMPLETED**
- **Repositories**: `spring-petclinic`, `flask-tutorial`, `django-realworld-example-app`, `microblog`, `node-express-realworld-example-app`, `musicstore`, `laravel58`, `sinatra`, `golang-example`, `todomvc`, `react-redux-realworld`, `eshop-on-web`, `orchard`, `struts-examples`, `ofbiz`, `webgoat`, `carddemo`, `mantisbt`, `bugzilla`, `juice-shop`
- **Elapsed**: 757 min 44 s; LLM cache mode `record` (record = every call live, responses recorded for replay)
- **Astra tiers**: {'reasoning': 'gpt-6-astra', 'coding': 'gpt-5.3-codex-PlayWright', 'fast': 'gpt-4.1-mini', 'fallback': 'gpt-5.4'}
- **Human surfaces**: review_mode=human; release-gate approvals and stakeholder answers were submitted over the API by a **scripted** reviewer/stakeholder (labelled as automation in every record).

## Result

**Agent success rate: 100.00%** (295/295 P1–P4 agent dispatches; threshold > 97.0%).

272 P3/P4 agent slots were **not admitted** because the authorized P2 release gate routed `spring-petclinic` (Retain), `flask-tutorial` (Retain), `microblog` (Retain), `node-express-realworld-example-app` (Retain), `musicstore` (Retire), `sinatra` (Retain), `todomvc` (Retain), `eshop-on-web` (Retain), `orchard` (Retain), `struts-examples` (Retain), `ofbiz` (Retain), `webgoat` (Retain), `carddemo` (Retain), `mantisbt` (Retain), `bugzilla` (Retain), `juice-shop` (Retain) to the non-delivery register — by design, no architecture or plan is produced for a non-delivery route. Counting those slots as failures would give 52.03%.

Success = artifact not FAILED **and** enriched by the live Astra agent loop (not seed fallback) **and** passes ContractValidator (envelope + payload schema + content hash).

| phase | ok / total |
|---|---|
| P1 Discovery | 220 / 220 |
| P2 Portfolio | 7 / 7 |
| P3 Architecture | 32 / 32 |
| P4 Planning | 36 / 36 |

- Tool calls: 5668; evidence ids cited: 3251; LLM findings: 1810; repair rounds: 22; failovers: 0
- Tokens: {'input': 27587886, 'output': 1198811, 'reasoning': 56918}

## Release gates

Assurance is per released item: model items that were neither entailed by the claim-support verifier nor tool-measured were confirmed by the approving reviewer (scripted here).

| phase | app | phase status | decision | assurance (before review) | confirmed by review |
|---|---|---|---|---|---|
| P1 | microblog | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 98 · unverified 139 | 139 |
| P1 | node-express-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 18 · entailed 129 · unverified 91 | 91 |
| P1 | flask-tutorial | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 127 · unverified 75 | 75 |
| P1 | django-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 104 · unverified 118 | 118 |
| P1 | spring-petclinic | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 20 · entailed 141 · unverified 91 | 91 |
| P1 | musicstore | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 121 · unverified 119 | 119 |
| P1 | laravel58 | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 117 · unverified 83 | 83 |
| P1 | sinatra | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 120 · unverified 85 | 85 |
| P1 | golang-example | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 20 · entailed 96 · unverified 130 | 130 |
| P1 | todomvc | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 132 · unverified 75 | 75 |
| P1 | react-redux-realworld | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 116 · unverified 93 | 93 |
| P1 | eshop-on-web | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 18 · entailed 133 · unverified 101 | 101 |
| P1 | orchard | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 96 · unverified 122 | 122 |
| P1 | struts-examples | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 118 · unverified 104 | 104 |
| P1 | ofbiz | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 101 · unverified 111 | 111 |
| P1 | webgoat | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 133 · unverified 93 | 93 |
| P1 | carddemo | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 20 · entailed 79 · unverified 119 | 119 |
| P1 | mantisbt | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 113 · unverified 119 | 119 |
| P1 | bugzilla | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 20 · entailed 120 · unverified 109 | 109 |
| P1 | juice-shop | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 109 · unverified 151 | 151 |
| P2 | PF1 | COMPLETED | AUTHORIZED | tool-measured 7 · entailed 23 · unverified 114 | 114 |
| P3 | spring-petclinic | NOT_ADMITTED | — | — | 0 |
| P4 | spring-petclinic | NOT_ADMITTED | — | — | 0 |
| P3 | flask-tutorial | NOT_ADMITTED | — | — | 0 |
| P4 | flask-tutorial | NOT_ADMITTED | — | — | 0 |
| P3 | microblog | NOT_ADMITTED | — | — | 0 |
| P4 | microblog | NOT_ADMITTED | — | — | 0 |
| P3 | node-express-realworld-example-app | NOT_ADMITTED | — | — | 0 |
| P4 | node-express-realworld-example-app | NOT_ADMITTED | — | — | 0 |
| P3 | musicstore | NOT_ADMITTED | — | — | 0 |
| P4 | musicstore | NOT_ADMITTED | — | — | 0 |
| P3 | sinatra | NOT_ADMITTED | — | — | 0 |
| P4 | sinatra | NOT_ADMITTED | — | — | 0 |
| P3 | todomvc | NOT_ADMITTED | — | — | 0 |
| P4 | todomvc | NOT_ADMITTED | — | — | 0 |
| P3 | eshop-on-web | NOT_ADMITTED | — | — | 0 |
| P4 | eshop-on-web | NOT_ADMITTED | — | — | 0 |
| P3 | orchard | NOT_ADMITTED | — | — | 0 |
| P4 | orchard | NOT_ADMITTED | — | — | 0 |
| P3 | struts-examples | NOT_ADMITTED | — | — | 0 |
| P4 | struts-examples | NOT_ADMITTED | — | — | 0 |
| P3 | ofbiz | NOT_ADMITTED | — | — | 0 |
| P4 | ofbiz | NOT_ADMITTED | — | — | 0 |
| P3 | webgoat | NOT_ADMITTED | — | — | 0 |
| P4 | webgoat | NOT_ADMITTED | — | — | 0 |
| P3 | carddemo | NOT_ADMITTED | — | — | 0 |
| P4 | carddemo | NOT_ADMITTED | — | — | 0 |
| P3 | mantisbt | NOT_ADMITTED | — | — | 0 |
| P4 | mantisbt | NOT_ADMITTED | — | — | 0 |
| P3 | bugzilla | NOT_ADMITTED | — | — | 0 |
| P4 | bugzilla | NOT_ADMITTED | — | — | 0 |
| P3 | juice-shop | NOT_ADMITTED | — | — | 0 |
| P4 | juice-shop | NOT_ADMITTED | — | — | 0 |
| P3 | laravel58 | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 34 · unverified 155 | 155 |
| P3 | django-realworld-example-app | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 26 · unverified 176 | 176 |
| P3 | golang-example | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 29 · unverified 172 | 172 |
| P3 | react-redux-realworld | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 31 · unverified 164 | 164 |
| P4 | react-redux-realworld | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 19 · unverified 77 | 77 |
| P4 | golang-example | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 22 · unverified 81 | 81 |
| P4 | laravel58 | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 14 · unverified 92 | 92 |
| P4 | django-realworld-example-app | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 19 · unverified 82 | 82 |

Reviews: 29 (decided by `scripted-reviewer`); stakeholder questions: 149 (149 answered).

## Per-agent results

| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| P1.A1 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 45 | 23 | ✅ |  |
| P1.A2 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 29 | 22 | ✅ |  |
| P1.A3 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 27 | 21 | ✅ |  |
| P1.A4 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 11 | 10 | ✅ |  |
| P1.A5 | spring-petclinic | PARTIAL | yes | fast | 7 | 0 | 9 | 5 | ✅ |  |
| P1.A6 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 26 | 19 | ✅ |  |
| P1.A7 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P1.A8 | spring-petclinic | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 24 | 15 | ✅ |  |
| P1.A10 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 20 | 11 | ✅ |  |
| P1.A11 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 19 | 12 | ✅ |  |
| P1.A1 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 0 | 26 | 18 | ✅ |  |
| P1.A2 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 15 | 8 | ✅ |  |
| P1.A3 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 0 | 14 | 8 | ✅ |  |
| P1.A4 | flask-tutorial | PARTIAL | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P1.A5 | flask-tutorial | PARTIAL | yes | fast | 7 | 0 | 11 | 11 | ✅ |  |
| P1.A6 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 18 | 11 | ✅ |  |
| P1.A7 | flask-tutorial | PARTIAL | yes | fast | 7 | 0 | 11 | 5 | ✅ |  |
| P1.A8 | flask-tutorial | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 23 | 12 | ✅ |  |
| P1.A10 | flask-tutorial | PARTIAL | yes | reasoning | 6 | 0 | 15 | 10 | ✅ |  |
| P1.A11 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 0 | 12 | 10 | ✅ |  |
| P1.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 41 | 22 | ✅ |  |
| P1.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 29 | 14 | ✅ |  |
| P1.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 31 | 18 | ✅ |  |
| P1.A4 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 6 | 2 | ✅ |  |
| P1.A5 | django-realworld-example-app | PARTIAL | yes | fast | 7 | 0 | 11 | 9 | ✅ |  |
| P1.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 16 | 19 | ✅ |  |
| P1.A7 | django-realworld-example-app | PARTIAL | yes | fast | 7 | 1 | 5 | 3 | ✅ |  |
| P1.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 30 | 15 | ✅ |  |
| P1.A10 | django-realworld-example-app | PARTIAL | yes | reasoning | 7 | 1 | 16 | 10 | ✅ |  |
| P1.A11 | django-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 13 | 9 | ✅ |  |
| P1.A1 | microblog | PARTIAL | yes | reasoning | 7 | 0 | 43 | 19 | ✅ |  |
| P1.A2 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 23 | 21 | ✅ |  |
| P1.A3 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 21 | 16 | ✅ |  |
| P1.A4 | microblog | PARTIAL | yes | fast | 6 | 0 | 8 | 7 | ✅ |  |
| P1.A5 | microblog | PARTIAL | yes | fast | 7 | 0 | 11 | 8 | ✅ |  |
| P1.A6 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 24 | 25 | ✅ |  |
| P1.A7 | microblog | PARTIAL | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P1.A8 | microblog | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | microblog | PARTIAL | yes | reasoning | 4 | 0 | 26 | 10 | ✅ |  |
| P1.A10 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 20 | 12 | ✅ |  |
| P1.A11 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 15 | 10 | ✅ |  |
| P1.A1 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 44 | 23 | ✅ |  |
| P1.A2 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 25 | 21 | ✅ |  |
| P1.A3 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 32 | 21 | ✅ |  |
| P1.A4 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P1.A5 | node-express-realworld-example-app | PARTIAL | yes | fast | 7 | 1 | 7 | 6 | ✅ |  |
| P1.A6 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 20 | 20 | ✅ |  |
| P1.A7 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P1.A8 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 24 | 10 | ✅ |  |
| P1.A10 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 25 | 14 | ✅ |  |
| P1.A11 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 21 | 11 | ✅ |  |
| P1.A1 | musicstore | PARTIAL | yes | reasoning | 9 | 0 | 62 | 29 | ✅ |  |
| P1.A2 | musicstore | PARTIAL | yes | reasoning | 7 | 0 | 27 | 20 | ✅ |  |
| P1.A3 | musicstore | PARTIAL | yes | reasoning | 10 | 0 | 36 | 22 | ✅ |  |
| P1.A4 | musicstore | PARTIAL | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P1.A5 | musicstore | PARTIAL | yes | fast | 8 | 1 | 9 | 6 | ✅ |  |
| P1.A6 | musicstore | PARTIAL | yes | reasoning | 7 | 0 | 30 | 18 | ✅ |  |
| P1.A7 | musicstore | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A8 | musicstore | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 22 | 11 | ✅ |  |
| P1.A10 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 18 | 11 | ✅ |  |
| P1.A11 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 16 | 9 | ✅ |  |
| P1.A1 | laravel58 | PARTIAL | yes | reasoning | 6 | 0 | 38 | 24 | ✅ |  |
| P1.A2 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 30 | 24 | ✅ |  |
| P1.A3 | laravel58 | PARTIAL | yes | reasoning | 6 | 0 | 32 | 17 | ✅ |  |
| P1.A4 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A5 | laravel58 | PARTIAL | yes | fast | 8 | 1 | 9 | 8 | ✅ |  |
| P1.A6 | laravel58 | PARTIAL | yes | reasoning | 4 | 0 | 20 | 12 | ✅ |  |
| P1.A7 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P1.A8 | laravel58 | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | laravel58 | PARTIAL | yes | reasoning | 6 | 0 | 31 | 17 | ✅ |  |
| P1.A10 | laravel58 | PARTIAL | yes | reasoning | 6 | 0 | 19 | 12 | ✅ |  |
| P1.A11 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 11 | 9 | ✅ |  |
| P1.A1 | sinatra | PARTIAL | yes | reasoning | 5 | 0 | 25 | 16 | ✅ |  |
| P1.A2 | sinatra | PARTIAL | yes | reasoning | 4 | 1 | 10 | 8 | ✅ |  |
| P1.A3 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 15 | 10 | ✅ |  |
| P1.A4 | sinatra | PARTIAL | yes | fast | 7 | 0 | 7 | 6 | ✅ |  |
| P1.A5 | sinatra | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A6 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 18 | 14 | ✅ |  |
| P1.A7 | sinatra | PARTIAL | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P1.A8 | sinatra | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | sinatra | PARTIAL | yes | reasoning | 4 | 1 | 11 | 5 | ✅ |  |
| P1.A10 | sinatra | PARTIAL | yes | reasoning | 6 | 0 | 17 | 11 | ✅ |  |
| P1.A11 | sinatra | PARTIAL | yes | reasoning | 6 | 0 | 21 | 10 | ✅ |  |
| P1.A1 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 33 | 14 | ✅ |  |
| P1.A2 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 21 | 15 | ✅ |  |
| P1.A3 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 19 | 12 | ✅ |  |
| P1.A4 | golang-example | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A5 | golang-example | PARTIAL | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P1.A6 | golang-example | PARTIAL | yes | reasoning | 4 | 0 | 16 | 16 | ✅ |  |
| P1.A7 | golang-example | PARTIAL | yes | fast | 7 | 1 | 5 | 3 | ✅ |  |
| P1.A8 | golang-example | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 21 | 11 | ✅ |  |
| P1.A10 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 20 | 10 | ✅ |  |
| P1.A11 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 17 | 10 | ✅ |  |
| P1.A1 | todomvc | PARTIAL | yes | reasoning | 8 | 0 | 56 | 20 | ✅ |  |
| P1.A2 | todomvc | PARTIAL | yes | reasoning | 8 | 0 | 39 | 19 | ✅ |  |
| P1.A3 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 25 | 16 | ✅ |  |
| P1.A4 | todomvc | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A5 | todomvc | PARTIAL | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P1.A6 | todomvc | PARTIAL | yes | reasoning | 5 | 0 | 21 | 15 | ✅ |  |
| P1.A7 | todomvc | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A8 | todomvc | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 21 | 17 | ✅ |  |
| P1.A10 | todomvc | PARTIAL | yes | reasoning | 7 | 0 | 23 | 11 | ✅ |  |
| P1.A11 | todomvc | PARTIAL | yes | reasoning | 4 | 0 | 12 | 9 | ✅ |  |
| P1.A1 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 25 | 14 | ✅ |  |
| P1.A2 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 20 | 12 | ✅ |  |
| P1.A3 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 23 | 10 | ✅ |  |
| P1.A4 | react-redux-realworld | PARTIAL | yes | fast | 6 | 0 | 6 | 4 | ✅ |  |
| P1.A5 | react-redux-realworld | PARTIAL | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P1.A6 | react-redux-realworld | PARTIAL | yes | reasoning | 4 | 0 | 17 | 13 | ✅ |  |
| P1.A7 | react-redux-realworld | PARTIAL | yes | fast | 9 | 2 | 8 | 4 | ✅ |  |
| P1.A8 | react-redux-realworld | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 36 | 13 | ✅ |  |
| P1.A10 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 16 | 12 | ✅ |  |
| P1.A11 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 16 | 11 | ✅ |  |
| P1.A1 | eshop-on-web | PARTIAL | yes | reasoning | 7 | 0 | 42 | 12 | ✅ |  |
| P1.A2 | eshop-on-web | PARTIAL | yes | reasoning | 7 | 0 | 37 | 20 | ✅ |  |
| P1.A3 | eshop-on-web | PARTIAL | yes | reasoning | 10 | 0 | 49 | 22 | ✅ |  |
| P1.A4 | eshop-on-web | PARTIAL | yes | fast | 6 | 0 | 9 | 7 | ✅ |  |
| P1.A5 | eshop-on-web | PARTIAL | yes | fast | 7 | 0 | 7 | 5 | ✅ |  |
| P1.A6 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 27 | 19 | ✅ |  |
| P1.A7 | eshop-on-web | PARTIAL | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P1.A8 | eshop-on-web | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | eshop-on-web | PARTIAL | yes | reasoning | 8 | 0 | 39 | 22 | ✅ |  |
| P1.A10 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | eshop-on-web | PARTIAL | yes | reasoning | 7 | 0 | 24 | 11 | ✅ |  |
| P1.A1 | orchard | PARTIAL | yes | reasoning | 7 | 0 | 42 | 20 | ✅ |  |
| P1.A2 | orchard | PARTIAL | yes | reasoning | 7 | 0 | 29 | 19 | ✅ |  |
| P1.A3 | orchard | PARTIAL | yes | reasoning | 9 | 0 | 46 | 20 | ✅ |  |
| P1.A4 | orchard | PARTIAL | yes | fast | 6 | 0 | 11 | 9 | ✅ |  |
| P1.A5 | orchard | PARTIAL | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P1.A6 | orchard | PARTIAL | yes | reasoning | 7 | 0 | 27 | 19 | ✅ |  |
| P1.A7 | orchard | PARTIAL | yes | fast | 7 | 1 | 5 | 2 | ✅ |  |
| P1.A8 | orchard | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | orchard | PARTIAL | yes | reasoning | 7 | 0 | 21 | 17 | ✅ |  |
| P1.A10 | orchard | PARTIAL | yes | reasoning | 6 | 0 | 20 | 10 | ✅ |  |
| P1.A11 | orchard | PARTIAL | yes | reasoning | 6 | 0 | 22 | 10 | ✅ |  |
| P1.A1 | struts-examples | PARTIAL | yes | reasoning | 7 | 0 | 48 | 21 | ✅ |  |
| P1.A2 | struts-examples | PARTIAL | yes | reasoning | 7 | 0 | 35 | 19 | ✅ |  |
| P1.A3 | struts-examples | PARTIAL | yes | reasoning | 8 | 0 | 42 | 20 | ✅ |  |
| P1.A4 | struts-examples | PARTIAL | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P1.A5 | struts-examples | PARTIAL | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P1.A6 | struts-examples | PARTIAL | yes | reasoning | 5 | 0 | 21 | 12 | ✅ |  |
| P1.A7 | struts-examples | PARTIAL | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P1.A8 | struts-examples | PARTIAL | yes | reasoning | 3 | 0 | 4 | 4 | ✅ |  |
| P1.A9 | struts-examples | PARTIAL | yes | reasoning | 7 | 0 | 35 | 15 | ✅ |  |
| P1.A10 | struts-examples | PARTIAL | yes | reasoning | 5 | 0 | 14 | 11 | ✅ |  |
| P1.A11 | struts-examples | PARTIAL | yes | reasoning | 9 | 0 | 25 | 11 | ✅ |  |
| P1.A1 | ofbiz | PARTIAL | yes | reasoning | 8 | 0 | 44 | 20 | ✅ |  |
| P1.A2 | ofbiz | PARTIAL | yes | reasoning | 6 | 0 | 27 | 18 | ✅ |  |
| P1.A3 | ofbiz | PARTIAL | yes | reasoning | 11 | 1 | 51 | 22 | ✅ |  |
| P1.A4 | ofbiz | PARTIAL | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P1.A5 | ofbiz | PARTIAL | yes | fast | 7 | 0 | 9 | 4 | ✅ |  |
| P1.A6 | ofbiz | PARTIAL | yes | reasoning | 8 | 0 | 34 | 19 | ✅ |  |
| P1.A7 | ofbiz | PARTIAL | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P1.A8 | ofbiz | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | ofbiz | PARTIAL | yes | reasoning | 9 | 0 | 33 | 13 | ✅ |  |
| P1.A10 | ofbiz | PARTIAL | yes | reasoning | 6 | 0 | 19 | 13 | ✅ |  |
| P1.A11 | ofbiz | PARTIAL | yes | reasoning | 6 | 0 | 19 | 12 | ✅ |  |
| P1.A1 | webgoat | PARTIAL | yes | reasoning | 8 | 0 | 44 | 13 | ✅ |  |
| P1.A2 | webgoat | PARTIAL | yes | reasoning | 8 | 0 | 31 | 25 | ✅ |  |
| P1.A3 | webgoat | PARTIAL | yes | reasoning | 7 | 0 | 38 | 20 | ✅ |  |
| P1.A4 | webgoat | PARTIAL | yes | fast | 6 | 0 | 9 | 9 | ✅ |  |
| P1.A5 | webgoat | PARTIAL | yes | fast | 7 | 0 | 10 | 7 | ✅ |  |
| P1.A6 | webgoat | PARTIAL | yes | reasoning | 6 | 0 | 25 | 16 | ✅ |  |
| P1.A7 | webgoat | PARTIAL | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P1.A8 | webgoat | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | webgoat | PARTIAL | yes | reasoning | 7 | 0 | 29 | 19 | ✅ |  |
| P1.A10 | webgoat | PARTIAL | yes | reasoning | 6 | 0 | 20 | 13 | ✅ |  |
| P1.A11 | webgoat | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A1 | carddemo | PARTIAL | yes | reasoning | 8 | 0 | 46 | 20 | ✅ |  |
| P1.A2 | carddemo | PARTIAL | yes | reasoning | 7 | 0 | 33 | 24 | ✅ |  |
| P1.A3 | carddemo | PARTIAL | yes | reasoning | 9 | 0 | 46 | 18 | ✅ |  |
| P1.A4 | carddemo | PARTIAL | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P1.A5 | carddemo | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A6 | carddemo | PARTIAL | yes | reasoning | 5 | 0 | 21 | 18 | ✅ |  |
| P1.A7 | carddemo | SKIPPED_APPROVED | yes | fast | 7 | 1 | 5 | 4 | ✅ |  |
| P1.A8 | carddemo | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | carddemo | PARTIAL | yes | reasoning | 10 | 1 | 29 | 10 | ✅ |  |
| P1.A10 | carddemo | PARTIAL | yes | reasoning | 6 | 0 | 17 | 10 | ✅ |  |
| P1.A11 | carddemo | PARTIAL | yes | reasoning | 6 | 0 | 18 | 12 | ✅ |  |
| P1.A1 | mantisbt | PARTIAL | yes | reasoning | 7 | 0 | 48 | 21 | ✅ |  |
| P1.A2 | mantisbt | PARTIAL | yes | reasoning | 6 | 0 | 27 | 17 | ✅ |  |
| P1.A3 | mantisbt | PARTIAL | yes | reasoning | 9 | 0 | 43 | 17 | ✅ |  |
| P1.A4 | mantisbt | PARTIAL | yes | fast | 7 | 0 | 9 | 8 | ✅ |  |
| P1.A5 | mantisbt | PARTIAL | yes | fast | 6 | 0 | 12 | 5 | ✅ |  |
| P1.A6 | mantisbt | PARTIAL | yes | reasoning | 5 | 0 | 31 | 23 | ✅ |  |
| P1.A7 | mantisbt | PARTIAL | yes | fast | 8 | 2 | 5 | 5 | ✅ |  |
| P1.A8 | mantisbt | PARTIAL | yes | reasoning | 3 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | mantisbt | PARTIAL | yes | reasoning | 5 | 0 | 22 | 12 | ✅ |  |
| P1.A10 | mantisbt | PARTIAL | yes | reasoning | 7 | 0 | 22 | 14 | ✅ |  |
| P1.A11 | mantisbt | PARTIAL | yes | reasoning | 5 | 0 | 17 | 10 | ✅ |  |
| P1.A1 | bugzilla | PARTIAL | yes | reasoning | 7 | 0 | 43 | 24 | ✅ |  |
| P1.A2 | bugzilla | PARTIAL | yes | reasoning | 7 | 0 | 29 | 19 | ✅ |  |
| P1.A3 | bugzilla | PARTIAL | yes | reasoning | 9 | 0 | 48 | 19 | ✅ |  |
| P1.A4 | bugzilla | PARTIAL | yes | fast | 6 | 0 | 8 | 7 | ✅ |  |
| P1.A5 | bugzilla | PARTIAL | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P1.A6 | bugzilla | PARTIAL | yes | reasoning | 6 | 0 | 27 | 19 | ✅ |  |
| P1.A7 | bugzilla | PARTIAL | yes | fast | 7 | 1 | 7 | 4 | ✅ |  |
| P1.A8 | bugzilla | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | bugzilla | PARTIAL | yes | reasoning | 6 | 0 | 29 | 12 | ✅ |  |
| P1.A10 | bugzilla | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | bugzilla | PARTIAL | yes | reasoning | 5 | 0 | 19 | 10 | ✅ |  |
| P1.A1 | juice-shop | PARTIAL | yes | reasoning | 7 | 0 | 39 | 20 | ✅ |  |
| P1.A2 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 27 | 21 | ✅ |  |
| P1.A3 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 29 | 17 | ✅ |  |
| P1.A4 | juice-shop | PARTIAL | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P1.A5 | juice-shop | PARTIAL | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P1.A6 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 22 | 18 | ✅ |  |
| P1.A7 | juice-shop | PARTIAL | yes | fast | 7 | 0 | 6 | 1 | ✅ |  |
| P1.A8 | juice-shop | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | juice-shop | PARTIAL | yes | reasoning | 7 | 0 | 27 | 12 | ✅ |  |
| P1.A10 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 22 | 13 | ✅ |  |
| P1.A11 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 20 | 10 | ✅ |  |
| P2.A1 | PF1 | PARTIAL | yes | reasoning | 10 | 0 | 39 | 15 | ✅ |  |
| P2.A2 | PF1 | PARTIAL | yes | reasoning | 6 | 0 | 44 | 43 | ✅ |  |
| P2.A3 | PF1 | COMPLETE | yes | fast | 6 | 0 | 12 | 2 | ✅ |  |
| P2.A4 | PF1 | COMPLETE | yes | fast | 5 | 0 | 34 | 19 | ✅ |  |
| P2.A5 | PF1 | PARTIAL | yes | fast | 6 | 0 | 11 | 5 | ✅ |  |
| P2.A6 | PF1 | PARTIAL | yes | reasoning | 7 | 0 | 46 | 30 | ✅ |  |
| P2.A7 | PF1 | PARTIAL | yes | reasoning | 7 | 0 | 31 | 15 | ✅ |  |
| P3.A1 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P3.A2 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P3.A3 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P3.A4 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P3.A5 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P3.A6 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P3.A7 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P3.A8 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P3.A1 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A2 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A3 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A4 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A5 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A6 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A7 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A8 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 50 | 28 | ✅ |  |
| P3.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 21 | 13 | ✅ |  |
| P3.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 21 | 16 | ✅ |  |
| P3.A4 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 23 | 13 | ✅ |  |
| P3.A5 | django-realworld-example-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P3.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 33 | 19 | ✅ |  |
| P3.A7 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P3.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 26 | 12 | ✅ |  |
| P3.A1 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P3.A2 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P3.A3 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P3.A4 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P3.A5 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P3.A6 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P3.A7 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P3.A8 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P3.A1 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P3.A2 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P3.A3 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P3.A4 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P3.A5 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P3.A6 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P3.A7 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P3.A8 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P3.A1 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P3.A2 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P3.A3 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P3.A4 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P3.A5 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P3.A6 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P3.A7 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P3.A8 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P3.A1 | laravel58 | PARTIAL | yes | reasoning | 8 | 0 | 52 | 26 | ✅ |  |
| P3.A2 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 25 | 17 | ✅ |  |
| P3.A3 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 17 | 12 | ✅ |  |
| P3.A4 | laravel58 | PARTIAL | yes | reasoning | 4 | 0 | 17 | 15 | ✅ |  |
| P3.A5 | laravel58 | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 4 | ✅ |  |
| P3.A6 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 25 | 22 | ✅ |  |
| P3.A7 | laravel58 | COMPLETE | yes | fast | 5 | 0 | 8 | 3 | ✅ |  |
| P3.A8 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 22 | 14 | ✅ |  |
| P3.A1 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P3.A2 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P3.A3 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P3.A4 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P3.A5 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P3.A6 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P3.A7 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P3.A8 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P3.A1 | golang-example | PARTIAL | yes | reasoning | 7 | 0 | 52 | 28 | ✅ |  |
| P3.A2 | golang-example | PARTIAL | yes | reasoning | 4 | 0 | 20 | 13 | ✅ |  |
| P3.A3 | golang-example | PARTIAL | yes | reasoning | 4 | 0 | 12 | 9 | ✅ |  |
| P3.A4 | golang-example | PARTIAL | yes | reasoning | 7 | 0 | 29 | 17 | ✅ |  |
| P3.A5 | golang-example | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 5 | ✅ |  |
| P3.A6 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 20 | 17 | ✅ |  |
| P3.A7 | golang-example | COMPLETE | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P3.A8 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 27 | 12 | ✅ |  |
| P3.A1 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A2 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A3 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A4 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A5 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A6 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A7 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A8 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A1 | react-redux-realworld | PARTIAL | yes | reasoning | 7 | 0 | 45 | 15 | ✅ |  |
| P3.A2 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 23 | 14 | ✅ |  |
| P3.A3 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 17 | 11 | ✅ |  |
| P3.A4 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 14 | 10 | ✅ |  |
| P3.A5 | react-redux-realworld | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P3.A6 | react-redux-realworld | PARTIAL | yes | reasoning | 3 | 0 | 14 | 12 | ✅ |  |
| P3.A7 | react-redux-realworld | COMPLETE | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P3.A8 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 26 | 12 | ✅ |  |
| P3.A1 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P3.A2 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P3.A3 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P3.A4 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P3.A5 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P3.A6 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P3.A7 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P3.A8 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P3.A1 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P3.A2 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P3.A3 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P3.A4 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P3.A5 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P3.A6 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P3.A7 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P3.A8 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P3.A1 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P3.A2 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P3.A3 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P3.A4 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P3.A5 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P3.A6 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P3.A7 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P3.A8 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P3.A1 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P3.A2 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P3.A3 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P3.A4 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P3.A5 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P3.A6 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P3.A7 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P3.A8 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P3.A1 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P3.A2 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P3.A3 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P3.A4 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P3.A5 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P3.A6 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P3.A7 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P3.A8 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P3.A1 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P3.A2 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P3.A3 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P3.A4 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P3.A5 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P3.A6 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P3.A7 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P3.A8 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P3.A1 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P3.A2 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P3.A3 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P3.A4 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P3.A5 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P3.A6 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P3.A7 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P3.A8 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P3.A1 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P3.A2 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P3.A3 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P3.A4 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P3.A5 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P3.A6 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P3.A7 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P3.A8 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P3.A1 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P3.A2 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P3.A3 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P3.A4 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P3.A5 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P3.A6 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P3.A7 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P3.A8 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P4.A1 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P4.A2 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P4.A3 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P4.A4 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P4.A5 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P4.A6 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P4.A7 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P4.A8 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P4.A9 | spring-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-petclinic in the IA02 non-delivery register (Retain) |
| P4.A1 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A2 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A3 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A4 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A5 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A6 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A7 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A8 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A9 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A1 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 6 | 2 | ✅ |  |
| P4.A2 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 18 | 5 | ✅ |  |
| P4.A3 | django-realworld-example-app | PARTIAL | yes | coding | 8 | 0 | 21 | 9 | ✅ |  |
| P4.A4 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 12 | 2 | ✅ |  |
| P4.A5 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P4.A6 | django-realworld-example-app | COMPLETE | yes | fast | 7 | 1 | 7 | 4 | ✅ |  |
| P4.A7 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P4.A8 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 17 | 1 | ✅ |  |
| P4.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 24 | 17 | ✅ |  |
| P4.A1 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P4.A2 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P4.A3 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P4.A4 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P4.A5 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P4.A6 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P4.A7 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P4.A8 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P4.A9 | microblog | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put microblog in the IA02 non-delivery register (Retain) |
| P4.A1 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P4.A2 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P4.A3 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P4.A4 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P4.A5 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P4.A6 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P4.A7 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P4.A8 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P4.A9 | node-express-realworld-example-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put node-express-realworld-example-app in the IA02 non-delivery register (Retain) |
| P4.A1 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P4.A2 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P4.A3 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P4.A4 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P4.A5 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P4.A6 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P4.A7 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P4.A8 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P4.A9 | musicstore | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put musicstore in the IA02 non-delivery register (Retire) |
| P4.A1 | laravel58 | COMPLETE | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P4.A2 | laravel58 | COMPLETE | yes | fast | 6 | 0 | 19 | 4 | ✅ |  |
| P4.A3 | laravel58 | PARTIAL | yes | coding | 6 | 0 | 26 | 16 | ✅ |  |
| P4.A4 | laravel58 | COMPLETE | yes | fast | 6 | 0 | 6 | 1 | ✅ |  |
| P4.A5 | laravel58 | COMPLETE | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P4.A6 | laravel58 | PARTIAL | yes | fast | 7 | 1 | 17 | 6 | ✅ |  |
| P4.A7 | laravel58 | COMPLETE | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P4.A8 | laravel58 | COMPLETE | yes | fast | 6 | 0 | 13 | 2 | ✅ |  |
| P4.A9 | laravel58 | PARTIAL | yes | reasoning | 7 | 0 | 30 | 22 | ✅ |  |
| P4.A1 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P4.A2 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P4.A3 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P4.A4 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P4.A5 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P4.A6 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P4.A7 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P4.A8 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P4.A9 | sinatra | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put sinatra in the IA02 non-delivery register (Retain) |
| P4.A1 | golang-example | COMPLETE | yes | fast | 6 | 0 | 6 | 2 | ✅ |  |
| P4.A2 | golang-example | COMPLETE | yes | fast | 6 | 0 | 15 | 3 | ✅ |  |
| P4.A3 | golang-example | PARTIAL | yes | coding | 7 | 0 | 21 | 15 | ✅ |  |
| P4.A4 | golang-example | COMPLETE | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P4.A5 | golang-example | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A6 | golang-example | PARTIAL | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P4.A7 | golang-example | COMPLETE | yes | fast | 7 | 1 | 11 | 5 | ✅ |  |
| P4.A8 | golang-example | COMPLETE | yes | fast | 3 | 0 | 8 | 2 | ✅ |  |
| P4.A9 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 25 | 18 | ✅ |  |
| P4.A1 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A2 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A3 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A4 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A5 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A6 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A7 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A8 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A9 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A1 | react-redux-realworld | COMPLETE | yes | fast | 7 | 1 | 7 | 1 | ✅ |  |
| P4.A2 | react-redux-realworld | COMPLETE | yes | fast | 4 | 0 | 12 | 6 | ✅ |  |
| P4.A3 | react-redux-realworld | PARTIAL | yes | coding | 9 | 0 | 20 | 12 | ✅ |  |
| P4.A4 | react-redux-realworld | COMPLETE | yes | fast | 6 | 0 | 11 | 2 | ✅ |  |
| P4.A5 | react-redux-realworld | COMPLETE | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P4.A6 | react-redux-realworld | COMPLETE | yes | fast | 6 | 0 | 10 | 3 | ✅ |  |
| P4.A7 | react-redux-realworld | COMPLETE | yes | fast | 7 | 1 | 13 | 2 | ✅ |  |
| P4.A8 | react-redux-realworld | COMPLETE | yes | fast | 6 | 0 | 19 | 2 | ✅ |  |
| P4.A9 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 23 | 18 | ✅ |  |
| P4.A1 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P4.A2 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P4.A3 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P4.A4 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P4.A5 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P4.A6 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P4.A7 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P4.A8 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P4.A9 | eshop-on-web | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-on-web in the IA02 non-delivery register (Retain) |
| P4.A1 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P4.A2 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P4.A3 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P4.A4 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P4.A5 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P4.A6 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P4.A7 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P4.A8 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P4.A9 | orchard | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put orchard in the IA02 non-delivery register (Retain) |
| P4.A1 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P4.A2 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P4.A3 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P4.A4 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P4.A5 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P4.A6 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P4.A7 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P4.A8 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P4.A9 | struts-examples | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put struts-examples in the IA02 non-delivery register (Retain) |
| P4.A1 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P4.A2 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P4.A3 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P4.A4 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P4.A5 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P4.A6 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P4.A7 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P4.A8 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P4.A9 | ofbiz | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put ofbiz in the IA02 non-delivery register (Retain) |
| P4.A1 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P4.A2 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P4.A3 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P4.A4 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P4.A5 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P4.A6 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P4.A7 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P4.A8 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P4.A9 | webgoat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put webgoat in the IA02 non-delivery register (Retain) |
| P4.A1 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P4.A2 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P4.A3 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P4.A4 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P4.A5 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P4.A6 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P4.A7 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P4.A8 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P4.A9 | carddemo | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put carddemo in the IA02 non-delivery register (Retain) |
| P4.A1 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P4.A2 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P4.A3 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P4.A4 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P4.A5 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P4.A6 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P4.A7 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P4.A8 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P4.A9 | mantisbt | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put mantisbt in the IA02 non-delivery register (Retain) |
| P4.A1 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P4.A2 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P4.A3 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P4.A4 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P4.A5 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P4.A6 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P4.A7 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P4.A8 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P4.A9 | bugzilla | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put bugzilla in the IA02 non-delivery register (Retain) |
| P4.A1 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P4.A2 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P4.A3 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P4.A4 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P4.A5 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P4.A6 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P4.A7 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P4.A8 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
| P4.A9 | juice-shop | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put juice-shop in the IA02 non-delivery register (Retain) |
