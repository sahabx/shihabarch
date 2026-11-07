---
id: c2-data-platform-rls
title: "The Data-Platform Decision: Evaluating 4 Candidates, Forking Twenty, Adding Row-Level Security"
status: reviewed
client: "Discover Islam Society (Path to Peace operations)"
client_public: true
period: "2026-09 (evaluation + fork); deployed"
pillars: [data, systems]
stack: [Twenty CRM, TypeScript, PostgreSQL, Docker, Traefik, Hostinger VPS, NocoDB, Teable, Mathesar]
metrics_ids: [agents, individuals_yr, countries]
summary: "Formal requirements-driven evaluation of NocoDB / Twenty / Teable / Mathesar for a master-individual data platform with row+field-level permissions; ended in a surgical Twenty fork adding a community row-level-security engine, white-labelling and a telemetry gate — deployed as the 'Path to Peace' CRM."
---

# C2 · Data-Platform Decision + Twenty RLS Fork

## Facts
- Hard requirements (written as PROBLEM.md / REQUIREMENTS.md before any code):
  - ONE master record of every Individual — one table, one serial-number space, one source of truth.
  - Plain-SQL queryable for cross-country reporting.
  - **Row-level AND field-level permissions**: which rows each agent sees, which fields each team edits.
  - Scale: ~100 internal agents, 5 campaigns in 5 countries, ~70,000 new individuals/year, mobile-first data entry.
- Prior NocoDB attempt **failed for a documented structural reason** (free-tier permissions scope to bases/tables/views → false choice). Failure recorded, not hidden.
- Per-candidate assessment files produced (nocodb-assessment.md, teable-assessment.md, twenty evaluation) + VERDICT.md + objective.md decision record with reversed decisions and risks.
- Fork delta implemented in `twentyhq/twenty`:
  - community **row-level security** ("row rules" engine) reusing Twenty's access-policy pipeline (four same-named replacements in `engine/twenty-orm/utils/our-rls/`),
  - Settings → Row-rules admin UI,
  - telemetry gate + white-label.
- Shipped as Docker image (`shahabu/p2p-data-fork`), deployed to Hostinger VPS behind Traefik, custom domain; data migration scripts prepared separately (p2p-data-prep) so tooling never mixes with the fork repo.

## career_cut
The strongest engineering-judgment artifact in the portfolio: a real architecture decision record, a failed first attempt analyzed to root cause, four candidates evaluated against written requirements, and a minimal-risk fork strategy (same-named module replacement instead of invasive patches). Bonus: AI-agent-assisted development with journal-first workflow and token-budgeted task lists.

## business_cut
"What you get": instead of fighting an off-the-shelf tool's permission model (or paying enterprise-tier fees), you get a permissively-licensed platform surgically extended to your exact access rules — and a decision record that shows your board/auditors exactly why. Applicable beyond CRM: any 'we outgrew spreadsheets but SaaS permissions don't fit our org' problem.

## Open items
- [VERIFY] whether the RLS patch can be open-sourced as a standalone repo/PR (strongest possible proof).
- [VERIFY] the ~100 agents / ~70k individuals figures for public use.
