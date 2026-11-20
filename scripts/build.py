#!/usr/bin/env python3
"""build.py — render site/ from content/ (stdlib only).

Design v5 (2026-11-20): "Shihab's Architecture" brand. Landing: big title →
interactive canvas background (first section of every page) → Specialties tiles →
Achievements → work history. Pages: Solutions, Projects, How I Work, About,
Case Studies (deep dives). No /ask, no /tech.
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
SITE = os.path.join(ROOT, "site")

DOMAIN = "https://shihabarch.tech"
BRAND = "Shihab’s Architecture"

SHORT_LABELS = {
    "conversations": "conversations handled",
    "contacts": "leads generated in two years",
    "reach": "avg. monthly campaign reach",
    "saved_bhd": "BHD saved in just one project",
    "saved_usd_yr": "USD/yr of subscriptions eliminated",
    "countries": "countries reached",
    "agents": "team members supported",
    "downtime": "downtime during a platform lock-out",
}
HOME_STATS = ["conversations", "contacts", "saved_bhd", "reach", "countries", "downtime"]

# ---------- frontmatter ----------
def parse_md(path):
    text = open(path, encoding="utf-8").read()
    fm, body = {}, text
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                k, v = k.strip(), v.strip()
                if v.startswith("[") and v.endswith("]"):
                    v = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
                elif v in ("true", "false"):
                    v = (v == "true")
                else:
                    v = v.strip("'\"")
                fm[k] = v
        body = m.group(2)
    return fm, body

# ---------- minimal markdown -> html ----------
def inline(s):
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" loading="lazy">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s

def md_to_html(md):
    out, lines, i = [], md.splitlines(), 0
    def flush_para(buf):
        if buf: out.append("<p>" + inline(" ".join(buf)) + "</p>"); buf.clear()
    para, lst, tbl = [], [], []
    while i < len(lines):
        ln = lines[i]
        if re.match(r"^\|", ln):  # table
            flush_para(para)
            if lst: out.append(render_list(lst)); lst.clear()
            tbl.append(ln); i += 1
            if i >= len(lines) or not re.match(r"^\|", lines[i]):
                out.append(render_table(tbl)); tbl.clear()
            continue
        elif tbl:
            out.append(render_table(tbl)); tbl.clear()
        if ln.startswith("#"):
            flush_para(para)
            if lst: out.append(render_list(lst)); lst.clear()
            lvl = len(ln) - len(ln.lstrip("#"))
            out.append(f"<h{min(lvl,4)}>{inline(ln.lstrip('#').strip())}</h{min(lvl,4)}>")
        elif re.match(r"^\s*[-*] ", ln):
            flush_para(para)
            lst.append(ln.strip()[2:])
        elif ln.strip() == "":
            flush_para(para)
            if lst: out.append(render_list(lst)); lst.clear()
        else:
            if lst: out.append(render_list(lst)); lst.clear()
            para.append(ln.strip())
        i += 1
    flush_para(para)
    if lst: out.append(render_list(lst))
    if tbl: out.append(render_table(tbl))
    return "\n".join(out)

def render_list(items):
    return "<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>"

def render_table(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(re.match(r"^:?-{3,}:?$", c or "-") for c in r)]
    if not cells: return ""
    head = "".join(f"<th>{inline(c)}</th>" for c in cells[0])
    body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:])
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"

def strip_business_cut(md):
    return re.sub(r"## business_cut\n.*?(?=\n## |\Z)", "", md, flags=re.S).strip()

def strip_first_h1(body):
    return re.sub(r"^[ \t\r\n]*#\s+[^\n]*\n*", "", body, count=1).strip()

def tags(pillars):
    return "".join(f'<span class="tag {p}">{p.replace("-", " ")}</span>' for p in pillars)

# ---------- icons ----------
ICON_SPAN = '<svg viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{}</svg>'

GITHUB_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56 0-.27-.01-1.17-.02-2.12-3.2.7-3.88-1.36-3.88-1.36-.52-1.33-1.28-1.68-1.28-1.68-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.02 1.75 2.68 1.25 3.34.95.1-.74.4-1.25.72-1.54-2.55-.29-5.23-1.28-5.23-5.68 0-1.26.45-2.28 1.18-3.09-.12-.29-.51-1.46.11-3.05 0 0 .96-.31 3.15 1.18a10.9 10.9 0 0 1 5.74 0c2.19-1.49 3.15-1.18 3.15-1.18.62 1.59.23 2.76.11 3.05.73.81 1.18 1.83 1.18 3.09 0 4.41-2.69 5.38-5.25 5.66.41.36.77 1.05.77 2.13 0 1.54-.01 2.78-.01 3.16 0 .31.21.68.8.56A10.52 10.52 0 0 0 23.5 12C23.5 5.65 18.35.5 12 .5z"/></svg>'

ICONS = {
    "servers": '<rect x="5" y="4" width="22" height="9" rx="2"/><path d="M9 8.5h.01M12 8.5h6"/><rect x="5" y="18" width="22" height="9" rx="2"/><path d="M9 22.5h.01M12 22.5h6"/>',
    "data": '<ellipse cx="16" cy="6.5" rx="8.5" ry="3.2"/><path d="M7.5 6.5v18c0 1.8 3.8 3.2 8.5 3.2s8.5-1.4 8.5-3.2v-18"/><path d="M7.5 15.5c0 1.8 3.8 3.2 8.5 3.2s8.5-1.4 8.5-3.2"/>',
    "ai": '<rect x="8" y="8" width="16" height="16" rx="3"/><rect x="13" y="13" width="6" height="6" rx="1.5" fill="currentColor" stroke="none"/><path d="M16 3v2.5M16 26.5V29M3 16h2.5M26.5 16H29M6.8 6.8l1.8 1.8M23.4 23.4l1.8 1.8M25.2 6.8l-1.8 1.8M8.6 23.4l-1.8 1.8"/>',
    "automation": '<circle cx="16" cy="16" r="4"/><path d="M16 2.5v3M16 26.5v3M2.5 16h3M26.5 16h3M6.2 6.2l2.1 2.1M23.7 23.7l2.1 2.1M25.8 6.2l-2.1 2.1M8.3 23.7l-2.1 2.1"/>',
    "business": '<rect x="3" y="5" width="9" height="7" rx="1.5"/><rect x="20" y="5" width="9" height="7" rx="1.5"/><rect x="11.5" y="20" width="9" height="7" rx="1.5"/><path d="M7.5 12v4M24.5 12v4M7.5 16h5M24.5 16h-5M16 16v4"/>',
    "communication": '<path d="M4 7a3 3 0 0 1 3-3h18a3 3 0 0 1 3 3v11a3 3 0 0 1-3 3H13l-6 4v-4H7a3 3 0 0 1-3-3z"/><path d="M10 11.5h12M10 16h7"/>',
    "social": '<circle cx="9" cy="16" r="4"/><circle cx="23" cy="6" r="2.5"/><circle cx="23" cy="26" r="2.5"/><path d="M12.5 14l8-6M12.5 18l8 6"/>',
    "security": '<path d="M16 3l9 4v7c0 5-3.8 8.6-9 10.5C10.8 22.6 7 19 7 14V7z"/><path d="M12 16l2.5 2.5L20.5 12"/>',
    "consultation": '<circle cx="16" cy="16" r="11"/><path d="M16 10v6l4 2"/><circle cx="16" cy="16" r="1.4" fill="currentColor" stroke="none"/>',
    "email": '<rect x="3" y="6" width="26" height="20" rx="3"/><path d="M3 9l13 9 13-9"/>',
    "project": '<rect x="4" y="5" width="24" height="22" rx="3"/><path d="M4 10h24"/><path d="M9 7.5h.01M12 7.5h.01"/>',
    "maintenance": '<path d="M27 9a11 11 0 1 0 .5 12"/><path d="M27 3v6h-6"/>',
}

def icon(kind):
    if kind == "github":
        return GITHUB_SVG
    return ICON_SPAN.format(ICONS.get(kind, ICONS["consultation"]))

def step_icon(i):
    icons = {
        1: '<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="7" y="5" width="18" height="22" rx="3"/><path d="M11 11h10M11 16h10M11 21h6"/></svg>',
        2: '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="10"/><path d="M11.5 16l3 3 6-6.5"/></svg>',
        3: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 5l9 4v7c0 5-3.5 8.5-9 10-5.5-1.5-9-5-9-10V9z"/><path d="M12 16l3 3 5.5-6.5"/></svg>',
        4: '<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="9" y="14" width="14" height="11" rx="2.5"/><path d="M12 14v-3a4 4 0 0 1 8 0v3"/></svg>',
        5: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 4l2.6 6.2 6.2 2.6 -6.2 2.6 -2.6 6.2 -2.6 -6.2 -6.2 -2.6 6.2 -2.6z"/></svg>',
    }
    return icons.get(i, icons[1])

MAP_SVG = """<svg class="map-svg" viewBox="0 0 640 320" role="img" aria-label="Stylized map showing Bahrain">
  <defs>
    <linearGradient id="sea" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0c1120"/><stop offset="1" stop-color="#0a0f1d"/>
    </linearGradient>
  </defs>
  <rect width="640" height="320" fill="url(#sea)"/>
  <g class="map-grid" stroke="#1e2a44" stroke-width="1" fill="none">
    <path d="M0 80h640M0 160h640M0 240h640M160 0v320M320 0v320M480 0v320"/>
  </g>
  <path class="land" d="M32 300 L70 238 L54 182 L130 150 L120 90 L210 70 L250 122 L236 202 L294 232 L292 300 Z" fill="#101726" stroke="#1e2a44" stroke-width="2"/>
  <path class="land" d="M470 300 L470 216 L430 192 L406 206 L402 254 L432 300 Z" fill="#101726" stroke="#1e2a44" stroke-width="2"/>
  <path class="land bahrain" d="M374 138 l14 -4 8 12 -6 14 -16 4 -8 -12 z" fill="#151e31" stroke="#4da3ff" stroke-width="2"/>
  <circle class="pin-ring" cx="382" cy="150" r="30" fill="none" stroke="#4da3ff" stroke-width="1.5"/>
  <circle class="pin-ring r2" cx="382" cy="150" r="46" fill="none" stroke="#4da3ff" stroke-width="1"/>
  <circle cx="382" cy="150" r="6" fill="#8b5cf6" stroke="#fff" stroke-width="2"/>
  <text x="382" y="112" text-anchor="middle" fill="#e8edf6" font-family="Space Grotesk, sans-serif" font-size="16" font-weight="700">Bahrain</text>
  <text x="382" y="130" text-anchor="middle" fill="#8b98af" font-family="Inter, sans-serif" font-size="11">26.1°N, 50.6°E</text>
