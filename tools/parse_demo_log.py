from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.demo_log_parser import parse_log_file, to_pretty_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse a sanitized demo player log and extract stall intervals."
    )
    parser.add_argument("log_path", help="Path to the demo log file.")
    parser.add_argument("--year", type=int, default=None, help="Optional explicit year.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    result = parse_log_file(args.log_path, year=args.year)
    print(to_pretty_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
