from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from parsers.resolution.app_log_parser import extract_resolutions_from_app_render_stats
from common.resolution_detector import to_pretty_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse a sanitized RTC-style app log and extract resolution transitions."
    )
    parser.add_argument("log_path", help="Path to the demo app log file.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    events = extract_resolutions_from_app_render_stats(args.log_path)
    result = {
        "count": len(events),
        "first_resolution": events[0]["resolution"] if events else None,
        "last_resolution": events[-1]["resolution"] if events else None,
        "events": events,
    }
    print(to_pretty_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
