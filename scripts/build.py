#!/usr/bin/env python3
"""build.py — render site/ from content/ (stdlib only).

Design v2 (2026-11-07): hero + stats band + timeline + visual cards,
self-hosted fonts (assets/fonts), reveal/count-up JS (assets/main.js).
Hand-maintained in site/: ask.html, assets/*, robots.txt.

Generates:
  site/index.html, site/about.html, site/services.html, site/how-i-work.html
  site/case-studies/index.html, site/case-studies/<id>.html   (career cut only)
  site/case-studies/<id>.md + site/*.md                        (markdown twins for AI ingestion)
  site/llms.txt, site/sitemap.xml, site/data/*.json
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
SITE = os.path.join(ROOT, "site")

DOMAIN = "https://shihabarch.tech"

# short labels for the stats band / card highlights (long labels live in profile.json)
SHORT_LABELS = {
    "conversations": "conversations handled across 20+ countries",
    "contacts": "people shared their contact details",
    "reach": "avg. monthly campaign reach",
    "saved_bhd": "BHD saved vs. the vendor quote",
    "saved_usd_yr": "USD/yr of SaaS spend eliminated",
    "countries": "countries served by the operation",
    "agents": "agents supported on the platform",
    "individuals_yr": "new records ingested per year",
    "promotions": "promotions in under two years",
    "downtime": "extended downtime in a platform crisis",
}
HOME_STATS = ["conversations", "saved_bhd", "contacts", "countries", "individuals_yr", "promotions"]
STACK_GROUPS = [("Infrastructure", "infra", 8), ("Data", "data", 8), ("Apps & Channels", "apps", 8), ("AI", "ai", 7)]

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
    """Career site shows career cut; business_cut stays in the .md twin only."""
    return re.sub(r"## business_cut\n.*?(?=\n## |\Z)", "", md, flags=re.S).strip()

def tags(pillars):
    return "".join(f'<span class="tag {p}">{p.replace("-", " ")}</span>' for p in pillars)

def fmt_metric(m):
    v = m["value"]
    if isinstance(v, int):
        return f'<b data-count="{v}">{v:,}</b>'
    return f"<b>{v}</b>"

# ---------- page shell ----------
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
<nav>
  <a class="logo" href="/">MS<span>◆</span></a>
  <a href="/case-studies/">Case Studies</a>
  <a href="/services.html">Services</a>
  <a href="/how-i-work.html">How I Work</a>
  <a href="/about.html">About</a>
  <a class="cta" href="/ask.html">Ask my AI</a>
</nav>
<main>
{body}
</main>
<footer><div class="inner">
  <p><b style="font-family:'Space Grotesk'">Mohammad Shahabuddin</b> · AI &amp; Systems Consultant · Bahrain</p>
  <p class="mono">Machine-readable: <a href="/llms.txt">/llms.txt</a> · <a href="/data/profile.json">/data/profile.json</a> · append <code>.md</code> to any page</p>
</div></footer>
</body></html>
"""

