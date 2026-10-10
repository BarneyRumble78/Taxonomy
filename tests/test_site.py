"""The built site keeps Minerva intact and follows the company site map."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"

PAGES = [
    "index.html",
    "approach/index.html",
    "minerva/index.html",
    "minerva/standard/index.html",
    "minerva/browser/index.html",
    "minerva/api/index.html",
    "minerva/mathematics/index.html",
    "minerva/claimguard/index.html",
    "minerva/evaluation/index.html",
    "minerva/changelog/index.html",
    "skynet/index.html",
    "defence/index.html",
    "blade-runner/index.html",
    "medical/index.html",
    "tech/index.html",
    "chris-townsend/index.html",
    "chris-townsend/speaking/index.html",
    "chris-townsend/writing/index.html",
    "chris-townsend/video/index.html",
    "chris-townsend/advisory/index.html",
    "contact/index.html",
    "privacy/index.html",
    "terms/index.html",
    "404.html",
]


def setup_module():
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "build_site.py")], cwd=ROOT)


def read(rel):
    return (DIST / rel).read_text(encoding="utf-8")


def test_minerva_keeps_the_tool_and_standard():
    page = read("minerva/index.html")
    assert "__LEX__" not in page and "__DATA__" not in page and "__CODEBOOK__" not in page
    for panel in ("p-home", "p-maths", "p-fields", "p-how", "p-ai", "p-uses", "p-try", "p-api", "p-about", "p-contact"):
        assert f'id="{panel}"' in page
    assert "function classify(" in page
    assert "Goods and Services Tax Act 1985" in page
    assert "deepClassify" in page
    assert "AI can retrieve evidence without knowing what kind of evidence it is." in page
    assert "Know what the evidence can actually support." in page
    assert "A claim must not be stated with greater certainty than its evidence warrants." in page
    assert "ClaimGuard" in page
    assert "IN DEVELOPMENT" in page
    assert "does not decide whether a claim is true" in page
    assert "Mathematics is the reference domain" in page
    assert "The pyramids underneath" in page
    assert "Check an AI answer" in page
    assert "Inspect a claim" in page
    assert "Connect to your agent" in page
    assert ".drawer[hidden]{display:none !important}" in page
    assert "Three things you can do with it" in page
    assert "63/63" in page
    assert "The Taxonomy" not in page
    assert 'href="/chris-townsend/"' in page
    assert 'href="/about/"' not in page


def test_homepage_follows_the_draft():
    home = read("index.html")
    assert "Know what the evidence can actually support." in home
    assert "Taxonomy is a New Zealand AI company." in home
    assert 'href="/minerva/standard/">Explore the standard →' in home
    assert 'href="/contact/">Talk to Chris →' in home
    assert "You're handed claims all day." in home
    assert "We put a label on every claim." in home
    assert "Three reasons to work with us." in home
    assert "62.1%" in home and "37.9%" in home and "203 claims" in home
    assert 'href="/minerva/evaluation/">See the evaluation →' in home
    assert "One method. Six divisions." in home
    assert "I'm Chris Townsend, founder and CEO of Taxonomy" in home
    assert "Got a claim that matters?" in home
    assert "[[CONFIRM final evidence-type list from the standard]]" in home
    assert "[[ONE-LINE OFFER TO CONFIRM]]" in home
    assert "[[PHOTO OF CHRIS]]" in home
    assert "[[BAIT PIECE:" in home
    assert 'class="tbc"' in home
    assert "Formula:" not in home
    assert "trademark" not in home.lower()
    assert 'location.replace("/minerva/#"+h)' in home
    assert "How sure should you be?" not in home
    assert "<h3>The rule</h3>" not in home


def test_site_map_pages_and_redirects():
    for rel in PAGES:
        assert (DIST / rel).is_file(), rel
    assert not (DIST / "about" / "index.html").exists()
    redirects = read("_redirects")
    for line in (
        "/try /minerva/#try 301",
        "/api /minerva/#api 301",
        "/maths /minerva/#maths 301",
        "/fields /minerva/#fields 301",
        "/how /minerva/#how 301",
        "/ai /minerva/#ai 301",
        "/uses /minerva/#uses 301",
        "/register /minerva/#contact 301",
        "/defense /defence/ 301",
        "/about /chris-townsend/ 301",
        "/about/ /chris-townsend/ 301",
    ):
        assert line in redirects
    skynet = read("skynet/index.html")
    assert "trademark" not in skynet.lower()
    assert "[[NAME UNDER REVIEW]]" in skynet
    assert "[[NAME CHECK]]" in read("blade-runner/index.html")
    evaluation = read("minerva/evaluation/index.html")
    assert "62.1%" in evaluation and "37.9%" in evaluation
    contact = read("contact/index.html")
    for option in ("Division", "Speaking", "Advisory", "Press"):
        assert f"<option>{option}</option>" in contact
    assert "This form does not send yet." in contact
    assert "[[CONFIRM contact address]]" not in contact
    chris = read("chris-townsend/index.html")
    for heading in ("Speaking", "Writing", "Video", "Advisory"):
        assert heading in chris
    for rel in PAGES:
        if rel == "minerva/index.html":
            continue
        page = read(rel)
        assert ".drawer[hidden]{display:none !important}" in page
        assert 'id="menubtn"' in page
        assert "Formula:" not in page