</svg>"""

# ---------- page shell ----------
NAV = """<nav class="site-nav">
  <a class="logo" href="/">Shihab’s <span>Architecture</span></a>
  <button class="nav-toggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  <div class="navlinks">
    <a href="/solutions.html">Solutions</a>
    <a href="/projects.html">Projects</a>
    <a href="/how-i-work.html">How I Work</a>
    <a href="/about.html">About</a>
  </div>
</nav>"""

def page(title, body, jsonld=None, desc="AI & Systems Consultant — Bahrain. Self-hosted infrastructure, data platforms and AI adoption, proven at multi-country scale."):
    full_title = title if title == BRAND else f"{title} — {BRAND}"
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}/">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css">
<script src="/assets/main.js" defer></script>{ld}</head>
<body>
<canvas id="arch-canvas" class="art-bg" aria-hidden="true"></canvas>
{NAV}
<main>
{body}
</main>
<footer><div class="inner">
  <p><b style="font-family:'Space Grotesk'">{BRAND}</b> · Mohammad Shahabuddin · Bahrain</p>
  <p class="mono"><a href="/case-studies/">Case studies</a> · <a href="/llms.txt">/llms.txt</a> · <a href="/data/profile.json">/data/profile.json</a></p>
</div></footer>
</body></html>
"""

