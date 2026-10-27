"""
Monthly API spend ledger. Each run writes only its own cost to `run_cost.json`;
the workflow's commit job adds that delta to `kosten.json` at the tip of the
default branch (`python3 budget.py merge-run-cost run_cost.json`), so the cap
holds across GitHub Actions runs that otherwise share no state and a stale
checkout can never overwrite newer totals. Standard library only: the commit
job runs it without installing the project.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

LEDGER_PATH = Path(__file__).parent / "kosten.json"
RUN_COST_PATH = Path(__file__).parent / "run_cost.json"

# The bot may use the free API credit ($100/month, reset on the 1st) but never
# more. The cap stays below it to leave headroom for cost-tracking gaps:
# BOT_MONTHLY_BUDGET_USD repo variable, unset 85. BOT_BUDGET_MONTH_OVERRIDE
# ("2026-10=12") replaces it for that one month only, e.g. when other usage
# already spent part of the credit. Forecasts fall back to Sonnet from 80 %.
DEFAULT_CAP_USD = 85.0
SAVE_SHARE = 0.8

BudgetMode = Literal["full", "save", "stop"]


def _current_month() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def _load_ledger() -> dict[str, float]:
    if not LEDGER_PATH.exists():
        return {}
    return json.loads(LEDGER_PATH.read_text())


def _add_to_ledger(month: str, cost_usd: float) -> None:
    ledger = _load_ledger()
    ledger[month] = round(ledger.get(month, 0.0) + cost_usd, 4)
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")


def spent_this_month() -> float:
    return _load_ledger().get(_current_month(), 0.0)


def cap_this_month() -> float:
    override = os.getenv("BOT_BUDGET_MONTH_OVERRIDE") or ""
    month, _, cap = override.partition("=")
    if month.strip() == _current_month() and cap.strip():
        return float(cap)
    return float(os.getenv("BOT_MONTHLY_BUDGET_USD") or DEFAULT_CAP_USD)


def remaining_until_stop() -> float:
    return max(cap_this_month() - spent_this_month(), 0.0)


def budget_mode() -> BudgetMode:
    spent = spent_this_month()
    cap = cap_this_month()
    if spent >= cap:
        return "stop"
    if spent >= SAVE_SHARE * cap:
        return "save"
    return "full"


def record_run_cost(cost_usd: float) -> None:
    """Write this run's cost for the commit job and update the local ledger."""
    if cost_usd <= 0:
        return
    month = _current_month()
    RUN_COST_PATH.write_text(
        json.dumps({"month": month, "cost_usd": round(cost_usd, 4)}) + "\n"
    )
    _add_to_ledger(month, cost_usd)


def merge_run_cost(run_cost_path: Path) -> None:
    run_cost = json.loads(run_cost_path.read_text())
    _add_to_ledger(run_cost["month"], float(run_cost["cost_usd"]))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "merge-run-cost":
        sys.exit("usage: python3 budget.py merge-run-cost <run_cost.json>")
    merge_run_cost(Path(sys.argv[2]))
