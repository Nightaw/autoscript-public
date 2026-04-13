from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.job_queue import enqueue_job, list_jobs, process_next_job, reset_jobs
from common.stall_detector import to_pretty_json


def main() -> int:
    reset_jobs()
    queued = enqueue_job("baseline_playback")
    finished = process_next_job()
    print(
        to_pretty_json(
            {
                "queued": queued,
                "finished": finished,
                "jobs": list_jobs(),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
