# shihabarch — content repo for shihabarch.tech

Single source of truth for the personal/career portfolio of **Mohammad Shahabuddin**,
and the upstream content for the Abqariyyah business site (business cut).

## The pipeline

```
content/                     ← WRITE HERE ONLY (curated facts; privacy-reviewed)
  ├── profile.json           ← canonical structured facts (roles, metrics, skills, links)
  ├── about.md / services.md / how-i-work.md
  ├── case-studies/*.md      ← frontmatter + career cut + business cut in one file
  └── llms.txt               ← generated (do not edit by hand)
        │
        ▼  scripts/build.py
site/                        ← deployable static output (Hostinger / Cloudflare Pages)
  ├── index.html, ask.html, case-studies/, *.md twins
  ├── data/profile.json      ← copied from content/profile.json
  ├── llms.txt               ← generated from case-study frontmatter + profile
  └── robots.txt             ← ALLOWS AI crawlers (intentional)
```

Rules:
1. **Write once, publish twice** — every case study has a `career_cut` and a
   `business_cut` section in the same file. shihabarch.tech renders career;
   Abqariyyah later renders business.
2. **Privacy firewall** — nothing enters `content/` from raw session/takeout data
   without manual curation. Mark unverified numbers with `[VERIFY]`.
3. **The `/ask` chat (Layer 2)** is grounded on `site/` output only (RAG over the
   .md twins + profile.json) — never on raw data.
4. Frontmatter status: `draft` → `reviewed` → `published`. Build warns on `draft`.

## Build

```bash
python3 scripts/build.py          # validate + render site/ from content/
```

No dependencies beyond python3 stdlib.

## Layout

- `content/` — source of truth (see above)
- `site/` — generated + static shell (html/css committed; safe to redeploy as-is)
- `scripts/build.py` — validator/renderer
- `qr/` — QR code assets for the CV (generate after first deploy; target `https://shihabarch.tech/ask?src=cv-qr`)

## Deploy notes

- Domain `shihabarch.tech` is parked on Hostinger DNS. Deploy = upload `site/` to a
  Hostinger hPanel site (or Cloudflare Pages — the cv-website repo used Cloudflare).
- Later: point `/ask` at a Dify/Botpress instance on the VPS (self-hosted, on-brand).

## Related

- Brainstorm & decisions: `~/Folder/portfolio/BRAINSTORM.md`
- Activity journal (source material): `~/Folder/portfolio/JOURNAL.md`
- Machine-readable activity data: `~/Folder/portfolio/analysis/` (private, do not publish)
