# E2E agentic acceptance run `run5`

- **Job**: `job-1791792319-d40469` — **COMPLETED**
- **Repositories**: `spring-petclinic`, `flask-tutorial`, `django-realworld-example-app`, `node-express-realworld-example-app`, `musicstore`, `laravel58`, `sinatra`, `golang-example`, `todomvc`, `react-redux-realworld`
- **Elapsed**: 85 min 43 s; LLM cache mode `record` (record = every call live, responses recorded for replay)
- **Astra tiers**: {'reasoning': 'gpt-6-astra', 'coding': 'gpt-5.3-codex-PlayWright', 'fast': 'gpt-4.1-mini', 'fallback': 'gpt-5.4'}
- **Human surfaces**: review_mode=human; release-gate approvals and stakeholder answers were submitted over the API by a **scripted** reviewer/stakeholder (labelled as automation in every record).

## Result

**Agent success rate: 100.00%** (253/253 P1–P4 agent dispatches; threshold > 97.0%).

34 P3/P4 agent slots were **not admitted** because the authorized P2 release gate routed `laravel58` (Retain), `todomvc` (Retain) to the non-delivery register — by design, no architecture or plan is produced for a non-delivery route. Counting those slots as failures would give 88.15%.

Success = artifact not FAILED **and** enriched by the live Astra agent loop (not seed fallback) **and** passes ContractValidator (envelope + payload schema + content hash).

| phase | ok / total |
|---|---|
| P1 Discovery | 110 / 110 |
| P2 Portfolio | 7 / 7 |
| P3 Architecture | 64 / 64 |
| P4 Planning | 72 / 72 |

- Tool calls: 4241; evidence ids cited: 2555; LLM findings: 1510; repair rounds: 25; failovers: 0
- Tokens: {'input': 18423252, 'output': 961300, 'reasoning': 53016}

## Release gates

| phase | app | phase status | decision |
|---|---|---|---|
| P1 | django-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | musicstore | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | flask-tutorial | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | spring-petclinic | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | node-express-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | laravel58 | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | sinatra | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | golang-example | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | todomvc | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | react-redux-realworld | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P2 | PF1 | COMPLETED | AUTHORIZED |
| P3 | laravel58 | NOT_ADMITTED | — |
| P4 | laravel58 | NOT_ADMITTED | — |
| P3 | todomvc | NOT_ADMITTED | — |
| P4 | todomvc | NOT_ADMITTED | — |
| P3 | spring-petclinic | COMPLETED | CONDITIONAL_PLANNING |
| P3 | flask-tutorial | COMPLETED | CONDITIONAL_PLANNING |
| P3 | musicstore | COMPLETED | CONDITIONAL_PLANNING |
| P3 | node-express-realworld-example-app | COMPLETED | CONDITIONAL_PLANNING |
| P3 | django-realworld-example-app | COMPLETED | CONDITIONAL_PLANNING |
| P4 | django-realworld-example-app | COMPLETED | SCOPED_PREPARATION |
| P4 | flask-tutorial | COMPLETED | SCOPED_PREPARATION |
| P4 | musicstore | COMPLETED | SCOPED_PREPARATION |
| P4 | node-express-realworld-example-app | COMPLETED | SCOPED_PREPARATION |
| P3 | sinatra | COMPLETED | CONDITIONAL_PLANNING |
| P3 | golang-example | COMPLETED | CONDITIONAL_PLANNING |
| P4 | spring-petclinic | COMPLETED | SCOPED_PREPARATION |
| P3 | react-redux-realworld | COMPLETED | CONDITIONAL_PLANNING |
| P4 | sinatra | COMPLETED | SCOPED_PREPARATION |
| P4 | golang-example | COMPLETED | SCOPED_PREPARATION |
| P4 | react-redux-realworld | COMPLETED | SCOPED_PREPARATION |

Reviews: 27 (decided by `scripted-reviewer`); stakeholder questions: 72 (72 answered).

