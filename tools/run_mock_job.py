from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.demo_job_runner import list_scenarios, run_demo_scenario
from common.stall_detector import to_pretty_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a mock worker job and output a structured quality report."
    )
    parser.add_argument(
        "--scenario",
        default="baseline_playback",
        help="Scenario name. Use --list to see available scenarios.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available scenarios and exit.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.list:
        print(to_pretty_json({"scenarios": list_scenarios()}))
        return 0

    print(to_pretty_json(run_demo_scenario(args.scenario)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
