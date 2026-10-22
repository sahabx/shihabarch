# ROADMAP — shihabarch.tech + Abqariyyah groundwork

Principle: **static site + data contracts + self-hosted services.** The site stays a
static build as long as possible; every future feature is a service on the VPS behind
an endpoint. No rewrite ever needed — the contracts are the groundwork.

## Phase 0 — v0.1 live (this week)
- [x] Content scaffolded, headline chosen, contact email in
- [ ] Human pass on `[VERIFY]` items + DIS approvals (metrics, testimonial, screenshots)
- [ ] Flip case studies `draft` → `reviewed` as verified
- [ ] Deploy `site/` to Hostinger (zip → public_html). Test: `/llms.txt`, `/data/profile.json`, `.md` twins all serve with correct MIME
- [ ] Generate QR (`qr/README.md`) → add to CV PDF
- Exit criteria: a recruiter can scan the CV and land on a real site.

## Phase 1 — data contracts complete (v0.2)
The groundwork for *any* future full-stack feature is: every fact exists as JSON.
- [ ] build.py also emits `/data/case-studies.json` (frontmatter index: id, title, period, pillars, stack, metrics)
- [ ] build.py emits `/data/metrics.json` (subset of profile.json) — dashboards/resume tools can consume it
- [ ] `sitemap.xml` generation in build.py
- [ ] Self-hosted analytics: **Umami** (or Plausible) in Docker on VPS — on-brand (no Google), 1 script tag
- Exit criteria: an AI or a script can reconstruct the whole portfolio from `/data/*` without scraping HTML.

## Phase 2 — first services (v0.3, the "full-stack" starts here)
Each service = one Docker container on the VPS behind Traefik, exposed at shihabarch.tech/*:
- [ ] `/ask` chat: **Dify** chatflow (already operated in Jul 2026), KB = `site/*.md` + `/data/*.json`; embed replaces ask.html placeholder; log scans via `?src=cv-qr`
- [ ] `/api/ask`: OpenAI-compatible thin wrapper over the same Dify app (stretch — big differentiator for AI-savvy visitors)
- [ ] Contact form → **n8n** webhook (already in stack) → email + NocoDB row. Static form, dynamic backend, zero site rewrite.
- [ ] Booking: **Cal.com self-hosted** at `/book` — becomes the Abqariyyah consultation funnel too
- Exit criteria: chat, form, and booking work while the site itself is still static files.

## Phase 3 — Abqariyyah site (parallel track, reuses everything)
- [ ] Buy domain (`.com` primary; `.bh` if WLL path chosen)
- [ ] New repo `abqariyyah/` — SAME pipeline: `content/` → build → `site/`; case studies render their `business_cut` sections (build.py flag: `--cut=business`)
- [ ] Pages: offer, 4 pillars, packages (project/consultancy/maintenance), proof (DIS named), process, `/book` (same Cal.com)
- [ ] Legal: freelance permit vs WLL decision → footer CR/permit number
- [ ] Billing when first client signs: **Invoice Ninja** self-hosted (or PayPal-only per phase-1 research if foreign clients)
- Exit criteria: one content source feeds two brands with two cuts.

## Phase 4 — real full-stack (only when a feature demands it)
Triggers, not dates:
- Client portal (status of engagements, report access) → auth needed → evaluate **Twenty fork** (you built RLS into it — clients as rows!) or Authentik + a small Next.js app
- Products (teaching platform, if un-parked) → Stripe constraint → revisit phase-1 research (Singapore/UAE entity)
- If the site itself ever needs SSR/DB → migrate `content/` into **Astro** (static-first, islands, API routes) — content pipeline ports 1:1 because everything is already markdown+JSON
Rule: never adopt a framework before a trigger exists.

## What "groundwork" means concretely today
1. Canonical data in `content/profile.json` (done)
2. Markdown-with-frontmatter case studies carrying both cuts (done)
3. Build script that can retarget (career/business cut) — small `--cut` flag to add in Phase 3
4. VPS + Traefik + Docker muscle memory (already have)
5. QR → `/ask?src=cv-qr` tracking from day one (Phase 0)
