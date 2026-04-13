from __future__ import annotations

from pathlib import Path

from common.parser_registry import mark_parser_run
from common.resolution_detector import extract_resolution_events


def extract_resolutions_by_raw_size(
    log_path: str | Path, year: int | None = None, blacklist: list[str] | None = None
) -> list[dict]:
    lines = Path(log_path).read_text(encoding="utf-8").splitlines()
    events = extract_resolution_events(lines, year=year, blacklist=blacklist)
    mark_parser_run("resolution.raw_size")
    return events
