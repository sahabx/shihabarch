---
id: c4-cost-sovereignty
title: "Cost & Sovereignty Audit: 8,000 BHD Saved, $3k/yr SaaS Eliminated, Zero Extended Downtime in a Platform Crisis"
status: draft
client: "Discover Islam Society"
client_public: true
period: "2024-11 → present"
pillars: [systems, workflow]
stack: [open-source replacement strategy, multi-VPS diversification, backups/DR]
metrics_ids: [saved_bhd, saved_usd_yr, downtime]
summary: "Transition from proprietary systems and SaaS subscriptions to a self-hosted open-source stack, plus a big-tech diversification strategy that kept operations running when Facebook blocked management credentials."
---

# C4 · Cost & Sovereignty

## Facts
- **Saved 8,000 BHD** (one-time) by transitioning from proprietary systems to open-source self-hosted solutions.
- **Eliminated ~$3,000 USD/year** in recurring SaaS subscriptions by consolidating tools under the self-hosted stack.
- **Big-tech diversification strategy**: removed critical single points of failure across platforms/providers (multiple VPS vendors — Hostinger, Contabo, DigitalOcean; self-controlled message processing via approved Facebook custom app).
- **Crisis proof**: when Facebook unexpectedly blocked management account credentials, operations were revived swiftly with **zero extended downtime** — because message processing ran through owned infrastructure.
- Backup & disaster-recovery design done explicitly (bare-metal vs Docker trade-off analysis, migration paths, Chatwoot DR plan, Apr 2026).
- Payment independence: Eazypay gateway integrated on owned website (landmark donation transaction).

## career_cut
CFO-language case study: quantified savings, risk framing (single points of failure), and a real incident where the architecture paid for itself. Complements the technical cases by showing business judgment — the reason for three promotions in under two years.

## business_cut
"What you get": an audit + migration plan that converts your SaaS spend into owned infrastructure — with the savings quantified before you commit, and a resilience story you can repeat to your board: when the platform locked the doors, this organization kept operating.

## Open items
- [VERIFY] the 8,000 BHD figure's breakdown for public use (what was replaced, over what horizon).
- [ ] Write the incident timeline (Facebook block → recovery) as a standalone 1-page story.
