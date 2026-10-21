# E2E agentic acceptance run `stability-holdout`

- **Job**: `job-1792176354-be3f2b` — **COMPLETED**
- **Repositories**: `eshop-modernizing`, `spring-framework-petclinic`, `cargotracker`, `jhipster-sample-app`, `saleor`, `djangoproject`, `angular-phonecat`, `opencart`, `human-essentials`, `gitea`
- **Elapsed**: 105 min 32 s; LLM cache mode `record` (record = every call live, responses recorded for replay)
- **Astra tiers**: {'reasoning': 'gpt-6-astra', 'coding': 'gpt-5.3-codex-PlayWright', 'fast': 'gpt-4.1-mini', 'fallback': 'gpt-5.4'}
- **Human surfaces**: review_mode=human; release-gate approvals and stakeholder answers were submitted over the API by a **scripted** reviewer/stakeholder (labelled as automation in every record).

## Result

**Agent success rate: 100.00%** (253/253 P1–P4 agent dispatches; threshold > 97.0%).

34 P3/P4 agent slots were **not admitted** because the authorized P2 release gate routed `cargotracker` (Retain), `angular-phonecat` (Retire) to the non-delivery register — by design, no architecture or plan is produced for a non-delivery route. Counting those slots as failures would give 88.15%.

Success = artifact not FAILED **and** enriched by the live Astra agent loop (not seed fallback) **and** passes ContractValidator (envelope + payload schema + content hash).

| phase | ok / total |
|---|---|
| P1 Discovery | 110 / 110 |
| P2 Portfolio | 7 / 7 |
| P3 Architecture | 64 / 64 |
| P4 Planning | 72 / 72 |

- Tool calls: 5075; evidence ids cited: 2904; LLM findings: 1540; repair rounds: 18; failovers: 0
- Tokens: {'input': 26513327, 'output': 1050285, 'reasoning': 62602}

## Release gates

| phase | app | phase status | decision |
|---|---|---|---|
| P1 | spring-framework-petclinic | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | eshop-modernizing | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | cargotracker | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | jhipster-sample-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | saleor | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | djangoproject | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | angular-phonecat | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | opencart | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | human-essentials | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | gitea | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P2 | PF1 | COMPLETED | AUTHORIZED |
| P3 | cargotracker | NOT_ADMITTED | — |
| P4 | cargotracker | NOT_ADMITTED | — |
| P3 | angular-phonecat | NOT_ADMITTED | — |
| P4 | angular-phonecat | NOT_ADMITTED | — |
| P3 | spring-framework-petclinic | COMPLETED | CONDITIONAL_PLANNING |
| P3 | djangoproject | COMPLETED | CONDITIONAL_PLANNING |
| P3 | jhipster-sample-app | COMPLETED | CONDITIONAL_PLANNING |
| P3 | saleor | COMPLETED | CONDITIONAL_PLANNING |
| P3 | eshop-modernizing | COMPLETED | CONDITIONAL_PLANNING |
| P4 | spring-framework-petclinic | COMPLETED | SCOPED_PREPARATION |
| P4 | eshop-modernizing | COMPLETED | SCOPED_PREPARATION |
| P4 | djangoproject | COMPLETED | SCOPED_PREPARATION |
| P4 | saleor | COMPLETED | SCOPED_PREPARATION |
| P3 | opencart | COMPLETED | CONDITIONAL_PLANNING |
| P3 | human-essentials | COMPLETED | CONDITIONAL_PLANNING |
| P4 | jhipster-sample-app | COMPLETED | SCOPED_PREPARATION |
| P3 | gitea | COMPLETED | CONDITIONAL_PLANNING |
| P4 | human-essentials | COMPLETED | SCOPED_PREPARATION |
| P4 | opencart | COMPLETED | SCOPED_PREPARATION |
| P4 | gitea | COMPLETED | SCOPED_PREPARATION |

Reviews: 27 (decided by `scripted-reviewer`); stakeholder questions: 71 (71 answered).

## Per-agent results

| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| P1.A1 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 40 | 16 | ✅ |  |
| P1.A2 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 28 | 21 | ✅ |  |
| P1.A3 | eshop-modernizing | PARTIAL | yes | reasoning | 8 | 0 | 36 | 23 | ✅ |  |
| P1.A4 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 12 | 10 | ✅ |  |
| P1.A5 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A6 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 24 | 18 | ✅ |  |
| P1.A7 | eshop-modernizing | PARTIAL | yes | fast | 7 | 0 | 8 | 4 | ✅ |  |
| P1.A8 | eshop-modernizing | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | eshop-modernizing | PARTIAL | yes | reasoning | 9 | 0 | 27 | 19 | ✅ |  |
| P1.A10 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | eshop-modernizing | PARTIAL | yes | reasoning | 5 | 0 | 17 | 12 | ✅ |  |
| P1.A1 | spring-framework-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 38 | 17 | ✅ |  |
| P1.A2 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 24 | 16 | ✅ |  |
| P1.A3 | spring-framework-petclinic | PARTIAL | yes | reasoning | 8 | 0 | 33 | 20 | ✅ |  |
| P1.A4 | spring-framework-petclinic | PARTIAL | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P1.A5 | spring-framework-petclinic | PARTIAL | yes | fast | 7 | 1 | 8 | 7 | ✅ |  |
| P1.A6 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 20 | 19 | ✅ |  |
| P1.A7 | spring-framework-petclinic | PARTIAL | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P1.A8 | spring-framework-petclinic | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 30 | 17 | ✅ |  |
| P1.A10 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 17 | 12 | ✅ |  |
| P1.A11 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 18 | 11 | ✅ |  |
| P1.A1 | cargotracker | PARTIAL | yes | reasoning | 8 | 0 | 44 | 26 | ✅ |  |
| P1.A2 | cargotracker | PARTIAL | yes | reasoning | 7 | 0 | 32 | 24 | ✅ |  |
| P1.A3 | cargotracker | PARTIAL | yes | reasoning | 8 | 0 | 40 | 23 | ✅ |  |
| P1.A4 | cargotracker | PARTIAL | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P1.A5 | cargotracker | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P1.A6 | cargotracker | PARTIAL | yes | reasoning | 5 | 0 | 28 | 18 | ✅ |  |
| P1.A7 | cargotracker | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P1.A8 | cargotracker | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | cargotracker | PARTIAL | yes | reasoning | 7 | 0 | 45 | 19 | ✅ |  |
| P1.A10 | cargotracker | PARTIAL | yes | reasoning | 5 | 0 | 17 | 11 | ✅ |  |
| P1.A11 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 23 | 11 | ✅ |  |
| P1.A1 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 41 | 22 | ✅ |  |
| P1.A2 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 31 | 21 | ✅ |  |
| P1.A3 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 30 | 25 | ✅ |  |
| P1.A4 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 6 | 4 | ✅ |  |
| P1.A5 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P1.A6 | jhipster-sample-app | PARTIAL | yes | reasoning | 5 | 0 | 29 | 17 | ✅ |  |
| P1.A7 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 14 | 10 | ✅ |  |
| P1.A8 | jhipster-sample-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 36 | 18 | ✅ |  |
| P1.A10 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 21 | 11 | ✅ |  |
| P1.A11 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 21 | 10 | ✅ |  |
| P1.A1 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 42 | 29 | ✅ |  |
| P1.A2 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 32 | 24 | ✅ |  |
| P1.A3 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 37 | 20 | ✅ |  |
| P1.A4 | saleor | PARTIAL | yes | fast | 6 | 0 | 9 | 7 | ✅ |  |
| P1.A5 | saleor | PARTIAL | yes | fast | 7 | 0 | 10 | 5 | ✅ |  |
| P1.A6 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 36 | 31 | ✅ |  |
| P1.A7 | saleor | PARTIAL | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P1.A8 | saleor | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 30 | 21 | ✅ |  |
| P1.A10 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 22 | 13 | ✅ |  |
| P1.A11 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 20 | 12 | ✅ |  |
| P1.A1 | djangoproject | PARTIAL | yes | reasoning | 9 | 0 | 60 | 29 | ✅ |  |
| P1.A2 | djangoproject | PARTIAL | yes | reasoning | 5 | 0 | 22 | 20 | ✅ |  |
| P1.A3 | djangoproject | PARTIAL | yes | reasoning | 8 | 0 | 42 | 23 | ✅ |  |
| P1.A4 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 11 | 11 | ✅ |  |
| P1.A5 | djangoproject | PARTIAL | yes | fast | 7 | 0 | 12 | 4 | ✅ |  |
| P1.A6 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 32 | 26 | ✅ |  |
| P1.A7 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P1.A8 | djangoproject | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 32 | 23 | ✅ |  |
| P1.A10 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 20 | 14 | ✅ |  |
| P1.A1 | angular-phonecat | PARTIAL | yes | reasoning | 6 | 0 | 32 | 19 | ✅ |  |
| P1.A2 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 19 | 16 | ✅ |  |
| P1.A3 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 18 | 14 | ✅ |  |
| P1.A4 | angular-phonecat | PARTIAL | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P1.A5 | angular-phonecat | PARTIAL | yes | fast | 7 | 0 | 7 | 4 | ✅ |  |
| P1.A6 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 19 | 19 | ✅ |  |
| P1.A7 | angular-phonecat | PARTIAL | yes | fast | 6 | 0 | 8 | 3 | ✅ |  |
| P1.A8 | angular-phonecat | PARTIAL | yes | reasoning | 2 | 0 | 1 | 2 | ✅ |  |
| P1.A9 | angular-phonecat | PARTIAL | yes | reasoning | 4 | 0 | 17 | 12 | ✅ |  |
| P1.A10 | angular-phonecat | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 14 | 12 | ✅ |  |
| P1.A1 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 46 | 25 | ✅ |  |
| P1.A2 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 36 | 27 | ✅ |  |
| P1.A3 | opencart | PARTIAL | yes | reasoning | 9 | 0 | 45 | 22 | ✅ |  |
| P1.A4 | opencart | PARTIAL | yes | fast | 7 | 0 | 9 | 8 | ✅ |  |
| P1.A5 | opencart | PARTIAL | yes | fast | 7 | 0 | 9 | 3 | ✅ |  |
| P1.A6 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 25 | 20 | ✅ |  |
| P1.A7 | opencart | PARTIAL | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P1.A8 | opencart | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 23 | 11 | ✅ |  |
| P1.A10 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 22 | 14 | ✅ |  |
| P1.A11 | opencart | PARTIAL | yes | reasoning | 5 | 0 | 18 | 12 | ✅ |  |
| P1.A1 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 45 | 18 | ✅ |  |
| P1.A2 | human-essentials | PARTIAL | yes | reasoning | 8 | 0 | 35 | 23 | ✅ |  |
| P1.A3 | human-essentials | PARTIAL | yes | reasoning | 8 | 0 | 41 | 28 | ✅ |  |
| P1.A4 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 12 | 13 | ✅ |  |
| P1.A5 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P1.A6 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 36 | 23 | ✅ |  |
| P1.A7 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P1.A8 | human-essentials | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | human-essentials | PARTIAL | yes | reasoning | 9 | 1 | 39 | 19 | ✅ |  |
| P1.A10 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 20 | 11 | ✅ |  |
| P1.A11 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 23 | 13 | ✅ |  |
| P1.A1 | gitea | PARTIAL | yes | reasoning | 8 | 0 | 52 | 41 | ✅ |  |
| P1.A2 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 28 | 19 | ✅ |  |
| P1.A3 | gitea | PARTIAL | yes | reasoning | 9 | 0 | 53 | 25 | ✅ |  |
| P1.A4 | gitea | PARTIAL | yes | fast | 7 | 0 | 9 | 3 | ✅ |  |
| P1.A5 | gitea | PARTIAL | yes | fast | 7 | 0 | 10 | 3 | ✅ |  |
| P1.A6 | gitea | PARTIAL | yes | reasoning | 6 | 0 | 31 | 15 | ✅ |  |
| P1.A7 | gitea | PARTIAL | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P1.A8 | gitea | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | gitea | PARTIAL | yes | reasoning | 9 | 0 | 30 | 17 | ✅ |  |
| P1.A10 | gitea | PARTIAL | yes | reasoning | 6 | 0 | 21 | 14 | ✅ |  |
| P1.A11 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 23 | 13 | ✅ |  |
| P2.A1 | PF1 | PARTIAL | yes | reasoning | 9 | 0 | 41 | 24 | ✅ |  |
| P2.A2 | PF1 | PARTIAL | yes | reasoning | 8 | 0 | 44 | 23 | ✅ |  |
| P2.A3 | PF1 | COMPLETE | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P2.A4 | PF1 | COMPLETE | yes | fast | 8 | 2 | 7 | 4 | ✅ |  |
| P2.A5 | PF1 | COMPLETE | yes | fast | 7 | 1 | 18 | 2 | ✅ |  |
| P2.A6 | PF1 | PARTIAL | yes | reasoning | 9 | 0 | 66 | 23 | ✅ |  |
| P2.A7 | PF1 | PARTIAL | yes | reasoning | 5 | 0 | 28 | 23 | ✅ |  |
| P3.A1 | eshop-modernizing | PARTIAL | yes | reasoning | 10 | 0 | 66 | 28 | ✅ |  |
| P3.A2 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 24 | 18 | ✅ |  |
| P3.A3 | eshop-modernizing | PARTIAL | yes | reasoning | 5 | 0 | 21 | 16 | ✅ |  |
| P3.A4 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 21 | 15 | ✅ |  |
| P3.A5 | eshop-modernizing | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 5 | ✅ |  |
| P3.A6 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 33 | 21 | ✅ |  |
| P3.A7 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P3.A8 | eshop-modernizing | PARTIAL | yes | reasoning | 5 | 0 | 28 | 14 | ✅ |  |
| P3.A1 | spring-framework-petclinic | PARTIAL | yes | reasoning | 9 | 0 | 52 | 29 | ✅ |  |
| P3.A2 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 27 | 16 | ✅ |  |
| P3.A3 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 25 | 19 | ✅ |  |
| P3.A4 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 18 | 13 | ✅ |  |
| P3.A5 | spring-framework-petclinic | SKIPPED_APPROVED | yes | fast | 6 | 0 | 9 | 10 | ✅ |  |
| P3.A6 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 28 | 16 | ✅ |  |
| P3.A7 | spring-framework-petclinic | COMPLETE | yes | fast | 6 | 0 | 14 | 5 | ✅ |  |
| P3.A8 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 24 | 14 | ✅ |  |
| P3.A1 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A2 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A3 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A4 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A5 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A6 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A7 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A8 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A1 | jhipster-sample-app | PARTIAL | yes | reasoning | 9 | 0 | 50 | 30 | ✅ |  |
| P3.A2 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 26 | 16 | ✅ |  |
| P3.A3 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 27 | 20 | ✅ |  |
| P3.A4 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 25 | 16 | ✅ |  |
| P3.A5 | jhipster-sample-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 7 | ✅ |  |
| P3.A6 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 29 | 22 | ✅ |  |
| P3.A7 | jhipster-sample-app | COMPLETE | yes | fast | 6 | 0 | 17 | 1 | ✅ |  |
| P3.A8 | jhipster-sample-app | PARTIAL | yes | reasoning | 5 | 0 | 31 | 14 | ✅ |  |
| P3.A1 | saleor | PARTIAL | yes | reasoning | 9 | 0 | 54 | 24 | ✅ |  |
| P3.A2 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 26 | 15 | ✅ |  |
| P3.A3 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 31 | 20 | ✅ |  |
| P3.A4 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 28 | 16 | ✅ |  |
| P3.A5 | saleor | SKIPPED_APPROVED | yes | fast | 6 | 0 | 9 | 5 | ✅ |  |
| P3.A6 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 44 | 25 | ✅ |  |
| P3.A7 | saleor | COMPLETE | yes | fast | 6 | 0 | 15 | 1 | ✅ |  |
| P3.A8 | saleor | PARTIAL | yes | reasoning | 5 | 0 | 27 | 14 | ✅ |  |
| P3.A1 | djangoproject | PARTIAL | yes | reasoning | 8 | 0 | 45 | 22 | ✅ |  |
| P3.A2 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 27 | 12 | ✅ |  |
| P3.A3 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 31 | 17 | ✅ |  |
| P3.A4 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 31 | 18 | ✅ |  |
| P3.A5 | djangoproject | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P3.A6 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 33 | 18 | ✅ |  |
| P3.A7 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 11 | 3 | ✅ |  |
| P3.A8 | djangoproject | PARTIAL | yes | reasoning | 5 | 0 | 28 | 14 | ✅ |  |
| P3.A1 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A2 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A3 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A4 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A5 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A6 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A7 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A8 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A1 | opencart | PARTIAL | yes | reasoning | 9 | 0 | 63 | 30 | ✅ |  |
| P3.A2 | opencart | PARTIAL | yes | reasoning | 5 | 0 | 22 | 17 | ✅ |  |
| P3.A3 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 25 | 16 | ✅ |  |
| P3.A4 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 29 | 19 | ✅ |  |
| P3.A5 | opencart | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P3.A6 | opencart | PARTIAL | yes | reasoning | 7 | 0 | 33 | 19 | ✅ |  |
| P3.A7 | opencart | COMPLETE | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P3.A8 | opencart | PARTIAL | yes | reasoning | 5 | 0 | 24 | 15 | ✅ |  |
| P3.A1 | human-essentials | PARTIAL | yes | reasoning | 9 | 0 | 46 | 30 | ✅ |  |
| P3.A2 | human-essentials | PARTIAL | yes | reasoning | 8 | 0 | 42 | 23 | ✅ |  |
| P3.A3 | human-essentials | PARTIAL | yes | reasoning | 9 | 0 | 36 | 19 | ✅ |  |
| P3.A4 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 25 | 19 | ✅ |  |
| P3.A5 | human-essentials | SKIPPED_APPROVED | yes | fast | 6 | 0 | 10 | 5 | ✅ |  |
| P3.A6 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 36 | 22 | ✅ |  |
| P3.A7 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 10 | 3 | ✅ |  |
| P3.A8 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 39 | 16 | ✅ |  |
| P3.A1 | gitea | PARTIAL | yes | reasoning | 9 | 0 | 55 | 24 | ✅ |  |
| P3.A2 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 29 | 15 | ✅ |  |
| P3.A3 | gitea | PARTIAL | yes | reasoning | 6 | 0 | 22 | 15 | ✅ |  |
| P3.A4 | gitea | PARTIAL | yes | reasoning | 8 | 0 | 36 | 16 | ✅ |  |
| P3.A5 | gitea | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 5 | ✅ |  |
| P3.A6 | gitea | PARTIAL | yes | reasoning | 10 | 0 | 45 | 18 | ✅ |  |
| P3.A7 | gitea | PARTIAL | yes | fast | 6 | 0 | 10 | 1 | ✅ |  |
| P3.A8 | gitea | PARTIAL | yes | reasoning | 5 | 0 | 30 | 14 | ✅ |  |
| P4.A1 | eshop-modernizing | COMPLETE | yes | fast | 4 | 0 | 3 | 1 | ✅ |  |
| P4.A2 | eshop-modernizing | COMPLETE | yes | fast | 4 | 0 | 11 | 3 | ✅ |  |
| P4.A3 | eshop-modernizing | PARTIAL | yes | coding | 9 | 1 | 15 | 8 | ✅ |  |
| P4.A4 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P4.A5 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 8 | 6 | ✅ |  |
| P4.A6 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 14 | 1 | ✅ |  |
| P4.A7 | eshop-modernizing | COMPLETE | yes | fast | 8 | 2 | 9 | 1 | ✅ |  |
| P4.A8 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 14 | 1 | ✅ |  |
| P4.A9 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 21 | 16 | ✅ |  |
| P4.A1 | spring-framework-petclinic | COMPLETE | yes | fast | 1 | 0 | 0 | 2 | ✅ |  |
| P4.A2 | spring-framework-petclinic | COMPLETE | yes | fast | 5 | 1 | 10 | 4 | ✅ |  |
| P4.A3 | spring-framework-petclinic | PARTIAL | yes | coding | 6 | 0 | 15 | 14 | ✅ |  |
| P4.A4 | spring-framework-petclinic | COMPLETE | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P4.A5 | spring-framework-petclinic | COMPLETE | yes | fast | 3 | 0 | 3 | 4 | ✅ |  |
| P4.A6 | spring-framework-petclinic | PARTIAL | yes | fast | 7 | 1 | 11 | 4 | ✅ |  |
| P4.A7 | spring-framework-petclinic | COMPLETE | yes | fast | 6 | 0 | 13 | 1 | ✅ |  |
| P4.A8 | spring-framework-petclinic | COMPLETE | yes | fast | 6 | 0 | 10 | 1 | ✅ |  |
| P4.A9 | spring-framework-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 22 | 17 | ✅ |  |
| P4.A1 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A2 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A3 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A4 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A5 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A6 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A7 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A8 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A9 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A1 | jhipster-sample-app | COMPLETE | yes | fast | 4 | 0 | 3 | 2 | ✅ |  |
| P4.A2 | jhipster-sample-app | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A3 | jhipster-sample-app | PARTIAL | yes | coding | 8 | 0 | 19 | 12 | ✅ |  |
| P4.A4 | jhipster-sample-app | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | jhipster-sample-app | PARTIAL | yes | fast | 7 | 1 | 7 | 5 | ✅ |  |
| P4.A6 | jhipster-sample-app | PARTIAL | yes | fast | 7 | 1 | 17 | 2 | ✅ |  |
| P4.A7 | jhipster-sample-app | COMPLETE | yes | fast | 7 | 1 | 10 | 1 | ✅ |  |
| P4.A8 | jhipster-sample-app | COMPLETE | yes | fast | 2 | 0 | 3 | 2 | ✅ |  |
| P4.A9 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 18 | 14 | ✅ |  |
| P4.A1 | saleor | COMPLETE | yes | fast | 4 | 0 | 3 | 1 | ✅ |  |
| P4.A2 | saleor | COMPLETE | yes | fast | 2 | 0 | 1 | 3 | ✅ |  |
| P4.A3 | saleor | PARTIAL | yes | coding | 5 | 0 | 13 | 10 | ✅ |  |
| P4.A4 | saleor | COMPLETE | yes | fast | 4 | 0 | 7 | 1 | ✅ |  |
| P4.A5 | saleor | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P4.A6 | saleor | PARTIAL | yes | fast | 6 | 0 | 14 | 2 | ✅ |  |
| P4.A7 | saleor | COMPLETE | yes | fast | 6 | 0 | 13 | 1 | ✅ |  |
| P4.A8 | saleor | COMPLETE | yes | fast | 6 | 0 | 20 | 1 | ✅ |  |
| P4.A9 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 23 | 18 | ✅ |  |
| P4.A1 | djangoproject | COMPLETE | yes | fast | 4 | 0 | 3 | 2 | ✅ |  |
| P4.A2 | djangoproject | COMPLETE | yes | fast | 2 | 0 | 1 | 2 | ✅ |  |
| P4.A3 | djangoproject | PARTIAL | yes | coding | 5 | 0 | 18 | 14 | ✅ |  |
| P4.A4 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A6 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 11 | 5 | ✅ |  |
| P4.A7 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 6 | 1 | ✅ |  |
| P4.A8 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 16 | 1 | ✅ |  |
| P4.A9 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 18 | 16 | ✅ |  |
| P4.A1 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A2 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A3 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A4 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A5 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A6 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A7 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A8 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A9 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A1 | opencart | COMPLETE | yes | fast | 1 | 0 | 0 | 2 | ✅ |  |
| P4.A2 | opencart | COMPLETE | yes | fast | 6 | 1 | 5 | 2 | ✅ |  |
| P4.A3 | opencart | PARTIAL | yes | coding | 4 | 0 | 16 | 8 | ✅ |  |
| P4.A4 | opencart | COMPLETE | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P4.A5 | opencart | COMPLETE | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P4.A6 | opencart | COMPLETE | yes | fast | 7 | 1 | 7 | 3 | ✅ |  |
| P4.A7 | opencart | PARTIAL | yes | fast | 6 | 0 | 12 | 2 | ✅ |  |
| P4.A8 | opencart | COMPLETE | yes | fast | 5 | 0 | 18 | 2 | ✅ |  |
| P4.A9 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 21 | 17 | ✅ |  |
| P4.A1 | human-essentials | COMPLETE | yes | fast | 3 | 0 | 2 | 2 | ✅ |  |
| P4.A2 | human-essentials | COMPLETE | yes | fast | 3 | 0 | 4 | 3 | ✅ |  |
| P4.A3 | human-essentials | PARTIAL | yes | coding | 10 | 1 | 22 | 11 | ✅ |  |
| P4.A4 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 7 | 8 | ✅ |  |
| P4.A6 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 16 | 6 | ✅ |  |
| P4.A7 | human-essentials | COMPLETE | yes | fast | 7 | 1 | 10 | 3 | ✅ |  |
| P4.A8 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 12 | 1 | ✅ |  |
| P4.A9 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 21 | 18 | ✅ |  |
| P4.A1 | gitea | COMPLETE | yes | fast | 2 | 0 | 1 | 1 | ✅ |  |
| P4.A2 | gitea | COMPLETE | yes | fast | 2 | 0 | 1 | 2 | ✅ |  |
| P4.A3 | gitea | PARTIAL | yes | coding | 4 | 0 | 16 | 14 | ✅ |  |
| P4.A4 | gitea | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | gitea | PARTIAL | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P4.A6 | gitea | COMPLETE | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P4.A7 | gitea | COMPLETE | yes | fast | 7 | 1 | 11 | 7 | ✅ |  |
| P4.A8 | gitea | COMPLETE | yes | fast | 6 | 0 | 11 | 1 | ✅ |  |
| P4.A9 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 29 | 18 | ✅ |  |
