from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.resolution_detector import parse_resolution_log, to_pretty_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse a sanitized decoder log and extract resolution transitions."
    )
    parser.add_argument("log_path", help="Path to the demo resolution log file.")
    parser.add_argument("--year", type=int, default=None, help="Optional explicit year.")
    parser.add_argument(
        "--blacklist",
        nargs="*",
        default=["1088x368"],
        help="Raw resolutions to ignore, e.g. 1088x368.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    result = parse_resolution_log(args.log_path, year=args.year, blacklist=args.blacklist)
    print(to_pretty_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
