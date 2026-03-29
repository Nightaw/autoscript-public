from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.resolution_detector import parse_resolution_log, to_pretty_json as resolution_json
from common.stall_detector import (
    parse_output_log,
    parse_timeout_log,
    to_pretty_json as stall_json,
)


def main() -> int:
    samples = ROOT / "samples" / "logs"

    output_summary = parse_output_log(samples / "demo_player.log")
    timeout_summary = parse_timeout_log(samples / "demo_timeout.log")
    resolution_summary = parse_resolution_log(samples / "demo_resolution.log")

    print("# Output-State Stall Demo")
    print(stall_json(output_summary))
    print("\n# Timeout Cluster Demo")
    print(stall_json(timeout_summary))
    print("\n# Resolution Transition Demo")
    print(resolution_json(resolution_summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
