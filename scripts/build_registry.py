"""Build registry/registry.json and registry/REGISTRY.md from section 12 of every pyramid."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
rows = []
for f in sorted((ROOT / "pyramids").glob("*.md")):
    code, s = f.stem, f.read_text(encoding="utf-8")
    m = re.search(r"## 12\..*?(?=\n## 13|\Z)", s, re.S)
    if not m:
        continue
    for i, label, home, uses in re.findall(r"^\|\s*(%s\.[^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|" % code, m.group(0), re.M):
        rows.append({"id": i, "label": label, "owner": code, "home": home,
                     "uses": [u.strip() for u in uses.split(",") if u.strip() and u.strip() != "—"]})
(ROOT / "registry").mkdir(exist_ok=True)
(ROOT / "registry" / "registry.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
md = ["| ID | Label | Owner | Home | Uses |", "|---|---|---|---|---|"] + [f"| {r['id']} | {r['label']} | {r['owner']} | {r['home']} | {', '.join(r['uses']) or '—'} |" for r in rows]
(ROOT / "registry" / "REGISTRY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"{len(rows)} registry rows")