# ---------- build ----------
def main():
    warnings = []
    profile = json.load(open(os.path.join(CONTENT, "profile.json"), encoding="utf-8"))
    os.makedirs(os.path.join(SITE, "data"), exist_ok=True)
    os.makedirs(os.path.join(SITE, "case-studies"), exist_ok=True)

    metrics = {m["id"]: m for m in profile["metrics"]}

    # canonical data copy
    shutil.copyfile(os.path.join(CONTENT, "profile.json"), os.path.join(SITE, "data", "profile.json"))

    # case studies
    cs_dir = os.path.join(CONTENT, "case-studies")
    studies = []
    cs_index = []
    for fn in sorted(os.listdir(cs_dir)):
        if not fn.endswith(".md") or fn.startswith("_"): continue
        fm, body = parse_md(os.path.join(cs_dir, fn))
        studies.append((fm, body))
        cs_index.append({k: fm.get(k) for k in ("id","title","status","client","client_public","period","pillars","stack","metrics_ids","summary")})
        if fm.get("status") == "draft":
            warnings.append(f"draft: {fn}")
        if fm.get("id") not in profile["case_studies"]:
            warnings.append(f"{fm.get('id')} not listed in profile.json case_studies")
        # md twin (full, both cuts)
        shutil.copyfile(os.path.join(cs_dir, fn), os.path.join(SITE, "case-studies", fn))
        # html (career cut) — header + sticky sidebar
        html_body = md_to_html(strip_business_cut(body))
        mids = fm.get("metrics_ids", [])
        side_metrics = "".join(
            f'<div class="kv"><span>{metrics[mid]["label"].split(",")[0].split("(")[0].strip()}</span><b>{metrics[mid]["value"]:,}</b></div>'
            if isinstance(metrics[mid]["value"], int) else
            f'<div class="kv"><span>{metrics[mid]["label"].split(",")[0].split("(")[0].strip()}</span><b>{metrics[mid]["value"]}</b></div>'
            for mid in mids if mid in metrics)
        side = f"""<aside class="cs-side reveal">
  <h4>Engagement</h4>
  <div class="kv"><span>Client</span><b>{fm.get("client", "")}</b></div>
  <div class="kv"><span>Period</span><b>{fm.get("period", "")}</b></div>
  <div class="kv"><span>Pillars</span><b>{", ".join(fm.get("pillars", []))}</b></div>
  <h4 style="margin-top:16px">Stack</h4>
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

    # case studies index — cards with a headline metric
    cards = []
    for i, (fm, _) in enumerate(studies, 1):
        mid = next((m for m in fm.get("metrics_ids", []) if m in metrics), None)
        metric_html = f'<b>{metrics[mid]["value"]:,}</b> <span class="unit">{SHORT_LABELS.get(mid, "")}</span>' if mid and isinstance(metrics[mid]["value"], int) else f'<b>{metrics[mid]["value"]}</b>' if mid else ""
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
  <p class="lead">Six documented builds — the requirements, the decisions, the numbers. Each page keeps a markdown twin for AI ingestion.</p>
</div>
<div class="cards">{"".join(cards)}</div>"""))

    # content pages
    for fn, out, eyebrow in [("about.md", "about.html", "The person"), ("services.md", "services.html", "What I do"), ("how-i-work.md", "how-i-work.html", "Method")]:
        p = os.path.join(CONTENT, fn)
        if not os.path.exists(p): continue
        fm, body = parse_md(p)
        if fm.get("status") == "draft": warnings.append(f"draft: {fn}")
        open(os.path.join(SITE, out), "w", encoding="utf-8").write(
            page(fm.get("title", out), f'<div class="page-head"><span class="eyebrow">{eyebrow}</span><h1>{fm.get("title", out)}</h1></div><div class="prose">{md_to_html(body)}</div>'))
        shutil.copyfile(p, os.path.join(SITE, fn))  # md twin

    # ---------- index ----------
    person = profile["person"]
    headline = person.get("headline_chosen") or person["headline_candidates"][0]
    head_role, _, head_rest = headline.partition("—")
    if not head_rest: head_role, head_rest = headline, ""
    stack = profile["stack"]

    stats_html = "".join(
        f'<div class="stat reveal"><b data-count="{metrics[i]["value"]}">{metrics[i]["value"]:,}</b><span>{SHORT_LABELS.get(i, metrics[i]["label"])}</span></div>'
        if isinstance(metrics[i]["value"], int)
        else f'<div class="stat reveal"><b>{metrics[i]["value"]}</b><span>{SHORT_LABELS.get(i, metrics[i]["label"])}</span></div>'
        for i in HOME_STATS if i in metrics)

    roles_html = "".join(
        f'<li class="reveal"><span class="when">{r["start"]} → {r["end"] or "present"}</span>'
        f'<b>{r["title"]}</b> · {r["org"]}' + (f'<p>{inline(r.get("note", ""))}</p>' if r.get("note") else '') + "</li>"
        for r in profile["roles"])

    # stack card (hero right)
    groups_html = "".join(
        f'<div class="stackgroup"><b>{label}</b><div class="pills">'
        + "".join(f'<span class="pill{" hl" if j < 3 else ""}">{s}</span>' for j, s in enumerate(stack.get(key, [])[:n]))
        + "</div></div>"
        for label, key, n in STACK_GROUPS)
    stackcard = f"""<div class="stackcard reveal">
  <h3><span class="dot"></span>Running in production</h3>
  <p class="sub">A one-man IT department across 3 VPS providers</p>
  {groups_html}
</div>"""

    # marquee: full stack in a slow loop
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
  <div class="foot"><span>{fm.get('period', '')}</span><span><b>{mv}</b> <span style="color:var(--mut2);font-size:11px">{SHORT_LABELS.get(mid, "")}</span></span></div>
