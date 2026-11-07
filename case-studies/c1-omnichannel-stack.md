---
id: c1-omnichannel-stack
title: "Self-Hosted Omnichannel Stack for Multi-Country Outreach"
status: reviewed
client: "Discover Islam Society"
client_public: true
period: "2024-11 → present"
pillars: [systems, ai-adoption, workflow]
stack: [Chatwoot, NocoDB, Grafana, n8n, Botpress, Dify, PostgreSQL, Docker, Bash, Hostinger VPS, Contabo, DigitalOcean, Facebook Marketing API, TikTok Business API, Eazypay]
metrics_ids: [conversations, contacts, reach, countries, promotions, downtime]
summary: "Replaced third-party SaaS with a fully self-hosted omnichannel communication + CRM + analytics + automation ecosystem serving local agents, offshore agents, and management across 20+ countries."
---

# C1 · Self-Hosted Omnichannel Stack

## Facts
- Single-handedly architected and deployed Chatwoot + NocoDB + Grafana + n8n + Botpress (later Dify) across Hostinger, Contabo and DigitalOcean VPS.
- Full lifecycle ownership: Bash scripting, YAML config, Docker orchestration, PostgreSQL administration, Rails console maintenance (Chatwoot is Ruby on Rails).
- Secured **Facebook approval for a custom application** — the organization receives, processes and serves Messenger conversations from its own systems (bypasses platform lock-in).
- **TikTok Business API integration** with the self-hosted Chatwoot for unified multi-platform engagement (developer registration, webhooks, channel plugin work, Jul 2026).
- Mobile-first web portal for call-center agents (CCA App) with bidirectional sync to the omnichannel platform — including a preserved failed first attempt (`Failed CCA App`) and a working rebuild.
- Corporate website built **in one day**, later integrated with **Eazypay** payment gateway; enabled a landmark high-value donation transaction.
- AI layer: automated responses, conversation classification, insight surfacing across the stack (Dify auto-reply bot, Botpress flows).

## career_cut
The story of ownership: no dev team, no SaaS budget — one person taking a multi-team, multi-country operation from third-party dependence to a sovereign stack. Highlights: the Facebook custom-app approval process (platform compliance + engineering), bare-metal Rails maintenance, and the crisis-recovery design (see C4). Engineering-judgment artifacts: deployment runbooks, journal-first decision logs.

## business_cut
"What you get": a communication + CRM backbone your organization owns — no per-seat fees, no vendor kill-switch, data stays on infrastructure you control. Proven at: 525,301 conversations, 44,542 contacts, 20+ countries, ~800k monthly reach. Reference: Discover Islam Society (nameable).

## Open items
- Screenshots to capture (see `site/assets/screenshots/README.md`): Chatwoot inbox, n8n workflow canvas, custom agent app. Grafana currently down — capture when restored.
- Resolved 2026-10-22: campaign numbers are my own work/pitch — no permission needed. ~~DIS testimonial~~ — not pursuing.
