# E2E agentic acceptance run `s1-r1-tune`

- **Job**: `job-1791867233-63338f` — **COMPLETED**
- **Repositories**: `spring-petclinic`, `flask-tutorial`, `django-realworld-example-app`, `microblog`, `node-express-realworld-example-app`, `musicstore`, `laravel58`, `sinatra`, `golang-example`, `todomvc`, `react-redux-realworld`, `eshop-on-web`, `orchard`, `struts-examples`, `ofbiz`, `webgoat`, `carddemo`, `mantisbt`, `bugzilla`, `juice-shop`
- **Elapsed**: 138 min 45 s; LLM cache mode `off` (record = every call live, responses recorded for replay)
- **Astra tiers**: {'reasoning': 'gpt-6-astra', 'coding': 'gpt-5.3-codex-PlayWright', 'fast': 'gpt-4.1-mini', 'fallback': 'gpt-5.4'}
- **Human surfaces**: review_mode=human; release-gate approvals and stakeholder answers were submitted over the API by a **scripted** reviewer/stakeholder (labelled as automation in every record).

## Result

**Agent success rate: 100.00%** (397/397 P1–P4 agent dispatches; threshold > 97.0%).

170 P3/P4 agent slots were **not admitted** because the authorized P2 release gate routed `flask-tutorial` (Retire), `laravel58` (Retire), `todomvc` (Retain), `orchard` (Retain), `struts-examples` (Retain), `ofbiz` (Retain), `webgoat` (Retain), `carddemo` (Retain), `bugzilla` (Retain), `juice-shop` (Retain) to the non-delivery register — by design, no architecture or plan is produced for a non-delivery route. Counting those slots as failures would give 70.02%.

Success = artifact not FAILED **and** enriched by the live Astra agent loop (not seed fallback) **and** passes ContractValidator (envelope + payload schema + content hash).

| phase | ok / total |
|---|---|
| P1 Discovery | 220 / 220 |
| P2 Portfolio | 7 / 7 |
| P3 Architecture | 80 / 80 |
| P4 Planning | 90 / 90 |

- Tool calls: 7280; evidence ids cited: 4357; LLM findings: 2384; repair rounds: 30; failovers: 0
- Tokens: {'input': 33731820, 'output': 1572119, 'reasoning': 79818}

## Release gates

| phase | app | phase status | decision |
|---|---|---|---|
| P1 | flask-tutorial | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | spring-petclinic | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | microblog | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | django-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | node-express-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | musicstore | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | laravel58 | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | sinatra | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | golang-example | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | todomvc | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | react-redux-realworld | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | eshop-on-web | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | orchard | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | struts-examples | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | webgoat | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | ofbiz | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | carddemo | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | bugzilla | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | mantisbt | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | juice-shop | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P2 | PF1 | COMPLETED | AUTHORIZED |
| P3 | flask-tutorial | NOT_ADMITTED | — |
| P4 | flask-tutorial | NOT_ADMITTED | — |
| P3 | laravel58 | NOT_ADMITTED | — |
| P4 | laravel58 | NOT_ADMITTED | — |
| P3 | todomvc | NOT_ADMITTED | — |
| P4 | todomvc | NOT_ADMITTED | — |
| P3 | orchard | NOT_ADMITTED | — |
| P4 | orchard | NOT_ADMITTED | — |
| P3 | struts-examples | NOT_ADMITTED | — |
| P4 | struts-examples | NOT_ADMITTED | — |
| P3 | ofbiz | NOT_ADMITTED | — |
| P4 | ofbiz | NOT_ADMITTED | — |
| P3 | webgoat | NOT_ADMITTED | — |
| P4 | webgoat | NOT_ADMITTED | — |
| P3 | carddemo | NOT_ADMITTED | — |
| P4 | carddemo | NOT_ADMITTED | — |
| P3 | bugzilla | NOT_ADMITTED | — |
| P4 | bugzilla | NOT_ADMITTED | — |
| P3 | juice-shop | NOT_ADMITTED | — |
| P4 | juice-shop | NOT_ADMITTED | — |
| P3 | django-realworld-example-app | COMPLETED | CONDITIONAL_PLANNING |
| P3 | microblog | COMPLETED | CONDITIONAL_PLANNING |
| P3 | node-express-realworld-example-app | COMPLETED | CONDITIONAL_PLANNING |
| P3 | spring-petclinic | COMPLETED | CONDITIONAL_PLANNING |
| P3 | musicstore | COMPLETED | CONDITIONAL_PLANNING |
| P4 | spring-petclinic | COMPLETED | SCOPED_PREPARATION |
| P4 | node-express-realworld-example-app | COMPLETED | SCOPED_PREPARATION |
| P4 | musicstore | COMPLETED | SCOPED_PREPARATION |
| P4 | microblog | COMPLETED | SCOPED_PREPARATION |
| P4 | django-realworld-example-app | COMPLETED | SCOPED_PREPARATION |
| P3 | sinatra | COMPLETED | CONDITIONAL_PLANNING |
| P3 | golang-example | COMPLETED | CONDITIONAL_PLANNING |
| P3 | react-redux-realworld | COMPLETED | CONDITIONAL_PLANNING |
| P3 | eshop-on-web | COMPLETED | CONDITIONAL_PLANNING |
| P3 | mantisbt | COMPLETED | CONDITIONAL_PLANNING |
| P4 | react-redux-realworld | COMPLETED | SCOPED_PREPARATION |
| P4 | sinatra | COMPLETED | SCOPED_PREPARATION |
| P4 | mantisbt | COMPLETED | SCOPED_PREPARATION |
| P4 | golang-example | COMPLETED | SCOPED_PREPARATION |
| P4 | eshop-on-web | COMPLETED | SCOPED_PREPARATION |

