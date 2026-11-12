#!/usr/bin/env python3
"""build.py — render site/ from content/ (stdlib only).

Design v3 (2026-11-07): plain-language business copy on the public pages,
illustrated Services, animated How-I-Work steps, wrist-friendly mobile nav,
a dedicated /tech.html holding all the technical terminology.
Hand-maintained in site/: ask.html, assets/*, robots.txt.
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
SITE = os.path.join(ROOT, "site")

DOMAIN = "https://shihabarch.tech"

SHORT_LABELS = {
    "conversations": "conversations handled",
    "contacts": "leads generated in two years",
    "reach": "avg. monthly campaign reach",
    "saved_bhd": "BHD saved vs. the vendor quote",
    "saved_usd_yr": "USD/yr of subscriptions eliminated",
    "countries": "countries reached",
    "agents": "team members supported",
    "downtime": "downtime during a platform lock-out",
}
HOME_STATS = ["conversations", "contacts", "saved_bhd", "reach", "countries", "downtime"]
STACK_GROUPS = [("Infrastructure", "infra", 8), ("Data", "data", 8), ("Apps & Channels", "apps", 8), ("AI", "ai", 7)]

# pillar heading name → case-study ids shown under each Services card
PILLAR_CASES = {
    "AI Adoption": ["c1-omnichannel-stack", "c6-realtime-language-ai"],
    "Data": ["c2-data-platform-rls", "c5-marketing-data-ops"],
    "Workflow": ["c3-nmc-pipeline", "c1-omnichannel-stack"],
    "Systems": ["c4-cost-sovereignty"],
}

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
    """page-head already renders the title; keep the .md twin but drop the h1 from HTML."""
    return re.sub(r"^[ \t\r\n]*#\s+[^\n]*\n*", "", body, count=1).strip()

def tags(pillars):
    return "".join(f'<span class="tag {p}">{p.replace("-", " ")}</span>' for p in pillars)

# ---------- illustrations ----------
def illu_ai():
    return """<svg class="illu" viewBox="0 0 96 96" aria-hidden="true">
<defs><linearGradient id="ig-ai" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4da3ff"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>
<rect x="18" y="24" width="58" height="38" rx="12" fill="#151e31" stroke="url(#ig-ai)" stroke-width="2"/>
<circle cx="36" cy="43" r="3" fill="#4da3ff" class="a1"/><circle cx="47" cy="43" r="3" fill="#8b5cf6" class="a2"/><circle cx="58" cy="43" r="3" fill="#c084fc" class="a3"/>
<path d="M27 54 Q47 47 67 54" stroke="url(#ig-ai)" stroke-width="2" fill="none" stroke-linecap="round"/>
<path class="spark" d="M78 14 l2.6 6.2 6.2 2.6 -6.2 2.6 -2.6 6.2 -2.6 -6.2 -6.2 -2.6 6.2 -2.6 z" fill="#c084fc"/>
<path class="spark s2" d="M16 60 l1.6 4 4 1.6 -4 1.6 -1.6 4 -1.6 -4 -4 -1.6 4 -1.6 z" fill="#4da3ff"/>
<circle cx="82" cy="52" r="2.2" fill="#8b5cf6" class="a2"/>
</svg>"""

def illu_data():
    return """<svg class="illu" viewBox="0 0 96 96" aria-hidden="true">
<defs><linearGradient id="ig-data" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4da3ff"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>
<ellipse cx="34" cy="26" rx="16" ry="6.5" fill="#151e31" stroke="url(#ig-data)" stroke-width="2"/>
<path d="M18 26 v15 a16 6.5 0 0 0 32 0 v-15" fill="#151e31" stroke="url(#ig-data)" stroke-width="2"/>
<path d="M18 41 v15 a16 6.5 0 0 0 32 0 v-15" fill="none" stroke="url(#ig-data)" stroke-width="2"/>
<path class="draw" d="M74 60 v-26 M64 42 l10 -10 10 10" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<path class="spark s2" d="M74 16 l1.5 3.6 3.6 1.5 -3.6 1.5 -1.5 3.6 -1.5 -3.6 -3.6 -1.5 3.6 -1.5 z" fill="#c084fc"/>
</svg>"""

def illu_workflow():
    return """<svg class="illu" viewBox="0 0 96 96" aria-hidden="true">
