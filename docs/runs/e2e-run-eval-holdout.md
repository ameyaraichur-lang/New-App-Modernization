# E2E agentic acceptance run `run-eval-holdout`

- **Job**: `job-1792248896-66d376` — **COMPLETED**
- **Repositories**: `eshop-modernizing`, `spring-framework-petclinic`, `cargotracker`, `jhipster-sample-app`, `saleor`, `djangoproject`, `angular-phonecat`, `opencart`, `human-essentials`, `gitea`
- **Elapsed**: 1060 min 32 s; LLM cache mode `record` (record = every call live, responses recorded for replay)
- **Astra tiers**: {'reasoning': 'gpt-6-astra', 'coding': 'gpt-5.3-codex-PlayWright', 'fast': 'gpt-4.1-mini', 'fallback': 'gpt-5.4'}
- **Human surfaces**: review_mode=human; release-gate approvals and stakeholder answers were submitted over the API by a **scripted** reviewer/stakeholder (labelled as automation in every record).

## Result

**Agent success rate: 100.00%** (219/219 P1–P4 agent dispatches; threshold > 97.0%).

68 P3/P4 agent slots were **not admitted** because the authorized P2 release gate routed `eshop-modernizing` (Retain), `spring-framework-petclinic` (Retain), `cargotracker` (Retain), `angular-phonecat` (Retire) to the non-delivery register — by design, no architecture or plan is produced for a non-delivery route. Counting those slots as failures would give 76.31%.

Success = artifact not FAILED **and** enriched by the live Astra agent loop (not seed fallback) **and** passes ContractValidator (envelope + payload schema + content hash).

| phase | ok / total |
|---|---|
| P1 Discovery | 110 / 110 |
| P2 Portfolio | 7 / 7 |
| P3 Architecture | 48 / 48 |
| P4 Planning | 54 / 54 |

- Tool calls: 4575; evidence ids cited: 2361; LLM findings: 1373; repair rounds: 18; failovers: 1
- Tokens: {'input': 25424131, 'output': 931704, 'reasoning': 52881}

## Release gates

Assurance is per released item: model items that were neither entailed by the claim-support verifier nor tool-measured were confirmed by the approving reviewer (scripted here).

| phase | app | phase status | decision | assurance (before review) | confirmed by review |
|---|---|---|---|---|---|
| P1 | spring-framework-petclinic | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 20 · entailed 98 · unverified 118 | 118 |
| P1 | eshop-modernizing | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 20 · entailed 110 · unverified 118 | 118 |
| P1 | cargotracker | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 20 · entailed 147 · unverified 90 | 90 |
| P1 | jhipster-sample-app | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 114 · unverified 107 | 107 |
| P1 | saleor | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 107 · unverified 127 | 127 |
| P1 | djangoproject | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 114 · unverified 137 | 137 |
| P1 | angular-phonecat | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 102 · unverified 88 | 88 |
| P1 | human-essentials | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 136 · unverified 103 | 103 |
| P1 | opencart | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 18 · entailed 105 · unverified 110 | 110 |
| P1 | gitea | COMPLETED | READY_FOR_PORTFOLIO_DECISION | tool-measured 19 · entailed 94 · unverified 137 | 137 |
| P2 | PF1 | COMPLETED | AUTHORIZED | tool-measured 7 · entailed 9 · unverified 116 | 116 |
| P3 | eshop-modernizing | NOT_ADMITTED | — | — | 0 |
| P4 | eshop-modernizing | NOT_ADMITTED | — | — | 0 |
| P3 | spring-framework-petclinic | NOT_ADMITTED | — | — | 0 |
| P4 | spring-framework-petclinic | NOT_ADMITTED | — | — | 0 |
| P3 | cargotracker | NOT_ADMITTED | — | — | 0 |
| P4 | cargotracker | NOT_ADMITTED | — | — | 0 |
| P3 | angular-phonecat | NOT_ADMITTED | — | — | 0 |
| P4 | angular-phonecat | NOT_ADMITTED | — | — | 0 |
| P3 | opencart | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 23 · unverified 185 | 185 |
| P3 | saleor | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 25 · unverified 192 | 192 |
| P3 | human-essentials | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 25 · unverified 187 | 187 |
| P3 | djangoproject | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 14 · unverified 205 | 205 |
| P3 | jhipster-sample-app | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 19 · unverified 185 | 185 |
| P4 | jhipster-sample-app | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 14 · unverified 75 | 75 |
| P4 | opencart | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 17 · unverified 85 | 85 |
| P4 | djangoproject | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 14 · unverified 92 | 92 |
| P4 | human-essentials | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 21 · unverified 90 | 90 |
| P3 | gitea | COMPLETED | CONDITIONAL_PLANNING | tool-measured 8 · entailed 27 · unverified 183 | 183 |
| P4 | saleor | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 22 · unverified 83 | 83 |
| P4 | gitea | COMPLETED | SCOPED_PREPARATION | tool-measured 9 · entailed 16 · unverified 100 | 100 |