</a>""")

    lang_chips = "".join(f'<span class="chip">{l.split("(")[0].strip()}</span>' for l in person.get("languages", [])[:4])

    jsonld = {"@context": "https://schema.org", "@type": "Person",
              "name": person["name"], "url": DOMAIN,
              "jobTitle": headline, "address": {"@type": "PostalAddress", "addressCountry": "BH"},
              "sameAs": [person["links"]["github"]]}

    body = f"""<div class="hero">
  <div class="hero-grid">
    <div>
      <span class="eyebrow">{inline(head_role.strip())} · Bahrain</span>
      <h1>Mohammad <em>Shahabuddin</em></h1>
      <p class="sub">{inline(head_rest.strip() if head_rest else headline)} — <strong>self-hosted, sovereign, and proven at multi-country scale</strong> for NGOs &amp; SMEs.</p>
      <div class="loc">{lang_chips}</div>
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
  <div class="sec-head"><span class="eyebrow">Track record</span><h2>From programmer to one-man platform engineering</h2></div>
  <ul class="timeline">{roles_html}</ul>
</section>
<section>
  <div class="sec-head"><span class="eyebrow">Selected work</span><h2>Builds you can verify</h2>
    <p>Every case study documents requirements, options considered, the decision — and the numbers. Screenshots and decision records available on request.</p></div>
  <div class="cards">{''.join(cards_home)}</div>
  <p style="margin-top:24px"><a class="btn ghost" href="/case-studies/">All six case studies →</a></p>
</section>
<div class="aicallout reveal">
  <h2>Recruiter shortcut: ask my AI</h2>
  <p>Scanning dozens of CVs? My assistant is grounded on this site's full content — stack, metrics, process — and answers in seconds. Or point <em>your own</em> AI at this site; it's built for that.</p>
  <a class="btn primary" href="/ask.html">Open the chat →</a>
  <p class="mono" style="margin-top:14px">"Read https://shihabarch.tech/llms.txt and answer: …" — works with any assistant.</p>
</div>"""
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(page("Mohammad Shahabuddin — " + head_role.strip(), body, jsonld))

    # data contracts (Phase 1)
    with open(os.path.join(SITE, "data", "case-studies.json"), "w", encoding="utf-8") as f:
        json.dump({"updated": profile["meta"]["updated"], "case_studies": cs_index}, f, indent=1)
    with open(os.path.join(SITE, "data", "metrics.json"), "w", encoding="utf-8") as f:
        json.dump({"updated": profile["meta"]["updated"], "metrics": profile["metrics"]}, f, indent=1)

    # sitemap
    urls = [DOMAIN + "/", DOMAIN + "/about.html", DOMAIN + "/services.html",
            DOMAIN + "/how-i-work.html", DOMAIN + "/ask.html", DOMAIN + "/case-studies/"]
    urls += [f"{DOMAIN}/case-studies/{fm['id']}.html" for fm, _ in studies]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
    sm += "</urlset>\n"
    open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write(sm)

    # llms.txt
    ll = [f"# Mohammad Shahabuddin — shihabarch.tech",
          f"> {headline}",
          "",
          "Bahrain-based technical solutions specialist. Self-hosted infrastructure, AI adoption,",
          "data platforms and workflow automation for NGOs and SMEs. Named reference:",
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
           "- [Services (four pillars + engagement modes)](https://shihabarch.tech/services.md)",
           "- [How I Work](https://shihabarch.tech/how-i-work.md)",
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
