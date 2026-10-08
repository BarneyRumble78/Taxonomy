"""The Worker's JavaScript engine must give the same placements as engine/taxonomy_engine.py."""
import csv, json, shutil, subprocess, sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import taxonomy_engine as te

EXTRA = ["Metformin reduced HbA1c more than placebo in a randomised trial of 400 adults.",
         "The judge held that the defendant owed a duty of care.", "Prove that every finite integral domain is a field.",
         "The Treaty of Waitangi was signed in 1840.", "Inflation rose to 7.3 percent in 2022 according to Stats NZ.",
         "Large language models hallucinate citations at rates that vary by prompt.", "Hello there.", ""]
JS = """
import { readFileSync } from 'node:fs';
import { createEngine } from './worker/engine.js';
const D = JSON.parse(readFileSync('./worker/data.json','utf8'));
const e = createEngine(D);
const claims = JSON.parse(readFileSync(0,'utf8'));
console.log(JSON.stringify(claims.map(c => e.classify(c))));
"""

@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_js_matches_python():
    rows = list(csv.DictReader(open(ROOT / "pilot" / "claims.tsv", encoding="utf-8"), delimiter="\t"))
    claims = [r.get("claim") or list(r.values())[1] for r in rows] + EXTRA
    out = subprocess.run(["node", "--input-type=module", "-e", JS], input=json.dumps(claims), capture_output=True, text=True, cwd=ROOT, check=True)
    js = json.loads(out.stdout)
    for c, j in zip(claims, js):
        assert te.classify(c) == j, c
