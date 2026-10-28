# JOURNAL — shihabarch content repo

Decision/context log for this repo. Update on every meaningful change.

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
