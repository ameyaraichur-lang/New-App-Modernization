# E2E agentic acceptance run `run-analyzers-holdout`

- **Job**: `job-1792321699-449172` — **COMPLETED**
- **Repositories**: `eshop-modernizing`, `spring-framework-petclinic`, `cargotracker`, `jhipster-sample-app`, `saleor`, `djangoproject`, `angular-phonecat`, `opencart`, `human-essentials`, `gitea`
- **Elapsed**: 312 min 57 s; LLM cache mode `record` (record = every call live, responses recorded for replay)
- **Astra tiers**: {'reasoning': 'gpt-6-astra', 'coding': 'gpt-5.3-codex-PlayWright', 'fast': 'gpt-4.1-mini', 'fallback': 'gpt-5.4'}
- **Human surfaces**: review_mode=human; release-gate approvals and stakeholder answers were submitted over the API by a **scripted** reviewer/stakeholder (labelled as automation in every record).

## Result

**Agent success rate: 100.00%** (202/202 P1–P4 agent dispatches; threshold > 97.0%).

85 P3/P4 agent slots were **not admitted** because the authorized P2 release gate routed `eshop-modernizing` (Retire), `spring-framework-petclinic` (Retain), `cargotracker` (Retain), `jhipster-sample-app` (Retain), `angular-phonecat` (Retire) to the non-delivery register — by design, no architecture or plan is produced for a non-delivery route. Counting those slots as failures would give 70.38%.

Success = artifact not FAILED **and** enriched by the live Astra agent loop (not seed fallback) **and** passes ContractValidator (envelope + payload schema + content hash).

| phase | ok / total |
|---|---|
| P1 Discovery | 110 / 110 |
| P2 Portfolio | 7 / 7 |
| P3 Architecture | 40 / 40 |
| P4 Planning | 45 / 45 |

- Tool calls: 4414; evidence ids cited: 2310; LLM findings: 1268; repair rounds: 16; failovers: 1
- Tokens: {'input': 24486421, 'output': 868185, 'reasoning': 46753}

## Release gates

Assurance is per released item: model items that were neither entailed by the claim-support verifier nor tool-measured were confirmed by the approving reviewer (scripted here).

| phase | app | phase status | decision | assurance (before review) | confirmed by review |
|---|---|---|---|---|---|
| P1 | cargotracker | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 20 · entailed 122 · unverified 115 | 115 |
| P1 | spring-framework-petclinic | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 20 · entailed 120 · unverified 97 | 97 |
| P1 | eshop-modernizing | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 20 · entailed 112 · unverified 115 | 115 |
| P1 | jhipster-sample-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 115 · unverified 120 | 120 |
| P1 | saleor | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 125 · unverified 112 | 112 |
| P1 | djangoproject | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 106 · unverified 141 | 141 |
| P1 | angular-phonecat | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 115 · unverified 74 | 74 |
| P1 | opencart | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 115 · unverified 102 | 102 |
| P1 | human-essentials | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 137 · unverified 108 | 108 |
| P1 | gitea | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 120 · unverified 119 | 119 |
| P2 | PF1 | COMPLETED | AUTHORIZED | tool-measured 7 · entailed 17 · unverified 109 | 109 |
| P3 | eshop-modernizing | NOT_ADMITTED | — | — | 0 |
| P4 | eshop-modernizing | NOT_ADMITTED | — | — | 0 |
| P3 | spring-framework-petclinic | NOT_ADMITTED | — | — | 0 |
| P4 | spring-framework-petclinic | NOT_ADMITTED | — | — | 0 |
| P3 | cargotracker | NOT_ADMITTED | — | — | 0 |
| P4 | cargotracker | NOT_ADMITTED | — | — | 0 |
| P3 | jhipster-sample-app | NOT_ADMITTED | — | — | 0 |
| P4 | jhipster-sample-app | NOT_ADMITTED | — | — | 0 |
| P3 | angular-phonecat | NOT_ADMITTED | — | — | 0 |
| P4 | angular-phonecat | NOT_ADMITTED | — | — | 0 |
| P3 | opencart | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 28 · unverified 169 | 169 |
| P3 | human-essentials | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 35 · unverified 185 | 185 |
| P3 | gitea | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 29 · unverified 182 | 182 |
| P3 | djangoproject | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 19 · unverified 212 | 212 |
| P3 | saleor | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 29 · unverified 189 | 189 |
| P4 | djangoproject | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 18 · unverified 89 | 89 |
| P4 | human-essentials | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 18 · unverified 83 | 83 |
| P4 | gitea | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 20 · unverified 77 | 77 |
| P4 | opencart | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 15 · unverified 90 | 90 |
| P4 | saleor | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 16 · unverified 81 | 81 |