# ---------- landing section renderers ----------
def render_specialties(specs):
    cards = []
    for s in specs:
        items = "".join(f"<li>{inline(x)}</li>" for x in s["items"])
        cards.append(f"""<article class="spec reveal">
  <div class="spec-icon">{icon(s["icon"])}</div>
  <div class="spec-body">
    <h3>{inline(s["name"])}</h3>
    <p class="spec-tag">{inline(s["tagline"])}</p>
    <ul class="spec-chips">{items}</ul>
  </div>
</article>""")
    return f"""<section class="specials" id="specialties">
  <div class="sec-head">
    <span class="eyebrow">Specialties</span>
    <h2>What I build & run</h2>
    <p>Six areas, one operating system of work — from the server in the rack to the AI answering a customer. Every item below is in active, production use.</p>
  </div>
  <div class="spec-grid">{''.join(cards)}</div>
</section>"""

def render_solutions_page(solutions):
    cards = "".join(f"""<article class="soln reveal">
  <div class="soln-icon">{icon(s["icon"])}</div>
  <div class="soln-body">
    <h2>{inline(s["name"])}</h2>
    <p>{inline(s["summary"])}</p>
  </div>
</article>""" for s in solutions)
    return f"""<div class="page-head">
  <span class="eyebrow">Solutions I provide</span>
  <h1>Solutions</h1>
  <p class="lead">Eight ways I help a business own its technology — from the database it runs on to the AI that answers its customers. No lock-in, no surprise bills.</p>
</div>
<div class="soln-grid">{cards}</div>"""

