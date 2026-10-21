---
id: c3-nmc-pipeline
title: "NMC-first: WhatsApp → Postgres Ingest Pipeline with Tailscale-Only Exposure"
status: draft
client: "Discover Islam Society (New Muslim Care)"
client_public: true
period: "2026-08 → present"
pillars: [data, systems, workflow]
stack: [WhatsApp linked-device (Baileys-class library), PostgreSQL, Docker, Tailscale, Google Sheets API, Node.js]
metrics_ids: []
summary: "Production realtime pipeline: WhatsApp group messages ingested via a legitimate linked device into Postgres, reachable only over a Tailscale network, with passive-ingest guardrails, versioned deployments and two-way Google Sheets sync for non-technical staff."
---

# C3 · NMC-first Pipeline (WhatsApp → Postgres)

## Facts
- QR-code linked-device login; realtime message capture for new-Muslim care operations.
- **Security posture by design**: Postgres never exposed to the public internet — reachable only via Tailscale; team + reporting scripts connect with a **read-only role**.
- **Compliance guardrails baked in** (documented in DEPLOY.md): read-only ingest (never sends messages), WhatsApp history sync disabled, passive presence (no online broadcast), exponential reconnect backoff, single bulk group sync + lazy metadata — explicitly *not* scraping; behaves as a normal WhatsApp Web linked device.
- Operational maturity: versioned deployments with SQL backups at each milestone (`backup_pre_webhook_*.sql`), JOURNAL.md decision log, DEPLOY.md / WEBHOOKS.md runbooks.
- Google Sheets synchronization layer so non-technical staff keep their existing interface while Postgres becomes the source of truth; sync debugging + full-system documentation (Oct 2026).
- 27 commits Aug 18 → Oct 14, 2026; still in active development.

## career_cut
Shows production discipline most portfolio projects lack: threat-model thinking (why Tailscale-only), platform-ToS-aware design (the guardrail list), backup-before-change habit, and documentation as a first-class deliverable. Also demonstrates explaining a full system's flow/logic/mapping to non-technical stakeholders.

## business_cut
"What you get": your team's chat-based field data (WhatsApp groups, DMs) turned into a queryable database — without exposing anything to the internet, without violating platform rules, and without retraining staff (they keep using Sheets/WhatsApp; you get Postgres + dashboards). Ideal for NGOs, field teams, community operations.

## Open items
- [VERIFY] publishable architecture diagram (the visualize-workflow pi session prototyped one).
- [ ] Add message-volume metric if DIS approves.
