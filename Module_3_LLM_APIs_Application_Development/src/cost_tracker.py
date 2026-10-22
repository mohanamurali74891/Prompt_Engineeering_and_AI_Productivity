"""
Module 3: LLM APIs & Application Development
=============================================
cost_tracker.py — Token usage & API cost estimation

Tracks token consumption across multiple LLM calls and estimates
API costs based on current pricing tables.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


# ─────────────────────────────────────────────────────────────
# Pricing tables (per 1M tokens, USD)
# Update these values as pricing changes.
# ─────────────────────────────────────────────────────────────

PRICING: Dict[str, Dict[str, float]] = {
    # Google Gemini
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "gemini-1.5-pro":   {"input": 3.50,  "output": 10.50},
    "gemini-1.0-pro":   {"input": 0.50,  "output": 1.50},

    # OpenAI
    "gpt-4o":           {"input": 5.00,  "output": 15.00},
    "gpt-4o-mini":      {"input": 0.15,  "output": 0.60},
    "gpt-3.5-turbo":    {"input": 0.50,  "output": 1.50},
}

# Fallback pricing for unknown models
DEFAULT_PRICING = {"input": 1.00, "output": 3.00}


# ─────────────────────────────────────────────────────────────
# Data classes
# ─────────────────────────────────────────────────────────────

@dataclass
class TokenRecord:
    """Record of tokens used in a single API call."""
    timestamp: float
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    label: str = ""             # Optional label for tracking purposes

    @property
    def datetime_str(self) -> str:
        return datetime.fromtimestamp(self.timestamp).strftime("%H:%M:%S")

    def __repr__(self):
        return (
            f"[{self.datetime_str}] {self.model} | "
            f"In: {self.prompt_tokens} | Out: {self.completion_tokens} | "
            f"Cost: ${self.estimated_cost_usd:.6f}"
        )


# ─────────────────────────────────────────────────────────────
# CostTracker
# ─────────────────────────────────────────────────────────────

class CostTracker:
    """
    Tracks token usage and cost estimates across one or more LLM sessions.

    Example
    -------
    >>> tracker = CostTracker(budget_usd=0.50)
    >>> tracker.record(model="gemini-1.5-flash", prompt_tokens=500, completion_tokens=200)
    >>> print(tracker.summary())
    """

    def __init__(self, budget_usd: Optional[float] = None):
        """
        Parameters
        ----------
        budget_usd : float, optional
            If set, warns when cumulative spend exceeds this amount.
        """
        self.budget_usd = budget_usd
        self._records: List[TokenRecord] = []
        self._session_start = time.time()

    # ── Recording ─────────────────────────────────────────────

    def record(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        label: str = "",
    ) -> TokenRecord:
        """
        Record a single API call's token usage.

        Parameters
        ----------
        model : str
            Model name (used to look up pricing).
        prompt_tokens : int
        completion_tokens : int
        label : str, optional
            Descriptive tag (e.g. "user_query", "system_test").

        Returns
        -------
        TokenRecord
        """
        total = prompt_tokens + completion_tokens
        cost = self._estimate_cost(model, prompt_tokens, completion_tokens)

        record = TokenRecord(
            timestamp=time.time(),
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total,
            estimated_cost_usd=cost,
            label=label,
        )
        self._records.append(record)

        # Budget warning
        if self.budget_usd and self.total_cost_usd > self.budget_usd:
            print(
                f"⚠️  BUDGET WARNING: Spent ${self.total_cost_usd:.4f} "
                f"(budget: ${self.budget_usd:.2f})"
            )
        return record

    def record_from_response(self, response, label: str = "") -> TokenRecord:
        """
        Convenience method to record from an LLMResponse object
        (from llm_client.py).
        """
        return self.record(
            model=response.model,
            prompt_tokens=response.prompt_tokens,
            completion_tokens=response.completion_tokens,
            label=label,
        )

    # ── Aggregates ────────────────────────────────────────────

    @property
    def total_prompt_tokens(self) -> int:
        return sum(r.prompt_tokens for r in self._records)

    @property
    def total_completion_tokens(self) -> int:
        return sum(r.completion_tokens for r in self._records)

    @property
    def total_tokens(self) -> int:
        return sum(r.total_tokens for r in self._records)

    @property
    def total_cost_usd(self) -> float:
        return sum(r.estimated_cost_usd for r in self._records)

    @property
    def call_count(self) -> int:
        return len(self._records)

    @property
    def session_duration_seconds(self) -> float:
        return time.time() - self._session_start

    # ── Per-model breakdown ───────────────────────────────────

    def breakdown_by_model(self) -> Dict[str, Dict]:
        """Return token and cost totals grouped by model."""
        breakdown: Dict[str, Dict] = {}
        for r in self._records:
            if r.model not in breakdown:
                breakdown[r.model] = {
                    "calls": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "cost_usd": 0.0,
                }
            d = breakdown[r.model]
            d["calls"] += 1
            d["prompt_tokens"] += r.prompt_tokens
            d["completion_tokens"] += r.completion_tokens
            d["total_tokens"] += r.total_tokens
            d["cost_usd"] += r.estimated_cost_usd
        return breakdown

    # ── Reset ─────────────────────────────────────────────────

    def reset(self):
        """Clear all recorded data and restart session timer."""
        self._records.clear()
        self._session_start = time.time()

    # ── Pricing ───────────────────────────────────────────────

    @staticmethod
    def _estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Estimate cost in USD for a single API call."""
        pricing = PRICING.get(model, DEFAULT_PRICING)
        input_cost  = (prompt_tokens     / 1_000_000) * pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost

    @staticmethod
    def get_pricing_table() -> str:
        """Return a formatted pricing reference table."""
        lines = [
            "╔══════════════════════╦══════════════╦═══════════════╗",
            "║ Model                ║ Input ($/1M) ║ Output ($/1M) ║",
            "╠══════════════════════╬══════════════╬═══════════════╣",
        ]
        for model, prices in PRICING.items():
            lines.append(
                f"║ {model:<20} ║ ${prices['input']:>11.3f} ║ ${prices['output']:>12.3f} ║"
            )
        lines.append("╚══════════════════════╩══════════════╩═══════════════╝")
        return "\n".join(lines)

    # ── Summary ───────────────────────────────────────────────

    def summary(self) -> str:
        """Return a human-readable usage and cost summary."""
        duration = self.session_duration_seconds
        minutes, seconds = divmod(int(duration), 60)
        lines = [
            "╔══════════════════════════════════════╗",
            "║      📊 Cost & Token Usage Report    ║",
            "╠══════════════════════════════════════╣",
            f"║  API calls     : {self.call_count:<19} ║",
            f"║  Prompt tokens : {self.total_prompt_tokens:<19,} ║",
            f"║  Output tokens : {self.total_completion_tokens:<19,} ║",
            f"║  Total tokens  : {self.total_tokens:<19,} ║",
            f"║  Estimated cost: ${self.total_cost_usd:<18.6f} ║",
            f"║  Session time  : {minutes:02d}m {seconds:02d}s              ║",
        ]
        if self.budget_usd:
            remaining = self.budget_usd - self.total_cost_usd
            lines.append(
                f"║  Budget left   : ${max(remaining, 0):<18.6f} ║"
            )
        lines.append("╚══════════════════════════════════════╝")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"CostTracker(calls={self.call_count}, "
            f"tokens={self.total_tokens:,}, "
            f"cost=${self.total_cost_usd:.6f})"
        )


# ─────────────────────────────────────────────────────────────
# Quick demo
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tracker = CostTracker(budget_usd=0.10)

    # Simulate several API calls
    tracker.record("gemini-1.5-flash", prompt_tokens=1200, completion_tokens=350, label="Q1")
    tracker.record("gemini-1.5-flash", prompt_tokens=980,  completion_tokens=220, label="Q2")
    tracker.record("gpt-4o-mini",       prompt_tokens=500,  completion_tokens=150, label="Q3")

    print(tracker.summary())
    print()
    print("📋 Per-model breakdown:")
    for model, stats in tracker.breakdown_by_model().items():
        print(f"  {model}: {stats['total_tokens']:,} tokens — ${stats['cost_usd']:.6f}")

    print()
    print("💰 Pricing reference:")
    print(CostTracker.get_pricing_table())