<defs><linearGradient id="ig-wf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4da3ff"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>
<rect x="12" y="32" width="20" height="20" rx="6" fill="#151e31" stroke="url(#ig-wf)" stroke-width="2"/>
<rect x="38" y="32" width="20" height="20" rx="6" fill="#151e31" stroke="url(#ig-wf)" stroke-width="2"/>
<rect x="64" y="32" width="20" height="20" rx="6" fill="#151e31" stroke="url(#ig-wf)" stroke-width="2"/>
<circle cx="22" cy="42" r="3" fill="#4da3ff" class="a1"/><circle cx="48" cy="42" r="3" fill="#8b5cf6"/><circle cx="74" cy="42" r="3" fill="#c084fc"/>
<path class="flow" d="M32 42 h5" stroke="url(#ig-wf)" stroke-width="2" stroke-linecap="round"/>
<path d="M38 39 l4 3 -4 3 z" fill="#8b5cf6"/>
<path class="flow f2" d="M58 42 h5" stroke="url(#ig-wf)" stroke-width="2" stroke-linecap="round"/>
<path d="M64 39 l4 3 -4 3 z" fill="#c084fc"/>
<path class="spark" d="M46 16 l2 4.8 4.8 2 -4.8 2 -2 4.8 -2 -4.8 -4.8 -2 4.8 -2 z" fill="#4da3ff"/>
</svg>"""

def illu_systems():
    return """<svg class="illu" viewBox="0 0 96 96" aria-hidden="true">
<defs><linearGradient id="ig-sys" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4da3ff"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>
<rect x="16" y="16" width="42" height="20" rx="5" fill="#151e31" stroke="url(#ig-sys)" stroke-width="2"/>
<circle cx="24" cy="26" r="2" fill="#34d399" class="a1"/><circle cx="32" cy="26" r="2" fill="#4da3ff"/><path d="M40 23 h12" stroke="#2e4a78" stroke-width="2" stroke-linecap="round"/>
<rect x="16" y="42" width="42" height="20" rx="5" fill="#151e31" stroke="url(#ig-sys)" stroke-width="2"/>
<circle cx="24" cy="52" r="2" fill="#8b5cf6" class="a2"/><circle cx="32" cy="52" r="2" fill="#4da3ff"/><path d="M40 49 h12" stroke="#2e4a78" stroke-width="2" stroke-linecap="round"/>
<path d="M74 20 h10 v16 a10 11 0 0 1 -10 11 a10 11 0 0 1 -10 -11 v-16 z" fill="#151e31" stroke="url(#ig-sys)" stroke-width="2"/>
<path class="draw" d="M66 28 l4 4 8 -9" fill="none" stroke="#34d399" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

ILLUS = {"AI Adoption": illu_ai(), "Data": illu_data(), "Workflow": illu_workflow(), "Systems": illu_systems()}

def step_icon(i):
    icons = {
        1: '<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="7" y="5" width="18" height="22" rx="3"/><path d="M11 11h10M11 16h10M11 21h6"/></svg>',
        2: '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="10"/><path d="M11.5 16l3 3 6-6.5"/></svg>',
        3: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 5l9 4v7c0 5-3.5 8.5-9 10-5.5-1.5-9-5-9-10V9z"/><path d="M12 16l3 3 5.5-6.5"/></svg>',
        4: '<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="9" y="14" width="14" height="11" rx="2.5"/><path d="M12 14v-3a4 4 0 0 1 8 0v3"/></svg>',
        5: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 4l2.6 6.2 6.2 2.6 -6.2 2.6 -2.6 6.2 -2.6 -6.2 -6.2 -2.6 6.2 -2.6z"/></svg>',
    }
    return icons.get(i, icons[1])

# ---------- page shell ----------
NAV = """<nav>
  <a class="logo" href="/">MS<span>◆</span></a>
  <div class="navlinks">
    <a href="/case-studies/">Case Studies</a>
    <a href="/services.html">Services</a>
    <a href="/how-i-work.html">How I Work</a>
    <a href="/about.html">About</a>
    <a href="/tech.html">Tech</a>
  </div>
  <a class="cta" href="/ask.html">Ask my AI</a>
</nav>"""

