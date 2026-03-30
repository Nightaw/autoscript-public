from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.demo_job_runner import build_markdown_report, list_scenarios


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export a demo scenario report as Markdown."
    )
    parser.add_argument(
        "--scenario",
        default="baseline_playback",
        help="Scenario name. Use --list to inspect available scenarios.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List scenarios and exit.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.list:
        for scenario in list_scenarios():
            print(f"{scenario['name']}: {scenario['title']}")
        return 0

    print(build_markdown_report(args.scenario))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
