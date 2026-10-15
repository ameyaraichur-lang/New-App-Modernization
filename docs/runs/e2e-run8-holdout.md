# E2E agentic acceptance run `run8-holdout`

- **Job**: `job-1792041165-85e6b2` — **COMPLETED**
- **Repositories**: `eshop-modernizing`, `spring-framework-petclinic`, `cargotracker`, `jhipster-sample-app`, `saleor`, `djangoproject`, `angular-phonecat`, `opencart`, `human-essentials`, `gitea`
- **Elapsed**: 123 min 52 s; LLM cache mode `record` (record = every call live, responses recorded for replay)
- **Astra tiers**: {'reasoning': 'gpt-6-astra', 'coding': 'gpt-5.3-codex-PlayWright', 'fast': 'gpt-4.1-mini', 'fallback': 'gpt-5.4'}
- **Human surfaces**: review_mode=human; release-gate approvals and stakeholder answers were submitted over the API by a **scripted** reviewer/stakeholder (labelled as automation in every record).

## Result

**Agent success rate: 100.00%** (219/219 P1–P4 agent dispatches; threshold > 97.0%).

68 P3/P4 agent slots were **not admitted** because the authorized P2 release gate routed `cargotracker` (Retain), `jhipster-sample-app` (Retain), `angular-phonecat` (Retire), `gitea` (Retain) to the non-delivery register — by design, no architecture or plan is produced for a non-delivery route. Counting those slots as failures would give 76.31%.

Success = artifact not FAILED **and** enriched by the live Astra agent loop (not seed fallback) **and** passes ContractValidator (envelope + payload schema + content hash).

| phase | ok / total |
|---|---|
| P1 Discovery | 110 / 110 |
| P2 Portfolio | 7 / 7 |
| P3 Architecture | 48 / 48 |
| P4 Planning | 54 / 54 |

- Tool calls: 4529; evidence ids cited: 2557; LLM findings: 1276; repair rounds: 16; failovers: 0
- Tokens: {'input': 23345068, 'output': 932361, 'reasoning': 49737}

## Release gates

| phase | app | phase status | decision |
|---|---|---|---|
| P1 | cargotracker | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | spring-framework-petclinic | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | eshop-modernizing | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | jhipster-sample-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | saleor | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | djangoproject | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | angular-phonecat | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | human-essentials | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | opencart | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P1 | gitea | COMPLETED | READY_FOR_PORTFOLIO_DECISION |
| P2 | PF1 | COMPLETED | AUTHORIZED |
| P3 | cargotracker | NOT_ADMITTED | — |
| P4 | cargotracker | NOT_ADMITTED | — |
| P3 | jhipster-sample-app | NOT_ADMITTED | — |
| P4 | jhipster-sample-app | NOT_ADMITTED | — |
| P3 | angular-phonecat | NOT_ADMITTED | — |
| P4 | angular-phonecat | NOT_ADMITTED | — |
| P3 | gitea | NOT_ADMITTED | — |
| P4 | gitea | NOT_ADMITTED | — |
| P3 | spring-framework-petclinic | COMPLETED | CONDITIONAL_PLANNING |
| P3 | eshop-modernizing | COMPLETED | CONDITIONAL_PLANNING |
| P3 | djangoproject | COMPLETED | CONDITIONAL_PLANNING |
| P3 | saleor | COMPLETED | CONDITIONAL_PLANNING |
| P3 | opencart | COMPLETED | CONDITIONAL_PLANNING |
| P4 | spring-framework-petclinic | COMPLETED | SCOPED_PREPARATION |
| P4 | eshop-modernizing | COMPLETED | SCOPED_PREPARATION |
| P4 | opencart | COMPLETED | SCOPED_PREPARATION |
| P4 | saleor | COMPLETED | SCOPED_PREPARATION |
| P3 | human-essentials | COMPLETED | CONDITIONAL_PLANNING |
| P4 | djangoproject | COMPLETED | SCOPED_PREPARATION |
| P4 | human-essentials | COMPLETED | SCOPED_PREPARATION |

