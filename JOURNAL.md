# JOURNAL — shihabarch content repo

Decision/context log for this repo. Update on every meaningful change.

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
