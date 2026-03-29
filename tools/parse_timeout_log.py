from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.stall_detector import parse_timeout_log, to_pretty_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse a sanitized timeout-heavy media log and cluster potential stall windows."
    )
    parser.add_argument("log_path", help="Path to the demo timeout log file.")
    parser.add_argument("--year", type=int, default=None, help="Optional explicit year.")
    parser.add_argument("--max-gap", type=float, default=1.0, help="Max gap between adjacent events in a cluster.")
    parser.add_argument("--min-events", type=int, default=3, help="Minimum events required to emit a stall window.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    result = parse_timeout_log(
        args.log_path,
        year=args.year,
        max_gap=args.max_gap,
        min_events=args.min_events,
    )
    print(to_pretty_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