def render_projects_page(projects):
    cards = []
    for p in projects:
        badges = [f'<span class="pkind">{p["kind"]}</span>']
        if p.get("confidential"):
            badges.append('<span class="pconf">Confidential</span>')
        for t in p.get("tags", []):
            badges.append(f'<span class="ptag">{t}</span>')
        metrics = "".join(f'<span class="pmetric"><b>{m["value"]}</b>{m["label"]}</span>' for m in p.get("metrics", []) if m.get("value"))
        mhtml = f'<div class="pmetrics">{metrics}</div>' if metrics else ""
        demo = f'<p class="pdemo">{p.get("demo", "")} · <a href="/about.html">contact me</a> to arrange it.</p>' if p.get("demo") else ""
        if p.get("link"):
            link = f'<a class="btn primary" href="{p["link"]}" target="_blank" rel="noopener">Visit {p.get("link_label", "site")} ↗</a>'
        else:
            link = ""
        live_cls = ' proj--live' if p.get("live") else ''
        cards.append(f"""<article class="proj{live_cls} reveal">
  <div class="proj-head"><div class="badges">{''.join(badges)}</div><h2>{inline(p["name"])}</h2></div>
  <p class="proj-sum">{inline(p["summary"])}</p>
  {mhtml}
  {demo}
  <div class="proj-foot">{link}</div>
</article>""")
    return f"""<div class="page-head">
  <span class="eyebrow">Projects</span>
  <h1>Selected Projects</h1>
  <p class="lead">Live sites are one click away. Internal tools are confidential by design — a live demonstration can be arranged on request.</p>
</div>
<div class="proj-grid">{''.join(cards)}</div>"""

# ---------- how-i-work renderer ----------
ENGAGE_ICONS = {"Project": "project", "Consultancy": "consultation", "Maintenance": "maintenance"}

