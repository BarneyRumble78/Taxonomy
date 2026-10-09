"""The built site keeps Minerva intact and adds the company pages."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"


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
    # The old account of the standard stays on the page.
    assert "Three things you can do with it" in page
    assert "63/63" in page
    assert "The Taxonomy" not in page


def test_company_pages_and_old_paths():
    home = read("index.html")
    assert "Taxonomy is an AI company. Minerva leads." in home
    assert 'location.replace("/minerva/#"+h)' in home
    assert "Chris Townsend" in home
    assert "ClaimGuard" in home
    for rel, line in (
        ("defence/index.html", "Defence is a division of Taxonomy."),
        ("skynet/index.html", "Skynet is a division of Taxonomy."),
        ("blade-runner/index.html", "Blade Runner is Taxonomy's division for AI-agent security."),
        ("about/index.html", "Placeholder."),
        ("contact/index.html", "No public email address has been added."),
        ("404.html", "Page not found"),
    ):
        text = read(rel)
        assert line in text
        assert "Coming soon." in text or rel in ("about/index.html", "contact/index.html", "404.html")
    skynet = read("skynet/index.html")
    assert "trademark" not in skynet.lower()
    main = skynet.split("<main>", 1)[1].split("</main>", 1)[0]
    assert main.count("Skynet") == 2
    assert "Coming soon." in main
    redirects = read("_redirects")
    assert "/try /minerva/#try 301" in redirects
    assert "/api /minerva/#api 301" in redirects
    assert "/defense /defence/ 301" in redirects
    about = read("about/index.html")
    for heading in ("Speaking", "Writing", "Video", "Advisory"):
        assert heading in about
