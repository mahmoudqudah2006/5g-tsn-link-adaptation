from __future__ import annotations

import argparse
import json
from pathlib import Path

from .channel import CorrelatedSNR
from .models import TSNStream
from .policies import FixedPolicy, ThresholdPolicy
from .simulator import simulate


def default_streams() -> list[TSNStream]:
    return [
        TSNStream("control", 2.0, 300, 2.0, 0),
        TSNStream("sensor", 5.0, 500, 5.0, 1),
        TSNStream("telemetry", 10.0, 900, 10.0, 2),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Abstract 5G-TSN link adaptation simulator")
    sub = parser.add_subparsers(dest="command", required=True)
    compare = sub.add_parser("compare")
    compare.add_argument("--duration-ms", type=float, default=2000.0)
    compare.add_argument("--seed", type=int, default=7)
    compare.add_argument("--mean-snr", type=float, default=12.0)
    compare.add_argument("--output", type=Path, default=Path("results/comparison.json"))
    args = parser.parse_args()

    results = {}
    for name, policy in [("fixed", FixedPolicy()), ("adaptive", ThresholdPolicy())]:
        channel = CorrelatedSNR(mean_db=args.mean_snr, seed=args.seed)
        results[name] = simulate(
            default_streams(), policy, channel, duration_ms=args.duration_ms, seed=args.seed
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