def render_engagement(modes):
    cards = []
    for m in modes:
        ico = ENGAGE_ICONS.get(m["mode"], "project")
        cards.append(f"""<article class="mode reveal">
  <div class="mode-icon">{icon(ico)}</div>
  <div class="mode-body">
    <h3>{m["mode"]}</h3>
    <p class="mode-what">{m["what"]}</p>
    <p class="mode-when"><span>Fits when</span>{m["when"]}</p>
  </div>
</article>""")
    return f"""<div class="engage">
  <div class="sec-head"><span class="eyebrow">Engagement</span><h2>How we engage</h2></div>
  <div class="engage-grid">{''.join(cards)}</div>
  <p class="engage-note">Pricing on request — simple, and stated before we start.</p>
</div>"""

def render_how_i_work(body, modes):
    body = strip_first_h1(body)
    parts = re.split(r"\n(?=## )", body)
    head_block = parts[0]
    sections = parts[1:]
    segs = re.split(r"\n(?=\d+\.\s)", head_block.strip())
    intro = md_to_html(segs[0].strip())
    steps = []
    for i, seg in enumerate(segs[1:], 1):
        m = re.match(r"(\d+)\.\s+\*\*(.+?)\*\*\.?\s*([\s\S]*)", seg)
        if not m: continue
        title, text = m.group(2), m.group(3).strip()
        steps.append(f"""<li class="step reveal">
  <div class="step-badge">{step_icon(i)}<span>{i}</span></div>
  <div class="step-body"><h3>{inline(title)}</h3><p>{inline(text)}</p></div>
</li>""")
    engagement = ""
    budget = ""
    for sec in sections:
        m = re.match(r"## (.+?)\n([\s\S]*)", sec)
        if not m: continue
        heading = m.group(1).strip(); content = m.group(2).strip()
        if heading.lower().startswith("how we engage"):
            engagement = render_engagement(modes)
        elif heading.lower().startswith("built for lean"):
            budget = f"""<div class="budget reveal">
  <div class="budget-icon">{icon("data")}</div>
  <div class="budget-body">{md_to_html(content)}</div>
</div>"""
    return f"""<div class="page-head">
  <span class="eyebrow">Method</span>
  <h1>How I Work</h1>
  <div class="lead">{intro}</div>
</div>
<ol class="steps">{''.join(steps)}</ol>
{engagement}
{budget}"""

# ---------- about renderer ----------
def render_contact(person):
    links = person.get("links", {})
    items = []
    if links.get("email"):
        items.append(f"""<a class="contact" href="mailto:{links['email']}">
  <span class="contact-icon">{icon("email")}</span>
  <span class="contact-txt"><b>Email</b><span>{links['email']}</span></span>
</a>""")
    if links.get("github"):
        items.append(f"""<a class="contact" href="{links['github']}" target="_blank" rel="noopener">
  <span class="contact-icon">{icon("github")}</span>
  <span class="contact-txt"><b>GitHub</b><span>Sahabx</span></span>
</a>""")
    return f'<div class="contact-grid">{"".join(items)}</div>'

def render_about(body, person):
    body = strip_first_h1(body)
    parts = re.split(r"\n(?=## )", body)
    intro = md_to_html(parts[0].strip())
    location = ""
    for sec in parts[1:]:
        m = re.match(r"## (.+?)\n([\s\S]*)", sec)
        if not m: continue
        heading = m.group(1).strip(); content = m.group(2).strip()
        if heading.lower().startswith("where"):
            location = md_to_html(content)
    return f"""<div class="page-head">
  <span class="eyebrow">The person</span>
  <h1>About</h1>
</div>
<div class="about-intro prose">{intro}</div>
<div class="about-loc">
  <div class="map">{MAP_SVG}<p class="map-cap">Bahrain · 26.1°N, 50.6°E</p></div>
  <div class="loc-copy prose">{location}</div>
</div>
<div class="about-contact">
  <div class="sec-head"><span class="eyebrow">Contact</span><h2>Get in touch</h2></div>
  {render_contact(person)}
</div>"""