Reviews: 21 (decided by `scripted-reviewer`); stakeholder questions: 71 (71 answered).

## Per-agent results

| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| P1.A1 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 39 | 12 | ✅ |  |
| P1.A2 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 34 | 21 | ✅ |  |
| P1.A3 | eshop-modernizing | PARTIAL | yes | reasoning | 8 | 0 | 41 | 21 | ✅ |  |
| P1.A4 | eshop-modernizing | PARTIAL | yes | fast | 7 | 0 | 18 | 9 | ✅ |  |
| P1.A5 | eshop-modernizing | PARTIAL | yes | fast | 8 | 1 | 11 | 7 | ✅ |  |
| P1.A6 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 23 | 11 | ✅ |  |
| P1.A7 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A8 | eshop-modernizing | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 19 | 7 | ✅ |  |
| P1.A10 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 24 | 11 | ✅ |  |
| P1.A11 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 29 | 13 | ✅ |  |
| P1.A1 | spring-framework-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 36 | 15 | ✅ |  |
| P1.A2 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 23 | 15 | ✅ |  |
| P1.A3 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 28 | 16 | ✅ |  |
| P1.A4 | spring-framework-petclinic | PARTIAL | yes | fast | 6 | 0 | 11 | 6 | ✅ |  |
| P1.A5 | spring-framework-petclinic | PARTIAL | yes | fast | 6 | 0 | 13 | 9 | ✅ |  |
| P1.A6 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 22 | 19 | ✅ |  |
| P1.A7 | spring-framework-petclinic | PARTIAL | yes | fast | 6 | 0 | 8 | 3 | ✅ |  |
| P1.A8 | spring-framework-petclinic | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 29 | 16 | ✅ |  |
| P1.A10 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 15 | 11 | ✅ |  |
| P1.A11 | spring-framework-petclinic | PARTIAL | yes | reasoning | 4 | 0 | 13 | 10 | ✅ |  |
| P1.A1 | cargotracker | PARTIAL | yes | reasoning | 7 | 0 | 40 | 19 | ✅ |  |
| P1.A2 | cargotracker | PARTIAL | yes | reasoning | 7 | 0 | 30 | 25 | ✅ |  |
| P1.A3 | cargotracker | PARTIAL | yes | reasoning | 9 | 0 | 42 | 24 | ✅ |  |
| P1.A4 | cargotracker | PARTIAL | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P1.A5 | cargotracker | SKIPPED_APPROVED | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P1.A6 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 26 | 18 | ✅ |  |
| P1.A7 | cargotracker | SKIPPED_APPROVED | yes | fast | 7 | 1 | 5 | 6 | ✅ |  |
| P1.A8 | cargotracker | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | cargotracker | PARTIAL | yes | reasoning | 7 | 0 | 37 | 18 | ✅ |  |
| P1.A10 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 19 | 15 | ✅ |  |
| P1.A11 | cargotracker | PARTIAL | yes | reasoning | 8 | 0 | 30 | 9 | ✅ |  |
| P1.A1 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 42 | 18 | ✅ |  |
| P1.A2 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 32 | 23 | ✅ |  |
| P1.A3 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 27 | 14 | ✅ |  |
| P1.A4 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 15 | 9 | ✅ |  |
| P1.A5 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 12 | 7 | ✅ |  |
| P1.A6 | jhipster-sample-app | PARTIAL | yes | reasoning | 5 | 0 | 27 | 17 | ✅ |  |
| P1.A7 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A8 | jhipster-sample-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 35 | 11 | ✅ |  |
| P1.A10 | jhipster-sample-app | PARTIAL | yes | reasoning | 8 | 0 | 24 | 11 | ✅ |  |
| P1.A11 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 20 | 12 | ✅ |  |
| P1.A1 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 37 | 27 | ✅ |  |
| P1.A2 | saleor | PARTIAL | yes | reasoning | 5 | 0 | 21 | 19 | ✅ |  |
| P1.A3 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 38 | 17 | ✅ |  |
| P1.A4 | saleor | PARTIAL | yes | fast | 6 | 0 | 8 | 8 | ✅ |  |
| P1.A5 | saleor | PARTIAL | yes | fast | 7 | 0 | 9 | 5 | ✅ |  |
| P1.A6 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 32 | 23 | ✅ |  |
| P1.A7 | saleor | PARTIAL | yes | fast | 7 | 0 | 7 | 1 | ✅ |  |
| P1.A8 | saleor | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 35 | 16 | ✅ |  |
| P1.A10 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 20 | 11 | ✅ |  |
| P1.A11 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 27 | 12 | ✅ |  |
| P1.A1 | djangoproject | PARTIAL | yes | reasoning | 9 | 0 | 58 | 25 | ✅ |  |
| P1.A2 | djangoproject | PARTIAL | yes | reasoning | 5 | 0 | 21 | 18 | ✅ |  |
| P1.A3 | djangoproject | PARTIAL | yes | reasoning | 9 | 0 | 44 | 17 | ✅ |  |
| P1.A4 | djangoproject | PARTIAL | yes | fast | 8 | 1 | 13 | 10 | ✅ |  |
| P1.A5 | djangoproject | PARTIAL | yes | fast | 7 | 1 | 7 | 4 | ✅ |  |
| P1.A6 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 24 | 20 | ✅ |  |
| P1.A7 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P1.A8 | djangoproject | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 26 | 11 | ✅ |  |
| P1.A10 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 22 | 13 | ✅ |  |
| P1.A11 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 23 | 11 | ✅ |  |
| P1.A1 | angular-phonecat | PARTIAL | yes | reasoning | 6 | 0 | 38 | 20 | ✅ |  |
| P1.A2 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 28 | 18 | ✅ |  |
| P1.A3 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 21 | 13 | ✅ |  |
| P1.A4 | angular-phonecat | PARTIAL | yes | fast | 6 | 0 | 6 | 5 | ✅ |  |
| P1.A5 | angular-phonecat | PARTIAL | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P1.A6 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 19 | 18 | ✅ |  |
| P1.A7 | angular-phonecat | PARTIAL | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P1.A8 | angular-phonecat | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | angular-phonecat | PARTIAL | yes | reasoning | 4 | 0 | 15 | 13 | ✅ |  |
| P1.A10 | angular-phonecat | PARTIAL | yes | reasoning | 6 | 0 | 20 | 11 | ✅ |  |
| P1.A11 | angular-phonecat | PARTIAL | yes | reasoning | 6 | 0 | 18 | 10 | ✅ |  |
| P1.A1 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 50 | 26 | ✅ |  |
| P1.A2 | opencart | PARTIAL | yes | reasoning | 9 | 0 | 42 | 23 | ✅ |  |
| P1.A3 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 40 | 16 | ✅ |  |
| P1.A4 | opencart | PARTIAL | yes | fast | 6 | 0 | 10 | 9 | ✅ |  |
| P1.A5 | opencart | PARTIAL | yes | fast | 7 | 0 | 13 | 8 | ✅ |  |
| P1.A6 | opencart | PARTIAL | yes | reasoning | 5 | 0 | 19 | 16 | ✅ |  |
| P1.A7 | opencart | PARTIAL | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P1.A8 | opencart | PARTIAL | yes | reasoning | 2 | 0 | 3 | 5 | ✅ |  |
| P1.A9 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 25 | 11 | ✅ |  |
| P1.A10 | opencart | PARTIAL | yes | reasoning | 7 | 0 | 21 | 12 | ✅ |  |
| P1.A11 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 23 | 15 | ✅ |  |
| P1.A1 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 48 | 19 | ✅ |  |
| P1.A2 | human-essentials | PARTIAL | yes | reasoning | 8 | 0 | 38 | 23 | ✅ |  |
| P1.A3 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 38 | 24 | ✅ |  |
| P1.A4 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 15 | 7 | ✅ |  |
| P1.A5 | human-essentials | PARTIAL | yes | fast | 7 | 0 | 10 | 5 | ✅ |  |
| P1.A6 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 30 | 22 | ✅ |  |
| P1.A7 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 7 | 6 | ✅ |  |
| P1.A8 | human-essentials | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | human-essentials | PARTIAL | yes | reasoning | 10 | 1 | 45 | 15 | ✅ |  |
| P1.A10 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 20 | 13 | ✅ |  |
| P1.A11 | human-essentials | PARTIAL | yes | reasoning | 9 | 0 | 33 | 15 | ✅ |  |
| P1.A1 | gitea | PARTIAL | yes | reasoning | 8 | 0 | 44 | 23 | ✅ |  |
| P1.A2 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 30 | 20 | ✅ |  |
| P1.A3 | gitea | PARTIAL | yes | reasoning | 10 | 0 | 63 | 20 | ✅ |  |
| P1.A4 | gitea | PARTIAL | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P1.A5 | gitea | PARTIAL | yes | fast | 7 | 0 | 9 | 6 | ✅ |  |
| P1.A6 | gitea | PARTIAL | yes | reasoning | 6 | 0 | 33 | 15 | ✅ |  |
| P1.A7 | gitea | PARTIAL | yes | fast | 7 | 0 | 6 | 3 | ✅ |  |
| P1.A8 | gitea | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | gitea | PARTIAL | yes | reasoning | 9 | 0 | 33 | 11 | ✅ |  |
| P1.A10 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 21 | 17 | ✅ |  |
| P1.A11 | gitea | PARTIAL | yes | reasoning | 5 | 0 | 19 | 14 | ✅ |  |
| P2.A1 | PF1 | PARTIAL | yes | reasoning | 9 | 0 | 28 | 19 | ✅ |  |
| P2.A2 | PF1 | PARTIAL | yes | reasoning | 9 | 0 | 57 | 43 | ✅ |  |
| P2.A3 | PF1 | COMPLETE | yes | fast | 6 | 0 | 16 | 2 | ✅ |  |
| P2.A4 | PF1 | COMPLETE | yes | fast | 6 | 0 | 51 | 20 | ✅ |  |
| P2.A5 | PF1 | COMPLETE | yes | fast | 4 | 0 | 8 | 4 | ✅ |  |
| P2.A6 | PF1 | PARTIAL | yes | reasoning | 7 | 0 | 70 | 31 | ✅ |  |
| P2.A7 | PF1 | PARTIAL | yes | reasoning | 6 | 0 | 29 | 19 | ✅ |  |
| P3.A1 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P3.A2 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P3.A3 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P3.A4 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P3.A5 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P3.A6 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P3.A7 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P3.A8 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P3.A1 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A2 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A3 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A4 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A5 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A6 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A7 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P3.A8 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
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
| P3.A1 | saleor | PARTIAL | yes | reasoning | 9 | 0 | 59 | 29 | ✅ |  |
| P3.A2 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 27 | 13 | ✅ |  |
| P3.A3 | saleor | PARTIAL | yes | reasoning | 9 | 0 | 34 | 18 | ✅ |  |
| P3.A4 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 33 | 21 | ✅ |  |
| P3.A5 | saleor | SKIPPED_APPROVED | yes | fast | 7 | 0 | 9 | 4 | ✅ |  |
| P3.A6 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 43 | 23 | ✅ |  |
| P3.A7 | saleor | PARTIAL | yes | fast | 7 | 1 | 13 | 5 | ✅ |  |
| P3.A8 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 39 | 14 | ✅ |  |
| P3.A1 | djangoproject | PARTIAL | yes | reasoning | 9 | 0 | 46 | 24 | ✅ |  |
| P3.A2 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 31 | 19 | ✅ |  |
| P3.A3 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 28 | 15 | ✅ |  |
| P3.A4 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 26 | 16 | ✅ |  |
| P3.A5 | djangoproject | SKIPPED_APPROVED | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P3.A6 | djangoproject | PARTIAL | yes | reasoning | 9 | 0 | 46 | 19 | ✅ |  |
| P3.A7 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 7 | 8 | ✅ |  |
| P3.A8 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 22 | 11 | ✅ |  |
| P3.A1 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A2 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A3 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A4 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A5 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A6 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A7 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A8 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A1 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 56 | 27 | ✅ |  |
| P3.A2 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 28 | 17 | ✅ |  |
| P3.A3 | opencart | PARTIAL | yes | reasoning | 9 | 0 | 29 | 19 | ✅ |  |
| P3.A4 | opencart | PARTIAL | yes | reasoning | 7 | 0 | 27 | 15 | ✅ |  |
| P3.A5 | opencart | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 6 | ✅ |  |
| P3.A6 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 35 | 20 | ✅ |  |
| P3.A7 | opencart | PARTIAL | yes | fast | 5 | 0 | 14 | 1 | ✅ |  |
| P3.A8 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 27 | 13 | ✅ |  |
| P3.A1 | human-essentials | PARTIAL | yes | reasoning | 10 | 0 | 59 | 25 | ✅ |  |
| P3.A2 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 39 | 16 | ✅ |  |
| P3.A3 | human-essentials | PARTIAL | yes | reasoning | 8 | 0 | 33 | 19 | ✅ |  |
| P3.A4 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 30 | 20 | ✅ |  |
| P3.A5 | human-essentials | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P3.A6 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 36 | 21 | ✅ |  |
| P3.A7 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 10 | 6 | ✅ |  |
| P3.A8 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 34 | 13 | ✅ |  |
| P3.A1 | gitea | PARTIAL | yes | reasoning | 9 | 0 | 65 | 28 | ✅ |  |
| P3.A2 | gitea | PARTIAL | yes | reasoning | 5 | 0 | 23 | 11 | ✅ |  |
| P3.A3 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 27 | 14 | ✅ |  |
| P3.A4 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 30 | 16 | ✅ |  |
| P3.A5 | gitea | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P3.A6 | gitea | PARTIAL | yes | reasoning | 8 | 0 | 45 | 15 | ✅ |  |
| P3.A7 | gitea | COMPLETE | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P3.A8 | gitea | PARTIAL | yes | reasoning | 6 | 0 | 27 | 12 | ✅ |  |
| P4.A1 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P4.A2 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P4.A3 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P4.A4 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P4.A5 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P4.A6 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P4.A7 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P4.A8 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P4.A9 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retire) |
| P4.A1 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A2 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A3 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A4 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A5 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A6 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A7 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A8 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
| P4.A9 | spring-framework-petclinic | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put spring-framework-petclinic in the IA02 non-delivery register (Retain) |
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
| P4.A1 | saleor | COMPLETE | yes | fast | 4 | 0 | 4 | 3 | ✅ |  |
| P4.A2 | saleor | COMPLETE | yes | fast | 6 | 0 | 17 | 1 | ✅ |  |
| P4.A3 | saleor | PARTIAL | yes | coding | 9 | 0 | 19 | 9 | ✅ |  |
| P4.A4 | saleor | COMPLETE | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P4.A5 | saleor | PARTIAL | yes | fast | 6 | 0 | 9 | 7 | ✅ |  |
| P4.A6 | saleor | PARTIAL | yes | fast | 7 | 1 | 20 | 8 | ✅ |  |
| P4.A7 | saleor | COMPLETE | yes | fast | 6 | 0 | 20 | 1 | ✅ |  |
| P4.A8 | saleor | COMPLETE | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P4.A9 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 23 | 17 | ✅ |  |
| P4.A1 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 15 | 2 | ✅ |  |
| P4.A2 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 13 | 2 | ✅ |  |
| P4.A3 | djangoproject | PARTIAL | yes | coding | 9 | 0 | 28 | 16 | ✅ |  |
| P4.A4 | djangoproject | COMPLETE | yes | fast | 2 | 0 | 3 | 3 | ✅ |  |
| P4.A5 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P4.A6 | djangoproject | COMPLETE | yes | fast | 8 | 2 | 10 | 2 | ✅ |  |
| P4.A7 | djangoproject | COMPLETE | yes | fast | 7 | 1 | 14 | 3 | ✅ |  |
| P4.A8 | djangoproject | COMPLETE | yes | fast | 8 | 2 | 12 | 2 | ✅ |  |
| P4.A9 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 21 | 14 | ✅ |  |
| P4.A1 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A2 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A3 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A4 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A5 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A6 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A7 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A8 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A9 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A1 | opencart | COMPLETE | yes | fast | 6 | 0 | 6 | 1 | ✅ |  |
| P4.A2 | opencart | COMPLETE | yes | fast | 2 | 0 | 1 | 3 | ✅ |  |
| P4.A3 | opencart | PARTIAL | yes | coding | 9 | 0 | 25 | 16 | ✅ |  |
| P4.A4 | opencart | COMPLETE | yes | fast | 2 | 0 | 2 | 3 | ✅ |  |
| P4.A5 | opencart | PARTIAL | yes | fast | 7 | 1 | 5 | 2 | ✅ |  |
| P4.A6 | opencart | PARTIAL | yes | fast | 6 | 0 | 16 | 5 | ✅ |  |
| P4.A7 | opencart | PARTIAL | yes | fast | 2 | 0 | 4 | 4 | ✅ |  |
| P4.A8 | opencart | PARTIAL | yes | fast | 6 | 0 | 22 | 2 | ✅ |  |
| P4.A9 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 22 | 15 | ✅ |  |
| P4.A1 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P4.A2 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P4.A3 | human-essentials | PARTIAL | yes | coding | 7 | 0 | 22 | 15 | ✅ |  |
| P4.A4 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P4.A5 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A6 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P4.A7 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 8 | 1 | ✅ |  |
| P4.A8 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 11 | 1 | ✅ |  |
| P4.A9 | human-essentials | PARTIAL | yes | reasoning | 5 | 0 | 20 | 14 | ✅ |  |
| P4.A1 | gitea | COMPLETE | yes | fast | 3 | 0 | 2 | 2 | ✅ |  |
| P4.A2 | gitea | COMPLETE | yes | fast | 6 | 0 | 7 | 2 | ✅ |  |
| P4.A3 | gitea | PARTIAL | yes | coding | 7 | 0 | 25 | 16 | ✅ |  |
| P4.A4 | gitea | COMPLETE | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P4.A5 | gitea | PARTIAL | yes | fast | 4 | 0 | 11 | 4 | ✅ |  |
| P4.A6 | gitea | PARTIAL | yes | fast | 6 | 0 | 15 | 2 | ✅ |  |
| P4.A7 | gitea | COMPLETE | yes | fast | 8 | 2 | 12 | 1 | ✅ |  |
| P4.A8 | gitea | COMPLETE | yes | fast | 7 | 1 | 13 | 1 | ✅ |  |
| P4.A9 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 26 | 17 | ✅ |  |