## Per-agent results

| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| P1.A1 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 39 | 24 | ✅ |  |
| P1.A2 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 29 | 21 | ✅ |  |
| P1.A3 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 25 | 19 | ✅ |  |
| P1.A4 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 10 | 10 | ✅ |  |
| P1.A5 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 8 | 7 | ✅ |  |
| P1.A6 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 26 | 21 | ✅ |  |
| P1.A7 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 11 | 4 | ✅ |  |
| P1.A8 | spring-petclinic | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | spring-petclinic | PARTIAL | yes | reasoning | 4 | 0 | 20 | 16 | ✅ |  |
| P1.A10 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 17 | 11 | ✅ |  |
| P1.A11 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 14 | 9 | ✅ |  |
| P1.A1 | flask-tutorial | PARTIAL | yes | reasoning | 6 | 0 | 26 | 18 | ✅ |  |
| P1.A2 | flask-tutorial | PARTIAL | yes | reasoning | 3 | 0 | 12 | 11 | ✅ |  |
| P1.A3 | flask-tutorial | PARTIAL | yes | reasoning | 3 | 0 | 11 | 8 | ✅ |  |
| P1.A4 | flask-tutorial | PARTIAL | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P1.A5 | flask-tutorial | PARTIAL | yes | fast | 6 | 0 | 14 | 12 | ✅ |  |
| P1.A6 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 15 | 13 | ✅ |  |
| P1.A7 | flask-tutorial | PARTIAL | yes | fast | 7 | 1 | 10 | 7 | ✅ |  |
| P1.A8 | flask-tutorial | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 21 | 11 | ✅ |  |
| P1.A10 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 0 | 14 | 10 | ✅ |  |
| P1.A11 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 13 | 9 | ✅ |  |
| P1.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 37 | 20 | ✅ |  |
| P1.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 23 | 20 | ✅ |  |
| P1.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 27 | 17 | ✅ |  |
| P1.A4 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P1.A5 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 8 | 7 | ✅ |  |
| P1.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 19 | 17 | ✅ |  |
| P1.A7 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 32 | 17 | ✅ |  |
| P1.A10 | django-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 22 | 11 | ✅ |  |
| P1.A11 | django-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 11 | 10 | ✅ |  |
| P1.A1 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 48 | 22 | ✅ |  |
| P1.A2 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 23 | 15 | ✅ |  |
| P1.A3 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 28 | 21 | ✅ |  |
| P1.A4 | node-express-realworld-example-app | PARTIAL | yes | fast | 7 | 1 | 10 | 7 | ✅ |  |
| P1.A5 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 8 | 7 | ✅ |  |
| P1.A6 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 22 | 21 | ✅ |  |
| P1.A7 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P1.A8 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 27 | 11 | ✅ |  |
| P1.A10 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 23 | 12 | ✅ |  |
| P1.A11 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 15 | 11 | ✅ |  |
| P1.A1 | musicstore | PARTIAL | yes | reasoning | 8 | 0 | 55 | 22 | ✅ |  |
| P1.A2 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 21 | 15 | ✅ |  |
| P1.A3 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 29 | 21 | ✅ |  |
| P1.A4 | musicstore | PARTIAL | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P1.A5 | musicstore | PARTIAL | yes | fast | 7 | 0 | 14 | 11 | ✅ |  |
| P1.A6 | musicstore | PARTIAL | yes | reasoning | 10 | 0 | 36 | 13 | ✅ |  |
| P1.A7 | musicstore | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A8 | musicstore | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | musicstore | PARTIAL | yes | reasoning | 7 | 0 | 29 | 16 | ✅ |  |
| P1.A10 | musicstore | PARTIAL | yes | reasoning | 6 | 0 | 17 | 10 | ✅ |  |
| P1.A11 | musicstore | PARTIAL | yes | reasoning | 4 | 0 | 13 | 9 | ✅ |  |
| P1.A1 | laravel58 | PARTIAL | yes | reasoning | 6 | 0 | 32 | 19 | ✅ |  |
| P1.A2 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 26 | 20 | ✅ |  |
| P1.A3 | laravel58 | PARTIAL | yes | reasoning | 7 | 0 | 28 | 17 | ✅ |  |
| P1.A4 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 13 | 2 | ✅ |  |
| P1.A5 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 8 | 6 | ✅ |  |
| P1.A6 | laravel58 | PARTIAL | yes | reasoning | 4 | 0 | 16 | 16 | ✅ |  |
| P1.A7 | laravel58 | PARTIAL | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P1.A8 | laravel58 | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | laravel58 | PARTIAL | yes | reasoning | 5 | 0 | 31 | 23 | ✅ |  |
| P1.A10 | laravel58 | PARTIAL | yes | reasoning | 6 | 0 | 18 | 10 | ✅ |  |
| P1.A11 | laravel58 | PARTIAL | yes | reasoning | 4 | 0 | 12 | 9 | ✅ |  |
| P1.A1 | sinatra | PARTIAL | yes | reasoning | 6 | 0 | 29 | 17 | ✅ |  |
| P1.A2 | sinatra | PARTIAL | yes | reasoning | 4 | 1 | 11 | 11 | ✅ |  |
| P1.A3 | sinatra | PARTIAL | yes | reasoning | 5 | 1 | 11 | 7 | ✅ |  |
| P1.A4 | sinatra | PARTIAL | yes | fast | 6 | 0 | 5 | 5 | ✅ |  |
| P1.A5 | sinatra | PARTIAL | yes | fast | 7 | 1 | 6 | 4 | ✅ |  |
| P1.A6 | sinatra | PARTIAL | yes | reasoning | 3 | 0 | 10 | 11 | ✅ |  |
| P1.A7 | sinatra | PARTIAL | yes | fast | 7 | 1 | 5 | 5 | ✅ |  |
| P1.A8 | sinatra | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | sinatra | PARTIAL | yes | reasoning | 4 | 1 | 11 | 9 | ✅ |  |
| P1.A10 | sinatra | PARTIAL | yes | reasoning | 5 | 0 | 14 | 10 | ✅ |  |
| P1.A11 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 10 | 9 | ✅ |  |
| P1.A1 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 34 | 21 | ✅ |  |
| P1.A2 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 17 | 13 | ✅ |  |
| P1.A3 | golang-example | PARTIAL | yes | reasoning | 4 | 0 | 18 | 16 | ✅ |  |
| P1.A4 | golang-example | PARTIAL | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P1.A5 | golang-example | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A6 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 19 | 18 | ✅ |  |
| P1.A7 | golang-example | SKIPPED_APPROVED | yes | fast | 7 | 1 | 5 | 3 | ✅ |  |
| P1.A8 | golang-example | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | golang-example | PARTIAL | yes | reasoning | 4 | 0 | 20 | 13 | ✅ |  |
| P1.A10 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 20 | 11 | ✅ |  |
| P1.A11 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 18 | 12 | ✅ |  |
| P1.A1 | todomvc | PARTIAL | yes | reasoning | 7 | 0 | 52 | 23 | ✅ |  |
| P1.A2 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 24 | 17 | ✅ |  |
| P1.A3 | todomvc | PARTIAL | yes | reasoning | 7 | 0 | 35 | 19 | ✅ |  |
| P1.A4 | todomvc | PARTIAL | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P1.A5 | todomvc | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A6 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 25 | 18 | ✅ |  |
| P1.A7 | todomvc | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A8 | todomvc | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 22 | 17 | ✅ |  |
| P1.A10 | todomvc | PARTIAL | yes | reasoning | 6 | 0 | 22 | 10 | ✅ |  |
| P1.A11 | todomvc | PARTIAL | yes | reasoning | 5 | 0 | 16 | 9 | ✅ |  |
| P1.A1 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 25 | 12 | ✅ |  |
| P1.A2 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 20 | 14 | ✅ |  |
| P1.A3 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 25 | 9 | ✅ |  |
| P1.A4 | react-redux-realworld | PARTIAL | yes | fast | 6 | 0 | 10 | 4 | ✅ |  |
| P1.A5 | react-redux-realworld | PARTIAL | yes | fast | 7 | 0 | 9 | 5 | ✅ |  |
| P1.A6 | react-redux-realworld | PARTIAL | yes | reasoning | 4 | 0 | 15 | 14 | ✅ |  |
| P1.A7 | react-redux-realworld | PARTIAL | yes | fast | 7 | 0 | 6 | 2 | ✅ |  |
| P1.A8 | react-redux-realworld | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 39 | 14 | ✅ |  |
| P1.A10 | react-redux-realworld | PARTIAL | yes | reasoning | 7 | 0 | 18 | 11 | ✅ |  |
| P1.A11 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 16 | 11 | ✅ |  |
| P2.A1 | PF1 | PARTIAL | yes | reasoning | 8 | 0 | 36 | 27 | ✅ |  |
| P2.A2 | PF1 | PARTIAL | yes | reasoning | 9 | 0 | 37 | 20 | ✅ |  |
| P2.A3 | PF1 | COMPLETE | yes | fast | 6 | 0 | 6 | 1 | ✅ |  |
| P2.A4 | PF1 | COMPLETE | yes | fast | 6 | 0 | 8 | 6 | ✅ |  |
| P2.A5 | PF1 | COMPLETE | yes | fast | 6 | 0 | 17 | 8 | ✅ |  |
| P2.A6 | PF1 | PARTIAL | yes | reasoning | 9 | 0 | 55 | 21 | ✅ |  |
| P2.A7 | PF1 | PARTIAL | yes | reasoning | 6 | 0 | 28 | 22 | ✅ |  |
| P3.A1 | spring-petclinic | PARTIAL | yes | reasoning | 8 | 0 | 54 | 35 | ✅ |  |
| P3.A2 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 25 | 18 | ✅ |  |
| P3.A3 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 24 | 19 | ✅ |  |
| P3.A4 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 23 | 16 | ✅ |  |
| P3.A5 | spring-petclinic | SKIPPED_APPROVED | yes | fast | 6 | 0 | 10 | 6 | ✅ |  |
| P3.A6 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 34 | 20 | ✅ |  |
| P3.A7 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P3.A8 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 35 | 16 | ✅ |  |
| P3.A1 | flask-tutorial | PARTIAL | yes | reasoning | 8 | 0 | 40 | 23 | ✅ |  |
| P3.A2 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 18 | 13 | ✅ |  |
| P3.A3 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 16 | 12 | ✅ |  |
| P3.A4 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 12 | 12 | ✅ |  |
| P3.A5 | flask-tutorial | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 7 | ✅ |  |
| P3.A6 | flask-tutorial | PARTIAL | yes | reasoning | 4 | 0 | 18 | 16 | ✅ |  |
| P3.A7 | flask-tutorial | COMPLETE | yes | fast | 7 | 1 | 9 | 1 | ✅ |  |
| P3.A8 | flask-tutorial | PARTIAL | yes | reasoning | 5 | 0 | 23 | 10 | ✅ |  |
| P3.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 51 | 33 | ✅ |  |
| P3.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 27 | 19 | ✅ |  |
| P3.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 21 | 15 | ✅ |  |
| P3.A4 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 19 | 14 | ✅ |  |
| P3.A5 | django-realworld-example-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P3.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 28 | 20 | ✅ |  |
| P3.A7 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 12 | 5 | ✅ |  |
| P3.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 29 | 16 | ✅ |  |
| P3.A1 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 8 | 0 | 52 | 27 | ✅ |  |
| P3.A2 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 23 | 17 | ✅ |  |
| P3.A3 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 17 | 14 | ✅ |  |
| P3.A4 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 22 | 16 | ✅ |  |
| P3.A5 | node-express-realworld-example-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P3.A6 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 35 | 27 | ✅ |  |
| P3.A7 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 18 | 1 | ✅ |  |
| P3.A8 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 28 | 12 | ✅ |  |
| P3.A1 | musicstore | PARTIAL | yes | reasoning | 10 | 0 | 54 | 26 | ✅ |  |
| P3.A2 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 23 | 18 | ✅ |  |
| P3.A3 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 21 | 12 | ✅ |  |
| P3.A4 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 15 | 13 | ✅ |  |
| P3.A5 | musicstore | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 6 | ✅ |  |
| P3.A6 | musicstore | PARTIAL | yes | reasoning | 7 | 0 | 29 | 15 | ✅ |  |
| P3.A7 | musicstore | PARTIAL | yes | fast | 5 | 0 | 8 | 5 | ✅ |  |
| P3.A8 | musicstore | PARTIAL | yes | reasoning | 5 | 0 | 28 | 13 | ✅ |  |
| P3.A1 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P3.A2 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P3.A3 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P3.A4 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P3.A5 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P3.A6 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P3.A7 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P3.A8 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P3.A1 | sinatra | PARTIAL | yes | reasoning | 8 | 0 | 47 | 18 | ✅ |  |
| P3.A2 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 16 | 10 | ✅ |  |
| P3.A3 | sinatra | PARTIAL | yes | reasoning | 4 | 0 | 13 | 9 | ✅ |  |
| P3.A4 | sinatra | PARTIAL | yes | reasoning | 3 | 0 | 8 | 7 | ✅ |  |
| P3.A5 | sinatra | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P3.A6 | sinatra | PARTIAL | yes | reasoning | 3 | 0 | 11 | 7 | ✅ |  |
| P3.A7 | sinatra | PARTIAL | yes | fast | 6 | 0 | 11 | 2 | ✅ |  |
| P3.A8 | sinatra | PARTIAL | yes | reasoning | 5 | 0 | 25 | 12 | ✅ |  |
| P3.A1 | golang-example | PARTIAL | yes | reasoning | 9 | 0 | 50 | 31 | ✅ |  |
| P3.A2 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 23 | 15 | ✅ |  |
| P3.A3 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 17 | 12 | ✅ |  |
| P3.A4 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 23 | 16 | ✅ |  |
| P3.A5 | golang-example | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 7 | ✅ |  |
| P3.A6 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 22 | 17 | ✅ |  |
| P3.A7 | golang-example | COMPLETE | yes | fast | 5 | 0 | 8 | 2 | ✅ |  |
| P3.A8 | golang-example | PARTIAL | yes | reasoning | 6 | 0 | 34 | 13 | ✅ |  |
| P3.A1 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A2 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A3 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A4 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A5 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A6 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A7 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A8 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P3.A1 | react-redux-realworld | PARTIAL | yes | reasoning | 9 | 0 | 52 | 27 | ✅ |  |
| P3.A2 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 24 | 17 | ✅ |  |
| P3.A3 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 18 | 10 | ✅ |  |
| P3.A4 | react-redux-realworld | PARTIAL | yes | reasoning | 4 | 0 | 15 | 13 | ✅ |  |
| P3.A5 | react-redux-realworld | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P3.A6 | react-redux-realworld | PARTIAL | yes | reasoning | 3 | 0 | 14 | 11 | ✅ |  |
| P3.A7 | react-redux-realworld | COMPLETE | yes | fast | 6 | 0 | 18 | 1 | ✅ |  |
| P3.A8 | react-redux-realworld | PARTIAL | yes | reasoning | 5 | 0 | 24 | 16 | ✅ |  |
| P4.A1 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 10 | 3 | ✅ |  |
| P4.A2 | spring-petclinic | COMPLETE | yes | fast | 5 | 1 | 12 | 3 | ✅ |  |
| P4.A3 | spring-petclinic | PARTIAL | yes | coding | 9 | 0 | 17 | 11 | ✅ |  |
| P4.A4 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P4.A5 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P4.A6 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P4.A7 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 13 | 1 | ✅ |  |
| P4.A8 | spring-petclinic | PARTIAL | yes | fast | 2 | 0 | 4 | 5 | ✅ |  |
| P4.A9 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 20 | 16 | ✅ |  |
| P4.A1 | flask-tutorial | COMPLETE | yes | fast | 4 | 0 | 3 | 3 | ✅ |  |
| P4.A2 | flask-tutorial | COMPLETE | yes | fast | 2 | 0 | 1 | 3 | ✅ |  |
| P4.A3 | flask-tutorial | PARTIAL | yes | coding | 8 | 0 | 19 | 11 | ✅ |  |
| P4.A4 | flask-tutorial | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | flask-tutorial | COMPLETE | yes | fast | 6 | 0 | 11 | 1 | ✅ |  |
| P4.A6 | flask-tutorial | COMPLETE | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P4.A7 | flask-tutorial | COMPLETE | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P4.A8 | flask-tutorial | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A9 | flask-tutorial | PARTIAL | yes | reasoning | 6 | 0 | 20 | 17 | ✅ |  |
| P4.A1 | django-realworld-example-app | COMPLETE | yes | fast | 3 | 0 | 2 | 3 | ✅ |  |
| P4.A2 | django-realworld-example-app | COMPLETE | yes | fast | 3 | 1 | 2 | 3 | ✅ |  |
| P4.A3 | django-realworld-example-app | PARTIAL | yes | coding | 10 | 0 | 21 | 9 | ✅ |  |
| P4.A4 | django-realworld-example-app | COMPLETE | yes | fast | 4 | 0 | 7 | 3 | ✅ |  |
| P4.A5 | django-realworld-example-app | PARTIAL | yes | fast | 7 | 1 | 7 | 7 | ✅ |  |
| P4.A6 | django-realworld-example-app | COMPLETE | yes | fast | 7 | 1 | 8 | 4 | ✅ |  |
| P4.A7 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 12 | 4 | ✅ |  |
| P4.A8 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P4.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 21 | 15 | ✅ |  |
| P4.A1 | node-express-realworld-example-app | COMPLETE | yes | fast | 4 | 0 | 3 | 1 | ✅ |  |
| P4.A2 | node-express-realworld-example-app | COMPLETE | yes | fast | 2 | 0 | 2 | 2 | ✅ |  |
| P4.A3 | node-express-realworld-example-app | PARTIAL | yes | coding | 8 | 0 | 27 | 14 | ✅ |  |
| P4.A4 | node-express-realworld-example-app | PARTIAL | yes | fast | 4 | 0 | 17 | 1 | ✅ |  |
| P4.A5 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P4.A6 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P4.A7 | node-express-realworld-example-app | COMPLETE | yes | fast | 7 | 1 | 12 | 2 | ✅ |  |
| P4.A8 | node-express-realworld-example-app | COMPLETE | yes | fast | 7 | 1 | 16 | 1 | ✅ |  |
| P4.A9 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 18 | 15 | ✅ |  |
| P4.A1 | musicstore | COMPLETE | yes | fast | 5 | 0 | 4 | 2 | ✅ |  |
| P4.A2 | musicstore | COMPLETE | yes | fast | 5 | 0 | 5 | 3 | ✅ |  |
| P4.A3 | musicstore | PARTIAL | yes | coding | 8 | 0 | 15 | 9 | ✅ |  |
| P4.A4 | musicstore | PARTIAL | yes | fast | 7 | 1 | 15 | 1 | ✅ |  |
| P4.A5 | musicstore | COMPLETE | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P4.A6 | musicstore | COMPLETE | yes | fast | 7 | 1 | 9 | 2 | ✅ |  |
| P4.A7 | musicstore | COMPLETE | yes | fast | 6 | 0 | 15 | 1 | ✅ |  |
| P4.A8 | musicstore | PARTIAL | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P4.A9 | musicstore | PARTIAL | yes | reasoning | 7 | 0 | 25 | 17 | ✅ |  |
| P4.A1 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P4.A2 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P4.A3 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P4.A4 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P4.A5 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P4.A6 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P4.A7 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P4.A8 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P4.A9 | laravel58 | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put laravel58 in the IA02 non-delivery register (Retain) |
| P4.A1 | sinatra | COMPLETE | yes | fast | 3 | 0 | 2 | 2 | ✅ |  |
| P4.A2 | sinatra | COMPLETE | yes | fast | 3 | 1 | 5 | 5 | ✅ |  |
| P4.A3 | sinatra | PARTIAL | yes | coding | 6 | 0 | 14 | 10 | ✅ |  |
| P4.A4 | sinatra | COMPLETE | yes | fast | 5 | 0 | 10 | 2 | ✅ |  |
| P4.A5 | sinatra | COMPLETE | yes | fast | 7 | 1 | 9 | 1 | ✅ |  |
| P4.A6 | sinatra | PARTIAL | yes | fast | 7 | 1 | 8 | 6 | ✅ |  |
| P4.A7 | sinatra | COMPLETE | yes | fast | 6 | 0 | 6 | 1 | ✅ |  |
| P4.A8 | sinatra | PARTIAL | yes | fast | 4 | 1 | 8 | 1 | ✅ |  |
| P4.A9 | sinatra | PARTIAL | yes | reasoning | 6 | 0 | 25 | 18 | ✅ |  |
| P4.A1 | golang-example | COMPLETE | yes | fast | 4 | 0 | 3 | 2 | ✅ |  |
| P4.A2 | golang-example | COMPLETE | yes | fast | 8 | 2 | 6 | 2 | ✅ |  |
| P4.A3 | golang-example | PARTIAL | yes | coding | 7 | 0 | 17 | 14 | ✅ |  |
| P4.A4 | golang-example | COMPLETE | yes | fast | 4 | 0 | 8 | 4 | ✅ |  |
| P4.A5 | golang-example | COMPLETE | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P4.A6 | golang-example | PARTIAL | yes | fast | 7 | 1 | 13 | 3 | ✅ |  |
| P4.A7 | golang-example | COMPLETE | yes | fast | 6 | 0 | 12 | 2 | ✅ |  |
| P4.A8 | golang-example | COMPLETE | yes | fast | 2 | 0 | 3 | 4 | ✅ |  |
| P4.A9 | golang-example | PARTIAL | yes | reasoning | 5 | 0 | 17 | 14 | ✅ |  |
| P4.A1 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A2 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A3 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A4 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A5 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A6 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A7 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A8 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A9 | todomvc | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put todomvc in the IA02 non-delivery register (Retain) |
| P4.A1 | react-redux-realworld | COMPLETE | yes | fast | 3 | 0 | 2 | 2 | ✅ |  |
| P4.A2 | react-redux-realworld | COMPLETE | yes | fast | 4 | 0 | 10 | 5 | ✅ |  |
| P4.A3 | react-redux-realworld | PARTIAL | yes | coding | 7 | 0 | 19 | 8 | ✅ |  |
| P4.A4 | react-redux-realworld | PARTIAL | yes | fast | 6 | 0 | 11 | 6 | ✅ |  |
| P4.A5 | react-redux-realworld | PARTIAL | yes | fast | 4 | 0 | 4 | 3 | ✅ |  |
| P4.A6 | react-redux-realworld | COMPLETE | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P4.A7 | react-redux-realworld | COMPLETE | yes | fast | 7 | 1 | 11 | 2 | ✅ |  |
| P4.A8 | react-redux-realworld | PARTIAL | yes | fast | 2 | 0 | 3 | 1 | ✅ |  |
| P4.A9 | react-redux-realworld | PARTIAL | yes | reasoning | 6 | 0 | 20 | 16 | ✅ |  |
