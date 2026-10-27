"""
Monthly API spend ledger. Each run adds its LLM cost to `kosten.json`
(committed back to the repo by the workflow), so the cap holds across
GitHub Actions runs that otherwise share no state.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

LEDGER_PATH = Path(__file__).parent / "kosten.json"

# The API credit ($100/month) is shared with other projects, so the bot's own
# cap comes from the BOT_MONTHLY_BUDGET_USD repo variable (unset: 85, which
# leaves headroom for cost-tracking gaps). Forecasts fall back to Sonnet from
# 80 % of the cap.
STOP_FROM_USD = float(os.getenv("BOT_MONTHLY_BUDGET_USD") or 85.0)
SAVE_FROM_USD = 0.8 * STOP_FROM_USD

BudgetMode = Literal["full", "save", "stop"]


def _current_month() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def _load_ledger() -> dict[str, float]:
    if not LEDGER_PATH.exists():
        return {}
    return json.loads(LEDGER_PATH.read_text())


def spent_this_month() -> float:
    return _load_ledger().get(_current_month(), 0.0)


def remaining_until_stop() -> float:
    return max(STOP_FROM_USD - spent_this_month(), 0.0)


def budget_mode() -> BudgetMode:
    spent = spent_this_month()
    if spent >= STOP_FROM_USD:
        return "stop"
    if spent >= SAVE_FROM_USD:
        return "save"
    return "full"


def record_cost(cost_usd: float) -> None:
    if cost_usd <= 0:
        return
    ledger = _load_ledger()
    month = _current_month()
    ledger[month] = round(ledger.get(month, 0.0) + cost_usd, 4)
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