Reviews: 23 (decided by `scripted-reviewer`); stakeholder questions: 71 (71 answered).

## Per-agent results

| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| P1.A1 | eshop-modernizing | PARTIAL | yes | reasoning | 8 | 0 | 48 | 19 | ✅ |  |
| P1.A2 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 32 | 23 | ✅ |  |
| P1.A3 | eshop-modernizing | PARTIAL | yes | reasoning | 8 | 0 | 38 | 25 | ✅ |  |
| P1.A4 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 23 | 9 | ✅ |  |
| P1.A5 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 10 | 6 | ✅ |  |
| P1.A6 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 23 | 19 | ✅ |  |
| P1.A7 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P1.A8 | eshop-modernizing | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 24 | 18 | ✅ |  |
| P1.A10 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 24 | 10 | ✅ |  |
| P1.A11 | eshop-modernizing | PARTIAL | yes | reasoning | 5 | 0 | 18 | 10 | ✅ |  |
| P1.A1 | spring-framework-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 40 | 17 | ✅ |  |
| P1.A2 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 22 | 16 | ✅ |  |
| P1.A3 | spring-framework-petclinic | PARTIAL | yes | reasoning | 8 | 0 | 32 | 24 | ✅ |  |
| P1.A4 | spring-framework-petclinic | PARTIAL | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P1.A5 | spring-framework-petclinic | PARTIAL | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P1.A6 | spring-framework-petclinic | PARTIAL | yes | reasoning | 4 | 0 | 17 | 16 | ✅ |  |
| P1.A7 | spring-framework-petclinic | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A8 | spring-framework-petclinic | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 26 | 13 | ✅ |  |
| P1.A10 | spring-framework-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 21 | 11 | ✅ |  |
| P1.A11 | spring-framework-petclinic | PARTIAL | yes | reasoning | 4 | 0 | 12 | 9 | ✅ |  |
| P1.A1 | cargotracker | PARTIAL | yes | reasoning | 7 | 0 | 39 | 23 | ✅ |  |
| P1.A2 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 26 | 21 | ✅ |  |
| P1.A3 | cargotracker | PARTIAL | yes | reasoning | 9 | 0 | 40 | 22 | ✅ |  |
| P1.A4 | cargotracker | PARTIAL | yes | fast | 6 | 0 | 15 | 7 | ✅ |  |
| P1.A5 | cargotracker | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P1.A6 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 28 | 20 | ✅ |  |
| P1.A7 | cargotracker | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 4 | ✅ |  |
| P1.A8 | cargotracker | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | cargotracker | PARTIAL | yes | reasoning | 7 | 0 | 39 | 24 | ✅ |  |
| P1.A10 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 18 | 11 | ✅ |  |
| P1.A11 | cargotracker | PARTIAL | yes | reasoning | 5 | 0 | 19 | 11 | ✅ |  |
| P1.A1 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 42 | 15 | ✅ |  |
| P1.A2 | jhipster-sample-app | PARTIAL | yes | reasoning | 8 | 0 | 40 | 29 | ✅ |  |
| P1.A3 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 31 | 17 | ✅ |  |
| P1.A4 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 7 | 7 | ✅ |  |
| P1.A5 | jhipster-sample-app | PARTIAL | yes | fast | 8 | 1 | 14 | 13 | ✅ |  |
| P1.A6 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 27 | 19 | ✅ |  |
| P1.A7 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A8 | jhipster-sample-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 27 | 11 | ✅ |  |
| P1.A10 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 22 | 12 | ✅ |  |
| P1.A1 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 36 | 27 | ✅ |  |
| P1.A2 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 26 | 18 | ✅ |  |
| P1.A3 | saleor | PARTIAL | yes | reasoning | 9 | 0 | 45 | 21 | ✅ |  |
| P1.A4 | saleor | PARTIAL | yes | fast | 7 | 0 | 14 | 11 | ✅ |  |
| P1.A5 | saleor | PARTIAL | yes | fast | 7 | 0 | 12 | 2 | ✅ |  |
| P1.A6 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 34 | 23 | ✅ |  |
| P1.A7 | saleor | PARTIAL | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P1.A8 | saleor | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | saleor | PARTIAL | yes | reasoning | 9 | 0 | 34 | 16 | ✅ |  |
| P1.A10 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 30 | 16 | ✅ |  |
| P1.A11 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 29 | 12 | ✅ |  |
| P1.A1 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 43 | 18 | ✅ |  |
| P1.A2 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 28 | 23 | ✅ |  |
| P1.A3 | djangoproject | PARTIAL | yes | reasoning | 8 | 0 | 37 | 15 | ✅ |  |
| P1.A4 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 12 | 10 | ✅ |  |
| P1.A5 | djangoproject | PARTIAL | yes | fast | 7 | 0 | 11 | 9 | ✅ |  |
| P1.A6 | djangoproject | PARTIAL | yes | reasoning | 5 | 0 | 21 | 19 | ✅ |  |
| P1.A7 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P1.A8 | djangoproject | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | djangoproject | PARTIAL | yes | reasoning | 8 | 0 | 37 | 21 | ✅ |  |
| P1.A10 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 20 | 13 | ✅ |  |
| P1.A11 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 21 | 12 | ✅ |  |
| P1.A1 | angular-phonecat | PARTIAL | yes | reasoning | 6 | 0 | 31 | 17 | ✅ |  |
| P1.A2 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 23 | 19 | ✅ |  |
| P1.A3 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 19 | 15 | ✅ |  |
| P1.A4 | angular-phonecat | PARTIAL | yes | fast | 7 | 1 | 6 | 6 | ✅ |  |
| P1.A5 | angular-phonecat | PARTIAL | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P1.A6 | angular-phonecat | PARTIAL | yes | reasoning | 4 | 0 | 16 | 12 | ✅ |  |
| P1.A7 | angular-phonecat | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A8 | angular-phonecat | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | angular-phonecat | PARTIAL | yes | reasoning | 4 | 0 | 14 | 13 | ✅ |  |
| P1.A10 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 14 | 11 | ✅ |  |
| P1.A11 | angular-phonecat | PARTIAL | yes | reasoning | 4 | 0 | 13 | 10 | ✅ |  |
| P1.A1 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 48 | 24 | ✅ |  |
| P1.A2 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 34 | 24 | ✅ |  |
| P1.A3 | opencart | PARTIAL | yes | reasoning | 9 | 0 | 45 | 16 | ✅ |  |
| P1.A4 | opencart | PARTIAL | yes | fast | 7 | 0 | 13 | 12 | ✅ |  |
| P1.A5 | opencart | PARTIAL | yes | fast | 7 | 0 | 11 | 1 | ✅ |  |
| P1.A6 | opencart | PARTIAL | yes | reasoning | 5 | 0 | 21 | 17 | ✅ |  |
| P1.A7 | opencart | PARTIAL | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P1.A8 | opencart | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 21 | 10 | ✅ |  |
| P1.A10 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 20 | 13 | ✅ |  |
| P1.A11 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 21 | 16 | ✅ |  |
| P1.A1 | human-essentials | PARTIAL | yes | reasoning | 9 | 1 | 50 | 22 | ✅ |  |
| P1.A2 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 35 | 22 | ✅ |  |
| P1.A3 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 39 | 24 | ✅ |  |
| P1.A4 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 19 | 17 | ✅ |  |
| P1.A5 | human-essentials | PARTIAL | yes | fast | 7 | 0 | 11 | 8 | ✅ |  |
| P1.A6 | human-essentials | PARTIAL | yes | reasoning | 5 | 0 | 28 | 24 | ✅ |  |
| P1.A7 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P1.A8 | human-essentials | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | human-essentials | PARTIAL | yes | reasoning | 11 | 1 | 53 | 23 | ✅ |  |
| P1.A10 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 25 | 12 | ✅ |  |
| P1.A11 | human-essentials | PARTIAL | yes | reasoning | 5 | 0 | 22 | 12 | ✅ |  |
| P1.A1 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 43 | 24 | ✅ |  |
| P1.A2 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 29 | 16 | ✅ |  |
| P1.A3 | gitea | PARTIAL | yes | reasoning | 9 | 0 | 55 | 25 | ✅ |  |
| P1.A4 | gitea | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A5 | gitea | PARTIAL | yes | fast | 8 | 1 | 7 | 4 | ✅ |  |
| P1.A6 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 34 | 24 | ✅ |  |
| P1.A7 | gitea | PARTIAL | yes | fast | 6 | 0 | 6 | 4 | ✅ |  |
| P1.A8 | gitea | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | gitea | PARTIAL | yes | reasoning | 9 | 0 | 30 | 16 | ✅ |  |
| P1.A10 | gitea | PARTIAL | yes | reasoning | 6 | 0 | 25 | 14 | ✅ |  |
| P1.A11 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 25 | 14 | ✅ |  |
| P2.A1 | PF1 | PARTIAL | yes | reasoning | 8 | 0 | 30 | 17 | ✅ |  |
| P2.A2 | PF1 | PARTIAL | yes | reasoning | 8 | 0 | 39 | 23 | ✅ |  |
| P2.A3 | PF1 | COMPLETE | yes | fast | 6 | 0 | 11 | 1 | ✅ |  |
| P2.A4 | PF1 | COMPLETE | yes | fast | 7 | 1 | 17 | 4 | ✅ |  |
| P2.A5 | PF1 | COMPLETE | yes | fast | 4 | 1 | 12 | 3 | ✅ |  |
| P2.A6 | PF1 | PARTIAL | yes | reasoning | 10 | 0 | 65 | 38 | ✅ |  |
| P2.A7 | PF1 | PARTIAL | yes | reasoning | 6 | 0 | 20 | 15 | ✅ |  |
| P3.A1 | eshop-modernizing | PARTIAL | yes | reasoning | 9 | 0 | 54 | 30 | ✅ |  |
| P3.A2 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 34 | 18 | ✅ |  |
| P3.A3 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 22 | 17 | ✅ |  |
| P3.A4 | eshop-modernizing | PARTIAL | yes | reasoning | 8 | 0 | 28 | 14 | ✅ |  |
| P3.A5 | eshop-modernizing | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P3.A6 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 38 | 17 | ✅ |  |
| P3.A7 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P3.A8 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 27 | 13 | ✅ |  |
| P3.A1 | spring-framework-petclinic | PARTIAL | yes | reasoning | 8 | 0 | 46 | 31 | ✅ |  |
| P3.A2 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 22 | 15 | ✅ |  |
| P3.A3 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 20 | 14 | ✅ |  |
| P3.A4 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 19 | 16 | ✅ |  |
| P3.A5 | spring-framework-petclinic | SKIPPED_APPROVED | yes | fast | 6 | 0 | 10 | 6 | ✅ |  |
| P3.A6 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 26 | 18 | ✅ |  |
| P3.A7 | spring-framework-petclinic | COMPLETE | yes | fast | 6 | 0 | 10 | 1 | ✅ |  |
| P3.A8 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 24 | 13 | ✅ |  |
| P3.A1 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A2 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A3 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A4 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A5 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A6 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A7 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A8 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P3.A1 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P3.A2 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P3.A3 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P3.A4 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P3.A5 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P3.A6 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P3.A7 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P3.A8 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P3.A1 | saleor | PARTIAL | yes | reasoning | 9 | 0 | 58 | 33 | ✅ |  |
| P3.A2 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 26 | 19 | ✅ |  |
| P3.A3 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 26 | 12 | ✅ |  |
| P3.A4 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 31 | 20 | ✅ |  |
| P3.A5 | saleor | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P3.A6 | saleor | PARTIAL | yes | reasoning | 9 | 0 | 52 | 21 | ✅ |  |
| P3.A7 | saleor | COMPLETE | yes | fast | 6 | 0 | 11 | 4 | ✅ |  |
| P3.A8 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 33 | 16 | ✅ |  |
| P3.A1 | djangoproject | PARTIAL | yes | reasoning | 9 | 0 | 51 | 26 | ✅ |  |
| P3.A2 | djangoproject | PARTIAL | yes | reasoning | 5 | 0 | 20 | 12 | ✅ |  |
| P3.A3 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 35 | 21 | ✅ |  |
| P3.A4 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 26 | 16 | ✅ |  |
| P3.A5 | djangoproject | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 7 | ✅ |  |
| P3.A6 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 39 | 27 | ✅ |  |
| P3.A7 | djangoproject | COMPLETE | yes | fast | 7 | 0 | 15 | 1 | ✅ |  |
| P3.A8 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 29 | 16 | ✅ |  |
| P3.A1 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A2 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A3 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A4 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A5 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A6 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A7 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A8 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A1 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 52 | 25 | ✅ |  |
| P3.A2 | opencart | PARTIAL | yes | reasoning | 5 | 0 | 21 | 13 | ✅ |  |
| P3.A3 | opencart | PARTIAL | yes | reasoning | 5 | 0 | 20 | 15 | ✅ |  |
| P3.A4 | opencart | PARTIAL | yes | reasoning | 7 | 0 | 27 | 19 | ✅ |  |
| P3.A5 | opencart | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P3.A6 | opencart | PARTIAL | yes | reasoning | 7 | 0 | 34 | 22 | ✅ |  |
| P3.A7 | opencart | COMPLETE | yes | fast | 6 | 0 | 15 | 4 | ✅ |  |
| P3.A8 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 26 | 13 | ✅ |  |
| P3.A1 | human-essentials | PARTIAL | yes | reasoning | 9 | 0 | 57 | 30 | ✅ |  |
| P3.A2 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 39 | 24 | ✅ |  |
| P3.A3 | human-essentials | PARTIAL | yes | reasoning | 8 | 0 | 36 | 18 | ✅ |  |
| P3.A4 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 24 | 15 | ✅ |  |
| P3.A5 | human-essentials | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P3.A6 | human-essentials | PARTIAL | yes | reasoning | 8 | 0 | 45 | 29 | ✅ |  |
| P3.A7 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 18 | 2 | ✅ |  |
| P3.A8 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 27 | 13 | ✅ |  |
| P3.A1 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P3.A2 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P3.A3 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P3.A4 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P3.A5 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P3.A6 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P3.A7 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P3.A8 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P4.A1 | eshop-modernizing | COMPLETE | yes | fast | 3 | 0 | 2 | 1 | ✅ |  |
| P4.A2 | eshop-modernizing | COMPLETE | yes | fast | 4 | 0 | 3 | 1 | ✅ |  |
| P4.A3 | eshop-modernizing | PARTIAL | yes | coding | 9 | 0 | 26 | 17 | ✅ |  |
| P4.A4 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P4.A5 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P4.A6 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 18 | 2 | ✅ |  |
| P4.A7 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 11 | 3 | ✅ |  |
| P4.A8 | eshop-modernizing | COMPLETE | yes | fast | 6 | 0 | 11 | 1 | ✅ |  |
| P4.A9 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 22 | 17 | ✅ |  |
| P4.A1 | spring-framework-petclinic | COMPLETE | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P4.A2 | spring-framework-petclinic | COMPLETE | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P4.A3 | spring-framework-petclinic | PARTIAL | yes | coding | 5 | 0 | 14 | 8 | ✅ |  |
| P4.A4 | spring-framework-petclinic | COMPLETE | yes | fast | 2 | 0 | 3 | 4 | ✅ |  |
| P4.A5 | spring-framework-petclinic | COMPLETE | yes | fast | 6 | 0 | 10 | 2 | ✅ |  |
| P4.A6 | spring-framework-petclinic | COMPLETE | yes | fast | 7 | 1 | 10 | 4 | ✅ |  |
| P4.A7 | spring-framework-petclinic | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P4.A8 | spring-framework-petclinic | COMPLETE | yes | fast | 6 | 0 | 16 | 1 | ✅ |  |
| P4.A9 | spring-framework-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 21 | 17 | ✅ |  |
| P4.A1 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A2 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A3 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A4 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A5 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A6 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A7 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A8 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A9 | cargotracker | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put cargotracker in the IA02 non-delivery register (Retain) |
| P4.A1 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P4.A2 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P4.A3 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P4.A4 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P4.A5 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P4.A6 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P4.A7 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P4.A8 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P4.A9 | jhipster-sample-app | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put jhipster-sample-app in the IA02 non-delivery register (Retain) |
| P4.A1 | saleor | COMPLETE | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P4.A2 | saleor | COMPLETE | yes | fast | 6 | 0 | 6 | 2 | ✅ |  |
| P4.A3 | saleor | PARTIAL | yes | coding | 9 | 0 | 19 | 15 | ✅ |  |
| P4.A4 | saleor | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P4.A5 | saleor | PARTIAL | yes | fast | 7 | 1 | 13 | 2 | ✅ |  |
| P4.A6 | saleor | COMPLETE | yes | fast | 7 | 1 | 13 | 3 | ✅ |  |
| P4.A7 | saleor | COMPLETE | yes | fast | 6 | 0 | 14 | 1 | ✅ |  |
| P4.A8 | saleor | COMPLETE | yes | fast | 4 | 0 | 9 | 1 | ✅ |  |
| P4.A9 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 23 | 17 | ✅ |  |
| P4.A1 | djangoproject | COMPLETE | yes | fast | 4 | 0 | 10 | 1 | ✅ |  |
| P4.A2 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 12 | 3 | ✅ |  |
| P4.A3 | djangoproject | COMPLETE | yes | coding | 7 | 0 | 22 | 16 | ✅ |  |
| P4.A4 | djangoproject | COMPLETE | yes | fast | 4 | 0 | 7 | 2 | ✅ |  |
| P4.A5 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 13 | 5 | ✅ |  |
| P4.A6 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 12 | 5 | ✅ |  |
| P4.A7 | djangoproject | PARTIAL | yes | fast | 7 | 1 | 8 | 2 | ✅ |  |
| P4.A8 | djangoproject | COMPLETE | yes | fast | 2 | 0 | 3 | 1 | ✅ |  |
| P4.A9 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 25 | 18 | ✅ |  |
| P4.A1 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A2 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A3 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A4 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A5 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A6 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A7 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A8 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A9 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A1 | opencart | COMPLETE | yes | fast | 6 | 0 | 12 | 2 | ✅ |  |
| P4.A2 | opencart | COMPLETE | yes | fast | 2 | 0 | 1 | 2 | ✅ |  |
| P4.A3 | opencart | PARTIAL | yes | coding | 9 | 0 | 18 | 15 | ✅ |  |
| P4.A4 | opencart | COMPLETE | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P4.A5 | opencart | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P4.A6 | opencart | COMPLETE | yes | fast | 7 | 1 | 13 | 6 | ✅ |  |
| P4.A7 | opencart | COMPLETE | yes | fast | 7 | 1 | 13 | 1 | ✅ |  |
| P4.A8 | opencart | PARTIAL | yes | fast | 6 | 0 | 14 | 1 | ✅ |  |
| P4.A9 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 25 | 20 | ✅ |  |
| P4.A1 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P4.A2 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A3 | human-essentials | PARTIAL | yes | coding | 9 | 2 | 18 | 13 | ✅ |  |
| P4.A4 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P4.A6 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 13 | 1 | ✅ |  |
| P4.A7 | human-essentials | COMPLETE | yes | fast | 7 | 1 | 9 | 1 | ✅ |  |
| P4.A8 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 10 | 1 | ✅ |  |
| P4.A9 | human-essentials | PARTIAL | yes | reasoning | 5 | 0 | 18 | 20 | ✅ |  |
| P4.A1 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P4.A2 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P4.A3 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P4.A4 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P4.A5 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P4.A6 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P4.A7 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P4.A8 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
| P4.A9 | gitea | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put gitea in the IA02 non-delivery register (Retain) |
