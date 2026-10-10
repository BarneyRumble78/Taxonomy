"""Build the static site into site/dist/ for Cloudflare Pages.

The company homepage is site/dist/index.html. Minerva, the knowledge
standard, is site/dist/minerva/index.html, built from site/template.html.
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"
PAGES = ROOT / "site" / "pages"

NAV = [
    ("home", "Home", "/"),
    ("approach", "Approach", "/approach/"),
    ("minerva", "Minerva", "/minerva/"),
    ("skynet", "Skynet", "/skynet/"),
    ("defence", "Defence", "/defence/"),
    ("blade", "Blade Runner", "/blade-runner/"),
    ("medical", "Medical", "/medical/"),
    ("tech", "Tech", "/tech/"),
    ("chris", "Chris", "/chris-townsend/"),
    ("contact", "Contact", "/contact/"),
]

DRAWER = [
    ("/", "Home", "Company"),
    ("/approach/", "Approach", "How we work"),
    ("/minerva/", "Minerva", "Truth-seeking and mapping"),
    ("/minerva/standard/", "Standard", "Minerva"),
    ("/minerva/browser/", "Browser tool", "Minerva"),
    ("/minerva/api/", "API", "Minerva"),
    ("/minerva/mathematics/", "Mathematics", "Minerva"),
    ("/minerva/claimguard/", "ClaimGuard", "Minerva"),
    ("/minerva/evaluation/", "Evaluation", "Minerva"),
    ("/minerva/changelog/", "Changelog", "Minerva"),
    ("/skynet/", "Skynet", "Division"),
    ("/defence/", "Defence", "Division"),
    ("/blade-runner/", "Blade Runner", "Division"),
    ("/medical/", "Medical", "Division"),
    ("/tech/", "Tech", "Division"),
    ("/chris-townsend/", "Chris Townsend", "Founder"),
    ("/chris-townsend/speaking/", "Speaking", "Chris Townsend"),
    ("/chris-townsend/writing/", "Writing", "Chris Townsend"),
    ("/chris-townsend/video/", "Video", "Chris Townsend"),
    ("/chris-townsend/advisory/", "Advisory", "Chris Townsend"),
    ("/contact/", "Contact", "Enquiry"),
    ("/privacy/", "Privacy", "Notice"),
    ("/terms/", "Terms", "Notice"),
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
/about /chris-townsend/ 301
/about/ /chris-townsend/ 301
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
<div class="util"><span>Taxonomy · New Zealand</span><span><a href="/minerva/">Minerva</a></span><span><a href="/chris-townsend/">Chris Townsend</a></span><span><a href="/contact/">Contact</a></span></div>
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
    <div><b>Taxonomy</b><a href="/">Home</a><a href="/approach/">Approach</a><a href="/chris-townsend/">About Chris</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></div>
    <div><b>Divisions</b><a href="/minerva/">Minerva</a><a href="/skynet/">Skynet</a><a href="/defence/">Defence</a><a href="/blade-runner/">Blade Runner</a><a href="/medical/">Medical</a><a href="/tech/">Tech</a></div>
    <div><b>Minerva</b><a href="/minerva/standard/">Standard</a><a href="/minerva/browser/">Browser tool</a><a href="/minerva/api/">API</a><a href="/minerva/mathematics/">Mathematics</a><a href="/minerva/claimguard/">ClaimGuard</a><a href="/minerva/evaluation/">Evaluation</a><a href="/minerva/changelog/">Changelog</a></div>
    <div><b>Chris Townsend</b><a href="/chris-townsend/speaking/">Speaking</a><a href="/chris-townsend/writing/">Writing</a><a href="/chris-townsend/video/">Video</a><a href="/chris-townsend/advisory/">Advisory</a></div>
  </div>
  <p>Taxonomy Ltd <span class="tbc">[[CONFIRM legal entity name]]</span> · New Zealand<br>
  <a href="/minerva/">Minerva</a> · <a href="/skynet/">Skynet</a> · <a href="/defence/">Defence</a> · <a href="/blade-runner/">Blade Runner</a> · <a href="/medical/">Medical</a> · <a href="/tech/">Tech</a> · <a href="/chris-townsend/">About Chris</a> · <a href="/contact/">Contact</a> · <a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a><br>
  <em>Know what the evidence can actually support.</em></p>
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
        ("index.html", "home.html", "Taxonomy", "Know what the evidence can actually support.", "home", "", True),
        ("approach/index.html", "approach.html", "Approach · Taxonomy", "How Taxonomy works: owner field, warrant, status and dependencies.", "approach", "Approach", False),
        ("minerva/standard/index.html", "minerva-standard.html", "The standard · Minerva", "The open standard: 25 fields and 984 stable IDs.", "minerva", '<a href="/minerva/">Minerva</a> &gt; Standard', False),
        ("minerva/browser/index.html", "minerva-browser.html", "Browser tool · Minerva", "The Minerva browser tool.", "minerva", '<a href="/minerva/">Minerva</a> &gt; Browser tool', False),
        ("minerva/api/index.html", "minerva-api.html", "API · Minerva", "API design for the Minerva standard.", "minerva", '<a href="/minerva/">Minerva</a> &gt; API', False),
        ("minerva/mathematics/index.html", "minerva-mathematics.html", "Mathematics · Minerva", "Mathematics, the reference domain.", "minerva", '<a href="/minerva/">Minerva</a> &gt; Mathematics', False),
        ("minerva/claimguard/index.html", "minerva-claimguard.html", "ClaimGuard · Minerva", "ClaimGuard is in development.", "minerva", '<a href="/minerva/">Minerva</a> &gt; ClaimGuard', False),
        ("minerva/evaluation/index.html", "minerva-evaluation.html", "Evaluation · Minerva", "Baseline scores on a frozen test set of 203 claims.", "minerva", '<a href="/minerva/">Minerva</a> &gt; Evaluation', False),
        ("minerva/changelog/index.html", "minerva-changelog.html", "Changelog · Minerva", "Standard versions and the ID stability policy.", "minerva", '<a href="/minerva/">Minerva</a> &gt; Changelog', False),
        ("skynet/index.html", "skynet.html", "Skynet · Taxonomy", "Skynet is a division of Taxonomy.", "skynet", "Skynet", False),
        ("defence/index.html", "defence.html", "Defence · Taxonomy", "Defence is a division of Taxonomy.", "defence", "Defence", False),
        ("blade-runner/index.html", "blade.html", "Blade Runner · Taxonomy", "Blade Runner is a division of Taxonomy.", "blade", "Blade Runner", False),
        ("medical/index.html", "medical.html", "Medical · Taxonomy", "Medical is a division of Taxonomy.", "medical", "Medical", False),
        ("tech/index.html", "tech.html", "Tech · Taxonomy", "Tech is a division of Taxonomy.", "tech", "Tech", False),
        ("chris-townsend/index.html", "chris.html", "Chris Townsend · Taxonomy", "Chris Townsend, founder and CEO of Taxonomy.", "chris", "Chris Townsend", False),
        ("chris-townsend/speaking/index.html", "chris-speaking.html", "Speaking · Chris Townsend", "Speaking.", "chris", '<a href="/chris-townsend/">Chris Townsend</a> &gt; Speaking', False),
        ("chris-townsend/writing/index.html", "chris-writing.html", "Writing · Chris Townsend", "Writing.", "chris", '<a href="/chris-townsend/">Chris Townsend</a> &gt; Writing', False),
        ("chris-townsend/video/index.html", "chris-video.html", "Video · Chris Townsend", "Video.", "chris", '<a href="/chris-townsend/">Chris Townsend</a> &gt; Video', False),
        ("chris-townsend/advisory/index.html", "chris-advisory.html", "Advisory · Chris Townsend", "Advisory.", "chris", '<a href="/chris-townsend/">Chris Townsend</a> &gt; Advisory', False),
        ("contact/index.html", "contact.html", "Contact · Taxonomy", "Contact Taxonomy.", "contact", "Contact", False),
        ("privacy/index.html", "privacy.html", "Privacy · Taxonomy", "Privacy.", "privacy", "Privacy", False),
        ("terms/index.html", "terms.html", "Terms · Taxonomy", "Terms.", "terms", "Terms", False),
        ("404.html", "404.html", "Page not found · Taxonomy", "That address is not on this site.", "", "Page not found", False),
    ]
    for rel, src, title, description, active, crumb, redirect in pages:
        body = (PAGES / src).read_text(encoding="utf-8").strip()
        write_page(rel, render_page(title, description, active, crumb, body, redirect))
    about = DIST / "about"
    if about.exists():
        shutil.rmtree(about)
        print("removed site/dist/about (redirects to /chris-townsend/)")
    (DIST / "_redirects").write_text(REDIRECTS, encoding="utf-8")
    print("site/dist/_redirects written")


if __name__ == "__main__":
    main()
