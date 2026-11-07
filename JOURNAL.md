# JOURNAL — shihabarch content repo

Decision/context log for this repo. Update on every meaningful change.

## 2026-11-07 (2) · Design v2 — the site no longer looks like a text file
- **Context**: site went live (GitHub Pages, custom domain shihabarch.tech). First look:
  "very bad for a portfolio site… basic and read-heavy, doesn't catch user attention". Fair —
  v1 was a default-font text wall.
- **Design v2** (same content pipeline, same .md twins, same data contracts — only presentation changed):
  - Self-hosted **Space Grotesk + Inter** (variable woff2, latin, 70KB total — no Google Fonts
    tracking, on-brand for sovereignty). Favicon added (SVG monogram).
  - **Hero**: eyebrow (role · Bahrain), huge name w/ gradient, headline sub, language chips,
    gradient CTA buttons, live "Running in production" stack card, slow stack **marquee**.
  - **Stats band**: 6 big gradient numbers with **count-up animation** (525,301 conversations,
  8,000 BHD saved, …).
  - **Career timeline** (roles as vertical timeline with dots), case-study cards with pillar
    tags (color-coded: AI violet / Data sky / Workflow emerald / Systems amber), headline
    metric per card, hover lift.
  - Case-study pages: header + **sticky sidebar** (client, period, pillars, stack pills, numbers).
  - Scroll **reveal animations** (IntersectionObserver, fail-safe: only active when JS runs
    — no-JS visitors see everything). prefers-reduced-motion respected.
  - ask.html restyled to match (gradient-border chat panel, chip suggestions).
- build.py templates rewritten (page shell, index, case-study detail+index, prose pages);
  SHORT_LABELS map added for terse stat labels (long labels stay in profile.json).
- Verified: fonts/CSS/JS/favicon serve 200, reveal + count-up fire in headless Chromium
  (viewport-dependent), business_cut still stripped from HTML, .md twins intact.
- Deployed via scripts/deploy-ghpages.sh --push.

## 2026-11-07 · /ask chat is real; QR generated; deploy zip ready — Phase 0+2 chat DONE
- **Context**: "finish both sites asap" session. AI Q&A was the main gap on this site.
- **Decisions**:
  - `/ask` is now a real chat page (hand-maintained `site/ask.html`), two layers:
    1. **Remote LLM** (preferred): `CHAT_API_URL` const at top of the script — points at the
       Abqariyyah full-stack app's `POST /api/chat` with `site=shihabarch` (grounded RAG,
       OpenAI-compatible, DeepSeek default). Set the URL when the Abqariyyah app is deployed
       and the domain bought. `?src=cv-qr` scan tracking is passed through and logged there.
    2. **Local retrieval** (always works, zero backend): the page fetches its own `.md` twins +
       `/data/*.json`, chunks them, scores with BM25-lite in the browser, answers with the best
       chunk + source links. No keys, no third parties — the site works TODAY.
  - QR generated: `qr/cv-qr.png|svg|black.png` → `https://shihabarch.tech/ask?src=cv-qr`.
  - Deploy package: `dist/shihabarch-site.zip` (34 files) — upload to Hostinger public_html.
  - Local retrieval verified against 5 test questions (headline, savings, omnichannel, process, languages).
- **Remaining (human only)**: upload zip to Hostinger, verify /llms.txt + /data/profile.json MIME,
  put QR on CV PDF, later set CHAT_API_URL in ask.html when Abqariyyah domain is live.

## 2026-10-22 · Headline chosen, contact added, Phase-1 data contracts implemented
- Mohammad set `headline_chosen` (fixed JSON quoting — value was unquoted) and added
  contact email; removed LinkedIn placeholder (decision: no LinkedIn for now).
- about.md contact block updated with email.
- **Full-stack strategy decided** (see ROADMAP.md): static site + data contracts +
  self-hosted services behind endpoints. No framework until a Phase-4 trigger exists.
- build.py now also emits Phase-1 contracts: `/data/case-studies.json` (6 entries),
  `/data/metrics.json` (10 entries), `sitemap.xml` (12 urls); llms.txt references the
  JSON endpoints.
- Next: [VERIFY] pass + DIS approvals → flip statuses → deploy to Hostinger → QR.

## 2026-10-21 · Repo scaffolded
- **Context**: Portfolio brainstorm (`~/Folder/portfolio/BRAINSTORM.md`) settled:
  personal/career site = shihabarch.tech (domain owned, parked on Hostinger DNS);
  business = Abqariyyah (name chosen, domain TBD); fully separate domains;
  DIS nameable as reference; solo; pricing = project/consultancy/maintenance.
- **Decisions made here**:
  - Single-source-of-truth pipeline: `content/` → `scripts/build.py` → `site/`.
  - "Write once, publish twice": each case study carries `career_cut` + `business_cut`;
    career HTML strips the business cut, the `.md` twin keeps both (for AI ingestion
    and later Abqariyyah reuse).
  - AI-native layer: generated `/llms.txt`, `.md` twins for every page,
    `/data/profile.json` canonical facts, robots.txt explicitly allows AI crawlers.
  - `/ask` chat is a placeholder page until Dify/Botpress widget is deployed (Layer 2);
    placeholder already teaches visitors to use llms.txt with their own AI.
  - Seeded 6 case studies (C1–C6) from `~/Folder/portfolio/JOURNAL.md` + CV + Dev repos.
    All marked `status: draft`; unverified numbers tagged `[VERIFY]` or `verify:true`.
- **Next steps (in order)**:
  1. Human pass: verify `[VERIFY]` items with DIS approval (metrics, screenshots, testimonial).
  2. Pick final headline (set `headline_chosen` in profile.json).
  3. Add contact email + optional LinkedIn; flip statuses draft → reviewed.
  4. Deploy `site/` to Hostinger (or Cloudflare Pages); confirm llms.txt + profile.json serve.
  5. Generate QR (`qr/README.md`), add to CV PDF.
  6. Stand up Dify chatflow on VPS with KB = site/*.md + profile.json; embed into ask.html.
  7. Flip statuses → published; regenerate sitemap.xml (TODO in build.py).
- **Deliberately not done**: no analytics yet, no sitemap generation yet, no CI.

## 2026-10-22 (2) · Verification round complete — all case studies reviewed
- Mohammad answered all 8 verification questions:
  1. ~100 agents / ~70k individuals/yr → approved (verify:false)
  2. Twenty RLS fork → stays PRIVATE; evidence = decision records + admin-UI screenshots
  3. NMC architecture diagram → hand-built SVG published (site/assets/nmc-architecture.svg, embedded in C3)
  4. 8,000 BHD story detailed: contractor quote stopped; 4 integrated systems (Chatwoot,
     CRM [NocoDB→Twenty], custom mobile app, Grafana) + n8n/scripts for 100 BHD/yr VPS
  5. Screenshots: Mohammad will capture n8n/Chatwoot/Twenty/custom app (Grafana down) —
     shot-list in site/assets/screenshots/README.md
  6. NO DIS testimonial (they're not comfortable with him seeking opportunity outside)
     ⚠ flag raised: consider anonymizing DIS on the career site while employed — his call
  7. Campaign numbers = his own pitch work, free to publish
  8. Hobbies removed from about.md
- All statuses flipped draft → reviewed. Build clean, zero warnings.
- Next: deploy to Hostinger; screenshots; QR. Abqariyyah repo scaffolded in parallel.
