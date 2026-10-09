"""Harness for model assist. Does not call Workers AI unless the owner passes --live.

The rule-based placement is the answer. A model code outside the fixed list is
dropped. Timeout or garbage JSON leaves the rule answer in place. assist.agrees
is false when the owners differ.

    python3 scripts/model_assist_eval.py
    python3 scripts/model_assist_eval.py --live https://your-worker.example/v1/classify

This pass does not run --live.
"""
import argparse, json, sys, urllib.request

CODES = "MA PH CH BI EA MD EN CS MS EC BU ST PO LA PL HI LN AR RE ED DE AG EV IS IK".split()


def filter_codes(payload, allowed):
    """Apply the Worker contract to a model payload. Returns the kept codes."""
    if not isinstance(payload, dict):
        return []
    codes = payload.get("codes")
    if not isinstance(codes, list):
        return []
    return [c for c in codes if c in allowed][:2]


def agrees(rule_owner, codes):
    return bool(codes) and codes[0] == rule_owner


def local_contract():
    """Checks that do not touch the network."""
    assert filter_codes({"codes": ["ZZ", "BI", "LA"]}, CODES) == ["BI", "LA"]
    assert filter_codes("not json", CODES) == []
    assert filter_codes({"codes": "PH"}, CODES) == []
    assert agrees("LA", []) is False
    assert agrees("LA", ["PH"]) is False
    assert agrees("LA", ["LA"]) is True
    return "local contract ok; live Workers AI was not called"


def live(url, text):
    body = json.dumps({"text": text, "assist": True}).encode()
    req = urllib.request.Request(url, data=body, headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode())


def main(argv):
    p = argparse.ArgumentParser(description="Model-assist contract harness. Live calls are owner-only.")
    p.add_argument("--live", metavar="URL", help="POST to a deployed /v1/classify. Omit to stay offline.")
    p.add_argument("--text", default="The importer must pay GST at the border under the Goods and Services Tax Act 1985.")
    args = p.parse_args(argv)
    print(local_contract())
    if not args.live:
        print("No --live URL. The live measurement is left for the owner after deploy.")
        return 0
    out = live(args.live, args.text)
    rule = (out.get("placement") or {}).get("owner")
    assist = out.get("assist") or {}
    print(json.dumps({"rule_owner": rule, "assist": assist}, indent=2))
    if rule and assist.get("codes") and assist["codes"][0] not in CODES:
        print("fault: a code outside the fixed list was returned")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