# ---------- markdown twins ----------
def solutions_md(solutions):
    out = ["---", "title: Solutions", "status: reviewed", "---", "",
           "# Solutions", "",
           "Eight ways I help a business own its technology — from the database it runs on to the AI that answers its customers.", ""]
    for s in solutions:
        out.append(f"## {s['name']}")
        out.append(s["summary"]); out.append("")
    return "\n".join(out)

def projects_md(projects):
    out = ["---", "title: Projects", "status: reviewed", "---", "",
           "# Projects", "",
           "Selected projects. Internal tools are confidential by design — a live demonstration can be arranged on request.", ""]
    for p in projects:
        out.append(f"## {p['name']} — {p['kind']}")
        out.append(p["summary"])
        for t in p.get("tags", []):
            out.append(f"- Tag: {t}")
        for m in p.get("metrics", []):
            out.append(f"- {m['value']} — {m['label']}")
        if p.get("demo"): out.append(f"- {p['demo']}")
        if p.get("link"): out.append(f"- [{p['link_label']}]({p['link']})")
        out.append("")
    return "\n".join(out)

# ---------- build ----------
def main():
    warnings = []
    profile = json.load(open(os.path.join(CONTENT, "profile.json"), encoding="utf-8"))
    os.makedirs(os.path.join(SITE, "data"), exist_ok=True)
    os.makedirs(os.path.join(SITE, "case-studies"), exist_ok=True)

    metrics = {m["id"]: m for m in profile["metrics"]}
    shutil.copyfile(os.path.join(CONTENT, "profile.json"), os.path.join(SITE, "data", "profile.json"))

    # case studies
    cs_dir = os.path.join(CONTENT, "case-studies")
    studies, cs_index = [], []
    for fn in sorted(os.listdir(cs_dir)):
        if not fn.endswith(".md") or fn.startswith("_"): continue
        fm, body = parse_md(os.path.join(cs_dir, fn))
        studies.append((fm, body))
        cs_index.append({k: fm.get(k) for k in ("id","title","status","client","client_public","period","pillars","stack","metrics_ids","summary")})
        if fm.get("status") == "draft": warnings.append(f"draft: {fn}")
        if fm.get("id") not in profile["case_studies"]: warnings.append(f"{fm.get('id')} not listed in profile.json case_studies")
        shutil.copyfile(os.path.join(cs_dir, fn), os.path.join(SITE, "case-studies", fn))
        html_body = md_to_html(strip_business_cut(body))
        side_metrics = "".join(
            (f'<div class="kv"><span>{metrics[mid]["label"].split(",")[0].split("(")[0].strip()}</span><b>{metrics[mid]["value"]:,}</b></div>' if isinstance(metrics[mid]["value"], int)
             else f'<div class="kv"><span>{metrics[mid]["label"].split(",")[0].split("(")[0].strip()}</span><b>{metrics[mid]["value"]}</b></div>')
            for mid in fm.get("metrics_ids", []) if mid in metrics)
        side = f"""<aside class="cs-side reveal">
  <h4>At a glance</h4>
  <div class="kv"><span>Client</span><b>{fm.get("client", "")}</b></div>
  <div class="kv"><span>When</span><b>{fm.get("period", "")}</b></div>
  <div class="kv"><span>Focus</span><b>{", ".join(fm.get("pillars", []))}</b></div>
  <h4 style="margin-top:16px">Tools used</h4>
  <div class="stack">{"".join(f'<span class="pill">{s}</span>' for s in fm.get("stack", []))}</div>
  {f'<h4 style="margin-top:16px">Headline numbers</h4>{side_metrics}' if side_metrics else ''}
</aside>"""
        header = f"""<div class="cs-head">
  <span class="eyebrow">Case study</span>
  <h1>{inline(fm['title'])}</h1>
  <p class="summary">{inline(fm.get('summary', ''))}</p>
  <div class="tags">{tags(fm.get('pillars', []))}</div>
</div>
<div class="cs-layout"><div class="prose reveal">{html_body}</div>{side}</div>"""
        open(os.path.join(SITE, "case-studies", fm["id"] + ".html"), "w", encoding="utf-8").write(
            page(fm["title"], header, desc=fm.get("summary", "")))

    cards = []
    for i, (fm, _) in enumerate(studies, 1):
        mid = next((m for m in fm.get("metrics_ids", []) if m in metrics), None)
        if mid and isinstance(metrics[mid]["value"], int):
            metric_html = f'<b>{metrics[mid]["value"]:,}</b> <span class="unit">{SHORT_LABELS.get(mid, "")}</span>'
        elif mid:
            metric_html = f'<b>{metrics[mid]["value"]}</b>'
        else:
            metric_html = ""
        cards.append(f"""<a class="card reveal" href="/case-studies/{fm['id']}.html">
  <span class="num">C{i}</span>
  <div class="tags">{tags(fm.get('pillars', []))}</div>
  <h3>{inline(fm['title'])}</h3>
  <p>{inline(fm.get('summary', ''))}</p>
  <div class="foot"><span>{fm.get('period', '')}</span><span>{metric_html}</span></div>
</a>""")
    open(os.path.join(SITE, "case-studies", "index.html"), "w", encoding="utf-8").write(
        page("Case Studies", f"""<div class="page-head">
  <span class="eyebrow">Evidence</span>
  <h1>Case Studies</h1>
  <p class="lead">Six documented builds — the requirements, the decisions, the numbers.</p>
</div>
<div class="cards">{"".join(cards)}</div>"""))

    # about (custom)
    fm, about_body = parse_md(os.path.join(CONTENT, "about.md"))
    open(os.path.join(SITE, "about.html"), "w", encoding="utf-8").write(
        page("About", render_about(about_body, profile["person"]), desc="About — " + BRAND))
    shutil.copyfile(os.path.join(CONTENT, "about.md"), os.path.join(SITE, "about.md"))

    # how-i-work (custom)
    fm, hiw_body = parse_md(os.path.join(CONTENT, "how-i-work.md"))
    open(os.path.join(SITE, "how-i-work.html"), "w", encoding="utf-8").write(
        page("How I Work", render_how_i_work(hiw_body, profile["engagement_modes"]), desc="How I Work — " + BRAND))
    shutil.copyfile(os.path.join(CONTENT, "how-i-work.md"), os.path.join(SITE, "how-i-work.md"))

    # solutions + projects (structured → page + .md twin)
    open(os.path.join(SITE, "solutions.html"), "w", encoding="utf-8").write(
        page("Solutions", render_solutions_page(profile["solutions"]), desc="Solutions I provide — " + BRAND))
    open(os.path.join(SITE, "solutions.md"), "w", encoding="utf-8").write(solutions_md(profile["solutions"]))
    open(os.path.join(SITE, "projects.html"), "w", encoding="utf-8").write(
        page("Projects", render_projects_page(profile["projects"]), desc="Selected Projects — " + BRAND))
    open(os.path.join(SITE, "projects.md"), "w", encoding="utf-8").write(projects_md(profile["projects"]))

    # ---------- index ----------
    person = profile["person"]
    headline = person.get("headline_chosen") or person["headline_candidates"][0]
    head_role = headline.partition("—")[0].strip() or headline

    stats_html = "".join(
        (f'<div class="stat reveal"><b data-count="{metrics[i]["value"]}">{metrics[i]["value"]:,}</b><span>{SHORT_LABELS.get(i, metrics[i]["label"])}</span></div>' if isinstance(metrics[i]["value"], int)
         else f'<div class="stat reveal"><b>{metrics[i]["value"]}</b><span>{SHORT_LABELS.get(i, metrics[i]["label"])}</span></div>')
        for i in HOME_STATS if i in metrics)

    roles_html = "".join(
        f'<li class="reveal"><span class="when">{r["start"]} → {r["end"] or "present"}</span>'
        f'<b>{r["title"]}</b> · {r["org"]}' + (f'<p>{inline(r.get("note", ""))}</p>' if r.get("note") else '') + "</li>"
        for r in profile["roles"])

    jsonld = {"@context": "https://schema.org", "@type": "Person",
              "name": person["name"], "url": DOMAIN,
              "jobTitle": headline, "address": {"@type": "PostalAddress", "addressCountry": "BH"},
              "sameAs": [person["links"]["github"]]}

    body = f"""<div class="hero">
  <div class="hero-copy">
    <span class="eyebrow">{inline(person["name"])} · {inline(head_role)} · Bahrain</span>
    <h1 class="display">Shihab’s <em>Architecture</em></h1>
    <p class="sub">End-to-end systems, data and AI infrastructure — <strong>designed, self-hosted and run so you own it</strong>. No lock-in, no surprise bills.</p>
    <div class="hero-ctas">
      <a class="btn primary" href="/solutions.html">See my solutions →</a>
      <a class="btn ghost" href="/projects.html">View projects</a>
    </div>
  </div>
</div>
{render_specialties(profile["specialties"])}
<section class="achievements">
  <div class="sec-head"><span class="eyebrow">Achievements</span><h2>Numbers from real production systems</h2></div>
  <div class="stats">{stats_html}</div>
</section>
<section>
  <div class="sec-head"><span class="eyebrow">Background</span><h2>Work history</h2></div>
  <ul class="timeline">{roles_html}</ul>
</section>"""
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(page("Shihab’s Architecture", body, jsonld))

    # data contracts
    with open(os.path.join(SITE, "data", "case-studies.json"), "w", encoding="utf-8") as f:
        json.dump({"updated": profile["meta"]["updated"], "case_studies": cs_index}, f, indent=1)
    with open(os.path.join(SITE, "data", "metrics.json"), "w", encoding="utf-8") as f:
        json.dump({"updated": profile["meta"]["updated"], "metrics": profile["metrics"]}, f, indent=1)

    # sitemap
    urls = [DOMAIN + "/", DOMAIN + "/about.html", DOMAIN + "/solutions.html",
            DOMAIN + "/projects.html", DOMAIN + "/how-i-work.html", DOMAIN + "/case-studies/"]
    urls += [f"{DOMAIN}/case-studies/{fm['id']}.html" for fm, _ in studies]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
    sm += "</urlset>\n"
    open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write(sm)

    # llms.txt
    ll = [f"# {BRAND} — Mohammad Shahabuddin",
          f"> {headline}",
          "",
          "Bahrain-based AI & Systems Consultant. Self-hosted infrastructure, data platforms,",
          "workflow automation and AI adoption for NGOs and SMEs. Brand: Shihab's Architecture.",
          "Named reference: Discover Islam Society.",
          "",
          "## Machine-readable data",
          "- [profile.json](https://shihabarch.tech/data/profile.json): canonical structured facts — roles, metrics, specialties, solutions, projects",
          "",
          "## Pages",
          "- [Solutions](https://shihabarch.tech/solutions.md)",
          "- [Projects](https://shihabarch.tech/projects.md)",
          "- [How I Work](https://shihabarch.tech/how-i-work.md)",
          "- [About](https://shihabarch.tech/about.md)",
          "",
          "## Case Studies"]
    for fm, _ in studies:
        ll.append(f"- [{fm['title']}](https://shihabarch.tech/case-studies/{fm['id']}.md): {fm.get('summary','')}")
    ll += ["", "## Notes for AI assistants",
           "- Markdown twin of any page: same URL with .md",
           "- JSON endpoints: /data/profile.json, /data/case-studies.json, /data/metrics.json",
           ""]
    open(os.path.join(SITE, "llms.txt"), "w", encoding="utf-8").write("\n".join(ll))

    print(f"built {len(studies)} case studies + pages into {SITE}")
    for w in warnings: print("  ⚠", w)
    return 0

if __name__ == "__main__":
    sys.exit(main())