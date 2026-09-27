"""Minimal reproducible model for PS2.

All parameter values are illustrative hypotheses, not empirical estimates.
Run: python model.py
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Regime:
    name: str
    transfer_cap: float
    transfer_efficiency: float
    license_fee: float
    release_cost: float


def load_regimes(path: Path) -> list[Regime]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [
            Regime(
                row["regime"],
                float(row["transfer_cap"]),
                float(row["transfer_efficiency"]),
                float(row["license_fee"]),
                float(row["release_cost"]),
            )
            for row in csv.DictReader(handle)
        ]


def evaluate_regime(
    regime: Regime,
    budget: float = 0.25,
    entrant_value: float = 1.20,
    competition_loss: float = 0.45,
    consumer_value: float = 1.50,
) -> dict[str, float | str | bool]:
    potential_transfer = min(regime.transfer_cap, regime.transfer_efficiency * budget)
    entrant_profit_if_entry = entrant_value * potential_transfer - budget - regime.license_fee
    enters = entrant_profit_if_entry >= 0
    ecto = potential_transfer if enters else 0.0
    entrant_profit = entrant_profit_if_entry if enters else 0.0
    incumbent_profit = (
        1.0
        - regime.release_cost
        - competition_loss * ecto
        + (regime.license_fee if enters else 0.0)
    )
    consumer_surplus = consumer_value * ecto
    welfare = incumbent_profit + entrant_profit + consumer_surplus
    return {
        "regime": regime.name,
        "entry": enters,
        "ecto": ecto,
        "incumbent_profit": incumbent_profit,
        "entrant_profit": entrant_profit,
        "consumer_surplus": consumer_surplus,
        "welfare": welfare,
    }


def evaluate_auction(values: list[float], first_price_shading: float = 0.20) -> list[dict[str, float | str]]:
    winner = max(range(len(values)), key=values.__getitem__)
    ordered = sorted(values, reverse=True)
    second_price = ordered[1]
    shaded_bids = [v * (1 - first_price_shading) for v in values]
    first_payment = shaded_bids[winner]
    optimum = max(values)
    return [
        {
            "mechanism": "Second-price, truthful benchmark",
            "winner": f"E{winner + 1}",
            "payment": second_price,
            "winner_utility": values[winner] - second_price,
            "revenue": second_price,
            "welfare": values[winner],
            "allocative_efficiency": values[winner] / optimum,
        },
        {
            "mechanism": "First-price, assumed 20% shading",
            "winner": f"E{winner + 1}",
            "payment": first_payment,
            "winner_utility": values[winner] - first_payment,
            "revenue": first_payment,
            "welfare": values[winner],
            "allocative_efficiency": values[winner] / optimum,
        },
    ]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    regimes = load_regimes(ROOT / "inputs" / "regimes.csv")
    regime_rows = [evaluate_regime(r) for r in regimes]
    auction_rows = evaluate_auction([9, 7, 6, 4, 2])
    write_csv(ROOT / "outputs" / "regime_results.csv", regime_rows)
    write_csv(ROOT / "outputs" / "auction_results.csv", auction_rows)

    private_choice = max(regime_rows, key=lambda row: float(row["incumbent_profit"]))
    social_choice = max(regime_rows, key=lambda row: float(row["welfare"]))
    licensed = next(row for row in regime_rows if row["regime"] == "Licensed distillation")
    open_weights = next(row for row in regime_rows if row["regime"] == "Open weights")
    closed_tax_threshold = float(private_choice["incumbent_profit"]) - float(licensed["incumbent_profit"])
    open_subsidy_threshold = float(licensed["incumbent_profit"]) - float(open_weights["incumbent_profit"])

    summary = [
        f"Private choice: {private_choice['regime']}",
        f"Social-welfare choice: {social_choice['regime']}",
        f"ECTO at budget 0.25: closed={regime_rows[0]['ecto']:.2f}, licensed={regime_rows[1]['ecto']:.2f}, open={regime_rows[2]['ecto']:.2f}",
        f"Minimum tax on closed regime to induce licensed distillation: {closed_tax_threshold:.3f}",
        f"Minimum subsidy to open weights, after closed is displaced, to beat licensed distillation: {open_subsidy_threshold:.3f}",
        "Auction: both treatments allocate the voucher to E1; second-price payment=7.0, first-price illustrative payment=7.2.",
        "Evidence status: deterministic output under illustrative, uncalibrated parameters.",
    ]
    (ROOT / "outputs" / "fresh_run.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
