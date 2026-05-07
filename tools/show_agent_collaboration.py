from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.agent_collaboration import (  # noqa: E402
    build_collaboration_trace,
    render_collaboration_markdown,
    trace_to_pretty_json,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Show the public agent-collaboration trace.")
    parser.add_argument("--task-id", default="8088", help="Sample agent task id.")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format.",
    )
    args = parser.parse_args()

    trace = build_collaboration_trace(args.task_id)
    if args.format == "markdown":
        print(render_collaboration_markdown(trace), end="")
    else:
        print(trace_to_pretty_json(trace), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
