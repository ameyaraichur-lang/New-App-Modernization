# E2E agentic acceptance run `run1`

- **Job**: `job-1791548430-a43248` — **COMPLETED**
- **Repositories**: `spring-petclinic`, `microblog`, `node-express-realworld-example-app`, `django-realworld-example-app`
- **Elapsed**: 42 min 41 s; LLM cache mode `record` (record = every call live, responses recorded for replay)
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

- Tool calls: 2047; evidence ids cited: 1243; LLM findings: 741; repair rounds: 25; failovers: 0
- Tokens: {'input': 9573219, 'output': 543579, 'reasoning': 30475}

## Release gates

| phase | app | phase status | decision |
|---|---|---|---|
| P1 | node-express-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | microblog | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | django-realworld-example-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | spring-petclinic | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P2 | PF1 | COMPLETED | AUTHORIZED |
| P3 | microblog | COMPLETED | CONDITIONAL_PLANNING |
| P3 | spring-petclinic | COMPLETED | CONDITIONAL_PLANNING |
| P3 | django-realworld-example-app | COMPLETED | CONDITIONAL_PLANNING |
| P3 | node-express-realworld-example-app | COMPLETED | CONDITIONAL_PLANNING |
| P4 | django-realworld-example-app | COMPLETED | SCOPED_PREPARATION |
| P4 | node-express-realworld-example-app | COMPLETED | SCOPED_PREPARATION |
| P4 | spring-petclinic | COMPLETED | SCOPED_PREPARATION |
| P4 | microblog | COMPLETED | SCOPED_PREPARATION |

Reviews: 32 (decided by `scripted-reviewer`); stakeholder questions: 65 (65 answered).

## Per-agent results

| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| P1.A1 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 29 | 14 | ✅ |  |
| P1.A2 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 28 | 20 | ✅ |  |
| P1.A3 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 17 | 12 | ✅ |  |
| P1.A4 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 12 | 8 | ✅ |  |
| P1.A5 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 6 | 7 | ✅ |  |
| P1.A6 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 26 | 19 | ✅ |  |
| P1.A7 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 13 | 6 | ✅ |  |
| P1.A8 | spring-petclinic | PARTIAL | yes | reasoning | 2 | 0 | 4 | 4 | ✅ |  |
| P1.A9 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 21 | 18 | ✅ |  |
| P1.A10 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 22 | 12 | ✅ |  |
| P1.A11 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 12 | 9 | ✅ |  |
| P1.A1 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 37 | 13 | ✅ |  |
| P1.A2 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 25 | 21 | ✅ |  |
| P1.A3 | microblog | PARTIAL | yes | reasoning | 7 | 0 | 25 | 17 | ✅ |  |
| P1.A4 | microblog | PARTIAL | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P1.A5 | microblog | PARTIAL | yes | fast | 6 | 0 | 10 | 5 | ✅ |  |
| P1.A6 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 30 | 28 | ✅ |  |
| P1.A7 | microblog | PARTIAL | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P1.A8 | microblog | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | microblog | PARTIAL | yes | reasoning | 4 | 0 | 16 | 10 | ✅ |  |
| P1.A10 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 19 | 13 | ✅ |  |
| P1.A11 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 15 | 9 | ✅ |  |
| P1.A1 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 36 | 19 | ✅ |  |
| P1.A2 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 26 | 18 | ✅ |  |
| P1.A3 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 26 | 22 | ✅ |  |
| P1.A4 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A5 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 8 | 6 | ✅ |  |
| P1.A6 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 23 | 17 | ✅ |  |
| P1.A7 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P1.A8 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 16 | 12 | ✅ |  |
| P1.A10 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 20 | 12 | ✅ |  |
| P1.A11 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 12 | 9 | ✅ |  |
| P1.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 29 | 15 | ✅ |  |
| P1.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 24 | 18 | ✅ |  |
| P1.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 32 | 25 | ✅ |  |
| P1.A4 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P1.A5 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 10 | 8 | ✅ |  |
| P1.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 18 | 19 | ✅ |  |
| P1.A7 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 22 | 12 | ✅ |  |
| P1.A10 | django-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 21 | 11 | ✅ |  |
| P1.A11 | django-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 10 | 9 | ✅ |  |
| P2.A1 | PF1 | PARTIAL | yes | reasoning | 8 | 0 | 31 | 17 | ✅ |  |
| P2.A2 | PF1 | PARTIAL | yes | reasoning | 9 | 1 | 36 | 13 | ✅ |  |
| P2.A3 | PF1 | COMPLETE | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P2.A4 | PF1 | COMPLETE | yes | fast | 8 | 2 | 10 | 1 | ✅ |  |
| P2.A5 | PF1 | COMPLETE | yes | fast | 7 | 1 | 12 | 5 | ✅ |  |
| P2.A6 | PF1 | PARTIAL | yes | reasoning | 6 | 0 | 32 | 23 | ✅ |  |
| P2.A7 | PF1 | PARTIAL | yes | reasoning | 7 | 1 | 19 | 13 | ✅ |  |
| P3.A1 | spring-petclinic | PARTIAL | yes | reasoning | 10 | 1 | 47 | 26 | ✅ |  |
| P3.A2 | spring-petclinic | PARTIAL | yes | reasoning | 8 | 1 | 26 | 15 | ✅ |  |
| P3.A3 | spring-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 22 | 18 | ✅ |  |
| P3.A4 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 1 | 23 | 16 | ✅ |  |
| P3.A5 | spring-petclinic | SKIPPED_APPROVED | yes | fast | 6 | 0 | 10 | 9 | ✅ |  |
| P3.A6 | spring-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 28 | 20 | ✅ |  |
| P3.A7 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 12 | 6 | ✅ |  |
| P3.A8 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 1 | 26 | 14 | ✅ |  |
| P3.A1 | microblog | PARTIAL | yes | reasoning | 10 | 1 | 46 | 24 | ✅ |  |
| P3.A2 | microblog | PARTIAL | yes | reasoning | 7 | 1 | 31 | 16 | ✅ |  |
| P3.A3 | microblog | PARTIAL | yes | reasoning | 4 | 0 | 14 | 11 | ✅ |  |
| P3.A4 | microblog | PARTIAL | yes | reasoning | 8 | 1 | 26 | 16 | ✅ |  |
| P3.A5 | microblog | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P3.A6 | microblog | PARTIAL | yes | reasoning | 5 | 0 | 25 | 15 | ✅ |  |
| P3.A7 | microblog | COMPLETE | yes | fast | 6 | 0 | 11 | 5 | ✅ |  |
| P3.A8 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 32 | 21 | ✅ |  |
| P3.A1 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 9 | 1 | 46 | 24 | ✅ |  |
| P3.A2 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 7 | 1 | 29 | 19 | ✅ |  |
| P3.A3 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 4 | 0 | 16 | 13 | ✅ |  |
| P3.A4 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 26 | 18 | ✅ |  |
| P3.A5 | node-express-realworld-example-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P3.A6 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 27 | 20 | ✅ |  |
| P3.A7 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P3.A8 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 29 | 18 | ✅ |  |
| P3.A1 | django-realworld-example-app | PARTIAL | yes | reasoning | 10 | 1 | 49 | 25 | ✅ |  |
| P3.A2 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 1 | 25 | 17 | ✅ |  |
| P3.A3 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 21 | 15 | ✅ |  |
| P3.A4 | django-realworld-example-app | PARTIAL | yes | reasoning | 7 | 1 | 23 | 13 | ✅ |  |
| P3.A5 | django-realworld-example-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P3.A6 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 24 | 20 | ✅ |  |
| P3.A7 | django-realworld-example-app | COMPLETE | yes | fast | 7 | 1 | 18 | 1 | ✅ |  |
| P3.A8 | django-realworld-example-app | PARTIAL | yes | reasoning | 5 | 0 | 23 | 14 | ✅ |  |
| P4.A1 | spring-petclinic | COMPLETE | yes | fast | 4 | 0 | 3 | 2 | ✅ |  |
| P4.A2 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 10 | 5 | ✅ |  |
| P4.A3 | spring-petclinic | PARTIAL | yes | coding | 8 | 1 | 14 | 9 | ✅ |  |
| P4.A4 | spring-petclinic | COMPLETE | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P4.A5 | spring-petclinic | PARTIAL | yes | fast | 7 | 1 | 7 | 7 | ✅ |  |
| P4.A6 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 13 | 1 | ✅ |  |
| P4.A7 | spring-petclinic | PARTIAL | yes | fast | 6 | 0 | 13 | 2 | ✅ |  |
| P4.A8 | spring-petclinic | COMPLETE | yes | fast | 5 | 1 | 9 | 1 | ✅ |  |
| P4.A9 | spring-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 24 | 18 | ✅ |  |
| P4.A1 | microblog | COMPLETE | yes | fast | 4 | 0 | 3 | 2 | ✅ |  |
| P4.A2 | microblog | COMPLETE | yes | fast | 2 | 0 | 6 | 2 | ✅ |  |
| P4.A3 | microblog | PARTIAL | yes | coding | 9 | 0 | 24 | 10 | ✅ |  |
| P4.A4 | microblog | COMPLETE | yes | fast | 6 | 0 | 5 | 5 | ✅ |  |
| P4.A5 | microblog | PARTIAL | yes | fast | 2 | 0 | 4 | 3 | ✅ |  |
| P4.A6 | microblog | COMPLETE | yes | fast | 6 | 0 | 11 | 4 | ✅ |  |
| P4.A7 | microblog | COMPLETE | yes | fast | 6 | 0 | 10 | 3 | ✅ |  |
| P4.A8 | microblog | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P4.A9 | microblog | PARTIAL | yes | reasoning | 6 | 0 | 22 | 18 | ✅ |  |
| P4.A1 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 6 | 1 | ✅ |  |
| P4.A2 | node-express-realworld-example-app | COMPLETE | yes | fast | 7 | 2 | 4 | 2 | ✅ |  |
| P4.A3 | node-express-realworld-example-app | PARTIAL | yes | coding | 8 | 0 | 23 | 15 | ✅ |  |
| P4.A4 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | node-express-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A6 | node-express-realworld-example-app | PARTIAL | yes | fast | 7 | 1 | 8 | 4 | ✅ |  |
| P4.A7 | node-express-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 15 | 6 | ✅ |  |
| P4.A8 | node-express-realworld-example-app | COMPLETE | yes | fast | 3 | 0 | 8 | 1 | ✅ |  |
| P4.A9 | node-express-realworld-example-app | PARTIAL | yes | reasoning | 7 | 0 | 25 | 18 | ✅ |  |
| P4.A1 | django-realworld-example-app | COMPLETE | yes | fast | 5 | 0 | 4 | 2 | ✅ |  |
| P4.A2 | django-realworld-example-app | COMPLETE | yes | fast | 7 | 1 | 6 | 2 | ✅ |  |
| P4.A3 | django-realworld-example-app | PARTIAL | yes | coding | 8 | 0 | 22 | 11 | ✅ |  |
| P4.A4 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P4.A5 | django-realworld-example-app | PARTIAL | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P4.A6 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 13 | 2 | ✅ |  |
| P4.A7 | django-realworld-example-app | COMPLETE | yes | fast | 6 | 0 | 10 | 3 | ✅ |  |
| P4.A8 | django-realworld-example-app | PARTIAL | yes | fast | 2 | 0 | 8 | 2 | ✅ |  |
| P4.A9 | django-realworld-example-app | PARTIAL | yes | reasoning | 6 | 0 | 23 | 18 | ✅ |  |
