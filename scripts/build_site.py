"""Build site/dist/index.html from site/template.html + site_data.json + engine/lexicon.json + pilot/codebook.md."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
t = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
data = json.loads((ROOT / "site" / "site_data.json").read_text(encoding="utf-8"))
lex = json.loads((ROOT / "engine" / "lexicon.json").read_text(encoding="utf-8"))
cb = (ROOT / "pilot" / "codebook.md").read_text(encoding="utf-8")
t = t.replace("__LEX__", json.dumps(lex, ensure_ascii=False)).replace("__CODEBOOK__", json.dumps(cb, ensure_ascii=False)).replace("__DATA__", json.dumps(data, ensure_ascii=False))
t = t.replace('<span>Text size: A A</span><span>Accessibility</span><span>Site map</span>', '<span><a href="#about" data-go="about" style="color:#c8d3e3">About</a></span><span><a href="#contact" data-go="contact" style="color:#c8d3e3">Register</a></span>')
t = re.sub(r"[Tt]he Taxonomy", "Taxonomy", t)
(ROOT / "site" / "dist").mkdir(exist_ok=True)
(ROOT / "site" / "dist" / "index.html").write_text(t, encoding="utf-8")
print("site/dist/index.html written,", len(t), "bytes")
