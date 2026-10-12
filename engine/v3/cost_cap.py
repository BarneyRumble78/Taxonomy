"""Per-field and global spend caps. No network calls.

The global figure is the remaining Anthropic budget for this programme.
A field run still has its own cap. Hybrid mode spends Claude money only on
rows the local model left as unsure or needs_review.
"""
from __future__ import annotations

import json
from pathlib import Path

GLOBAL_BUDGET = 90.0
FIELD_BUDGET = 10.0
# Measured on the EV Sonnet run of 12 Oct 2026: $0.90 per 1,000 items.
USD_PER_THOUSAND = 0.90
ESCALATE_STATUS = frozenset({"unsure", "needs_review"})


class CostCap(Exception):
    """The next call would pass a field cap or the global cap."""

    def __init__(self, usd, limit, scope):
        self.usd = usd
        self.limit = limit
        self.scope = scope
        super().__init__(f"stopped at ${usd:.4f}, {scope} max-cost ${limit:.2f}")


def empty_ledger():
    return {"spent": 0.0, "fields": {}}


def load_ledger(path):
    path = Path(path)
    if not path.exists():
        return empty_ledger()
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("spent", 0.0)
    data.setdefault("fields", {})
    return data


def save_ledger(path, ledger):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")


def projected(ledger, field, usd):
    field_spent = float(ledger.get("fields", {}).get(field) or 0) + float(usd)
    global_spent = float(ledger.get("spent") or 0) + float(usd)
    return field_spent, global_spent


def allow(ledger, field, usd, field_cap, global_cap):
    """False when this increment would pass either cap. A cap of 0 is off."""
    field_spent, global_spent = projected(ledger, field, usd)
    if field_cap and field_spent > field_cap + 1e-9:
        return False, "field", field_spent, field_cap
    if global_cap and global_spent > global_cap + 1e-9:
        return False, "global", global_spent, global_cap
    return True, "", 0.0, 0.0


def record(ledger, field, usd):
    amount = float(usd)
    ledger["spent"] = round(float(ledger.get("spent") or 0) + amount, 6)
    fields = ledger.setdefault("fields", {})
    fields[field] = round(float(fields.get(field) or 0) + amount, 6)
    return ledger


def hybrid_estimate(model_items, escalate_items, usd_per_thousand=USD_PER_THOUSAND):
    """Ollama is free. Claude is priced only for the escalated rows."""
    rate = float(usd_per_thousand)
    escalate = int(escalate_items)
    model_n = int(model_items)
    return {
        "ollama_items": model_n,
        "escalate_items": escalate,
        "usd_per_thousand": rate,
        "claude_usd": round(escalate * rate / 1000, 6),
        "upper_if_all_model_items": round(model_n * rate / 1000, 6),
    }
