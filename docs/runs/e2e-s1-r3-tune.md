# E2E agentic acceptance run `s1-r3-tune`

- **Job**: `job-1791886685-a4e2e2` — **COMPLETED**
- **Repositories**: `spring-petclinic`, `flask-tutorial`, `django-realworld-example-app`, `microblog`, `node-express-realworld-example-app`, `musicstore`, `laravel58`, `sinatra`, `golang-example`, `todomvc`, `react-redux-realworld`, `eshop-on-web`, `orchard`, `struts-examples`, `ofbiz`, `webgoat`, `carddemo`, `mantisbt`, `bugzilla`, `juice-shop`
- **Elapsed**: 1065 min 50 s; LLM cache mode `off` (record = every call live, responses recorded for replay)
- **Astra tiers**: {'reasoning': 'gpt-6-astra', 'coding': 'gpt-5.3-codex-PlayWright', 'fast': 'gpt-4.1-mini', 'fallback': 'gpt-5.4'}
- **Human surfaces**: review_mode=human; release-gate approvals and stakeholder answers were submitted over the API by a **scripted** reviewer/stakeholder (labelled as automation in every record).

## Result

**Agent success rate: 87.78%** (438/499 P1–P4 agent dispatches; threshold > 97.0%).

68 P3/P4 agent slots were **not admitted** because the authorized P2 release gate routed `flask-tutorial` (Retain), `laravel58` (Retire), `webgoat` (Retain), `carddemo` (Retain) to the non-delivery register — by design, no architecture or plan is produced for a non-delivery route. Counting those slots as failures would give 77.25%.

Success = artifact not FAILED **and** enriched by the live Astra agent loop (not seed fallback) **and** passes ContractValidator (envelope + payload schema + content hash).

| phase | ok / total |
|---|---|
| P1 Discovery | 220 / 220 |
| P2 Portfolio | 7 / 7 |
| P3 Architecture | 103 / 128 |
| P4 Planning | 108 / 144 |

- Tool calls: 8032; evidence ids cited: 4861; LLM findings: 2639; repair rounds: 37; failovers: 1
- Tokens: {'input': 37404100, 'output': 1780385, 'reasoning': 103071}

## Release gates

| phase | app | phase status | decision |
|---|---|---|---|
| P1 | node-express-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | flask-tutorial | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | microblog | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | spring-petclinic | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | django-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | musicstore | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | laravel58 | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | sinatra | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | golang-example | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | todomvc | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | react-redux-realworld | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | eshop-on-web | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | struts-examples | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | orchard | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | ofbiz | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | webgoat | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | carddemo | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | mantisbt | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | bugzilla | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | juice-shop | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P2 | PF1 | COMPLETED | AUTHORIZED |
| P3 | flask-tutorial | NOT_ADMITTED | — |
| P4 | flask-tutorial | NOT_ADMITTED | — |
| P3 | laravel58 | NOT_ADMITTED | — |
| P4 | laravel58 | NOT_ADMITTED | — |
| P3 | webgoat | NOT_ADMITTED | — |
| P4 | webgoat | NOT_ADMITTED | — |
| P3 | carddemo | NOT_ADMITTED | — |
| P4 | carddemo | NOT_ADMITTED | — |
| P3 | microblog | COMPLETED | CONDITIONAL_PLANNING |
| P3 | django-realworld-example-app | COMPLETED | CONDITIONAL_PLANNING |
| P3 | musicstore | COMPLETED | CONDITIONAL_PLANNING |
| P3 | node-express-realworld-example-app | COMPLETED | CONDITIONAL_PLANNING |
| P3 | spring-petclinic | COMPLETED | CONDITIONAL_PLANNING |
| P4 | node-express-realworld-example-app | COMPLETED | SCOPED_PREPARATION |
| P4 | django-realworld-example-app | COMPLETED | SCOPED_PREPARATION |
| P4 | microblog | COMPLETED | SCOPED_PREPARATION |
| P4 | spring-petclinic | COMPLETED | SCOPED_PREPARATION |
| P3 | sinatra | COMPLETED | CONDITIONAL_PLANNING |
| P4 | musicstore | COMPLETED | SCOPED_PREPARATION |
| P3 | golang-example | COMPLETED | CONDITIONAL_PLANNING |
| P3 | todomvc | COMPLETED | CONDITIONAL_PLANNING |
| P3 | react-redux-realworld | COMPLETED | CONDITIONAL_PLANNING |
| P3 | eshop-on-web | COMPLETED | CONDITIONAL_PLANNING |
| P4 | golang-example | COMPLETED | SCOPED_PREPARATION |
| P4 | sinatra | COMPLETED | SCOPED_PREPARATION |
| P4 | react-redux-realworld | COMPLETED | SCOPED_PREPARATION |
| P3 | orchard | COMPLETED | CONDITIONAL_PLANNING |
| P4 | todomvc | COMPLETED | SCOPED_PREPARATION |
| P3 | struts-examples | COMPLETED | — |
| P4 | eshop-on-web | COMPLETED | SCOPED_PREPARATION |
| P3 | ofbiz | COMPLETED | — |
| P3 | mantisbt | COMPLETED | — |
| P3 | bugzilla | COMPLETED | — |
| P3 | juice-shop | COMPLETED | CONDITIONAL_PLANNING |
| P4 | orchard | COMPLETED | SCOPED_PREPARATION |
| P4 | juice-shop | COMPLETED | SCOPED_PREPARATION |

Reviews: 59 (decided by `scripted-reviewer`); stakeholder questions: 143 (143 answered).

## Per-agent results

| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| P1.A1 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 38 | 17 | ✅ |  |
| P1.A2 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 29 | 22 | ✅ |  |
| P1.A3 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 29 | 20 | ✅ |  |
| P1.A4 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 10 | 6 | ✅ |  |
| P1.A5 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 8 | 8 | ✅ |  |
| P1.A6 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 24 | 19 | ✅ |  |
| P1.A7 | spring-petclinic | PARTIAL | yes | fast | 7 | 0 | 9 | 3 | ✅ |  |
| P1.A8 | spring-petclinic | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 27 | 17 | ✅ |  |
| P1.A10 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 18 | 13 | ✅ |  |
| P1.A11 | spring-petclinic | PARTIAL | yes | reasoning | 4 | 0 | 13 | 12 | ✅ |  |
| P1.A1 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 0 | 25 | 18 | ✅ |  |
| P1.A2 | flask-tutorial | PARTIAL | yes | reasoning | 3 | 0 | 13 | 9 | ✅ |  |
| P1.A3 | flask-tutorial | PARTIAL | yes | reasoning | 3 | 0 | 10 | 9 | ✅ |  |
| P1.A4 | flask-tutorial | PARTIAL | yes | fast | 6 | 0 | 8 | 6 | ✅ |  |
| P1.A5 | flask-tutorial | PARTIAL | yes | fast | 7 | 0 | 8 | 6 | ✅ |  |
| P1.A6 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 0 | 20 | 16 | ✅ |  |
| P1.A7 | flask-tutorial | PARTIAL | yes | fast | 6 | 0 | 10 | 7 | ✅ |  |
| P1.A8 | flask-tutorial | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 1 | 20 | 11 | ✅ |  |
| P1.A10 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 0 | 15 | 11 | ✅ |  |
| P1.A11 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 14 | 10 | ✅ |  |
| P1.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 34 | 16 | ✅ |  |
| P1.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 24 | 14 | ✅ |  |
| P1.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 26 | 14 | ✅ |  |
| P1.A4 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P1.A5 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 8 | 6 | ✅ |  |
| P1.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 18 | 14 | ✅ |  |
| P1.A7 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 27 | 21 | ✅ |  |
| P1.A10 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 21 | 11 | ✅ |  |
| P1.A11 | django-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 13 | 11 | ✅ |  |
| P1.A1 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 38 | 23 | ✅ |  |
| P1.A2 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 25 | 20 | ✅ |  |
| P1.A3 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 22 | 18 | ✅ |  |
| P1.A4 | microblog | PARTIAL | yes | fast | 6 | 0 | 8 | 7 | ✅ |  |
| P1.A5 | microblog | PARTIAL | yes | fast | 6 | 0 | 10 | 8 | ✅ |  |
| P1.A6 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 25 | 23 | ✅ |  |
| P1.A7 | microblog | PARTIAL | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P1.A8 | microblog | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | microblog | PARTIAL | yes | reasoning | 4 | 0 | 27 | 14 | ✅ |  |
| P1.A10 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 18 | 12 | ✅ |  |
| P1.A11 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 14 | 9 | ✅ |  |
| P1.A1 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 38 | 24 | ✅ |  |
| P1.A2 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 26 | 23 | ✅ |  |
| P1.A3 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 36 | 27 | ✅ |  |
| P1.A4 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P1.A5 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P1.A6 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 18 | 18 | ✅ |  |
| P1.A7 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P1.A8 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 27 | 22 | ✅ |  |
| P1.A10 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 14 | 11 | ✅ |  |
| P1.A1 | musicstore | PARTIAL | yes | reasoning | 8 | 0 | 51 | 20 | ✅ |  |
| P1.A2 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 25 | 20 | ✅ |  |
| P1.A3 | musicstore | PARTIAL | yes | reasoning | 7 | 0 | 31 | 20 | ✅ |  |
| P1.A4 | musicstore | PARTIAL | yes | fast | 6 | 0 | 10 | 4 | ✅ |  |
| P1.A5 | musicstore | PARTIAL | yes | fast | 6 | 0 | 12 | 10 | ✅ |  |
| P1.A6 | musicstore | PARTIAL | yes | reasoning | 8 | 0 | 33 | 24 | ✅ |  |
| P1.A7 | musicstore | PARTIAL | yes | fast | 7 | 0 | 10 | 8 | ✅ |  |
| P1.A8 | musicstore | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 24 | 12 | ✅ |  |
| P1.A10 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 17 | 10 | ✅ |  |
| P1.A11 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 16 | 9 | ✅ |  |
| P1.A1 | laravel58 | PARTIAL | yes | reasoning | 6 | 0 | 32 | 17 | ✅ |  |
| P1.A2 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 26 | 22 | ✅ |  |
| P1.A3 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 23 | 18 | ✅ |  |
| P1.A4 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P1.A5 | laravel58 | PARTIAL | yes | fast | 7 | 0 | 10 | 4 | ✅ |  |
| P1.A6 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 22 | 19 | ✅ |  |
| P1.A7 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P1.A8 | laravel58 | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 32 | 19 | ✅ |  |
| P1.A10 | laravel58 | PARTIAL | yes | reasoning | 6 | 0 | 17 | 11 | ✅ |  |
| P1.A11 | laravel58 | PARTIAL | yes | reasoning | 4 | 0 | 12 | 10 | ✅ |  |
| P1.A1 | sinatra | PARTIAL | yes | reasoning | 6 | 0 | 30 | 20 | ✅ |  |
| P1.A2 | sinatra | PARTIAL | yes | reasoning | 3 | 0 | 10 | 10 | ✅ |  |
| P1.A3 | sinatra | PARTIAL | yes | reasoning | 4 | 1 | 10 | 10 | ✅ |  |
| P1.A4 | sinatra | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A5 | sinatra | PARTIAL | yes | fast | 6 | 0 | 8 | 3 | ✅ |  |
| P1.A6 | sinatra | PARTIAL | yes | reasoning | 3 | 0 | 10 | 11 | ✅ |  |
| P1.A7 | sinatra | PARTIAL | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P1.A8 | sinatra | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | sinatra | PARTIAL | yes | reasoning | 5 | 1 | 10 | 9 | ✅ |  |
| P1.A10 | sinatra | PARTIAL | yes | reasoning | 5 | 0 | 12 | 10 | ✅ |  |
| P1.A11 | sinatra | PARTIAL | yes | reasoning | 5 | 0 | 13 | 10 | ✅ |  |
| P1.A1 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 33 | 20 | ✅ |  |
| P1.A2 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 18 | 14 | ✅ |  |
| P1.A3 | golang-example | PARTIAL | yes | reasoning | 4 | 0 | 19 | 14 | ✅ |  |
| P1.A4 | golang-example | PARTIAL | yes | fast | 6 | 0 | 5 | 5 | ✅ |  |
| P1.A5 | golang-example | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A6 | golang-example | PARTIAL | yes | reasoning | 4 | 0 | 17 | 13 | ✅ |  |
| P1.A7 | golang-example | SKIPPED_APPROVED | yes | fast | 7 | 1 | 5 | 5 | ✅ |  |
| P1.A8 | golang-example | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 22 | 13 | ✅ |  |
| P1.A10 | golang-example | PARTIAL | yes | reasoning | 7 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 17 | 13 | ✅ |  |
| P1.A1 | todomvc | PARTIAL | yes | reasoning | 8 | 0 | 49 | 17 | ✅ |  |
| P1.A2 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 26 | 19 | ✅ |  |
| P1.A3 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 28 | 17 | ✅ |  |
| P1.A4 | todomvc | PARTIAL | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P1.A5 | todomvc | PARTIAL | yes | fast | 6 | 0 | 13 | 5 | ✅ |  |
| P1.A6 | todomvc | PARTIAL | yes | reasoning | 5 | 0 | 23 | 13 | ✅ |  |
| P1.A7 | todomvc | PARTIAL | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P1.A8 | todomvc | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 23 | 13 | ✅ |  |
| P1.A10 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 21 | 12 | ✅ |  |
| P1.A11 | todomvc | PARTIAL | yes | reasoning | 5 | 0 | 13 | 10 | ✅ |  |
| P1.A1 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 29 | 14 | ✅ |  |
| P1.A2 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 22 | 18 | ✅ |  |
| P1.A3 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 22 | 12 | ✅ |  |
| P1.A4 | react-redux-realworld | PARTIAL | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P1.A5 | react-redux-realworld | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A6 | react-redux-realworld | PARTIAL | yes | reasoning | 4 | 0 | 17 | 16 | ✅ |  |
| P1.A7 | react-redux-realworld | PARTIAL | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P1.A8 | react-redux-realworld | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 34 | 20 | ✅ |  |
| P1.A10 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 16 | 11 | ✅ |  |
| P1.A11 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 16 | 12 | ✅ |  |
| P1.A1 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 38 | 15 | ✅ |  |
| P1.A2 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 32 | 25 | ✅ |  |
| P1.A3 | eshop-on-web | PARTIAL | yes | reasoning | 8 | 0 | 43 | 26 | ✅ |  |
| P1.A4 | eshop-on-web | PARTIAL | yes | fast | 6 | 0 | 12 | 8 | ✅ |  |
| P1.A5 | eshop-on-web | PARTIAL | yes | fast | 6 | 0 | 7 | 7 | ✅ |  |
| P1.A6 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 27 | 19 | ✅ |  |
| P1.A7 | eshop-on-web | PARTIAL | yes | fast | 7 | 0 | 7 | 4 | ✅ |  |
| P1.A8 | eshop-on-web | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 36 | 21 | ✅ |  |
| P1.A10 | eshop-on-web | PARTIAL | yes | reasoning | 7 | 0 | 22 | 10 | ✅ |  |
| P1.A11 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 18 | 11 | ✅ |  |
| P1.A1 | orchard | PARTIAL | yes | reasoning | 7 | 0 | 37 | 23 | ✅ |  |
| P1.A2 | orchard | PARTIAL | yes | reasoning | 6 | 0 | 24 | 19 | ✅ |  |
| P1.A3 | orchard | PARTIAL | yes | reasoning | 10 | 0 | 49 | 26 | ✅ |  |
| P1.A4 | orchard | PARTIAL | yes | fast | 6 | 0 | 11 | 2 | ✅ |  |
| P1.A5 | orchard | PARTIAL | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P1.A6 | orchard | PARTIAL | yes | reasoning | 8 | 0 | 33 | 28 | ✅ |  |
| P1.A7 | orchard | PARTIAL | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P1.A8 | orchard | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | orchard | PARTIAL | yes | reasoning | 7 | 0 | 27 | 21 | ✅ |  |
| P1.A10 | orchard | PARTIAL | yes | reasoning | 7 | 0 | 21 | 12 | ✅ |  |
| P1.A11 | orchard | PARTIAL | yes | reasoning | 5 | 0 | 20 | 14 | ✅ |  |
| P1.A1 | struts-examples | PARTIAL | yes | reasoning | 6 | 0 | 35 | 18 | ✅ |  |
| P1.A2 | struts-examples | PARTIAL | yes | reasoning | 8 | 0 | 37 | 19 | ✅ |  |
| P1.A3 | struts-examples | PARTIAL | yes | reasoning | 6 | 0 | 31 | 18 | ✅ |  |
| P1.A4 | struts-examples | PARTIAL | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P1.A5 | struts-examples | PARTIAL | yes | fast | 7 | 0 | 9 | 5 | ✅ |  |
| P1.A6 | struts-examples | PARTIAL | yes | reasoning | 6 | 0 | 27 | 14 | ✅ |  |
| P1.A7 | struts-examples | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A8 | struts-examples | PARTIAL | yes | reasoning | 3 | 0 | 4 | 3 | ✅ |  |
| P1.A9 | struts-examples | PARTIAL | yes | reasoning | 7 | 0 | 37 | 19 | ✅ |  |
| P1.A10 | struts-examples | PARTIAL | yes | reasoning | 6 | 0 | 20 | 11 | ✅ |  |
| P1.A11 | struts-examples | PARTIAL | yes | reasoning | 8 | 0 | 22 | 14 | ✅ |  |
| P1.A1 | ofbiz | PARTIAL | yes | reasoning | 8 | 0 | 42 | 22 | ✅ |  |
| P1.A2 | ofbiz | PARTIAL | yes | reasoning | 7 | 0 | 35 | 31 | ✅ |  |
| P1.A3 | ofbiz | PARTIAL | yes | reasoning | 9 | 0 | 42 | 19 | ✅ |  |
| P1.A4 | ofbiz | PARTIAL | yes | fast | 6 | 0 | 17 | 14 | ✅ |  |
| P1.A5 | ofbiz | PARTIAL | yes | fast | 7 | 0 | 6 | 1 | ✅ |  |
| P1.A6 | ofbiz | PARTIAL | yes | reasoning | 8 | 0 | 30 | 20 | ✅ |  |
| P1.A7 | ofbiz | PARTIAL | yes | fast | 7 | 0 | 6 | 1 | ✅ |  |
| P1.A8 | ofbiz | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | ofbiz | PARTIAL | yes | reasoning | 7 | 0 | 28 | 13 | ✅ |  |
| P1.A10 | ofbiz | PARTIAL | yes | reasoning | 8 | 0 | 30 | 13 | ✅ |  |
| P1.A11 | ofbiz | PARTIAL | yes | reasoning | 6 | 0 | 23 | 12 | ✅ |  |
| P1.A1 | webgoat | PARTIAL | yes | reasoning | 7 | 0 | 38 | 22 | ✅ |  |
| P1.A2 | webgoat | PARTIAL | yes | reasoning | 7 | 0 | 36 | 22 | ✅ |  |
| P1.A3 | webgoat | PARTIAL | yes | reasoning | 7 | 0 | 32 | 17 | ✅ |  |
| P1.A4 | webgoat | PARTIAL | yes | fast | 6 | 0 | 12 | 11 | ✅ |  |
| P1.A5 | webgoat | PARTIAL | yes | fast | 7 | 0 | 6 | 4 | ✅ |  |
| P1.A6 | webgoat | PARTIAL | yes | reasoning | 6 | 0 | 23 | 22 | ✅ |  |
| P1.A7 | webgoat | PARTIAL | yes | fast | 7 | 0 | 7 | 2 | ✅ |  |
| P1.A8 | webgoat | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | webgoat | PARTIAL | yes | reasoning | 7 | 0 | 32 | 19 | ✅ |  |
| P1.A10 | webgoat | PARTIAL | yes | reasoning | 6 | 0 | 24 | 12 | ✅ |  |
| P1.A11 | webgoat | PARTIAL | yes | reasoning | 5 | 0 | 13 | 11 | ✅ |  |
| P1.A1 | carddemo | PARTIAL | yes | reasoning | 7 | 0 | 44 | 20 | ✅ |  |
| P1.A2 | carddemo | PARTIAL | yes | reasoning | 6 | 0 | 24 | 19 | ✅ |  |
| P1.A3 | carddemo | PARTIAL | yes | reasoning | 9 | 0 | 37 | 21 | ✅ |  |
| P1.A4 | carddemo | PARTIAL | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P1.A5 | carddemo | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P1.A6 | carddemo | PARTIAL | yes | reasoning | 5 | 0 | 21 | 16 | ✅ |  |
| P1.A7 | carddemo | SKIPPED_APPROVED | yes | fast | 7 | 1 | 5 | 3 | ✅ |  |
| P1.A8 | carddemo | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | carddemo | PARTIAL | yes | reasoning | 10 | 1 | 33 | 27 | ✅ |  |
| P1.A10 | carddemo | PARTIAL | yes | reasoning | 7 | 0 | 17 | 11 | ✅ |  |
| P1.A11 | carddemo | PARTIAL | yes | reasoning | 4 | 0 | 11 | 10 | ✅ |  |
| P1.A1 | mantisbt | PARTIAL | yes | reasoning | 7 | 0 | 45 | 26 | ✅ |  |
| P1.A2 | mantisbt | PARTIAL | yes | reasoning | 6 | 0 | 27 | 21 | ✅ |  |
| P1.A3 | mantisbt | PARTIAL | yes | reasoning | 8 | 0 | 40 | 23 | ✅ |  |
| P1.A4 | mantisbt | PARTIAL | yes | fast | 7 | 0 | 9 | 6 | ✅ |  |
| P1.A5 | mantisbt | PARTIAL | yes | fast | 7 | 1 | 8 | 4 | ✅ |  |
| P1.A6 | mantisbt | PARTIAL | yes | reasoning | 6 | 0 | 36 | 26 | ✅ |  |
| P1.A7 | mantisbt | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A8 | mantisbt | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | mantisbt | PARTIAL | yes | reasoning | 7 | 0 | 28 | 18 | ✅ |  |
| P1.A10 | mantisbt | PARTIAL | yes | reasoning | 6 | 0 | 20 | 10 | ✅ |  |
| P1.A11 | mantisbt | PARTIAL | yes | reasoning | 7 | 0 | 24 | 14 | ✅ |  |
| P1.A1 | bugzilla | PARTIAL | yes | reasoning | 7 | 0 | 46 | 29 | ✅ |  |
| P1.A2 | bugzilla | PARTIAL | yes | reasoning | 6 | 0 | 25 | 19 | ✅ |  |
| P1.A3 | bugzilla | PARTIAL | yes | reasoning | 8 | 0 | 49 | 26 | ✅ |  |
| P1.A4 | bugzilla | PARTIAL | yes | fast | 6 | 0 | 8 | 9 | ✅ |  |
| P1.A5 | bugzilla | PARTIAL | yes | fast | 6 | 0 | 8 | 8 | ✅ |  |
| P1.A6 | bugzilla | PARTIAL | yes | reasoning | 6 | 0 | 27 | 21 | ✅ |  |
| P1.A7 | bugzilla | PARTIAL | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P1.A8 | bugzilla | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | bugzilla | PARTIAL | yes | reasoning | 7 | 0 | 28 | 18 | ✅ |  |
| P1.A10 | bugzilla | PARTIAL | yes | reasoning | 6 | 0 | 18 | 11 | ✅ |  |
| P1.A11 | bugzilla | PARTIAL | yes | reasoning | 5 | 0 | 13 | 8 | ✅ |  |
| P1.A1 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 34 | 19 | ✅ |  |
| P1.A2 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 28 | 25 | ✅ |  |
| P1.A3 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 30 | 18 | ✅ |  |
| P1.A4 | juice-shop | PARTIAL | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P1.A5 | juice-shop | PARTIAL | yes | fast | 7 | 0 | 9 | 5 | ✅ |  |
| P1.A6 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 22 | 20 | ✅ |  |
| P1.A7 | juice-shop | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A8 | juice-shop | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 24 | 10 | ✅ |  |
| P1.A10 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 21 | 11 | ✅ |  |
| P1.A11 | juice-shop | PARTIAL | yes | reasoning | 7 | 0 | 24 | 14 | ✅ |  |
| P2.A1 | PF1 | PARTIAL | yes | reasoning | 9 | 0 | 35 | 29 | ✅ |  |
| P2.A2 | PF1 | PARTIAL | yes | reasoning | 9 | 0 | 40 | 27 | ✅ |  |
| P2.A3 | PF1 | COMPLETE | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P2.A4 | PF1 | COMPLETE | yes | fast | 7 | 1 | 8 | 2 | ✅ |  |
| P2.A5 | PF1 | COMPLETE | yes | fast | 6 | 0 | 11 | 2 | ✅ |  |
| P2.A6 | PF1 | PARTIAL | yes | reasoning | 10 | 0 | 60 | 23 | ✅ |  |
| P2.A7 | PF1 | PARTIAL | yes | reasoning | 6 | 0 | 26 | 13 | ✅ |  |
| P3.A1 | spring-petclinic | PARTIAL | yes | reasoning | 9 | 0 | 49 | 30 | ✅ |  |
| P3.A2 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 29 | 16 | ✅ |  |
| P3.A3 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 21 | 15 | ✅ |  |
| P3.A4 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 25 | 19 | ✅ |  |
| P3.A5 | spring-petclinic | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P3.A6 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 28 | 15 | ✅ |  |
| P3.A7 | spring-petclinic | COMPLETE | yes | fast | 7 | 1 | 11 | 4 | ✅ |  |
| P3.A8 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 28 | 15 | ✅ |  |
| P3.A1 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A2 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A3 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A4 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A5 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A6 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A7 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A8 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P3.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 49 | 29 | ✅ |  |
| P3.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 22 | 16 | ✅ |  |
| P3.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 20 | 16 | ✅ |  |
| P3.A4 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 15 | 13 | ✅ |  |
| P3.A5 | django-realworld-example-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P3.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 22 | 14 | ✅ |  |
| P3.A7 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P3.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 25 | 15 | ✅ |  |
| P3.A1 | microblog | PARTIAL | yes | reasoning | 7 | 0 | 43 | 22 | ✅ |  |
| P3.A2 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 23 | 17 | ✅ |  |
| P3.A3 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 19 | 12 | ✅ |  |
| P3.A4 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 32 | 20 | ✅ |  |
| P3.A5 | microblog | SKIPPED_APPROVED | yes | fast | 7 | 0 | 6 | 4 | ✅ |  |
| P3.A6 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 26 | 19 | ✅ |  |
| P3.A7 | microblog | PARTIAL | yes | fast | 6 | 0 | 10 | 4 | ✅ |  |
| P3.A8 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 33 | 14 | ✅ |  |
| P3.A1 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 9 | 0 | 56 | 25 | ✅ |  |
| P3.A2 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 26 | 15 | ✅ |  |
| P3.A3 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 20 | 15 | ✅ |  |
| P3.A4 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 22 | 16 | ✅ |  |
| P3.A5 | node-express-realworld-example-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P3.A6 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 23 | 22 | ✅ |  |
| P3.A7 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P3.A8 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 29 | 16 | ✅ |  |
| P3.A1 | musicstore | PARTIAL | yes | reasoning | 10 | 1 | 57 | 32 | ✅ |  |
| P3.A2 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 18 | 14 | ✅ |  |
| P3.A3 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 21 | 15 | ✅ |  |
| P3.A4 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 18 | 14 | ✅ |  |
| P3.A5 | musicstore | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P3.A6 | musicstore | PARTIAL | yes | reasoning | 7 | 0 | 32 | 18 | ✅ |  |
| P3.A7 | musicstore | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P3.A8 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 25 | 13 | ✅ |  |
| P3.A1 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A2 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A3 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A4 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A5 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A6 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A7 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A8 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A1 | sinatra | PARTIAL | yes | reasoning | 7 | 0 | 43 | 20 | ✅ |  |
| P3.A2 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 14 | 9 | ✅ |  |
| P3.A3 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 14 | 10 | ✅ |  |
| P3.A4 | sinatra | PARTIAL | yes | reasoning | 3 | 0 | 9 | 7 | ✅ |  |
| P3.A5 | sinatra | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P3.A6 | sinatra | PARTIAL | yes | reasoning | 3 | 0 | 10 | 9 | ✅ |  |
| P3.A7 | sinatra | PARTIAL | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P3.A8 | sinatra | PARTIAL | yes | reasoning | 5 | 0 | 24 | 14 | ✅ |  |
| P3.A1 | golang-example | PARTIAL | yes | reasoning | 7 | 0 | 45 | 28 | ✅ |  |
| P3.A2 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 21 | 16 | ✅ |  |
| P3.A3 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 18 | 14 | ✅ |  |
| P3.A4 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 21 | 13 | ✅ |  |
| P3.A5 | golang-example | SKIPPED_APPROVED | yes | fast | 6 | 0 | 9 | 5 | ✅ |  |
| P3.A6 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 24 | 19 | ✅ |  |
| P3.A7 | golang-example | COMPLETE | yes | fast | 5 | 0 | 13 | 4 | ✅ |  |
| P3.A8 | golang-example | PARTIAL | yes | reasoning | 6 | 1 | 24 | 16 | ✅ |  |
| P3.A1 | todomvc | PARTIAL | yes | reasoning | 9 | 0 | 59 | 29 | ✅ |  |
| P3.A2 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 28 | 17 | ✅ |  |
| P3.A3 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 22 | 16 | ✅ |  |
| P3.A4 | todomvc | PARTIAL | yes | reasoning | 5 | 0 | 21 | 14 | ✅ |  |
| P3.A5 | todomvc | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P3.A6 | todomvc | PARTIAL | yes | reasoning | 7 | 0 | 26 | 17 | ✅ |  |
| P3.A7 | todomvc | PARTIAL | yes | fast | 6 | 0 | 11 | 4 | ✅ |  |
| P3.A8 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 29 | 10 | ✅ |  |
| P3.A1 | react-redux-realworld | PARTIAL | yes | reasoning | 7 | 0 | 46 | 23 | ✅ |  |
| P3.A2 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 21 | 16 | ✅ |  |
| P3.A3 | react-redux-realworld | PARTIAL | yes | reasoning | 4 | 0 | 17 | 9 | ✅ |  |
| P3.A4 | react-redux-realworld | PARTIAL | yes | reasoning | 4 | 0 | 13 | 11 | ✅ |  |
| P3.A5 | react-redux-realworld | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 4 | ✅ |  |
| P3.A6 | react-redux-realworld | PARTIAL | yes | reasoning | 4 | 0 | 15 | 11 | ✅ |  |
| P3.A7 | react-redux-realworld | COMPLETE | yes | fast | 7 | 1 | 7 | 2 | ✅ |  |
| P3.A8 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 24 | 10 | ✅ |  |
| P3.A1 | eshop-on-web | PARTIAL | yes | reasoning | 8 | 0 | 42 | 29 | ✅ |  |
| P3.A2 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 28 | 23 | ✅ |  |
| P3.A3 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 24 | 17 | ✅ |  |
| P3.A4 | eshop-on-web | PARTIAL | yes | reasoning | 7 | 0 | 26 | 17 | ✅ |  |
| P3.A5 | eshop-on-web | SKIPPED_APPROVED | yes | fast | 6 | 0 | 10 | 5 | ✅ |  |
| P3.A6 | eshop-on-web | PARTIAL | yes | reasoning | 7 | 0 | 34 | 18 | ✅ |  |
| P3.A7 | eshop-on-web | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P3.A8 | eshop-on-web | PARTIAL | yes | reasoning | 7 | 0 | 29 | 16 | ✅ |  |
| P3.A1 | orchard | PARTIAL | yes | reasoning | 9 | 0 | 49 | 27 | ✅ |  |
| P3.A2 | orchard | PARTIAL | yes | reasoning | 9 | 0 | 28 | 17 | ✅ |  |
| P3.A3 | orchard | PARTIAL | yes | reasoning | 5 | 0 | 22 | 19 | ✅ |  |
| P3.A4 | orchard | PARTIAL | yes | reasoning | 6 | 0 | 27 | 19 | ✅ |  |
| P3.A5 | orchard | SKIPPED_APPROVED | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P3.A6 | orchard | PARTIAL | yes | reasoning | 9 | 0 | 45 | 23 | ✅ |  |
| P3.A7 | orchard | PARTIAL | yes | fast | 6 | 0 | 12 | 1 | ✅ |  |
| P3.A8 | orchard | PARTIAL | yes | reasoning | 7 | 0 | 29 | 16 | ✅ |  |
| P3.A1 | struts-examples | PARTIAL | yes | reasoning | 10 | 0 | 71 | 30 | ✅ |  |
| P3.A2 | struts-examples | PARTIAL | yes | reasoning | 7 | 0 | 30 | 21 | ✅ |  |
| P3.A3 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | struts-examples | PARTIAL | yes | reasoning | 7 | 0 | 32 | 20 | ✅ |  |
| P3.A5 | struts-examples | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P3.A6 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | struts-examples | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | ofbiz | PARTIAL | yes | reasoning | 10 | 0 | 58 | 30 | ✅ |  |
| P3.A2 | ofbiz | PARTIAL | no |  |  | 0 | 0 | 0 | ❌ | not enriched (seed-fallback: LLMConfigError: gpt-6-astra: auth failed (403)) |
| P3.A3 | ofbiz | PARTIAL | no |  |  | 0 | 0 | 0 | ❌ | not enriched (seed-fallback: LLMConfigError: gpt-6-astra: auth failed (403)) |
| P3.A4 | ofbiz | PARTIAL | no |  |  | 0 | 0 | 0 | ❌ | not enriched (seed-fallback: LLMConfigError: gpt-6-astra: auth failed (403)) |
| P3.A5 | ofbiz | SKIPPED_APPROVED | no |  |  | 0 | 0 | 0 | ❌ | not enriched (seed-fallback: LLMConfigError: gpt-4.1-mini: auth failed (403)) |
| P3.A6 | ofbiz | PARTIAL | no |  |  | 0 | 0 | 0 | ❌ | not enriched (seed-fallback: LLMConfigError: gpt-6-astra: auth failed (403)) |
| P3.A7 | ofbiz | PARTIAL | no |  |  | 0 | 0 | 0 | ❌ | not enriched (seed-fallback: LLMConfigError: gpt-4.1-mini: auth failed (403)) |
| P3.A8 | ofbiz | PARTIAL | no |  |  | 0 | 0 | 0 | ❌ | not enriched (seed-fallback: LLMConfigError: gpt-6-astra: auth failed (403)) |
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
| P3.A1 | mantisbt | PARTIAL | yes | reasoning | 8 | 0 | 48 | 25 | ✅ |  |
| P3.A2 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | mantisbt | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | bugzilla | PARTIAL | yes | reasoning | 9 | 0 | 55 | 25 | ✅ |  |
| P3.A2 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A3 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A4 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A5 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A6 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A7 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A8 | bugzilla | NOT_DISPATCHED | no |  |  | 0 | 0 | 0 | ❌ | no artifact published |
| P3.A1 | juice-shop | PARTIAL | yes | reasoning | 9 | 0 | 58 | 34 | ✅ |  |
| P3.A2 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 28 | 15 | ✅ |  |
| P3.A3 | juice-shop | PARTIAL | yes | reasoning | 5 | 0 | 27 | 14 | ✅ |  |
| P3.A4 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 24 | 14 | ✅ |  |
| P3.A5 | juice-shop | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P3.A6 | juice-shop | PARTIAL | yes | reasoning | 8 | 0 | 36 | 20 | ✅ |  |
| P3.A7 | juice-shop | PARTIAL | yes | fast | 6 | 0 | 10 | 1 | ✅ |  |
| P3.A8 | juice-shop | PARTIAL | yes | reasoning | 5 | 0 | 21 | 13 | ✅ |  |
| P4.A1 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P4.A2 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 13 | 1 | ✅ |  |
| P4.A3 | spring-petclinic | PARTIAL | yes | coding | 6 | 1 | 17 | 13 | ✅ |  |
| P4.A4 | spring-petclinic | COMPLETE | yes | fast | 4 | 0 | 9 | 2 | ✅ |  |
| P4.A5 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P4.A6 | spring-petclinic | COMPLETE | yes | fast | 7 | 1 | 9 | 4 | ✅ |  |
| P4.A7 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 12 | 1 | ✅ |  |
| P4.A8 | spring-petclinic | COMPLETE | yes | fast | 2 | 0 | 3 | 2 | ✅ |  |
| P4.A9 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 24 | 17 | ✅ |  |
| P4.A1 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A2 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A3 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A4 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A5 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A6 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A7 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A8 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A9 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retain) |
| P4.A1 | django-realworld-example-app | COMPLETE | yes | fast | 5 | 1 | 3 | 2 | ✅ |  |
| P4.A2 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P4.A3 | django-realworld-example-app | PARTIAL | yes | coding | 10 | 1 | 18 | 9 | ✅ |  |
| P4.A4 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 11 | 2 | ✅ |  |
| P4.A5 | django-realworld-example-app | COMPLETE | yes | fast | 7 | 1 | 5 | 2 | ✅ |  |
| P4.A6 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P4.A7 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 9 | 5 | ✅ |  |
| P4.A8 | django-realworld-example-app | COMPLETE | yes | fast | 2 | 0 | 3 | 2 | ✅ |  |
| P4.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 24 | 17 | ✅ |  |
| P4.A1 | microblog | COMPLETE | yes | fast | 4 | 0 | 3 | 2 | ✅ |  |
| P4.A2 | microblog | COMPLETE | yes | fast | 6 | 0 | 17 | 3 | ✅ |  |
| P4.A3 | microblog | PARTIAL | yes | coding | 9 | 0 | 23 | 12 | ✅ |  |
| P4.A4 | microblog | COMPLETE | yes | fast | 6 | 0 | 11 | 2 | ✅ |  |
| P4.A5 | microblog | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A6 | microblog | COMPLETE | yes | fast | 6 | 0 | 10 | 5 | ✅ |  |
| P4.A7 | microblog | COMPLETE | yes | fast | 6 | 0 | 16 | 1 | ✅ |  |
| P4.A8 | microblog | COMPLETE | yes | fast | 4 | 0 | 9 | 4 | ✅ |  |
| P4.A9 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 20 | 15 | ✅ |  |
| P4.A1 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P4.A2 | node-express-realworld-example-app | COMPLETE | yes | fast | 4 | 1 | 4 | 3 | ✅ |  |
| P4.A3 | node-express-realworld-example-app | PARTIAL | yes | coding | 8 | 0 | 14 | 9 | ✅ |  |
| P4.A4 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 23 | 4 | ✅ |  |
| P4.A5 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P4.A6 | node-express-realworld-example-app | PARTIAL | yes | fast | 7 | 1 | 7 | 4 | ✅ |  |
| P4.A7 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P4.A8 | node-express-realworld-example-app | COMPLETE | yes | fast | 2 | 0 | 3 | 4 | ✅ |  |
| P4.A9 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 19 | 17 | ✅ |  |
| P4.A1 | musicstore | COMPLETE | yes | fast | 6 | 0 | 6 | 2 | ✅ |  |
| P4.A2 | musicstore | COMPLETE | yes | fast | 7 | 1 | 5 | 6 | ✅ |  |
| P4.A3 | musicstore | PARTIAL | yes | coding | 10 | 0 | 24 | 9 | ✅ |  |
| P4.A4 | musicstore | COMPLETE | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P4.A5 | musicstore | COMPLETE | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P4.A6 | musicstore | PARTIAL | yes | fast | 6 | 0 | 15 | 6 | ✅ |  |
| P4.A7 | musicstore | COMPLETE | yes | fast | 6 | 0 | 12 | 1 | ✅ |  |
| P4.A8 | musicstore | COMPLETE | yes | fast | 7 | 1 | 25 | 1 | ✅ |  |
| P4.A9 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 20 | 17 | ✅ |  |
| P4.A1 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A2 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A3 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A4 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A5 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A6 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A7 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A8 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A9 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A1 | sinatra | COMPLETE | yes | fast | 1 | 0 | 0 | 2 | ✅ |  |
| P4.A2 | sinatra | COMPLETE | yes | fast | 4 | 1 | 10 | 5 | ✅ |  |
| P4.A3 | sinatra | PARTIAL | yes | coding | 10 | 1 | 19 | 14 | ✅ |  |
| P4.A4 | sinatra | COMPLETE | yes | fast | 4 | 0 | 3 | 2 | ✅ |  |
| P4.A5 | sinatra | PARTIAL | yes | fast | 6 | 0 | 7 | 8 | ✅ |  |
| P4.A6 | sinatra | PARTIAL | yes | fast | 6 | 0 | 18 | 6 | ✅ |  |
| P4.A7 | sinatra | PARTIAL | yes | fast | 6 | 0 | 13 | 2 | ✅ |  |
| P4.A8 | sinatra | COMPLETE | yes | fast | 4 | 1 | 8 | 2 | ✅ |  |
| P4.A9 | sinatra | PARTIAL | yes | reasoning | 6 | 0 | 23 | 18 | ✅ |  |
| P4.A1 | golang-example | COMPLETE | yes | fast | 4 | 0 | 3 | 3 | ✅ |  |
| P4.A2 | golang-example | COMPLETE | yes | fast | 2 | 0 | 1 | 3 | ✅ |  |
| P4.A3 | golang-example | PARTIAL | yes | coding | 5 | 0 | 16 | 13 | ✅ |  |
| P4.A4 | golang-example | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | golang-example | PARTIAL | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P4.A6 | golang-example | COMPLETE | yes | fast | 7 | 1 | 7 | 3 | ✅ |  |
| P4.A7 | golang-example | COMPLETE | yes | fast | 6 | 0 | 11 | 2 | ✅ |  |
| P4.A8 | golang-example | COMPLETE | yes | fast | 2 | 0 | 3 | 4 | ✅ |  |
| P4.A9 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 22 | 16 | ✅ |  |
| P4.A1 | todomvc | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A2 | todomvc | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P4.A3 | todomvc | PARTIAL | yes | coding | 10 | 1 | 14 | 11 | ✅ |  |
| P4.A4 | todomvc | COMPLETE | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P4.A5 | todomvc | PARTIAL | yes | fast | 6 | 0 | 10 | 5 | ✅ |  |
| P4.A6 | todomvc | COMPLETE | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P4.A7 | todomvc | COMPLETE | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P4.A8 | todomvc | COMPLETE | yes | fast | 2 | 0 | 4 | 4 | ✅ |  |
| P4.A9 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 18 | 15 | ✅ |  |
| P4.A1 | react-redux-realworld | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A2 | react-redux-realworld | COMPLETE | yes | fast | 5 | 0 | 9 | 4 | ✅ |  |
| P4.A3 | react-redux-realworld | PARTIAL | yes | coding | 6 | 0 | 13 | 12 | ✅ |  |
| P4.A4 | react-redux-realworld | COMPLETE | yes | fast | 3 | 0 | 6 | 4 | ✅ |  |
| P4.A5 | react-redux-realworld | COMPLETE | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P4.A6 | react-redux-realworld | PARTIAL | yes | fast | 6 | 0 | 6 | 6 | ✅ |  |
| P4.A7 | react-redux-realworld | COMPLETE | yes | fast | 7 | 1 | 14 | 2 | ✅ |  |
| P4.A8 | react-redux-realworld | COMPLETE | yes | fast | 6 | 0 | 14 | 1 | ✅ |  |
| P4.A9 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 21 | 17 | ✅ |  |
| P4.A1 | eshop-on-web | COMPLETE | yes | fast | 4 | 1 | 2 | 3 | ✅ |  |
| P4.A2 | eshop-on-web | COMPLETE | yes | fast | 3 | 0 | 4 | 2 | ✅ |  |
| P4.A3 | eshop-on-web | PARTIAL | yes | coding | 10 | 1 | 19 | 10 | ✅ |  |
| P4.A4 | eshop-on-web | PARTIAL | yes | fast | 4 | 0 | 17 | 9 | ✅ |  |
| P4.A5 | eshop-on-web | COMPLETE | yes | fast | 7 | 1 | 11 | 2 | ✅ |  |
| P4.A6 | eshop-on-web | PARTIAL | yes | fast | 7 | 1 | 18 | 7 | ✅ |  |
| P4.A7 | eshop-on-web | COMPLETE | yes | fast | 6 | 0 | 18 | 1 | ✅ |  |
| P4.A8 | eshop-on-web | COMPLETE | yes | fast | 8 | 2 | 10 | 1 | ✅ |  |
| P4.A9 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 18 | 14 | ✅ |  |
| P4.A1 | orchard | COMPLETE | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P4.A2 | orchard | COMPLETE | yes | fast | 6 | 0 | 11 | 3 | ✅ |  |
| P4.A3 | orchard | PARTIAL | yes | coding | 9 | 0 | 17 | 8 | ✅ |  |
| P4.A4 | orchard | COMPLETE | yes | fast | 6 | 0 | 19 | 2 | ✅ |  |
| P4.A5 | orchard | PARTIAL | yes | fast | 6 | 0 | 10 | 6 | ✅ |  |
| P4.A6 | orchard | COMPLETE | yes | fast | 6 | 0 | 6 | 4 | ✅ |  |
| P4.A7 | orchard | COMPLETE | yes | fast | 7 | 1 | 11 | 2 | ✅ |  |
| P4.A8 | orchard | COMPLETE | yes | fast | 2 | 0 | 3 | 4 | ✅ |  |
| P4.A9 | orchard | PARTIAL | yes | reasoning | 5 | 0 | 16 | 14 | ✅ |  |
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
| P4.A1 | juice-shop | COMPLETE | yes | fast | 6 | 0 | 6 | 2 | ✅ |  |
| P4.A2 | juice-shop | COMPLETE | yes | fast | 3 | 0 | 2 | 3 | ✅ |  |
| P4.A3 | juice-shop | PARTIAL | yes | coding | 8 | 0 | 20 | 10 | ✅ |  |
| P4.A4 | juice-shop | PARTIAL | yes | fast | 4 | 0 | 9 | 6 | ✅ |  |
| P4.A5 | juice-shop | COMPLETE | yes | fast | 7 | 1 | 8 | 4 | ✅ |  |
| P4.A6 | juice-shop | PARTIAL | yes | fast | 6 | 0 | 10 | 6 | ✅ |  |
| P4.A7 | juice-shop | COMPLETE | yes | fast | 8 | 2 | 11 | 2 | ✅ |  |
| P4.A8 | juice-shop | PARTIAL | yes | fast | 2 | 0 | 4 | 5 | ✅ |  |
| P4.A9 | juice-shop | PARTIAL | yes | reasoning | 5 | 0 | 17 | 14 | ✅ |  |

