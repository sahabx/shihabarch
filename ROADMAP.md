# ROADMAP — shihabarch.tech + Abqariyyah groundwork

Principle: **static site + data contracts + self-hosted services.** The site stays a
static build as long as possible; every future feature is a service on the VPS behind
an endpoint. No rewrite ever needed — the contracts are the groundwork.

## Phase 0 — v0.1 live (this week)
- [x] Content scaffolded, headline chosen, contact email in
- [x] Human pass on `[VERIFY]` items + DIS approvals (done 2026-10-22 — no testimonial; DIS named only as referenceable)
- [x] Flip case studies `draft` → `reviewed` as verified
- [ ] Upload `dist/shihabarch-site.zip` to Hostinger public_html. Test: `/llms.txt`, `/data/profile.json`, `.md` twins all serve with correct MIME
- [x] Generate QR (`qr/`) → add to CV PDF (PNG/SVG generated; placing on the PDF is manual)
- Exit criteria: a recruiter can scan the CV and land on a real site. ✅ (pending upload only)

## Phase 1 — data contracts complete (v0.2)
The groundwork for *any* future full-stack feature is: every fact exists as JSON.
- [ ] build.py also emits `/data/case-studies.json` (frontmatter index: id, title, period, pillars, stack, metrics)
- [ ] build.py emits `/data/metrics.json` (subset of profile.json) — dashboards/resume tools can consume it
- [ ] `sitemap.xml` generation in build.py
- [ ] Self-hosted analytics: **Umami** (or Plausible) in Docker on VPS — on-brand (no Google), 1 script tag
- Exit criteria: an AI or a script can reconstruct the whole portfolio from `/data/*` without scraping HTML.

## Phase 2 — first services (v0.3, the "full-stack" starts here)
Each service = one Docker container on the VPS behind Traefik, exposed at shihabarch.tech/*:
- [x] `/ask` chat — **DONE 2026-11-07, simpler than planned**: instead of a separate Dify chatflow,
  the Abqariyyah Next.js app serves `POST /api/chat` (grounded RAG, BM25 retrieval + OpenAI-compatible
  LLM, DeepSeek default). ask.html calls it cross-origin (CORS_ORIGINS). Local in-browser retrieval
  fallback means the page is never broken. Dify can still replace it later — the endpoint contract
  (`POST {question, site, source} → {answer, sources[]}`) stays the same.
- [x] Chat logging — `chat_log` table in Abqariyyah's SQLite (`site`, `question`, `answer`, `source` incl. cv-qr scans)
- [ ] Set `CHAT_API_URL` in site/ask.html once the Abqariyyah domain resolves → re-zip & re-upload
- [ ] Contact form → n8n webhook or Abqariyyah `/api/contact` (NOTIFY_URL) — optional, email already works
- [ ] Booking: Cal.com self-hosted at `/book` — becomes the Abqariyyah consultation funnel too
- Exit criteria: chat, form, and booking work while the site itself is still static files. (chat ✅)

## Phase 3 — Abqariyyah site (parallel track, reuses everything)
- [x] **DONE 2026-11-07 — rebuilt as a full-stack Next.js app** (per explicit decision: business site =
  full-stack foundation for future features). See `../abqariyyah/`: App Router pages, SQLite + migrations,
  `/api/chat` (serves both sites), `/api/contact` (leads table + optional n8n webhook), `/api/health`,
  Dockerfile (standalone) + docker-compose with Traefik labels. Case studies still edited HERE and synced
  via `npm run sync` (content/shared).
- [ ] Buy domain → update `content/business.json` → brand.domain + Traefik Host rule → deploy
- [ ] Legal: freelance permit vs WLL decision → footer CR/permit number (brand.legal.cr_number)
- [ ] Billing when first client signs: **Invoice Ninja** self-hosted (or PayPal-only per phase-1 research if foreign clients)
- Exit criteria: one content source feeds two brands with two cuts. ✅ (deployment pending domain)

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