def page(title, body, jsonld=None, desc="AI & Systems Consultant — Bahrain. Self-hosted infrastructure, data platforms and AI adoption, proven at multi-country scale."):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Mohammad Shahabuddin</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} — Mohammad Shahabuddin">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{DOMAIN}/">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css">
<script src="/assets/main.js" defer></script>{ld}</head>
<body>
{NAV}
<main>
{body}
</main>
<footer><div class="inner">
  <p><b style="font-family:'Space Grotesk'">Mohammad Shahabuddin</b> · AI &amp; Systems Consultant · Bahrain</p>
  <p class="mono">Machine-readable: <a href="/llms.txt">/llms.txt</a> · <a href="/data/profile.json">/data/profile.json</a> · <a href="/tech.html">plain-English toolkit</a></p>
</div></footer>
</body></html>
"""

# ---------- services renderer ----------
def render_services(body, title):
    parts = re.split(r"\n(?=## )", body.strip())
    intro_html = ""
    pillar_blocks, engagement = [], ""
    for p in parts:
        m = re.match(r"## (.+?)\n([\s\S]*)", p)
        if not m:
            # leading "# title" + intro
            intro_html = md_to_html(strip_first_h1(p))
            continue
        heading, content = m.group(1), m.group(2).strip()
        if heading.startswith("How we engage"):
            engagement = md_to_html(content)
        else:
            pillar_blocks.append((heading, content))
    cards = []
    for heading, content in pillar_blocks:
        name, _, tagline = heading.partition(" — ")
        items = [x.strip()[2:] for x in re.findall(r"(?m)^[-*] (.+)$", content)]
        items_html = "".join(f"<li>{inline(x)}</li>" for x in items)
        cases = PILLAR_CASES.get(name, [])
        proof = ""
        if cases:
            links = " · ".join(f'<a href="/case-studies/{c}.html">C{c[1]}</a>' for c in cases)
            proof = f'<p class="svc-proof">See how → {links}</p>'
        illu = ILLUS.get(name, illu_ai())
        cards.append(f"""<section class="svc reveal">
  <div class="illus">{illu}</div>
  <div class="svc-body">
    <h2>{inline(name)}</h2>
    <p class="svc-tag">{inline(tagline)}</p>
    <ul>{items_html}</ul>
    {proof}
  </div>
</section>""")
    return f"""<div class="page-head">
  <span class="eyebrow">What I do</span>
  <h1>{inline(title)}</h1>
  <div class="lead">{intro_html}</div>
</div>
<div class="svc-grid">{''.join(cards)}</div>
<div class="prose engage">{engagement}</div>"""

# ---------- how-i-work renderer ----------
def render_how_i_work(body):
    steps_html = []
    segs = re.split(r"\n(?=\d+\.\s)", body.strip())
    intro = md_to_html(strip_first_h1(segs[0]))
    for i, seg in enumerate(segs[1:], 1):
        m = re.match(r"(\d+)\.\s+\*\*(.+?)\*\*\.?\s*([\s\S]*)", seg)
        if not m: continue
        title, text = m.group(2), m.group(3).strip()
        steps_html.append(f"""<li class="step reveal">
  <div class="step-badge">{step_icon(i)}<span>{i}</span></div>
  <div class="step-body"><h3>{inline(title)}</h3><p>{inline(text)}</p></div>
</li>""")
    return f"""<div class="page-head">
  <span class="eyebrow">Method</span>
  <h1>How I Work</h1>
  <div class="lead">{intro}</div>
