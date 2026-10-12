# E2E agentic acceptance run `run2`

- **Job**: `job-1791605204-92d529` — **COMPLETED**
- **Repositories**: `spring-petclinic`, `microblog`, `node-express-realworld-example-app`, `django-realworld-example-app`
- **Elapsed**: 63 min 1 s; LLM cache mode `record` (record = every call live, responses recorded for replay)
- **Astra tiers**: {'reasoning': 'gpt-6-astra', 'coding': 'gpt-5.3-codex-PlayWright', 'fast': 'gpt-4.1-mini', 'fallback': 'gpt-5.4'}
- **Human surfaces**: review_mode=human; release-gate approvals and stakeholder answers were submitted over the API by a **scripted** reviewer/stakeholder (labelled as automation in every record).

## Result

**Agent success rate: 100.00%** (119/119 P1–P4 agent dispatches; threshold > 97.0%).

Success = artifact not FAILED **and** enriched by the live Astra agent loop (not seed fallback) **and** passes ContractValidator (envelope + payload schema + content hash).

| phase | ok / total |
|---|---|
| P1 Discovery | 44 / 44 |
| P2 Portfolio | 7 / 7 |
| P3 Architecture | 32 / 32 |
| P4 Planning | 36 / 36 |

- Tool calls: 2046; evidence ids cited: 1226; LLM findings: 738; repair rounds: 3; failovers: 0
- Tokens: {'input': 9095568, 'output': 457565, 'reasoning': 23262}

## Release gates

| phase | app | phase status | decision |
|---|---|---|---|
| P1 | spring-petclinic | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | django-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | microblog | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | node-express-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P2 | PF1 | COMPLETED | AUTHORIZED |
| P3 | django-realworld-example-app | COMPLETED | CONDITIONAL_PLANNING |
| P3 | node-express-realworld-example-app | COMPLETED | CONDITIONAL_PLANNING |
| P3 | spring-petclinic | COMPLETED | CONDITIONAL_PLANNING |
| P3 | microblog | COMPLETED | CONDITIONAL_PLANNING |
| P4 | microblog | COMPLETED | SCOPED_PREPARATION |
| P4 | node-express-realworld-example-app | COMPLETED | SCOPED_PREPARATION |
| P4 | django-realworld-example-app | COMPLETED | SCOPED_PREPARATION |
| P4 | spring-petclinic | COMPLETED | SCOPED_PREPARATION |

Reviews: 17 (decided by `scripted-reviewer`); stakeholder questions: 28 (28 answered).

## Per-agent results

| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| P1.A1 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 37 | 26 | ✅ |  |
| P1.A2 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 26 | 21 | ✅ |  |
| P1.A3 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 29 | 19 | ✅ |  |
| P1.A4 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 13 | 10 | ✅ |  |
| P1.A5 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P1.A6 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 25 | 23 | ✅ |  |
| P1.A7 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 5 | 5 | ✅ |  |
| P1.A8 | spring-petclinic | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 19 | 14 | ✅ |  |
| P1.A10 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 18 | 11 | ✅ |  |
| P1.A11 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 13 | 9 | ✅ |  |
| P1.A1 | microblog | PARTIAL | yes | reasoning | 7 | 0 | 43 | 19 | ✅ |  |
| P1.A2 | microblog | PARTIAL | yes | reasoning | 4 | 0 | 20 | 16 | ✅ |  |
| P1.A3 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 22 | 19 | ✅ |  |
| P1.A4 | microblog | PARTIAL | yes | fast | 6 | 0 | 7 | 8 | ✅ |  |
| P1.A5 | microblog | PARTIAL | yes | fast | 6 | 0 | 9 | 7 | ✅ |  |
| P1.A6 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 27 | 27 | ✅ |  |
| P1.A7 | microblog | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A8 | microblog | PARTIAL | yes | reasoning | 2 | 0 | 1 | 3 | ✅ |  |
| P1.A9 | microblog | PARTIAL | yes | reasoning | 4 | 0 | 19 | 12 | ✅ |  |
| P1.A10 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 19 | 10 | ✅ |  |
| P1.A11 | microblog | PARTIAL | yes | reasoning | 4 | 0 | 11 | 9 | ✅ |  |
| P1.A1 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 40 | 18 | ✅ |  |
| P1.A2 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 29 | 18 | ✅ |  |
| P1.A3 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 30 | 24 | ✅ |  |
| P1.A4 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P1.A5 | node-express-realworld-example-app | PARTIAL | yes | fast | 7 | 0 | 10 | 11 | ✅ |  |
| P1.A6 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 19 | 17 | ✅ |  |
| P1.A7 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P1.A8 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 18 | 15 | ✅ |  |
| P1.A10 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 20 | 10 | ✅ |  |
| P1.A11 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 14 | 10 | ✅ |  |
| P1.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 39 | 13 | ✅ |  |
| P1.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 23 | 19 | ✅ |  |
| P1.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 23 | 15 | ✅ |  |
| P1.A4 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P1.A5 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 10 | 8 | ✅ |  |
| P1.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 20 | 19 | ✅ |  |
| P1.A7 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P1.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 20 | 10 | ✅ |  |
| P1.A10 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 18 | 11 | ✅ |  |
| P1.A11 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 12 | 9 | ✅ |  |
| P2.A1 | PF1 | PARTIAL | yes | reasoning | 8 | 0 | 26 | 17 | ✅ |  |
| P2.A2 | PF1 | PARTIAL | yes | reasoning | 8 | 0 | 28 | 20 | ✅ |  |
| P2.A3 | PF1 | COMPLETE | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P2.A4 | PF1 | COMPLETE | yes | fast | 4 | 0 | 7 | 3 | ✅ |  |
| P2.A5 | PF1 | COMPLETE | yes | fast | 3 | 0 | 4 | 3 | ✅ |  |
| P2.A6 | PF1 | PARTIAL | yes | reasoning | 6 | 0 | 24 | 16 | ✅ |  |
| P2.A7 | PF1 | PARTIAL | yes | reasoning | 5 | 0 | 15 | 13 | ✅ |  |
| P3.A1 | spring-petclinic | PARTIAL | yes | reasoning | 9 | 0 | 51 | 27 | ✅ |  |
| P3.A2 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 24 | 14 | ✅ |  |
| P3.A3 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 22 | 18 | ✅ |  |
| P3.A4 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 18 | 13 | ✅ |  |
| P3.A5 | spring-petclinic | SKIPPED_APPROVED | yes | fast | 6 | 0 | 10 | 6 | ✅ |  |
| P3.A6 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 26 | 18 | ✅ |  |
| P3.A7 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P3.A8 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 29 | 11 | ✅ |  |
| P3.A1 | microblog | PARTIAL | yes | reasoning | 9 | 0 | 47 | 21 | ✅ |  |
| P3.A2 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 22 | 18 | ✅ |  |
| P3.A3 | microblog | PARTIAL | yes | reasoning | 4 | 0 | 16 | 12 | ✅ |  |
| P3.A4 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 24 | 15 | ✅ |  |
| P3.A5 | microblog | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 6 | ✅ |  |
| P3.A6 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 25 | 16 | ✅ |  |
| P3.A7 | microblog | COMPLETE | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P3.A8 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 32 | 18 | ✅ |  |
| P3.A1 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 9 | 0 | 45 | 20 | ✅ |  |
| P3.A2 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 25 | 17 | ✅ |  |
| P3.A3 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 21 | 13 | ✅ |  |
| P3.A4 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 25 | 17 | ✅ |  |
| P3.A5 | node-express-realworld-example-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 6 | ✅ |  |
| P3.A6 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 30 | 20 | ✅ |  |
| P3.A7 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 8 | 3 | ✅ |  |
| P3.A8 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 33 | 15 | ✅ |  |
| P3.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 9 | 0 | 49 | 26 | ✅ |  |
| P3.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 26 | 14 | ✅ |  |
| P3.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 22 | 17 | ✅ |  |
| P3.A4 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 22 | 15 | ✅ |  |
| P3.A5 | django-realworld-example-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 3 | ✅ |  |
| P3.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 24 | 18 | ✅ |  |
| P3.A7 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 10 | 5 | ✅ |  |
| P3.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 31 | 12 | ✅ |  |
| P4.A1 | spring-petclinic | COMPLETE | yes | fast | 4 | 0 | 3 | 2 | ✅ |  |
| P4.A2 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 6 | 2 | ✅ |  |
| P4.A3 | spring-petclinic | PARTIAL | yes | coding | 9 | 0 | 22 | 9 | ✅ |  |
| P4.A4 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P4.A5 | spring-petclinic | PARTIAL | yes | fast | 2 | 0 | 3 | 4 | ✅ |  |
| P4.A6 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 13 | 3 | ✅ |  |
| P4.A7 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 10 | 4 | ✅ |  |
| P4.A8 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 13 | 1 | ✅ |  |
| P4.A9 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 23 | 17 | ✅ |  |
| P4.A1 | microblog | COMPLETE | yes | fast | 3 | 0 | 2 | 2 | ✅ |  |
| P4.A2 | microblog | COMPLETE | yes | fast | 6 | 0 | 6 | 2 | ✅ |  |
| P4.A3 | microblog | PARTIAL | yes | coding | 9 | 0 | 17 | 12 | ✅ |  |
| P4.A4 | microblog | COMPLETE | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P4.A5 | microblog | PARTIAL | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P4.A6 | microblog | COMPLETE | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P4.A7 | microblog | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A8 | microblog | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P4.A9 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 25 | 18 | ✅ |  |
| P4.A1 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 13 | 2 | ✅ |  |
| P4.A2 | node-express-realworld-example-app | COMPLETE | yes | fast | 5 | 0 | 17 | 2 | ✅ |  |
| P4.A3 | node-express-realworld-example-app | PARTIAL | yes | coding | 9 | 0 | 28 | 11 | ✅ |  |
| P4.A4 | node-express-realworld-example-app | COMPLETE | yes | fast | 5 | 0 | 4 | 3 | ✅ |  |
| P4.A5 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 1 | 8 | 4 | ✅ |  |
| P4.A6 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 8 | 3 | ✅ |  |
| P4.A7 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 8 | 3 | ✅ |  |
| P4.A8 | node-express-realworld-example-app | COMPLETE | yes | fast | 4 | 0 | 17 | 1 | ✅ |  |
| P4.A9 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 23 | 15 | ✅ |  |
| P4.A1 | django-realworld-example-app | COMPLETE | yes | fast | 3 | 0 | 2 | 2 | ✅ |  |
| P4.A2 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P4.A3 | django-realworld-example-app | PARTIAL | yes | coding | 9 | 0 | 21 | 11 | ✅ |  |
| P4.A4 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P4.A6 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P4.A7 | django-realworld-example-app | COMPLETE | yes | fast | 7 | 1 | 11 | 1 | ✅ |  |
| P4.A8 | django-realworld-example-app | COMPLETE | yes | fast | 7 | 1 | 27 | 1 | ✅ |  |
| P4.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 24 | 16 | ✅ |  |