Reviews: 23 (decided by `scripted-reviewer`); stakeholder questions: 71 (71 answered).

## Per-agent results

| agent | app | status | enriched | tier | turns | repairs | tools | cited | ok | reason |
|---|---|---|---|---|---|---|---|---|---|---|
| P1.A1 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 39 | 16 | ✅ |  |
| P1.A2 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 37 | 25 | ✅ |  |
| P1.A3 | eshop-modernizing | PARTIAL | yes | reasoning | 8 | 0 | 34 | 11 | ✅ |  |
| P1.A4 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 16 | 10 | ✅ |  |
| P1.A5 | eshop-modernizing | PARTIAL | yes | fast | 7 | 0 | 11 | 6 | ✅ |  |
| P1.A6 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 24 | 12 | ✅ |  |
| P1.A7 | eshop-modernizing | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P1.A8 | eshop-modernizing | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | eshop-modernizing | PARTIAL | yes | reasoning | 7 | 0 | 22 | 9 | ✅ |  |
| P1.A10 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | eshop-modernizing | PARTIAL | yes | reasoning | 6 | 0 | 24 | 12 | ✅ |  |
| P1.A1 | spring-framework-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 37 | 15 | ✅ |  |
| P1.A2 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 25 | 21 | ✅ |  |
| P1.A3 | spring-framework-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 31 | 16 | ✅ |  |
| P1.A4 | spring-framework-petclinic | PARTIAL | yes | fast | 6 | 0 | 7 | 5 | ✅ |  |
| P1.A5 | spring-framework-petclinic | PARTIAL | yes | fast | 7 | 1 | 8 | 4 | ✅ |  |
| P1.A6 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 20 | 14 | ✅ |  |
| P1.A7 | spring-framework-petclinic | PARTIAL | yes | fast | 7 | 1 | 6 | 3 | ✅ |  |
| P1.A8 | spring-framework-petclinic | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | spring-framework-petclinic | PARTIAL | yes | reasoning | 5 | 0 | 27 | 14 | ✅ |  |
| P1.A10 | spring-framework-petclinic | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | spring-framework-petclinic | PARTIAL | yes | reasoning | 7 | 0 | 20 | 13 | ✅ |  |
| P1.A1 | cargotracker | PARTIAL | yes | reasoning | 8 | 0 | 44 | 21 | ✅ |  |
| P1.A2 | cargotracker | PARTIAL | yes | reasoning | 7 | 0 | 34 | 26 | ✅ |  |
| P1.A3 | cargotracker | PARTIAL | yes | reasoning | 9 | 0 | 43 | 20 | ✅ |  |
| P1.A4 | cargotracker | PARTIAL | yes | fast | 7 | 0 | 12 | 6 | ✅ |  |
| P1.A5 | cargotracker | SKIPPED_APPROVED | yes | fast | 6 | 0 | 9 | 7 | ✅ |  |
| P1.A6 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 26 | 17 | ✅ |  |
| P1.A7 | cargotracker | SKIPPED_APPROVED | yes | fast | 7 | 1 | 7 | 2 | ✅ |  |
| P1.A8 | cargotracker | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 31 | 14 | ✅ |  |
| P1.A10 | cargotracker | PARTIAL | yes | reasoning | 6 | 0 | 19 | 13 | ✅ |  |
| P1.A11 | cargotracker | PARTIAL | yes | reasoning | 8 | 0 | 37 | 13 | ✅ |  |
| P1.A1 | jhipster-sample-app | PARTIAL | yes | reasoning | 8 | 0 | 45 | 22 | ✅ |  |
| P1.A2 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 27 | 16 | ✅ |  |
| P1.A3 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 26 | 12 | ✅ |  |
| P1.A4 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 6 | 4 | ✅ |  |
| P1.A5 | jhipster-sample-app | PARTIAL | yes | fast | 7 | 0 | 11 | 9 | ✅ |  |
| P1.A6 | jhipster-sample-app | PARTIAL | yes | reasoning | 5 | 0 | 29 | 12 | ✅ |  |
| P1.A7 | jhipster-sample-app | PARTIAL | yes | fast | 6 | 0 | 5 | 2 | ✅ |  |
| P1.A8 | jhipster-sample-app | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 34 | 12 | ✅ |  |
| P1.A10 | jhipster-sample-app | PARTIAL | yes | reasoning | 5 | 0 | 17 | 11 | ✅ |  |
| P1.A11 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 17 | 10 | ✅ |  |
| P1.A1 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 43 | 26 | ✅ |  |
| P1.A2 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 25 | 17 | ✅ |  |
| P1.A3 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 36 | 16 | ✅ |  |
| P1.A4 | saleor | PARTIAL | yes | fast | 6 | 0 | 14 | 13 | ✅ |  |
| P1.A5 | saleor | PARTIAL | yes | fast | 6 | 0 | 9 | 4 | ✅ |  |
| P1.A6 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 41 | 18 | ✅ |  |
| P1.A7 | saleor | PARTIAL | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P1.A8 | saleor | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 31 | 13 | ✅ |  |
| P1.A10 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 23 | 14 | ✅ |  |
| P1.A11 | saleor | PARTIAL | yes | reasoning | 7 | 0 | 25 | 12 | ✅ |  |
| P1.A1 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 42 | 16 | ✅ |  |
| P1.A2 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 25 | 18 | ✅ |  |
| P1.A3 | djangoproject | PARTIAL | yes | reasoning | 8 | 0 | 44 | 15 | ✅ |  |
| P1.A4 | djangoproject | PARTIAL | yes | fast | 7 | 0 | 8 | 8 | ✅ |  |
| P1.A5 | djangoproject | PARTIAL | yes | fast | 7 | 0 | 9 | 6 | ✅ |  |
| P1.A6 | djangoproject | PARTIAL | yes | reasoning | 5 | 0 | 23 | 16 | ✅ |  |
| P1.A7 | djangoproject | PARTIAL | yes | fast | 7 | 0 | 9 | 2 | ✅ |  |
| P1.A8 | djangoproject | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 30 | 16 | ✅ |  |
| P1.A10 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 18 | 11 | ✅ |  |
| P1.A11 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 21 | 13 | ✅ |  |
| P1.A1 | angular-phonecat | PARTIAL | yes | reasoning | 6 | 0 | 38 | 21 | ✅ |  |
| P1.A2 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 21 | 14 | ✅ |  |
| P1.A3 | angular-phonecat | PARTIAL | yes | reasoning | 6 | 0 | 22 | 12 | ✅ |  |
| P1.A4 | angular-phonecat | PARTIAL | yes | fast | 6 | 0 | 8 | 4 | ✅ |  |
| P1.A5 | angular-phonecat | PARTIAL | yes | fast | 7 | 0 | 10 | 4 | ✅ |  |
| P1.A6 | angular-phonecat | PARTIAL | yes | reasoning | 5 | 0 | 19 | 15 | ✅ |  |
| P1.A7 | angular-phonecat | PARTIAL | yes | fast | 6 | 0 | 5 | 3 | ✅ |  |
| P1.A8 | angular-phonecat | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | angular-phonecat | PARTIAL | yes | reasoning | 4 | 0 | 17 | 13 | ✅ |  |
| P1.A10 | angular-phonecat | PARTIAL | yes | reasoning | 6 | 0 | 19 | 11 | ✅ |  |
| P1.A11 | angular-phonecat | PARTIAL | yes | reasoning | 4 | 0 | 13 | 10 | ✅ |  |
| P1.A1 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 50 | 22 | ✅ |  |
| P1.A2 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 31 | 18 | ✅ |  |
| P1.A3 | opencart | PARTIAL | yes | reasoning | 9 | 0 | 41 | 21 | ✅ |  |
| P1.A4 | opencart | PARTIAL | yes | fast | 6 | 0 | 10 | 8 | ✅ |  |
| P1.A5 | opencart | PARTIAL | yes | fast | 8 | 1 | 8 | 2 | ✅ |  |
| P1.A6 | opencart | PARTIAL | yes | reasoning | 4 | 0 | 20 | 17 | ✅ |  |
| P1.A7 | opencart | PARTIAL | yes | fast | 6 | 0 | 5 | 1 | ✅ |  |
| P1.A8 | opencart | PARTIAL | yes | reasoning | 2 | 0 | 3 | 4 | ✅ |  |
| P1.A9 | opencart | PARTIAL | yes | reasoning | 7 | 0 | 22 | 8 | ✅ |  |
| P1.A10 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 19 | 14 | ✅ |  |
| P1.A11 | opencart | PARTIAL | yes | reasoning | 7 | 0 | 27 | 10 | ✅ |  |
| P1.A1 | human-essentials | PARTIAL | yes | reasoning | 8 | 0 | 53 | 24 | ✅ |  |
| P1.A2 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 30 | 21 | ✅ |  |
| P1.A3 | human-essentials | PARTIAL | yes | reasoning | 8 | 0 | 36 | 19 | ✅ |  |
| P1.A4 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 19 | 19 | ✅ |  |
| P1.A5 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P1.A6 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 33 | 27 | ✅ |  |
| P1.A7 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P1.A8 | human-essentials | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | human-essentials | PARTIAL | yes | reasoning | 11 | 2 | 36 | 7 | ✅ |  |
| P1.A10 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 21 | 16 | ✅ |  |
| P1.A11 | human-essentials | PARTIAL | yes | reasoning | 9 | 0 | 37 | 10 | ✅ |  |
| P1.A1 | gitea | PARTIAL | yes | reasoning | 8 | 0 | 45 | 24 | ✅ |  |
| P1.A2 | gitea | PARTIAL | yes | reasoning | 6 | 0 | 26 | 16 | ✅ |  |
| P1.A3 | gitea | PARTIAL | yes | reasoning | 9 | 0 | 53 | 19 | ✅ |  |
| P1.A4 | gitea | PARTIAL | yes | fast | 7 | 0 | 10 | 7 | ✅ |  |
| P1.A5 | gitea | PARTIAL | yes | fast | 8 | 1 | 9 | 6 | ✅ |  |
| P1.A6 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 33 | 15 | ✅ |  |
| P1.A7 | gitea | PARTIAL | yes | fast | 7 | 0 | 6 | 1 | ✅ |  |
| P1.A8 | gitea | PARTIAL | yes | reasoning | 2 | 0 | 3 | 3 | ✅ |  |
| P1.A9 | gitea | PARTIAL | yes | reasoning | 8 | 0 | 31 | 10 | ✅ |  |
| P1.A10 | gitea | PARTIAL | yes | reasoning | 6 | 0 | 20 | 11 | ✅ |  |
| P1.A11 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 27 | 15 | ✅ |  |
| P2.A1 | PF1 | PARTIAL | yes | reasoning | 10 | 0 | 37 | 18 | ✅ |  |
| P2.A2 | PF1 | PARTIAL | yes | reasoning | 7 | 0 | 34 | 22 | ✅ |  |
| P2.A3 | PF1 | COMPLETE | yes | fast | 7 | 1 | 8 | 2 | ✅ |  |
| P2.A4 | PF1 | COMPLETE | yes | fast | 7 | 1 | 10 | 3 | ✅ |  |
| P2.A5 | PF1 | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P2.A6 | PF1 | PARTIAL | yes | reasoning | 10 | 0 | 72 | 29 | ✅ |  |
| P2.A7 | PF1 | PARTIAL | yes | reasoning | 5 | 0 | 25 | 19 | ✅ |  |
| P3.A1 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P3.A2 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P3.A3 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P3.A4 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P3.A5 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P3.A6 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P3.A7 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P3.A8 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
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
| P3.A1 | jhipster-sample-app | PARTIAL | yes | reasoning | 8 | 0 | 61 | 25 | ✅ |  |
| P3.A2 | jhipster-sample-app | PARTIAL | yes | reasoning | 7 | 0 | 32 | 18 | ✅ |  |
| P3.A3 | jhipster-sample-app | PARTIAL | yes | reasoning | 5 | 0 | 22 | 17 | ✅ |  |
| P3.A4 | jhipster-sample-app | PARTIAL | yes | reasoning | 5 | 0 | 18 | 15 | ✅ |  |
| P3.A5 | jhipster-sample-app | SKIPPED_APPROVED | yes | fast | 6 | 0 | 9 | 5 | ✅ |  |
| P3.A6 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 30 | 23 | ✅ |  |
| P3.A7 | jhipster-sample-app | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P3.A8 | jhipster-sample-app | PARTIAL | yes | reasoning | 6 | 0 | 26 | 14 | ✅ |  |
| P3.A1 | saleor | PARTIAL | yes | reasoning | 10 | 0 | 63 | 22 | ✅ |  |
| P3.A2 | saleor | PARTIAL | yes | reasoning | 10 | 0 | 36 | 17 | ✅ |  |
| P3.A3 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 27 | 16 | ✅ |  |
| P3.A4 | saleor | PARTIAL | yes | reasoning | 8 | 0 | 30 | 17 | ✅ |  |
| P3.A5 | saleor | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 5 | ✅ |  |
| P3.A6 | saleor | PARTIAL | yes | reasoning | 9 | 0 | 52 | 29 | ✅ |  |
| P3.A7 | saleor | COMPLETE | yes | fast | 6 | 0 | 12 | 4 | ✅ |  |
| P3.A8 | saleor | PARTIAL | yes | reasoning | 5 | 0 | 20 | 11 | ✅ |  |
| P3.A1 | djangoproject | PARTIAL | yes | reasoning | 10 | 0 | 54 | 26 | ✅ |  |
| P3.A2 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 24 | 15 | ✅ |  |
| P3.A3 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 30 | 17 | ✅ |  |
| P3.A4 | djangoproject | PARTIAL | yes | reasoning | 7 | 0 | 28 | 20 | ✅ |  |
| P3.A5 | djangoproject | SKIPPED_APPROVED | yes | fast | 6 | 0 | 7 | 3 | ✅ |  |
| P3.A6 | djangoproject | PARTIAL | yes | reasoning | 9 | 0 | 42 | 17 | ✅ |  |
| P3.A7 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 16 | 1 | ✅ |  |
| P3.A8 | djangoproject | PARTIAL | yes | reasoning | 6 | 0 | 36 | 16 | ✅ |  |
| P3.A1 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A2 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A3 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A4 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A5 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A6 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A7 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A8 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P3.A1 | opencart | PARTIAL | yes | reasoning | 10 | 0 | 64 | 30 | ✅ |  |
| P3.A2 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 32 | 15 | ✅ |  |
| P3.A3 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 27 | 15 | ✅ |  |
| P3.A4 | opencart | PARTIAL | yes | reasoning | 6 | 0 | 24 | 17 | ✅ |  |
| P3.A5 | opencart | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P3.A6 | opencart | PARTIAL | yes | reasoning | 8 | 0 | 39 | 25 | ✅ |  |
| P3.A7 | opencart | COMPLETE | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P3.A8 | opencart | PARTIAL | yes | reasoning | 7 | 0 | 34 | 14 | ✅ |  |
| P3.A1 | human-essentials | PARTIAL | yes | reasoning | 9 | 0 | 57 | 29 | ✅ |  |
| P3.A2 | human-essentials | PARTIAL | yes | reasoning | 8 | 0 | 44 | 19 | ✅ |  |
| P3.A3 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 28 | 15 | ✅ |  |
| P3.A4 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 28 | 18 | ✅ |  |
| P3.A5 | human-essentials | SKIPPED_APPROVED | yes | fast | 6 | 0 | 8 | 6 | ✅ |  |
| P3.A6 | human-essentials | PARTIAL | yes | reasoning | 7 | 0 | 38 | 25 | ✅ |  |
| P3.A7 | human-essentials | COMPLETE | yes | fast | 6 | 0 | 16 | 3 | ✅ |  |
| P3.A8 | human-essentials | PARTIAL | yes | reasoning | 5 | 0 | 26 | 18 | ✅ |  |
| P3.A1 | gitea | PARTIAL | yes | reasoning | 10 | 0 | 60 | 16 | ✅ |  |
| P3.A2 | gitea | PARTIAL | yes | reasoning | 8 | 0 | 37 | 14 | ✅ |  |
| P3.A3 | gitea | PARTIAL | yes | reasoning | 7 | 0 | 28 | 19 | ✅ |  |
| P3.A4 | gitea | PARTIAL | yes | reasoning | 8 | 0 | 31 | 16 | ✅ |  |
| P3.A5 | gitea | SKIPPED_APPROVED | yes | fast | 6 | 0 | 6 | 6 | ✅ |  |
| P3.A6 | gitea | PARTIAL | yes | reasoning | 8 | 0 | 39 | 16 | ✅ |  |
| P3.A7 | gitea | PARTIAL | yes | fast | 6 | 0 | 13 | 3 | ✅ |  |
| P3.A8 | gitea | PARTIAL | yes | reasoning | 5 | 0 | 24 | 12 | ✅ |  |
| P4.A1 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P4.A2 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P4.A3 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P4.A4 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P4.A5 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P4.A6 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P4.A7 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P4.A8 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
| P4.A9 | eshop-modernizing | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put eshop-modernizing in the IA02 non-delivery register (Retain) |
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
| P4.A1 | jhipster-sample-app | COMPLETE | yes | fast | 3 | 0 | 3 | 1 | ✅ |  |
| P4.A2 | jhipster-sample-app | COMPLETE | yes | fast | 6 | 0 | 12 | 1 | ✅ |  |
| P4.A3 | jhipster-sample-app | PARTIAL | yes | coding | 9 | 0 | 24 | 9 | ✅ |  |
| P4.A4 | jhipster-sample-app | COMPLETE | yes | fast | 5 | 0 | 12 | 6 | ✅ |  |
| P4.A5 | jhipster-sample-app | COMPLETE | yes | fast | 6 | 0 | 8 | 2 | ✅ |  |
| P4.A6 | jhipster-sample-app | PARTIAL | yes | fast | 8 | 2 | 13 | 2 | ✅ |  |
| P4.A7 | jhipster-sample-app | COMPLETE | yes | fast | 6 | 0 | 9 | 1 | ✅ |  |
| P4.A8 | jhipster-sample-app | COMPLETE | yes | fast | 6 | 0 | 20 | 1 | ✅ |  |
| P4.A9 | jhipster-sample-app | PARTIAL | yes | reasoning | 5 | 0 | 21 | 16 | ✅ |  |
| P4.A1 | saleor | COMPLETE | yes | fast | 5 | 1 | 4 | 2 | ✅ |  |
| P4.A2 | saleor | COMPLETE | yes | fast | 7 | 1 | 7 | 3 | ✅ |  |
| P4.A3 | saleor | PARTIAL | yes | coding | 8 | 0 | 16 | 12 | ✅ |  |
| P4.A4 | saleor | COMPLETE | yes | fast | 5 | 0 | 16 | 1 | ✅ |  |
| P4.A5 | saleor | PARTIAL | yes | fast | 6 | 0 | 5 | 6 | ✅ |  |
| P4.A6 | saleor | PARTIAL | yes | fast | 7 | 1 | 13 | 7 | ✅ |  |
| P4.A7 | saleor | COMPLETE | yes | fast | 6 | 0 | 12 | 2 | ✅ |  |
| P4.A8 | saleor | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A9 | saleor | PARTIAL | yes | reasoning | 6 | 0 | 24 | 15 | ✅ |  |
| P4.A1 | djangoproject | COMPLETE | yes | fast | 5 | 0 | 5 | 1 | ✅ |  |
| P4.A2 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 10 | 3 | ✅ |  |
| P4.A3 | djangoproject | COMPLETE | yes | coding | 9 | 0 | 20 | 12 | ✅ |  |
| P4.A4 | djangoproject | COMPLETE | yes | fast | 4 | 0 | 9 | 4 | ✅ |  |
| P4.A5 | djangoproject | PARTIAL | yes | fast | 6 | 0 | 9 | 3 | ✅ |  |
| P4.A6 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 10 | 8 | ✅ |  |
| P4.A7 | djangoproject | COMPLETE | yes | fast | 6 | 0 | 8 | 3 | ✅ |  |
| P4.A8 | djangoproject | COMPLETE | yes | fast | 2 | 0 | 3 | 3 | ✅ |  |
| P4.A9 | djangoproject | PARTIAL | yes | reasoning | 5 | 0 | 20 | 16 | ✅ |  |
| P4.A1 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A2 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A3 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A4 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A5 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A6 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A7 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A8 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A9 | angular-phonecat | NOT_ADMITTED | no |  |  | 0 | 0 | 0 | — | not admitted: P2 G2 put angular-phonecat in the IA02 non-delivery register (Retire) |
| P4.A1 | opencart | COMPLETE | yes | fast | 4 | 0 | 3 | 2 | ✅ |  |
| P4.A2 | opencart | COMPLETE | yes | fast | 6 | 0 | 12 | 1 | ✅ |  |
| P4.A3 | opencart | PARTIAL | yes | coding | 9 | 0 | 15 | 8 | ✅ |  |
| P4.A4 | opencart | PARTIAL | yes | fast | 2 | 0 | 5 | 6 | ✅ |  |
| P4.A5 | opencart | COMPLETE | yes | fast | 3 | 0 | 3 | 4 | ✅ |  |
| P4.A6 | opencart | COMPLETE | yes | fast | 6 | 0 | 6 | 3 | ✅ |  |
| P4.A7 | opencart | COMPLETE | yes | fast | 2 | 0 | 3 | 3 | ✅ |  |
| P4.A8 | opencart | COMPLETE | yes | fast | 2 | 0 | 3 | 4 | ✅ |  |
| P4.A9 | opencart | PARTIAL | yes | reasoning | 5 | 0 | 20 | 16 | ✅ |  |
| P4.A1 | human-essentials | COMPLETE | yes | fast | 4 | 0 | 4 | 2 | ✅ |  |
| P4.A2 | human-essentials | COMPLETE | yes | fast | 2 | 0 | 4 | 3 | ✅ |  |
| P4.A3 | human-essentials | PARTIAL | yes | coding | 7 | 0 | 23 | 8 | ✅ |  |
| P4.A4 | human-essentials | COMPLETE | yes | fast | 4 | 0 | 4 | 2 | ✅ |  |
| P4.A5 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 7 | 4 | ✅ |  |
| P4.A6 | human-essentials | PARTIAL | yes | fast | 6 | 0 | 9 | 6 | ✅ |  |
| P4.A7 | human-essentials | COMPLETE | yes | fast | 7 | 1 | 10 | 1 | ✅ |  |
| P4.A8 | human-essentials | COMPLETE | yes | fast | 7 | 1 | 25 | 1 | ✅ |  |
| P4.A9 | human-essentials | PARTIAL | yes | reasoning | 6 | 0 | 23 | 20 | ✅ |  |
| P4.A1 | gitea | COMPLETE | yes | fast | 4 | 0 | 3 | 2 | ✅ |  |
| P4.A2 | gitea | COMPLETE | yes | fast | 6 | 1 | 4 | 3 | ✅ |  |
| P4.A3 | gitea | PARTIAL | yes | coding | 7 | 0 | 23 | 11 | ✅ |  |
| P4.A4 | gitea | COMPLETE | yes | fast | 6 | 0 | 7 | 1 | ✅ |  |
| P4.A5 | gitea | COMPLETE | yes | fast | 6 | 0 | 13 | 4 | ✅ |  |
| P4.A6 | gitea | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A7 | gitea | COMPLETE | yes | fast | 6 | 0 | 9 | 2 | ✅ |  |
| P4.A8 | gitea | COMPLETE | yes | fast | 7 | 1 | 11 | 2 | ✅ |  |
| P4.A9 | gitea | PARTIAL | yes | reasoning | 6 | 0 | 21 | 15 | ✅ |  |