</div>
<ol class="steps">{''.join(steps_html)}</ol>"""

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
  <p class="meta" style="margin-top:14px">Tool names explained in <a href="/tech.html">plain English →</a></p>
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
  <p class="lead">Six documented builds — the requirements, the decisions, the numbers. Technical terms are explained over on the <a href="/tech.html">Toolkit page</a>.</p>
</div>
<div class="cards">{"".join(cards)}</div>"""))

    # content pages: about, tech (generic), services & how-i-work (custom)
    for fn, out, eyebrow, custom in [
        ("about.md", "about.html", "The person", False),
        ("tech.md", "tech.html", "The toolkit", False),
        ("services.md", "services.html", "What I do", True),
        ("how-i-work.md", "how-i-work.html", "Method", True),
    ]:
        p = os.path.join(CONTENT, fn)
        if not os.path.exists(p):
            warnings.append(f"missing: {fn}"); continue
        fm, body = parse_md(p)
        if fm.get("status") == "draft": warnings.append(f"draft: {fn}")
        t = fm.get("title", out)
        if custom:
            rendered = render_services(body, t) if fn == "services.md" else render_how_i_work(body)
        else:
            rendered = f'<div class="page-head"><span class="eyebrow">{eyebrow}</span><h1>{inline(t)}</h1></div><div class="prose">{md_to_html(strip_first_h1(body))}</div>'
        open(os.path.join(SITE, out), "w", encoding="utf-8").write(page(t, rendered, desc=fm.get("note", "") or f"{t} — Mohammad Shahabuddin"))
        shutil.copyfile(p, os.path.join(SITE, fn))  # md twin

    # ---------- index ----------
    person = profile["person"]
    headline = person.get("headline_chosen") or person["headline_candidates"][0]
    head_role = headline.partition("—")[0].strip() or headline
    stack = profile["stack"]

    stats_html = "".join(
        (f'<div class="stat reveal"><b data-count="{metrics[i]["value"]}">{metrics[i]["value"]:,}</b><span>{SHORT_LABELS.get(i, metrics[i]["label"])}</span></div>' if isinstance(metrics[i]["value"], int)
         else f'<div class="stat reveal"><b>{metrics[i]["value"]}</b><span>{SHORT_LABELS.get(i, metrics[i]["label"])}</span></div>')
        for i in HOME_STATS if i in metrics)

    roles_html = "".join(
        f'<li class="reveal"><span class="when">{r["start"]} → {r["end"] or "present"}</span>'
        f'<b>{r["title"]}</b> · {r["org"]}' + (f'<p>{inline(r.get("note", ""))}</p>' if r.get("note") else '') + "</li>"
        for r in profile["roles"])

    groups_html = "".join(
        f'<div class="stackgroup"><b>{label}</b><div class="pills">'
        + "".join(f'<span class="pill{" hl" if j < 3 else ""}">{s}</span>' for j, s in enumerate(stack.get(key, [])[:n]))
        + "</div></div>"
        for label, key, n in STACK_GROUPS)
    stackcard = f"""<div class="stackcard reveal">
  <h3><span class="dot"></span>Running in production</h3>
  {groups_html}
  <p class="gloss"><a href="/tech.html">What does all this mean? →</a></p>
</div>"""

    all_stack = [s for key in ("infra", "data", "apps", "ai", "apis") for s in stack.get(key, [])]
    mq = "".join(f"<span>{s}</span>" for s in all_stack)
    marquee = f'<div class="marquee"><div class="track">{mq}{mq}</div></div>'

    cards_home = []
    for i, (fm, _) in enumerate(studies[:4], 1):
        mid = next((m for m in fm.get("metrics_ids", []) if m in metrics), None)
        mv = f'{metrics[mid]["value"]:,}' if mid and isinstance(metrics[mid]["value"], int) else (metrics[mid]["value"] if mid else "")
        cards_home.append(f"""<a class="card reveal" href="/case-studies/{fm['id']}.html">
  <span class="num">C{i}</span>
  <div class="tags">{tags(fm.get('pillars', []))}</div>
  <h3>{inline(fm['title'])}</h3>
  <p>{inline(fm.get('summary', ''))}</p>
  <div class="foot"><span>{fm.get('period', '')}</span><span>{f'<b>{mv}</b> ' if mv else ''}<span style="color:var(--mut2);font-size:11px">{SHORT_LABELS.get(mid, "")}</span></span></div>
</a>""")

    jsonld = {"@context": "https://schema.org", "@type": "Person",
              "name": person["name"], "url": DOMAIN,
              "jobTitle": headline, "address": {"@type": "PostalAddress", "addressCountry": "BH"},
              "sameAs": [person["links"]["github"]]}

    body = f"""<div class="hero">
  <div class="hero-grid">
    <div>
      <span class="eyebrow">{inline(head_role)} · Bahrain</span>
      <h1>Mohammad <em>Shahabuddin</em></h1>
      <p class="sub">I help businesses adopt AI and bring order to their data, workflow and infrastructure — systems they own, with no lock-in and no surprise bills.</p>
      <div class="hero-ctas">
        <a class="btn primary" href="/ask.html">Ask my AI →</a>
        <a class="btn ghost" href="/case-studies/">See the evidence</a>
      </div>
    </div>
    {stackcard}
  </div>
  {marquee}
</div>
<div class="stats">{stats_html}</div>
<section>
  <div class="sec-head"><span class="eyebrow">Background</span><h2>Work history</h2></div>
  <ul class="timeline">{roles_html}</ul>
</section>
<section>
  <div class="sec-head"><span class="eyebrow">Selected work</span><h2>Builds you can verify</h2>
    <p>Every case study documents the requirements, the options, the decision — and the numbers. Screenshots and decision records available on request.</p></div>
  <div class="cards">{''.join(cards_home)}</div>
  <p style="margin-top:24px"><a class="btn ghost" href="/case-studies/">All six case studies →</a></p>
</section>
<div class="aicallout reveal">
  <h2>Recruiter shortcut: ask my AI</h2>
  <p>Scanning dozens of CVs? My assistant is grounded on this site's full content — stack, metrics, process — and answers in seconds. Or point <em>your own</em> AI at this site; it's built for that.</p>
  <a class="btn primary" href="/ask.html">Open the chat →</a>
  <p class="mono" style="margin-top:14px">"Read https://shihabarch.tech/llms.txt and answer: …" — works with any assistant.</p>
</div>"""
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(page("Mohammad Shahabuddin", body, jsonld))

    # data contracts
    with open(os.path.join(SITE, "data", "case-studies.json"), "w", encoding="utf-8") as f:
        json.dump({"updated": profile["meta"]["updated"], "case_studies": cs_index}, f, indent=1)
    with open(os.path.join(SITE, "data", "metrics.json"), "w", encoding="utf-8") as f:
        json.dump({"updated": profile["meta"]["updated"], "metrics": profile["metrics"]}, f, indent=1)

    # sitemap
    urls = [DOMAIN + "/", DOMAIN + "/about.html", DOMAIN + "/services.html",
            DOMAIN + "/how-i-work.html", DOMAIN + "/tech.html", DOMAIN + "/ask.html", DOMAIN + "/case-studies/"]
    urls += [f"{DOMAIN}/case-studies/{fm['id']}.html" for fm, _ in studies]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
    sm += "</urlset>\n"
    open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write(sm)

    # llms.txt
    ll = [f"# Mohammad Shahabuddin — shihabarch.tech",
          f"> {headline}",
          "",
          "Bahrain-based AI & Systems Consultant. Self-hosted infrastructure, data platforms,",
          "workflow automation and AI adoption for NGOs and SMEs. Named reference:",
          "Discover Islam Society. Business/services entity: Abqariyyah.",
          "",
          "## Machine-readable data",
          "- [profile.json](https://shihabarch.tech/data/profile.json): canonical structured facts — roles, metrics, skills, stack",
          "",
          "## Case Studies"]
    for fm, _ in studies:
        ll.append(f"- [{fm['title']}](https://shihabarch.tech/case-studies/{fm['id']}.md): {fm.get('summary','')}")
    ll += ["", "## Pages",
           "- [About](https://shihabarch.tech/about.md)",
           "- [Services — four pillars](https://shihabarch.tech/services.md)",
           "- [How I Work](https://shihabarch.tech/how-i-work.md)",
           "- [Tech Toolkit — terminology in plain English](https://shihabarch.tech/tech.md)",
           "- [Ask my AI](https://shihabarch.tech/ask.html): hosted chat grounded on this site's content",
           "", "## Notes for AI assistants",
           "- Markdown twin of any page: same URL with .md",
           "- JSON endpoints: /data/profile.json, /data/case-studies.json, /data/metrics.json",
           "- Metrics flagged verify:true in profile.json are approximate and pending client approval.",
           ""]
    open(os.path.join(SITE, "llms.txt"), "w", encoding="utf-8").write("\n".join(ll))

    print(f"built {len(studies)} case studies + pages into {SITE}")
    for w in warnings: print("  ⚠", w)
    return 0

if __name__ == "__main__":
    sys.exit(main())