Reviews: 41 (decided by `scripted-reviewer`); stakeholder questions: 141 (141 answered).

## Per-agent results

| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| P1.A1 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 31 | 23 | ✅ |  |
| P1.A2 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 30 | 23 | ✅ |  |
| P1.A3 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 24 | 19 | ✅ |  |
| P1.A4 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 13 | 10 | ✅ |  |
| P1.A5 | spring-petclinic | PARTIAL | yes | fast | 7 | 1 | 10 | 6 | ✅ |  |
| P1.A6 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 22 | 17 | ✅ |  |
| P1.A7 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 10 | 5 | ✅ |  |
| P1.A8 | spring-petclinic | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 30 | 18 | ✅ |  |
| P1.A10 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 19 | 10 | ✅ |  |
| P1.A11 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 14 | 12 | ✅ |  |
| P1.A1 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 0 | 25 | 17 | ✅ |  |
| P1.A2 | flask-tutorial | PARTIAL | yes | reasoning | 3 | 0 | 12 | 10 | ✅ |  |
| P1.A3 | flask-tutorial | PARTIAL | yes | reasoning | 3 | 0 | 11 | 10 | ✅ |  |
| P1.A4 | flask-tutorial | PARTIAL | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P1.A5 | flask-tutorial | PARTIAL | yes | fast | 7 | 0 | 16 | 10 | ✅ |  |
| P1.A6 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 19 | 20 | ✅ |  |
| P1.A7 | flask-tutorial | PARTIAL | yes | fast | 6 | 0 | 11 | 6 | ✅ |  |
| P1.A8 | flask-tutorial | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 22 | 12 | ✅ |  |
| P1.A10 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 0 | 14 | 11 | ✅ |  |
| P1.A11 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 0 | 12 | 9 | ✅ |  |
| P1.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 38 | 13 | ✅ |  |
| P1.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 29 | 20 | ✅ |  |
| P1.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 33 | 22 | ✅ |  |
| P1.A4 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 9 | 5 | ✅ |  |
| P1.A5 | django-realworld-example-app | PARTIAL | yes | fast | 7 | 0 | 12 | 9 | ✅ |  |
| P1.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 19 | 17 | ✅ |  |
| P1.A7 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 28 | 17 | ✅ |  |
| P1.A10 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 20 | 11 | ✅ |  |
| P1.A11 | django-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 14 | 11 | ✅ |  |
| P1.A1 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 36 | 19 | ✅ |  |
| P1.A2 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 25 | 18 | ✅ |  |
| P1.A3 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 22 | 18 | ✅ |  |
| P1.A4 | microblog | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A5 | microblog | PARTIAL | yes | fast | 7 | 0 | 12 | 8 | ✅ |  |
| P1.A6 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 25 | 19 | ✅ |  |
| P1.A7 | microblog | PARTIAL | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P1.A8 | microblog | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 31 | 16 | ✅ |  |
| P1.A10 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 21 | 11 | ✅ |  |
| P1.A11 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 14 | 10 | ✅ |  |
| P1.A1 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 50 | 26 | ✅ |  |
| P1.A2 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 26 | 18 | ✅ |  |
| P1.A3 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 28 | 23 | ✅ |  |
| P1.A4 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P1.A5 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 7 | 7 | ✅ |  |
| P1.A6 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 20 | 17 | ✅ |  |
| P1.A7 | node-express-realworld-example-app | PARTIAL | yes | fast | 7 | 1 | 8 | 2 | ✅ |  |
| P1.A8 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 27 | 16 | ✅ |  |
| P1.A10 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 19 | 10 | ✅ |  |
| P1.A11 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 18 | 13 | ✅ |  |
| P1.A1 | musicstore | PARTIAL | yes | reasoning | 8 | 0 | 53 | 23 | ✅ |  |
| P1.A2 | musicstore | PARTIAL | yes | reasoning | 7 | 0 | 25 | 19 | ✅ |  |
| P1.A3 | musicstore | PARTIAL | yes | reasoning | 9 | 0 | 32 | 20 | ✅ |  |
| P1.A4 | musicstore | PARTIAL | yes | fast | 6 | 0 | 10 | 3 | ✅ |  |
| P1.A5 | musicstore | PARTIAL | yes | fast | 7 | 0 | 11 | 7 | ✅ |  |
| P1.A6 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 28 | 17 | ✅ |  |
| P1.A7 | musicstore | PARTIAL | yes | fast | 6 | 0 | 15 | 5 | ✅ |  |
| P1.A8 | musicstore | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | musicstore | PARTIAL | yes | reasoning | 7 | 0 | 27 | 15 | ✅ |  |
| P1.A10 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 18 | 11 | ✅ |  |
| P1.A11 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 16 | 9 | ✅ |  |
| P1.A1 | laravel58 | PARTIAL | yes | reasoning | 7 | 0 | 38 | 19 | ✅ |  |
| P1.A2 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 27 | 25 | ✅ |  |
| P1.A3 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 27 | 23 | ✅ |  |
| P1.A4 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 12 | 4 | ✅ |  |
| P1.A5 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P1.A6 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 22 | 18 | ✅ |  |
| P1.A7 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P1.A8 | laravel58 | PARTIAL | yes | reasoning | 4 | 0 | 4 | 4 | ✅ |  |
| P1.A9 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 30 | 20 | ✅ |  |
| P1.A10 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 14 | 10 | ✅ |  |
| P1.A11 | laravel58 | PARTIAL | yes | reasoning | 4 | 0 | 9 | 6 | ✅ |  |
| P1.A1 | sinatra | PARTIAL | yes | reasoning | 5 | 0 | 22 | 11 | ✅ |  |
| P1.A2 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 11 | 9 | ✅ |  |
| P1.A3 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 13 | 10 | ✅ |  |
| P1.A4 | sinatra | PARTIAL | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P1.A5 | sinatra | PARTIAL | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P1.A6 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 13 | 12 | ✅ |  |
| P1.A7 | sinatra | PARTIAL | yes | fast | 7 | 1 | 7 | 6 | ✅ |  |
| P1.A8 | sinatra | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | sinatra | PARTIAL | yes | reasoning | 3 | 0 | 10 | 7 | ✅ |  |
| P1.A10 | sinatra | PARTIAL | yes | reasoning | 6 | 0 | 15 | 11 | ✅ |  |
| P1.A11 | sinatra | PARTIAL | yes | reasoning | 5 | 0 | 15 | 9 | ✅ |  |
| P1.A1 | golang-example | PARTIAL | yes | reasoning | 7 | 0 | 37 | 21 | ✅ |  |
| P1.A2 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 18 | 15 | ✅ |  |
| P1.A3 | golang-example | PARTIAL | yes | reasoning | 4 | 0 | 16 | 14 | ✅ |  |
| P1.A4 | golang-example | PARTIAL | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P1.A5 | golang-example | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P1.A6 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 19 | 20 | ✅ |  |
| P1.A7 | golang-example | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P1.A8 | golang-example | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 20 | 11 | ✅ |  |
| P1.A10 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | golang-example | PARTIAL | yes | reasoning | 9 | 0 | 19 | 11 | ✅ |  |
| P1.A1 | todomvc | PARTIAL | yes | reasoning | 8 | 0 | 51 | 19 | ✅ |  |
| P1.A2 | todomvc | PARTIAL | yes | reasoning | 7 | 0 | 35 | 18 | ✅ |  |
| P1.A3 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 26 | 15 | ✅ |  |
| P1.A4 | todomvc | PARTIAL | yes | fast | 6 | 0 | 10 | 5 | ✅ |  |
| P1.A5 | todomvc | PARTIAL | yes | fast | 6 | 0 | 19 | 8 | ✅ |  |
| P1.A6 | todomvc | PARTIAL | yes | reasoning | 5 | 0 | 22 | 13 | ✅ |  |
| P1.A7 | todomvc | PARTIAL | yes | fast | 6 | 0 | 16 | 3 | ✅ |  |
| P1.A8 | todomvc | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | todomvc | PARTIAL | yes | reasoning | 5 | 0 | 23 | 13 | ✅ |  |
| P1.A10 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 18 | 12 | ✅ |  |
| P1.A11 | todomvc | PARTIAL | yes | reasoning | 5 | 0 | 15 | 10 | ✅ |  |
| P1.A1 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 25 | 12 | ✅ |  |
| P1.A2 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 21 | 16 | ✅ |  |
| P1.A3 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 22 | 14 | ✅ |  |
| P1.A4 | react-redux-realworld | PARTIAL | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P1.A5 | react-redux-realworld | PARTIAL | yes | fast | 7 | 0 | 10 | 4 | ✅ |  |
| P1.A6 | react-redux-realworld | PARTIAL | yes | reasoning | 4 | 0 | 16 | 12 | ✅ |  |
| P1.A7 | react-redux-realworld | PARTIAL | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P1.A8 | react-redux-realworld | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 37 | 16 | ✅ |  |
| P1.A10 | react-redux-realworld | PARTIAL | yes | reasoning | 7 | 0 | 18 | 13 | ✅ |  |
| P1.A11 | react-redux-realworld | PARTIAL | yes | reasoning | 4 | 0 | 11 | 11 | ✅ |  |
| P1.A1 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 36 | 17 | ✅ |  |
| P1.A2 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 32 | 25 | ✅ |  |
| P1.A3 | eshop-on-web | PARTIAL | yes | reasoning | 7 | 0 | 38 | 19 | ✅ |  |
| P1.A4 | eshop-on-web | PARTIAL | yes | fast | 6 | 0 | 9 | 7 | ✅ |  |
| P1.A5 | eshop-on-web | PARTIAL | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P1.A6 | eshop-on-web | PARTIAL | yes | reasoning | 7 | 0 | 30 | 25 | ✅ |  |
| P1.A7 | eshop-on-web | PARTIAL | yes | fast | 6 | 0 | 14 | 4 | ✅ |  |
| P1.A8 | eshop-on-web | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 40 | 17 | ✅ |  |
| P1.A10 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 17 | 13 | ✅ |  |
| P1.A11 | eshop-on-web | PARTIAL | yes | reasoning | 8 | 0 | 25 | 15 | ✅ |  |
| P1.A1 | orchard | PARTIAL | yes | reasoning | 7 | 0 | 40 | 27 | ✅ |  |
| P1.A2 | orchard | PARTIAL | yes | reasoning | 6 | 0 | 24 | 16 | ✅ |  |
| P1.A3 | orchard | PARTIAL | yes | reasoning | 8 | 0 | 40 | 25 | ✅ |  |
| P1.A4 | orchard | PARTIAL | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P1.A5 | orchard | PARTIAL | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P1.A6 | orchard | PARTIAL | yes | reasoning | 7 | 0 | 30 | 23 | ✅ |  |
| P1.A7 | orchard | PARTIAL | yes | fast | 7 | 0 | 6 | 1 | ✅ |  |
| P1.A8 | orchard | PARTIAL | yes | reasoning | 3 | 0 | 4 | 3 | ✅ |  |
| P1.A9 | orchard | PARTIAL | yes | reasoning | 8 | 0 | 32 | 16 | ✅ |  |
| P1.A10 | orchard | PARTIAL | yes | reasoning | 9 | 0 | 43 | 15 | ✅ |  |
| P1.A11 | orchard | PARTIAL | yes | reasoning | 7 | 0 | 33 | 16 | ✅ |  |
| P1.A1 | struts-examples | PARTIAL | yes | reasoning | 7 | 0 | 44 | 23 | ✅ |  |
| P1.A2 | struts-examples | PARTIAL | yes | reasoning | 7 | 0 | 32 | 19 | ✅ |  |
| P1.A3 | struts-examples | PARTIAL | yes | reasoning | 7 | 0 | 35 | 17 | ✅ |  |
| P1.A4 | struts-examples | PARTIAL | yes | fast | 6 | 0 | 5 | 5 | ✅ |  |
| P1.A5 | struts-examples | PARTIAL | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P1.A6 | struts-examples | PARTIAL | yes | reasoning | 6 | 0 | 29 | 19 | ✅ |  |
| P1.A7 | struts-examples | PARTIAL | yes | fast | 7 | 1 | 8 | 2 | ✅ |  |
| P1.A8 | struts-examples | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | struts-examples | PARTIAL | yes | reasoning | 9 | 0 | 39 | 22 | ✅ |  |
| P1.A10 | struts-examples | PARTIAL | yes | reasoning | 7 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | struts-examples | PARTIAL | yes | reasoning | 7 | 0 | 17 | 10 | ✅ |  |
| P1.A1 | ofbiz | PARTIAL | yes | reasoning | 9 | 0 | 51 | 25 | ✅ |  |
| P1.A2 | ofbiz | PARTIAL | yes | reasoning | 7 | 0 | 31 | 24 | ✅ |  |
| P1.A3 | ofbiz | PARTIAL | yes | reasoning | 8 | 1 | 35 | 19 | ✅ |  |
| P1.A4 | ofbiz | PARTIAL | yes | fast | 6 | 0 | 10 | 10 | ✅ |  |
| P1.A5 | ofbiz | PARTIAL | yes | fast | 7 | 1 | 7 | 5 | ✅ |  |
| P1.A6 | ofbiz | PARTIAL | yes | reasoning | 7 | 0 | 29 | 18 | ✅ |  |
| P1.A7 | ofbiz | PARTIAL | yes | fast | 7 | 0 | 7 | 2 | ✅ |  |
| P1.A8 | ofbiz | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | ofbiz | PARTIAL | yes | reasoning | 6 | 0 | 23 | 15 | ✅ |  |
| P1.A10 | ofbiz | PARTIAL | yes | reasoning | 7 | 0 | 22 | 10 | ✅ |  |
| P1.A11 | ofbiz | PARTIAL | yes | reasoning | 7 | 0 | 26 | 14 | ✅ |  |
| P1.A1 | webgoat | PARTIAL | yes | reasoning | 7 | 0 | 40 | 18 | ✅ |  |
| P1.A2 | webgoat | PARTIAL | yes | reasoning | 7 | 0 | 33 | 26 | ✅ |  |
| P1.A3 | webgoat | PARTIAL | yes | reasoning | 8 | 0 | 38 | 23 | ✅ |  |
| P1.A4 | webgoat | PARTIAL | yes | fast | 8 | 1 | 19 | 11 | ✅ |  |
| P1.A5 | webgoat | PARTIAL | yes | fast | 7 | 0 | 6 | 5 | ✅ |  |
| P1.A6 | webgoat | PARTIAL | yes | reasoning | 6 | 0 | 26 | 25 | ✅ |  |
| P1.A7 | webgoat | PARTIAL | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P1.A8 | webgoat | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | webgoat | PARTIAL | yes | reasoning | 6 | 0 | 28 | 21 | ✅ |  |
| P1.A10 | webgoat | PARTIAL | yes | reasoning | 6 | 0 | 21 | 12 | ✅ |  |
| P1.A11 | webgoat | PARTIAL | yes | reasoning | 6 | 0 | 21 | 15 | ✅ |  |
| P1.A1 | carddemo | PARTIAL | yes | reasoning | 8 | 0 | 49 | 25 | ✅ |  |
| P1.A2 | carddemo | PARTIAL | yes | reasoning | 7 | 0 | 28 | 25 | ✅ |  |
| P1.A3 | carddemo | PARTIAL | yes | reasoning | 8 | 0 | 46 | 27 | ✅ |  |
| P1.A4 | carddemo | PARTIAL | yes | fast | 6 | 0 | 6 | 2 | ✅ |  |
| P1.A5 | carddemo | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P1.A6 | carddemo | PARTIAL | yes | reasoning | 6 | 0 | 25 | 21 | ✅ |  |
| P1.A7 | carddemo | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A8 | carddemo | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | carddemo | PARTIAL | yes | reasoning | 10 | 1 | 26 | 23 | ✅ |  |
| P1.A10 | carddemo | PARTIAL | yes | reasoning | 6 | 0 | 20 | 12 | ✅ |  |
| P1.A11 | carddemo | PARTIAL | yes | reasoning | 4 | 0 | 11 | 11 | ✅ |  |
| P1.A1 | mantisbt | PARTIAL | yes | reasoning | 8 | 0 | 47 | 27 | ✅ |  |
| P1.A2 | mantisbt | PARTIAL | yes | reasoning | 7 | 0 | 28 | 19 | ✅ |  |
| P1.A3 | mantisbt | PARTIAL | yes | reasoning | 7 | 0 | 36 | 21 | ✅ |  |
| P1.A4 | mantisbt | PARTIAL | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P1.A5 | mantisbt | PARTIAL | yes | fast | 6 | 0 | 9 | 7 | ✅ |  |
| P1.A6 | mantisbt | PARTIAL | yes | reasoning | 7 | 0 | 42 | 29 | ✅ |  |
| P1.A7 | mantisbt | PARTIAL | yes | fast | 8 | 2 | 6 | 2 | ✅ |  |
| P1.A8 | mantisbt | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | mantisbt | PARTIAL | yes | reasoning | 7 | 0 | 25 | 16 | ✅ |  |
| P1.A10 | mantisbt | PARTIAL | yes | reasoning | 6 | 0 | 22 | 12 | ✅ |  |
| P1.A11 | mantisbt | PARTIAL | yes | reasoning | 6 | 0 | 21 | 12 | ✅ |  |
| P1.A1 | bugzilla | PARTIAL | yes | reasoning | 7 | 0 | 44 | 27 | ✅ |  |
| P1.A2 | bugzilla | PARTIAL | yes | reasoning | 5 | 0 | 20 | 17 | ✅ |  |
| P1.A3 | bugzilla | PARTIAL | yes | reasoning | 8 | 0 | 44 | 27 | ✅ |  |
| P1.A4 | bugzilla | PARTIAL | yes | fast | 6 | 0 | 8 | 8 | ✅ |  |
| P1.A5 | bugzilla | PARTIAL | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P1.A6 | bugzilla | PARTIAL | yes | reasoning | 5 | 0 | 22 | 18 | ✅ |  |
| P1.A7 | bugzilla | PARTIAL | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P1.A8 | bugzilla | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | bugzilla | PARTIAL | yes | reasoning | 7 | 0 | 33 | 18 | ✅ |  |
| P1.A10 | bugzilla | PARTIAL | yes | reasoning | 6 | 0 | 16 | 10 | ✅ |  |
| P1.A11 | bugzilla | PARTIAL | yes | reasoning | 5 | 0 | 19 | 12 | ✅ |  |
| P1.A1 | juice-shop | PARTIAL | yes | reasoning | 8 | 0 | 44 | 21 | ✅ |  |
| P1.A2 | juice-shop | PARTIAL | yes | reasoning | 5 | 0 | 20 | 19 | ✅ |  |
| P1.A3 | juice-shop | PARTIAL | yes | reasoning | 7 | 0 | 33 | 18 | ✅ |  |
| P1.A4 | juice-shop | PARTIAL | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P1.A5 | juice-shop | PARTIAL | yes | fast | 7 | 0 | 11 | 7 | ✅ |  |
| P1.A6 | juice-shop | PARTIAL | yes | reasoning | 5 | 0 | 22 | 20 | ✅ |  |
| P1.A7 | juice-shop | PARTIAL | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P1.A8 | juice-shop | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 24 | 10 | ✅ |  |
| P1.A10 | juice-shop | PARTIAL | yes | reasoning | 6 | 0 | 18 | 10 | ✅ |  |
| P1.A11 | juice-shop | PARTIAL | yes | reasoning | 5 | 0 | 19 | 12 | ✅ |  |
| P2.A1 | PF1 | PARTIAL | yes | reasoning | 10 | 0 | 36 | 26 | ✅ |  |
| P2.A2 | PF1 | PARTIAL | yes | reasoning | 9 | 0 | 43 | 20 | ✅ |  |
| P2.A3 | PF1 | PARTIAL | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P2.A4 | PF1 | COMPLETE | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P2.A5 | PF1 | COMPLETE | yes | fast | 7 | 1 | 12 | 2 | ✅ |  |
| P2.A6 | PF1 | PARTIAL | yes | reasoning | 10 | 0 | 76 | 37 | ✅ |  |
| P2.A7 | PF1 | PARTIAL | yes | reasoning | 6 | 0 | 35 | 10 | ✅ |  |
| P3.A1 | spring-petclinic | PARTIAL | yes | reasoning | 8 | 0 | 50 | 31 | ✅ |  |
| P3.A2 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 24 | 14 | ✅ |  |
| P3.A3 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 21 | 19 | ✅ |  |
| P3.A4 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 22 | 18 | ✅ |  |
| P3.A5 | spring-petclinic | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 8 | ✅ |  |
| P3.A6 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 32 | 23 | ✅ |  |
| P3.A7 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 11 | 3 | ✅ |  |
| P3.A8 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 31 | 16 | ✅ |  |
| P3.A1 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P3.A2 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P3.A3 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P3.A4 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P3.A5 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P3.A6 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P3.A7 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P3.A8 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P3.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 53 | 30 | ✅ |  |
| P3.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 26 | 16 | ✅ |  |
| P3.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 19 | 15 | ✅ |  |
| P3.A4 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 17 | 14 | ✅ |  |
| P3.A5 | django-realworld-example-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P3.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 25 | 15 | ✅ |  |
| P3.A7 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P3.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 7 | 1 | 35 | 18 | ✅ |  |
| P3.A1 | microblog | PARTIAL | yes | reasoning | 8 | 0 | 48 | 22 | ✅ |  |
| P3.A2 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 19 | 16 | ✅ |  |
| P3.A3 | microblog | PARTIAL | yes | reasoning | 4 | 0 | 16 | 15 | ✅ |  |
| P3.A4 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 24 | 16 | ✅ |  |
| P3.A5 | microblog | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 8 | ✅ |  |
| P3.A6 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 27 | 21 | ✅ |  |
| P3.A7 | microblog | PARTIAL | yes | fast | 6 | 0 | 9 | 5 | ✅ |  |
| P3.A8 | microblog | PARTIAL | yes | reasoning | 4 | 0 | 19 | 14 | ✅ |  |
| P3.A1 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 10 | 0 | 59 | 26 | ✅ |  |
| P3.A2 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 25 | 17 | ✅ |  |
| P3.A3 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 16 | 11 | ✅ |  |
| P3.A4 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 25 | 16 | ✅ |  |
| P3.A5 | node-express-realworld-example-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P3.A6 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 34 | 24 | ✅ |  |
| P3.A7 | node-express-realworld-example-app | COMPLETE | yes | fast | 4 | 0 | 11 | 3 | ✅ |  |
| P3.A8 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 31 | 14 | ✅ |  |
| P3.A1 | musicstore | PARTIAL | yes | reasoning | 9 | 0 | 49 | 29 | ✅ |  |
| P3.A2 | musicstore | PARTIAL | yes | reasoning | 4 | 0 | 14 | 12 | ✅ |  |
| P3.A3 | musicstore | PARTIAL | yes | reasoning | 4 | 0 | 19 | 14 | ✅ |  |
| P3.A4 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 20 | 16 | ✅ |  |
| P3.A5 | musicstore | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 7 | ✅ |  |
| P3.A6 | musicstore | PARTIAL | yes | reasoning | 8 | 0 | 30 | 17 | ✅ |  |
| P3.A7 | musicstore | PARTIAL | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P3.A8 | musicstore | PARTIAL | yes | reasoning | 4 | 0 | 22 | 13 | ✅ |  |
| P3.A1 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A2 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A3 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A4 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A5 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A6 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A7 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A8 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P3.A1 | sinatra | PARTIAL | yes | reasoning | 8 | 0 | 45 | 19 | ✅ |  |
| P3.A2 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 15 | 10 | ✅ |  |
| P3.A3 | sinatra | PARTIAL | yes | reasoning | 3 | 0 | 9 | 7 | ✅ |  |
| P3.A4 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 12 | 8 | ✅ |  |
| P3.A5 | sinatra | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P3.A6 | sinatra | PARTIAL | yes | reasoning | 3 | 0 | 10 | 9 | ✅ |  |
| P3.A7 | sinatra | COMPLETE | yes | fast | 6 | 0 | 8 | 3 | ✅ |  |
| P3.A8 | sinatra | PARTIAL | yes | reasoning | 5 | 0 | 25 | 18 | ✅ |  |
| P3.A1 | golang-example | PARTIAL | yes | reasoning | 8 | 0 | 47 | 23 | ✅ |  |
| P3.A2 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 22 | 16 | ✅ |  |
| P3.A3 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 16 | 12 | ✅ |  |
| P3.A4 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 21 | 16 | ✅ |  |
| P3.A5 | golang-example | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 6 | ✅ |  |
| P3.A6 | golang-example | PARTIAL | yes | reasoning | 7 | 0 | 26 | 21 | ✅ |  |
| P3.A7 | golang-example | COMPLETE | yes | fast | 6 | 0 | 10 | 3 | ✅ |  |
| P3.A8 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 31 | 18 | ✅ |  |
| P3.A1 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A2 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A3 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A4 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A5 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A6 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A7 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A8 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A1 | react-redux-realworld | PARTIAL | yes | reasoning | 10 | 0 | 52 | 25 | ✅ |  |
| P3.A2 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 21 | 14 | ✅ |  |
| P3.A3 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 16 | 11 | ✅ |  |
| P3.A4 | react-redux-realworld | PARTIAL | yes | reasoning | 4 | 0 | 12 | 13 | ✅ |  |
| P3.A5 | react-redux-realworld | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 4 | ✅ |  |
| P3.A6 | react-redux-realworld | PARTIAL | yes | reasoning | 4 | 0 | 16 | 14 | ✅ |  |
| P3.A7 | react-redux-realworld | COMPLETE | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P3.A8 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 23 | 17 | ✅ |  |
| P3.A1 | eshop-on-web | PARTIAL | yes | reasoning | 8 | 0 | 49 | 28 | ✅ |  |
| P3.A2 | eshop-on-web | PARTIAL | yes | reasoning | 8 | 0 | 33 | 22 | ✅ |  |
| P3.A3 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 28 | 18 | ✅ |  |
| P3.A4 | eshop-on-web | PARTIAL | yes | reasoning | 5 | 0 | 20 | 12 | ✅ |  |
| P3.A5 | eshop-on-web | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P3.A6 | eshop-on-web | PARTIAL | yes | reasoning | 7 | 0 | 34 | 21 | ✅ |  |
| P3.A7 | eshop-on-web | COMPLETE | yes | fast | 6 | 0 | 13 | 1 | ✅ |  |
| P3.A8 | eshop-on-web | PARTIAL | yes | reasoning | 5 | 0 | 25 | 12 | ✅ |  |
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
| P3.A1 | mantisbt | PARTIAL | yes | reasoning | 8 | 0 | 47 | 21 | ✅ |  |
| P3.A2 | mantisbt | PARTIAL | yes | reasoning | 6 | 0 | 26 | 14 | ✅ |  |
| P3.A3 | mantisbt | PARTIAL | yes | reasoning | 5 | 0 | 18 | 12 | ✅ |  |
| P3.A4 | mantisbt | PARTIAL | yes | reasoning | 7 | 0 | 29 | 19 | ✅ |  |
| P3.A5 | mantisbt | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P3.A6 | mantisbt | PARTIAL | yes | reasoning | 8 | 0 | 37 | 21 | ✅ |  |
| P3.A7 | mantisbt | PARTIAL | yes | fast | 6 | 0 | 11 | 5 | ✅ |  |
| P3.A8 | mantisbt | PARTIAL | yes | reasoning | 6 | 0 | 23 | 14 | ✅ |  |
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
| P4.A1 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P4.A2 | spring-petclinic | COMPLETE | yes | fast | 5 | 1 | 3 | 2 | ✅ |  |
| P4.A3 | spring-petclinic | PARTIAL | yes | coding | 9 | 0 | 24 | 10 | ✅ |  |
| P4.A4 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P4.A6 | spring-petclinic | COMPLETE | yes | fast | 8 | 2 | 9 | 5 | ✅ |  |
| P4.A7 | spring-petclinic | COMPLETE | yes | fast | 7 | 1 | 11 | 2 | ✅ |  |
| P4.A8 | spring-petclinic | COMPLETE | yes | fast | 2 | 0 | 7 | 2 | ✅ |  |
| P4.A9 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 22 | 16 | ✅ |  |
| P4.A1 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P4.A2 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P4.A3 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P4.A4 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P4.A5 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P4.A6 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P4.A7 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P4.A8 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P4.A9 | flask-tutorial | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put flask-tutorial in the IA02 non-delivery register (Retire) |
| P4.A1 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A2 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 20 | 7 | ✅ |  |
| P4.A3 | django-realworld-example-app | PARTIAL | yes | coding | 9 | 0 | 23 | 14 | ✅ |  |
| P4.A4 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P4.A6 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 8 | 3 | ✅ |  |
| P4.A7 | django-realworld-example-app | COMPLETE | yes | fast | 7 | 1 | 11 | 2 | ✅ |  |
| P4.A8 | django-realworld-example-app | COMPLETE | yes | fast | 2 | 0 | 3 | 2 | ✅ |  |
| P4.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 24 | 17 | ✅ |  |
| P4.A1 | microblog | COMPLETE | yes | fast | 4 | 0 | 3 | 3 | ✅ |  |
| P4.A2 | microblog | COMPLETE | yes | fast | 6 | 0 | 12 | 2 | ✅ |  |
| P4.A3 | microblog | PARTIAL | yes | coding | 5 | 0 | 15 | 10 | ✅ |  |
| P4.A4 | microblog | COMPLETE | yes | fast | 3 | 0 | 6 | 4 | ✅ |  |
| P4.A5 | microblog | COMPLETE | yes | fast | 6 | 0 | 13 | 2 | ✅ |  |
| P4.A6 | microblog | PARTIAL | yes | fast | 6 | 0 | 14 | 6 | ✅ |  |
| P4.A7 | microblog | PARTIAL | yes | fast | 6 | 0 | 15 | 3 | ✅ |  |
| P4.A8 | microblog | COMPLETE | yes | fast | 7 | 1 | 11 | 4 | ✅ |  |
| P4.A9 | microblog | PARTIAL | yes | reasoning | 7 | 0 | 20 | 16 | ✅ |  |
| P4.A1 | node-express-realworld-example-app | COMPLETE | yes | fast | 4 | 0 | 3 | 2 | ✅ |  |
| P4.A2 | node-express-realworld-example-app | COMPLETE | yes | fast | 5 | 0 | 5 | 2 | ✅ |  |
| P4.A3 | node-express-realworld-example-app | PARTIAL | yes | coding | 9 | 1 | 19 | 12 | ✅ |  |
| P4.A4 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P4.A5 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A6 | node-express-realworld-example-app | COMPLETE | yes | fast | 7 | 1 | 6 | 4 | ✅ |  |
| P4.A7 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 6 | 4 | ✅ |  |
| P4.A8 | node-express-realworld-example-app | PARTIAL | yes | fast | 3 | 0 | 12 | 2 | ✅ |  |
| P4.A9 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 25 | 17 | ✅ |  |
| P4.A1 | musicstore | COMPLETE | yes | fast | 6 | 0 | 12 | 1 | ✅ |  |
| P4.A2 | musicstore | COMPLETE | yes | fast | 7 | 1 | 5 | 5 | ✅ |  |
| P4.A3 | musicstore | COMPLETE | yes | coding | 7 | 0 | 15 | 10 | ✅ |  |
| P4.A4 | musicstore | COMPLETE | yes | fast | 6 | 0 | 11 | 3 | ✅ |  |
| P4.A5 | musicstore | PARTIAL | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A6 | musicstore | COMPLETE | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P4.A7 | musicstore | COMPLETE | yes | fast | 6 | 0 | 13 | 1 | ✅ |  |
| P4.A8 | musicstore | COMPLETE | yes | fast | 2 | 0 | 4 | 2 | ✅ |  |
| P4.A9 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 23 | 16 | ✅ |  |
| P4.A1 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A2 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A3 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A4 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A5 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A6 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A7 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A8 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A9 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retire) |
| P4.A1 | sinatra | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A2 | sinatra | COMPLETE | yes | fast | 7 | 1 | 6 | 2 | ✅ |  |
| P4.A3 | sinatra | PARTIAL | yes | coding | 7 | 1 | 12 | 10 | ✅ |  |
| P4.A4 | sinatra | COMPLETE | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P4.A5 | sinatra | PARTIAL | yes | fast | 6 | 0 | 8 | 6 | ✅ |  |
| P4.A6 | sinatra | COMPLETE | yes | fast | 6 | 0 | 11 | 3 | ✅ |  |
| P4.A7 | sinatra | COMPLETE | yes | fast | 6 | 0 | 11 | 1 | ✅ |  |
| P4.A8 | sinatra | COMPLETE | yes | fast | 2 | 0 | 3 | 1 | ✅ |  |
| P4.A9 | sinatra | PARTIAL | yes | reasoning | 6 | 0 | 22 | 16 | ✅ |  |
| P4.A1 | golang-example | COMPLETE | yes | fast | 6 | 0 | 6 | 1 | ✅ |  |
| P4.A2 | golang-example | COMPLETE | yes | fast | 7 | 1 | 6 | 1 | ✅ |  |
| P4.A3 | golang-example | PARTIAL | yes | coding | 10 | 1 | 21 | 13 | ✅ |  |
| P4.A4 | golang-example | COMPLETE | yes | fast | 4 | 0 | 5 | 4 | ✅ |  |
| P4.A5 | golang-example | PARTIAL | yes | fast | 5 | 0 | 7 | 6 | ✅ |  |
| P4.A6 | golang-example | COMPLETE | yes | fast | 7 | 1 | 16 | 5 | ✅ |  |
| P4.A7 | golang-example | COMPLETE | yes | fast | 7 | 1 | 14 | 2 | ✅ |  |
| P4.A8 | golang-example | COMPLETE | yes | fast | 3 | 0 | 8 | 1 | ✅ |  |
| P4.A9 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 20 | 15 | ✅ |  |
| P4.A1 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A2 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A3 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A4 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A5 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A6 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A7 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A8 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A9 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A1 | react-redux-realworld | COMPLETE | yes | fast | 5 | 0 | 5 | 2 | ✅ |  |
| P4.A2 | react-redux-realworld | COMPLETE | yes | fast | 4 | 0 | 11 | 7 | ✅ |  |
| P4.A3 | react-redux-realworld | PARTIAL | yes | coding | 9 | 0 | 27 | 11 | ✅ |  |
| P4.A4 | react-redux-realworld | COMPLETE | yes | fast | 3 | 0 | 14 | 6 | ✅ |  |
| P4.A5 | react-redux-realworld | PARTIAL | yes | fast | 5 | 0 | 6 | 7 | ✅ |  |
| P4.A6 | react-redux-realworld | PARTIAL | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P4.A7 | react-redux-realworld | COMPLETE | yes | fast | 7 | 1 | 7 | 2 | ✅ |  |
| P4.A8 | react-redux-realworld | COMPLETE | yes | fast | 4 | 0 | 7 | 4 | ✅ |  |
| P4.A9 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 23 | 14 | ✅ |  |
| P4.A1 | eshop-on-web | COMPLETE | yes | fast | 1 | 0 | 0 | 2 | ✅ |  |
| P4.A2 | eshop-on-web | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A3 | eshop-on-web | PARTIAL | yes | coding | 7 | 0 | 15 | 9 | ✅ |  |
| P4.A4 | eshop-on-web | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | eshop-on-web | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A6 | eshop-on-web | COMPLETE | yes | fast | 7 | 1 | 7 | 2 | ✅ |  |
| P4.A7 | eshop-on-web | COMPLETE | yes | fast | 6 | 0 | 10 | 4 | ✅ |  |
| P4.A8 | eshop-on-web | COMPLETE | yes | fast | 7 | 1 | 11 | 1 | ✅ |  |
| P4.A9 | eshop-on-web | PARTIAL | yes | reasoning | 6 | 0 | 21 | 15 | ✅ |  |
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
| P4.A1 | mantisbt | COMPLETE | yes | fast | 3 | 0 | 2 | 2 | ✅ |  |
| P4.A2 | mantisbt | COMPLETE | yes | fast | 6 | 0 | 14 | 2 | ✅ |  |
| P4.A3 | mantisbt | PARTIAL | yes | coding | 5 | 0 | 10 | 11 | ✅ |  |
| P4.A4 | mantisbt | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | mantisbt | COMPLETE | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P4.A6 | mantisbt | COMPLETE | yes | fast | 6 | 0 | 15 | 2 | ✅ |  |
| P4.A7 | mantisbt | COMPLETE | yes | fast | 6 | 0 | 11 | 1 | ✅ |  |
| P4.A8 | mantisbt | COMPLETE | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P4.A9 | mantisbt | PARTIAL | yes | reasoning | 6 | 0 | 18 | 20 | ✅ |  |
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