## Failures

- `P3/struts-examples/A3`: no artifact published
- `P3/struts-examples/A6`: no artifact published
- `P3/struts-examples/A7`: no artifact published
- `P3/struts-examples/A8`: no artifact published
- `P3/ofbiz/A2`: not enriched (seed-fallback: LLMConfigError: gpt-6-astra: auth failed (403))
- `P3/ofbiz/A3`: not enriched (seed-fallback: LLMConfigError: gpt-6-astra: auth failed (403))
- `P3/ofbiz/A4`: not enriched (seed-fallback: LLMConfigError: gpt-6-astra: auth failed (403))
- `P3/ofbiz/A5`: not enriched (seed-fallback: LLMConfigError: gpt-4.1-mini: auth failed (403))
- `P3/ofbiz/A6`: not enriched (seed-fallback: LLMConfigError: gpt-6-astra: auth failed (403))
- `P3/ofbiz/A7`: not enriched (seed-fallback: LLMConfigError: gpt-4.1-mini: auth failed (403))
- `P3/ofbiz/A8`: not enriched (seed-fallback: LLMConfigError: gpt-6-astra: auth failed (403))
- `P3/mantisbt/A2`: no artifact published
- `P3/mantisbt/A3`: no artifact published
- `P3/mantisbt/A4`: no artifact published
- `P3/mantisbt/A5`: no artifact published
- `P3/mantisbt/A6`: no artifact published
- `P3/mantisbt/A7`: no artifact published
- `P3/mantisbt/A8`: no artifact published
- `P3/bugzilla/A2`: no artifact published
- `P3/bugzilla/A3`: no artifact published
- `P3/bugzilla/A4`: no artifact published
- `P3/bugzilla/A5`: no artifact published
- `P3/bugzilla/A6`: no artifact published
- `P3/bugzilla/A7`: no artifact published
- `P3/bugzilla/A8`: no artifact published
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
