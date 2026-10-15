# E2E agentic acceptance run `run7-holdout`

- **Job**: `job-1791970992-f5f3cf` — **COMPLETED**
- **Repositories**: `eshop-modernizing`, `spring-framework-petclinic`, `cargotracker`, `jhipster-sample-app`, `saleor`, `djangoproject`, `angular-phonecat`, `opencart`, `human-essentials`, `gitea`
- **Elapsed**: 112 min 51 s; LLM cache mode `record` (record = every call live, responses recorded for replay)
- **Astra tiers**: {'reasoning': 'gpt-6-astra', 'coding': 'gpt-5.3-codex-PlayWright', 'fast': 'gpt-4.1-mini', 'fallback': 'gpt-5.4'}
- **Human surfaces**: review_mode=human; release-gate approvals and stakeholder answers were submitted over the API by a **scripted** reviewer/stakeholder (labelled as automation in every record).

## Result

**Agent success rate: 100.00%** (253/253 P1–P4 agent dispatches; threshold > 97.0%).

34 P3/P4 agent slots were **not admitted** because the authorized P2 release gate routed `spring-framework-petclinic` (Retain), `angular-phonecat` (Retire) to the non-delivery register — by design, no architecture or plan is produced for a non-delivery route. Counting those slots as failures would give 88.15%.

Success = artifact not FAILED **and** enriched by the live Astra agent loop (not seed fallback) **and** passes ContractValidator (envelope + payload schema + content hash).

| phase | ok / total |
|---|---|
| P1 Discovery | 110 / 110 |
| P2 Portfolio | 7 / 7 |
| P3 Architecture | 64 / 64 |
| P4 Planning | 72 / 72 |

- Tool calls: 5175; evidence ids cited: 2859; LLM findings: 1508; repair rounds: 15; failovers: 0
- Tokens: {'input': 27364372, 'output': 1084601, 'reasoning': 60028}

## Release gates

| phase | app | phase status | decision |
|---|---|---|---|
| P1 | eshop-modernizing | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | cargotracker | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | spring-framework-petclinic | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | jhipster-sample-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | saleor | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | djangoproject | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | angular-phonecat | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | human-essentials | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | opencart | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | gitea | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P2 | PF1 | COMPLETED | AUTHORIZED |
| P3 | spring-framework-petclinic | NOT_ADMITTED | — |
| P4 | spring-framework-petclinic | NOT_ADMITTED | — |
| P3 | angular-phonecat | NOT_ADMITTED | — |
| P4 | angular-phonecat | NOT_ADMITTED | — |
| P3 | eshop-modernizing | COMPLETED | CONDITIONAL_PLANNING |
| P3 | jhipster-sample-app | COMPLETED | CONDITIONAL_PLANNING |
| P3 | saleor | COMPLETED | CONDITIONAL_PLANNING |
| P3 | djangoproject | COMPLETED | CONDITIONAL_PLANNING |
| P3 | cargotracker | COMPLETED | CONDITIONAL_PLANNING |
| P4 | cargotracker | COMPLETED | SCOPED_PREPARATION |
| P4 | jhipster-sample-app | COMPLETED | SCOPED_PREPARATION |
| P3 | opencart | COMPLETED | CONDITIONAL_PLANNING |
| P4 | saleor | COMPLETED | SCOPED_PREPARATION |
| P3 | human-essentials | COMPLETED | CONDITIONAL_PLANNING |
| P3 | gitea | COMPLETED | CONDITIONAL_PLANNING |
| P4 | eshop-modernizing | COMPLETED | SCOPED_PREPARATION |
| P4 | djangoproject | COMPLETED | SCOPED_PREPARATION |
| P4 | opencart | COMPLETED | SCOPED_PREPARATION |
| P4 | human-essentials | COMPLETED | SCOPED_PREPARATION |
| P4 | gitea | COMPLETED | SCOPED_PREPARATION |

Reviews: 27 (decided by `scripted-reviewer`); stakeholder questions: 71 (71 answered).

## Per-agent results

| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| P1.A1 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 40 | 12 | ✅ |  |
| P1.A2 | eshop-modernizing | PARTIAL | yes | reasoning | 8 | 0 | 30 | 23 | ✅ |  |
| P1.A3 | eshop-modernizing | PARTIAL | yes | reasoning | 9 | 0 | 37 | 21 | ✅ |  |
| P1.A4 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 14 | 10 | ✅ |  |
| P1.A5 | eshop-modernizing | PARTIAL | yes | fast | 7 | 0 | 10 | 6 | ✅ |  |
| P1.A6 | eshop-modernizing | PARTIAL | yes | reasoning | 5 | 0 | 17 | 14 | ✅ |  |
| P1.A7 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 10 | 5 | ✅ |  |
| P1.A8 | eshop-modernizing | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 25 | 20 | ✅ |  |
| P1.A10 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 22 | 11 | ✅ |  |
| P1.A11 | eshop-modernizing | PARTIAL | yes | reasoning | 10 | 0 | 41 | 14 | ✅ |  |
| P1.A1 | spring-framework-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 40 | 20 | ✅ |  |
| P1.A2 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 21 | 15 | ✅ |  |
| P1.A3 | spring-framework-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 27 | 18 | ✅ |  |
| P1.A4 | spring-framework-petclinic | PARTIAL | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P1.A5 | spring-framework-petclinic | PARTIAL | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P1.A6 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 23 | 18 | ✅ |  |
| P1.A7 | spring-framework-petclinic | PARTIAL | yes | fast | 6 | 0 | 6 | 2 | ✅ |  |
| P1.A8 | spring-framework-petclinic | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 28 | 14 | ✅ |  |
| P1.A10 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 14 | 10 | ✅ |  |
| P1.A11 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 16 | 12 | ✅ |  |
| P1.A1 | cargotracker | PARTIAL | yes | reasoning | 7 | 0 | 40 | 24 | ✅ |  |
| P1.A2 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 27 | 25 | ✅ |  |
| P1.A3 | cargotracker | PARTIAL | yes | reasoning | 8 | 0 | 40 | 24 | ✅ |  |
| P1.A4 | cargotracker | PARTIAL | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P1.A5 | cargotracker | SKIPPED_APPROVED | yes | fast | 6 | 0 | 10 | 7 | ✅ |  |
| P1.A6 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 29 | 21 | ✅ |  |
| P1.A7 | cargotracker | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 1 | ✅ |  |
| P1.A8 | cargotracker | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | cargotracker | PARTIAL | yes | reasoning | 10 | 0 | 44 | 20 | ✅ |  |
| P1.A10 | cargotracker | PARTIAL | yes | reasoning | 7 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 20 | 10 | ✅ |  |
| P1.A1 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 43 | 24 | ✅ |  |
| P1.A2 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 30 | 26 | ✅ |  |
| P1.A3 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 25 | 17 | ✅ |  |
| P1.A4 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P1.A5 | jhipster-sample-app | PARTIAL | yes | fast | 7 | 0 | 13 | 13 | ✅ |  |
| P1.A6 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 32 | 20 | ✅ |  |
| P1.A7 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A8 | jhipster-sample-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 29 | 12 | ✅ |  |
| P1.A10 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 25 | 11 | ✅ |  |
| P1.A11 | jhipster-sample-app | PARTIAL | yes | reasoning | 5 | 0 | 20 | 13 | ✅ |  |
| P1.A1 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 41 | 25 | ✅ |  |
| P1.A2 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 26 | 20 | ✅ |  |
| P1.A3 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 40 | 22 | ✅ |  |
| P1.A4 | saleor | PARTIAL | yes | fast | 6 | 0 | 11 | 9 | ✅ |  |
| P1.A5 | saleor | PARTIAL | yes | fast | 7 | 0 | 19 | 10 | ✅ |  |
| P1.A6 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 34 | 26 | ✅ |  |
| P1.A7 | saleor | PARTIAL | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P1.A8 | saleor | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 31 | 16 | ✅ |  |
| P1.A10 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 19 | 14 | ✅ |  |
| P1.A11 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 32 | 14 | ✅ |  |
| P1.A1 | djangoproject | PARTIAL | yes | reasoning | 9 | 0 | 52 | 19 | ✅ |  |
| P1.A2 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 23 | 18 | ✅ |  |
| P1.A3 | djangoproject | PARTIAL | yes | reasoning | 9 | 0 | 35 | 14 | ✅ |  |
| P1.A4 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 11 | 11 | ✅ |  |
| P1.A5 | djangoproject | PARTIAL | yes | fast | 7 | 0 | 12 | 8 | ✅ |  |
| P1.A6 | djangoproject | PARTIAL | yes | reasoning | 5 | 0 | 23 | 17 | ✅ |  |
| P1.A7 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P1.A8 | djangoproject | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | djangoproject | PARTIAL | yes | reasoning | 8 | 0 | 34 | 19 | ✅ |  |
| P1.A10 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 19 | 10 | ✅ |  |
| P1.A11 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 18 | 13 | ✅ |  |
| P1.A1 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 28 | 15 | ✅ |  |
| P1.A2 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 20 | 15 | ✅ |  |
| P1.A3 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 21 | 15 | ✅ |  |
| P1.A4 | angular-phonecat | PARTIAL | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P1.A5 | angular-phonecat | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A6 | angular-phonecat | PARTIAL | yes | reasoning | 4 | 0 | 17 | 13 | ✅ |  |
| P1.A7 | angular-phonecat | PARTIAL | yes | fast | 8 | 2 | 10 | 4 | ✅ |  |
| P1.A8 | angular-phonecat | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | angular-phonecat | PARTIAL | yes | reasoning | 4 | 0 | 14 | 13 | ✅ |  |
| P1.A10 | angular-phonecat | PARTIAL | yes | reasoning | 6 | 0 | 20 | 13 | ✅ |  |
| P1.A11 | angular-phonecat | PARTIAL | yes | reasoning | 4 | 0 | 13 | 10 | ✅ |  |
| P1.A1 | opencart | PARTIAL | yes | reasoning | 9 | 0 | 53 | 29 | ✅ |  |
| P1.A2 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 32 | 19 | ✅ |  |
| P1.A3 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 40 | 17 | ✅ |  |
| P1.A4 | opencart | PARTIAL | yes | fast | 7 | 0 | 10 | 10 | ✅ |  |
| P1.A5 | opencart | PARTIAL | yes | fast | 6 | 0 | 6 | 1 | ✅ |  |
| P1.A6 | opencart | PARTIAL | yes | reasoning | 5 | 0 | 24 | 15 | ✅ |  |
| P1.A7 | opencart | PARTIAL | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P1.A8 | opencart | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 22 | 10 | ✅ |  |
| P1.A10 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 18 | 12 | ✅ |  |
| P1.A11 | opencart | PARTIAL | yes | reasoning | 7 | 0 | 17 | 10 | ✅ |  |
| P1.A1 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 46 | 18 | ✅ |  |
| P1.A2 | human-essentials | PARTIAL | yes | reasoning | 8 | 0 | 31 | 22 | ✅ |  |
| P1.A3 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 37 | 20 | ✅ |  |
| P1.A4 | human-essentials | PARTIAL | yes | fast | 7 | 0 | 15 | 15 | ✅ |  |
| P1.A5 | human-essentials | PARTIAL | yes | fast | 7 | 0 | 12 | 5 | ✅ |  |
| P1.A6 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 35 | 20 | ✅ |  |
| P1.A7 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P1.A8 | human-essentials | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | human-essentials | PARTIAL | yes | reasoning | 9 | 1 | 40 | 20 | ✅ |  |
| P1.A10 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | human-essentials | PARTIAL | yes | reasoning | 5 | 0 | 17 | 10 | ✅ |  |
| P1.A1 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 40 | 25 | ✅ |  |
| P1.A2 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 31 | 16 | ✅ |  |
| P1.A3 | gitea | PARTIAL | yes | reasoning | 9 | 0 | 48 | 19 | ✅ |  |
| P1.A4 | gitea | PARTIAL | yes | fast | 7 | 0 | 10 | 7 | ✅ |  |
| P1.A5 | gitea | PARTIAL | yes | fast | 7 | 0 | 10 | 7 | ✅ |  |
| P1.A6 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 33 | 22 | ✅ |  |
| P1.A7 | gitea | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A8 | gitea | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 29 | 16 | ✅ |  |
| P1.A10 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 22 | 14 | ✅ |  |
| P1.A11 | gitea | PARTIAL | yes | reasoning | 5 | 0 | 20 | 10 | ✅ |  |
| P2.A1 | PF1 | PARTIAL | yes | reasoning | 9 | 0 | 33 | 27 | ✅ |  |
| P2.A2 | PF1 | PARTIAL | yes | reasoning | 9 | 0 | 40 | 29 | ✅ |  |
| P2.A3 | PF1 | COMPLETE | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P2.A4 | PF1 | COMPLETE | yes | fast | 6 | 0 | 33 | 13 | ✅ |  |
| P2.A5 | PF1 | COMPLETE | yes | fast | 4 | 1 | 6 | 3 | ✅ |  |
| P2.A6 | PF1 | PARTIAL | yes | reasoning | 9 | 0 | 61 | 29 | ✅ |  |
| P2.A7 | PF1 | PARTIAL | yes | reasoning | 5 | 0 | 19 | 11 | ✅ |  |
| P3.A1 | eshop-modernizing | PARTIAL | yes | reasoning | 9 | 0 | 48 | 29 | ✅ |  |
| P3.A2 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 26 | 17 | ✅ |  |
| P3.A3 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 26 | 17 | ✅ |  |
| P3.A4 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 25 | 16 | ✅ |  |
| P3.A5 | eshop-modernizing | SKIPPED_APPROVED | yes | fast | 6 | 0 | 9 | 7 | ✅ |  |
| P3.A6 | eshop-modernizing | PARTIAL | yes | reasoning | 8 | 0 | 35 | 18 | ✅ |  |
| P3.A7 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 10 | 3 | ✅ |  |
| P3.A8 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 34 | 14 | ✅ |  |
| P3.A1 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A2 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A3 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A4 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A5 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A6 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A7 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A8 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A1 | cargotracker | PARTIAL | yes | reasoning | 8 | 0 | 53 | 22 | ✅ |  |
| P3.A2 | cargotracker | PARTIAL | yes | reasoning | 7 | 0 | 33 | 18 | ✅ |  |
| P3.A3 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 25 | 17 | ✅ |  |
| P3.A4 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 22 | 15 | ✅ |  |
| P3.A5 | cargotracker | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P3.A6 | cargotracker | PARTIAL | yes | reasoning | 9 | 0 | 41 | 22 | ✅ |  |
| P3.A7 | cargotracker | COMPLETE | yes | fast | 6 | 0 | 11 | 1 | ✅ |  |
| P3.A8 | cargotracker | PARTIAL | yes | reasoning | 5 | 0 | 26 | 13 | ✅ |  |
| P3.A1 | jhipster-sample-app | PARTIAL | yes | reasoning | 9 | 0 | 51 | 26 | ✅ |  |
| P3.A2 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 26 | 18 | ✅ |  |
| P3.A3 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 26 | 18 | ✅ |  |
| P3.A4 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 25 | 18 | ✅ |  |
| P3.A5 | jhipster-sample-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P3.A6 | jhipster-sample-app | PARTIAL | yes | reasoning | 10 | 0 | 37 | 24 | ✅ |  |
| P3.A7 | jhipster-sample-app | COMPLETE | yes | fast | 6 | 0 | 10 | 4 | ✅ |  |
| P3.A8 | jhipster-sample-app | PARTIAL | yes | reasoning | 5 | 0 | 24 | 11 | ✅ |  |
| P3.A1 | saleor | PARTIAL | yes | reasoning | 10 | 0 | 53 | 25 | ✅ |  |
| P3.A2 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 32 | 19 | ✅ |  |
| P3.A3 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 31 | 18 | ✅ |  |
| P3.A4 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 36 | 22 | ✅ |  |
| P3.A5 | saleor | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P3.A6 | saleor | PARTIAL | yes | reasoning | 9 | 0 | 48 | 25 | ✅ |  |
| P3.A7 | saleor | PARTIAL | yes | fast | 6 | 0 | 12 | 4 | ✅ |  |
| P3.A8 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 32 | 14 | ✅ |  |
| P3.A1 | djangoproject | PARTIAL | yes | reasoning | 8 | 0 | 49 | 27 | ✅ |  |
| P3.A2 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 28 | 18 | ✅ |  |
| P3.A3 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 35 | 21 | ✅ |  |
| P3.A4 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 24 | 15 | ✅ |  |
| P3.A5 | djangoproject | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P3.A6 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 37 | 22 | ✅ |  |
| P3.A7 | djangoproject | PARTIAL | yes | fast | 7 | 1 | 12 | 4 | ✅ |  |
| P3.A8 | djangoproject | PARTIAL | yes | reasoning | 8 | 0 | 40 | 13 | ✅ |  |
| P3.A1 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A2 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A3 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A4 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A5 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A6 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A7 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A8 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A1 | opencart | PARTIAL | yes | reasoning | 9 | 0 | 56 | 32 | ✅ |  |
| P3.A2 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 30 | 16 | ✅ |  |
| P3.A3 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 24 | 14 | ✅ |  |
| P3.A4 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 23 | 16 | ✅ |  |
| P3.A5 | opencart | SKIPPED_APPROVED | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P3.A6 | opencart | PARTIAL | yes | reasoning | 9 | 0 | 45 | 26 | ✅ |  |
| P3.A7 | opencart | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P3.A8 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 32 | 16 | ✅ |  |
| P3.A1 | human-essentials | PARTIAL | yes | reasoning | 10 | 0 | 61 | 30 | ✅ |  |
| P3.A2 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 38 | 17 | ✅ |  |
| P3.A3 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 32 | 19 | ✅ |  |
| P3.A4 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 26 | 17 | ✅ |  |
| P3.A5 | human-essentials | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P3.A6 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 39 | 24 | ✅ |  |
| P3.A7 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P3.A8 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 35 | 15 | ✅ |  |
| P3.A1 | gitea | PARTIAL | yes | reasoning | 10 | 0 | 62 | 28 | ✅ |  |
| P3.A2 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 28 | 13 | ✅ |  |
| P3.A3 | gitea | PARTIAL | yes | reasoning | 6 | 0 | 26 | 15 | ✅ |  |
| P3.A4 | gitea | PARTIAL | yes | reasoning | 8 | 0 | 34 | 19 | ✅ |  |
| P3.A5 | gitea | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P3.A6 | gitea | PARTIAL | yes | reasoning | 8 | 0 | 42 | 18 | ✅ |  |
| P3.A7 | gitea | COMPLETE | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P3.A8 | gitea | PARTIAL | yes | reasoning | 6 | 0 | 30 | 14 | ✅ |  |
| P4.A1 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 8 | 3 | ✅ |  |
| P4.A2 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 13 | 1 | ✅ |  |
| P4.A3 | eshop-modernizing | PARTIAL | yes | coding | 9 | 1 | 13 | 10 | ✅ |  |
| P4.A4 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P4.A5 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 12 | 9 | ✅ |  |
| P4.A6 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 15 | 6 | ✅ |  |
| P4.A7 | eshop-modernizing | COMPLETE | yes | fast | 7 | 1 | 11 | 2 | ✅ |  |
| P4.A8 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P4.A9 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 21 | 18 | ✅ |  |
| P4.A1 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A2 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A3 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A4 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A5 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A6 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A7 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A8 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A9 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A1 | cargotracker | COMPLETE | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P4.A2 | cargotracker | COMPLETE | yes | fast | 3 | 0 | 3 | 2 | ✅ |  |
| P4.A3 | cargotracker | PARTIAL | yes | coding | 9 | 0 | 19 | 10 | ✅ |  |
| P4.A4 | cargotracker | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | cargotracker | PARTIAL | yes | fast | 7 | 1 | 8 | 2 | ✅ |  |
| P4.A6 | cargotracker | COMPLETE | yes | fast | 6 | 0 | 14 | 15 | ✅ |  |
| P4.A7 | cargotracker | COMPLETE | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P4.A8 | cargotracker | PARTIAL | yes | fast | 5 | 0 | 15 | 1 | ✅ |  |
| P4.A9 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 24 | 18 | ✅ |  |
| P4.A1 | jhipster-sample-app | COMPLETE | yes | fast | 6 | 0 | 6 | 2 | ✅ |  |
| P4.A2 | jhipster-sample-app | COMPLETE | yes | fast | 4 | 0 | 6 | 2 | ✅ |  |
| P4.A3 | jhipster-sample-app | PARTIAL | yes | coding | 4 | 0 | 14 | 9 | ✅ |  |
| P4.A4 | jhipster-sample-app | COMPLETE | yes | fast | 3 | 0 | 4 | 2 | ✅ |  |
| P4.A5 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 6 | 4 | ✅ |  |
| P4.A6 | jhipster-sample-app | COMPLETE | yes | fast | 8 | 2 | 9 | 4 | ✅ |  |
| P4.A7 | jhipster-sample-app | COMPLETE | yes | fast | 6 | 0 | 13 | 2 | ✅ |  |
| P4.A8 | jhipster-sample-app | COMPLETE | yes | fast | 6 | 0 | 10 | 1 | ✅ |  |
| P4.A9 | jhipster-sample-app | PARTIAL | yes | reasoning | 5 | 0 | 19 | 17 | ✅ |  |
| P4.A1 | saleor | COMPLETE | yes | fast | 6 | 0 | 6 | 2 | ✅ |  |
| P4.A2 | saleor | COMPLETE | yes | fast | 5 | 0 | 4 | 2 | ✅ |  |
| P4.A3 | saleor | PARTIAL | yes | coding | 8 | 1 | 19 | 10 | ✅ |  |
| P4.A4 | saleor | COMPLETE | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P4.A5 | saleor | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A6 | saleor | COMPLETE | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P4.A7 | saleor | COMPLETE | yes | fast | 6 | 0 | 12 | 4 | ✅ |  |
| P4.A8 | saleor | COMPLETE | yes | fast | 4 | 0 | 9 | 3 | ✅ |  |
| P4.A9 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 18 | 14 | ✅ |  |
| P4.A1 | djangoproject | COMPLETE | yes | fast | 5 | 0 | 7 | 3 | ✅ |  |
| P4.A2 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P4.A3 | djangoproject | PARTIAL | yes | coding | 5 | 0 | 18 | 11 | ✅ |  |
| P4.A4 | djangoproject | COMPLETE | yes | fast | 4 | 0 | 5 | 1 | ✅ |  |
| P4.A5 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P4.A6 | djangoproject | PARTIAL | yes | fast | 8 | 2 | 13 | 6 | ✅ |  |
| P4.A7 | djangoproject | COMPLETE | yes | fast | 7 | 1 | 10 | 1 | ✅ |  |
| P4.A8 | djangoproject | COMPLETE | yes | fast | 7 | 1 | 11 | 2 | ✅ |  |
| P4.A9 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 20 | 15 | ✅ |  |
| P4.A1 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A2 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A3 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A4 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A5 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A6 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A7 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A8 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A9 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A1 | opencart | COMPLETE | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P4.A2 | opencart | COMPLETE | yes | fast | 2 | 0 | 2 | 3 | ✅ |  |
| P4.A3 | opencart | PARTIAL | yes | coding | 3 | 0 | 4 | 7 | ✅ |  |
| P4.A4 | opencart | COMPLETE | yes | fast | 3 | 0 | 4 | 2 | ✅ |  |
| P4.A5 | opencart | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A6 | opencart | COMPLETE | yes | fast | 6 | 0 | 20 | 10 | ✅ |  |
| P4.A7 | opencart | COMPLETE | yes | fast | 6 | 0 | 13 | 1 | ✅ |  |
| P4.A8 | opencart | COMPLETE | yes | fast | 4 | 0 | 10 | 1 | ✅ |  |
| P4.A9 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 19 | 15 | ✅ |  |
| P4.A1 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 12 | 2 | ✅ |  |
| P4.A2 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P4.A3 | human-essentials | PARTIAL | yes | coding | 9 | 0 | 18 | 10 | ✅ |  |
| P4.A4 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P4.A5 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 13 | 3 | ✅ |  |
| P4.A6 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 28 | 6 | ✅ |  |
| P4.A7 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P4.A8 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 12 | 1 | ✅ |  |
| P4.A9 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 21 | 17 | ✅ |  |
| P4.A1 | gitea | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A2 | gitea | COMPLETE | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P4.A3 | gitea | PARTIAL | yes | coding | 8 | 0 | 22 | 14 | ✅ |  |
| P4.A4 | gitea | COMPLETE | yes | fast | 4 | 0 | 3 | 2 | ✅ |  |
| P4.A5 | gitea | PARTIAL | yes | fast | 6 | 0 | 10 | 6 | ✅ |  |
| P4.A6 | gitea | COMPLETE | yes | fast | 6 | 0 | 10 | 7 | ✅ |  |
| P4.A7 | gitea | PARTIAL | yes | fast | 2 | 0 | 4 | 5 | ✅ |  |
| P4.A8 | gitea | COMPLETE | yes | fast | 2 | 0 | 3 | 1 | ✅ |  |
| P4.A9 | gitea | PARTIAL | yes | reasoning | 8 | 0 | 25 | 17 | ✅ |  |
