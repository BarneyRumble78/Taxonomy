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
    "minerva/fields/index.html",
    "minerva/fields/MA/index.html",
    "minerva/fields/PH/index.html",
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
    assert "proof, measurement, observation, expert consensus, model output and so on." in home
    assert "settled, contested, provisional, retracted." in home
    assert "25 fields and gives 984 stable IDs" in home
    assert "Satellite and imagery intelligence." in home
    assert "Know which parts of an assessment rest on evidence, and which rest on assumption." in home
    assert "See the evidence grade behind a clinical claim before it reaches a decision." in home
    assert "Engineering and AI architecture built to say what it knows, and no more." in home
    assert "Security research for AI agents:" in home
    assert "Keynotes and workshops on AI, evidence and knowing what you know." in home
    assert "You'll get a reply from a person, not a bot." in home
    assert "Taxonomy · New Zealand" in home
    assert "Taxonomy Ltd" not in home
    assert "[[" not in home
    assert 'class="tbc"' not in home
    assert "PHOTO OF CHRIS" not in home
    assert "BAIT PIECE" not in home
    assert "Get the card" not in home
    assert "NAME UNDER REVIEW" not in home
    assert "NAME CHECK" not in home
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
    assert "[[NAME UNDER REVIEW]]" not in skynet
    assert "[[NAME CHECK]]" not in read("blade-runner/index.html")
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
    fields = read("minerva/fields/index.html")
    assert "PH — Physics" in fields or "PH —" in fields
    assert "Misplaced items: 33." in fields
    ma = read("minerva/fields/MA/index.html")
    assert 'id="filter"' in ma
    assert "fetch(" not in ma
    assert (DIST / "minerva" / "data" / "MA.json").is_file()
    assert "DRAFT." in read("minerva/standard/index.html")
    assert "POST /v1/verify" in read("minerva/api/index.html")
    assert "does not publish a verdict accuracy figure" in read("minerva/evaluation/index.html")
