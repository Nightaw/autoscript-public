from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.adaptation_updates import (
    build_adaptation_snapshot,
    render_adaptation_markdown,
    snapshot_to_pretty_json,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Show the latest public-safe adaptation sync snapshot.")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()

    snapshot = build_adaptation_snapshot()
    if args.format == "markdown":
        print(render_adaptation_markdown(snapshot))
    else:
        print(snapshot_to_pretty_json(snapshot), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
