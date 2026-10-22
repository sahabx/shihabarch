#!/usr/bin/env python3
"""build.py — render site/ from content/ (stdlib only).

Generates:
  site/index.html, site/about.html, site/services.html, site/how-i-work.html
  site/case-studies/index.html, site/case-studies/<id>.html   (career cut only)
  site/case-studies/<id>.md + site/*.md                        (markdown twins for AI ingestion)
  site/llms.txt                                                (generated; do not hand-edit)
  site/data/profile.json                                       (copy of canonical facts)
Hand-maintained in site/: ask.html, assets/style.css, robots.txt, data/.gitkeep
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
SITE = os.path.join(ROOT, "site")

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

# ---------- page shell ----------
def page(title, body, jsonld=None):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Mohammad Shahabuddin</title>
<link rel="stylesheet" href="/assets/style.css">{ld}</head>
<body>
<nav><a href="/">MS</a> <a href="/case-studies/">Case Studies</a> <a href="/services.html">Services</a> <a href="/how-i-work.html">How I Work</a> <a href="/about.html">About</a> <a href="/ask.html">Ask my AI</a></nav>
<main>
{body}
</main>
<footer><p>Machine-readable: <a href="/llms.txt">/llms.txt</a> · <a href="/data/profile.json">/data/profile.json</a> · markdown twin: append <code>.md</code> to any page path.</p>
<p>Services &amp; engagements: Abqariyyah (coming soon).</p></footer>
</body></html>
"""

# ---------- build ----------
def main():
    warnings = []
    profile = json.load(open(os.path.join(CONTENT, "profile.json"), encoding="utf-8"))
    os.makedirs(os.path.join(SITE, "data"), exist_ok=True)
    os.makedirs(os.path.join(SITE, "case-studies"), exist_ok=True)

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
        # html (career cut)
        html_body = md_to_html(strip_business_cut(body))
        meta = f'<p class="meta">{fm.get("client","")} · {fm.get("period","")} · pillars: {", ".join(fm.get("pillars",[]))}</p>'
        open(os.path.join(SITE, "case-studies", fm["id"] + ".html"), "w", encoding="utf-8").write(
            page(fm["title"], f"<h1>{inline(fm['title'])}</h1>{meta}{html_body}"))

    # case studies index
    cards = "".join(
        f'<a class="card" href="/case-studies/{fm["id"]}.html"><h3>{inline(fm["title"])}</h3>'
        f'<p>{inline(fm.get("summary",""))}</p><span class="pillars">{", ".join(fm.get("pillars",[]))}</span></a>'
        for fm, _ in studies)
    open(os.path.join(SITE, "case-studies", "index.html"), "w", encoding="utf-8").write(
        page("Case Studies", f"<h1>Case Studies</h1><div class='cards'>{cards}</div>"))

    # content pages
    for fn, out in [("about.md", "about.html"), ("services.md", "services.html"), ("how-i-work.md", "how-i-work.html")]:
        p = os.path.join(CONTENT, fn)
        if not os.path.exists(p): continue
        fm, body = parse_md(p)
        if fm.get("status") == "draft": warnings.append(f"draft: {fn}")
        open(os.path.join(SITE, out), "w", encoding="utf-8").write(page(fm.get("title", out), md_to_html(body)))
        shutil.copyfile(p, os.path.join(SITE, fn))  # md twin

    # index.html
    headline = profile["person"].get("headline_chosen") or profile["person"]["headline_candidates"][0]
    metrics_html = "".join(
        f'<div class="metric"><b>{m["value"] if not isinstance(m["value"], str) else m["value"]}</b><span>{inline(m["label"])}{"  [VERIFY]" if m.get("verify") else ""}</span></div>'
        for m in profile["metrics"][:6])
    roles_html = "".join(
        f'<li><b>{r["title"]}</b> · {r["org"]} · {r["start"]} → {r["end"] or "present"}</li>'
        for r in profile["roles"])
    jsonld = {"@context": "https://schema.org", "@type": "Person",
              "name": profile["person"]["name"], "url": "https://shihabarch.tech",
              "jobTitle": headline, "address": {"@type": "PostalAddress", "addressCountry": "BH"},
              "sameAs": [profile["person"]["links"]["github"]]}
    body = f"""<h1>Mohammad Shahabuddin</h1>
<p class="lead">{inline(headline)}</p>
<div class="metrics">{metrics_html}</div>
<h2>Track record</h2><ul class="roles">{roles_html}</ul>
<h2>Selected work</h2>
<div class="cards">{''.join(f'<a class="card" href="/case-studies/{fm["id"]}.html"><h3>{inline(fm["title"])}</h3><span class="pillars">{", ".join(fm.get("pillars",[]))}</span></a>' for fm,_ in studies[:4])}</div>
<p><a class="btn" href="/case-studies/">All case studies →</a> <a class="btn" href="/ask.html">Ask my AI about me →</a></p>"""
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(page("Home", body, jsonld))

    # data contracts (Phase 1): JSON endpoints so any AI/script can rebuild the portfolio
    with open(os.path.join(SITE, "data", "case-studies.json"), "w", encoding="utf-8") as f:
        json.dump({"updated": profile["meta"]["updated"], "case_studies": cs_index}, f, indent=1)
    with open(os.path.join(SITE, "data", "metrics.json"), "w", encoding="utf-8") as f:
        json.dump({"updated": profile["meta"]["updated"], "metrics": profile["metrics"]}, f, indent=1)

    # sitemap
    urls = ["https://shihabarch.tech/", "https://shihabarch.tech/about.html",
            "https://shihabarch.tech/services.html", "https://shihabarch.tech/how-i-work.html",
            "https://shihabarch.tech/ask.html", "https://shihabarch.tech/case-studies/"]
    urls += [f"https://shihabarch.tech/case-studies/{fm['id']}.html" for fm, _ in studies]
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
