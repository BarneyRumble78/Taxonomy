"""Build the static site into site/dist/ for Cloudflare Pages.

The company homepage is site/dist/index.html. Minerva, the knowledge
standard, is site/dist/minerva/index.html, built from site/template.html.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"
PAGES = ROOT / "site" / "pages"

NAV = [
    ("home", "Taxonomy", "/"),
    ("minerva", "Minerva", "/minerva/"),
    ("defence", "Defence", "/defence/"),
    ("skynet", "Skynet", "/skynet/"),
    ("blade", "Blade Runner", "/blade-runner/"),
    ("about", "About", "/about/"),
    ("contact", "Contact", "/contact/"),
]

DRAWER = [
    ("/", "Taxonomy", "The company"),
    ("/minerva/", "Minerva", "Lead division"),
    ("/defence/", "Defence", "Division"),
    ("/skynet/", "Skynet", "Division"),
    ("/blade-runner/", "Blade Runner", "AI-agent security"),
    ("/about/", "About", "Chris Townsend"),
    ("/contact/", "Contact", "Speaking, writing, advisory"),
]

# Former single-page section names, plus the American spelling of Defence.
REDIRECTS = """\
/maths /minerva/#maths 301
/maths/ /minerva/#maths 301
/fields /minerva/#fields 301
/fields/ /minerva/#fields 301
/how /minerva/#how 301
/how/ /minerva/#how 301
/ai /minerva/#ai 301
/ai/ /minerva/#ai 301
/uses /minerva/#uses 301
/uses/ /minerva/#uses 301
/try /minerva/#try 301
/try/ /minerva/#try 301
/api /minerva/#api 301
/api/ /minerva/#api 301
/register /minerva/#contact 301
/register/ /minerva/#contact 301
/defense /defence/ 301
/defense/ /defence/ 301
"""

HASH_REDIRECT = """<script>
(function(){
  var known={home:1,maths:1,fields:1,how:1,ai:1,uses:1,try:1,api:1,about:1,contact:1};
  var h=(location.hash||"").replace(/^#/,"").split("&")[0];
  if(known[h]) location.replace("/minerva/#"+h);
})();
</script>"""

MENU_SCRIPT = """<script>
document.getElementById('menubtn').addEventListener('click',function(){
  var d=document.getElementById('drawer');
  var open=d.hidden;
  d.hidden=!open;
  this.setAttribute('aria-expanded',open?'true':'false');
});
</script>"""


def build_minerva():
    t = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
    data = json.loads((ROOT / "site" / "site_data.json").read_text(encoding="utf-8"))
    lex = json.loads((ROOT / "engine" / "lexicon.json").read_text(encoding="utf-8"))
    cb = (ROOT / "pilot" / "codebook.md").read_text(encoding="utf-8")
    t = (
        t.replace("__LEX__", json.dumps(lex, ensure_ascii=False))
        .replace("__CODEBOOK__", json.dumps(cb, ensure_ascii=False))
        .replace("__DATA__", json.dumps(data, ensure_ascii=False))
    )
    t = re.sub(r"[Tt]he Taxonomy", "Taxonomy", t)
    out = DIST / "minerva" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(t, encoding="utf-8")
    print(f"site/dist/minerva/index.html written, {len(t)} bytes")
    return t


def style_block():
    raw = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
    match = re.search(r"<style>.*?</style>", raw, re.S)
    if not match:
        raise SystemExit("style block missing from site/template.html")
    return match.group(0)


def render_page(title, description, active, crumb_tail, body, hash_redirect=False):
    tabs = []
    for key, label, href in NAV:
        current = ' aria-current="page"' if key == active else ""
        tabs.append(f'<a class="tab" href="{href}"{current}>{label}</a>')
    drawer = "".join(
        f'<a href="{href}">{label}<small>{desc}</small></a>' for href, label, desc in DRAWER
    )
    crumb = 'You are here: <a href="/">Home</a>'
    if crumb_tail:
        crumb += " &gt; " + crumb_tail
    redirect = HASH_REDIRECT if hash_redirect else ""
    return f"""<!DOCTYPE html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<title>{title}</title>
{style_block()}
{redirect}
</head>
<body>
<div class="page">
<div class="util"><span>Taxonomy · New Zealand</span><span><a href="/minerva/">Minerva</a></span><span><a href="/about/">About</a></span><span><a href="/contact/">Contact</a></span></div>
<div class="banner">
  <button class="menubtn" id="menubtn" type="button" aria-expanded="false" aria-controls="drawer"><span class="bars" aria-hidden="true"><i></i><i></i><i></i></span>Menu</button>
  <svg class="seal" viewBox="0 0 60 60" aria-hidden="true"><circle cx="30" cy="30" r="28" fill="#173a6b" stroke="#c9a227" stroke-width="3"/><circle cx="30" cy="30" r="22" fill="none" stroke="#c9a227" stroke-width="1"/><polygon points="30,13 45,42 15,42" fill="#c9a227"/><line x1="20.5" y1="31" x2="39.5" y2="31" stroke="#173a6b" stroke-width="1.6"/><line x1="25.5" y1="22" x2="34.5" y2="22" stroke="#173a6b" stroke-width="1.6"/></svg>
  <a class="brand" href="/"><b>Taxonomy</b><span>An AI company · New Zealand</span></a>
  <form class="search" role="search" action="/minerva/" method="get"><label for="q" style="position:absolute;left:-9999px">Search a field</label><input id="q" name="q" placeholder="Search a field, e.g. Law"><button type="submit">Go</button></form>
</div>
<nav class="drawer" id="drawer" hidden aria-label="Site menu">{drawer}</nav>
<nav class="tabs" aria-label="Taxonomy">{''.join(tabs)}</nav>
<div class="crumb">{crumb}</div>
<div class="body">
{body}
</div>
<footer>
  <div class="fcols">
    <div><b>Taxonomy</b><a href="/">Company</a><a href="/about/">About</a><a href="/contact/">Contact</a></div>
    <div><b>Divisions</b><a href="/minerva/">Minerva</a><a href="/defence/">Defence</a><a href="/skynet/">Skynet</a><a href="/blade-runner/">Blade Runner</a></div>
    <div><b>Minerva</b><a href="/minerva/#maths">Mathematics</a><a href="/minerva/#fields">The 25 fields</a><a href="/minerva/#try">Use the tool</a><a href="/minerva/#api">API</a></div>
    <div><b>The standard</b><a href="/minerva/#how">How it works</a><a href="/minerva/#about">About the standard</a><a href="/minerva/#contact">Register</a></div>
  </div>
  <p>Taxonomy · New Zealand · © 2026 Chris Townsend. Minerva publishes the knowledge standard.</p>
</footer>
</div>
{MENU_SCRIPT}
</body>
</html>
"""


def write_page(rel, html):
    out = DIST / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"site/dist/{rel} written, {len(html)} bytes")


def main():
    build_minerva()
    pages = [
        ("index.html", "home.html", "Taxonomy", "Taxonomy is an AI company in New Zealand. Minerva is the lead division.", "home", "", True),
        ("defence/index.html", "defence.html", "Defence · Taxonomy", "Defence is a division of Taxonomy.", "defence", "Defence", False),
        ("skynet/index.html", "skynet.html", "Skynet · Taxonomy", "Skynet is a division of Taxonomy.", "skynet", "Skynet", False),
        ("blade-runner/index.html", "blade.html", "Blade Runner · Taxonomy", "Blade Runner is Taxonomy's division for AI-agent security.", "blade", "Blade Runner", False),
        ("about/index.html", "about.html", "About · Taxonomy", "Chris Townsend, founder and CEO of Taxonomy, AI architect, New Zealand.", "about", "About", False),
        ("contact/index.html", "contact.html", "Contact · Taxonomy", "Contact Taxonomy. Public address details are not yet published.", "contact", "Contact", False),
        ("404.html", "404.html", "Page not found · Taxonomy", "That address is not on this site.", "", "Page not found", False),
    ]
    for rel, src, title, description, active, crumb, redirect in pages:
        body = (PAGES / src).read_text(encoding="utf-8").strip()
        write_page(rel, render_page(title, description, active, crumb, body, redirect))
    (DIST / "_redirects").write_text(REDIRECTS, encoding="utf-8")
    print("site/dist/_redirects written")


if __name__ == "__main__":
    main()
