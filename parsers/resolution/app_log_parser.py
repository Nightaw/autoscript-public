from __future__ import annotations

from datetime import datetime
import re
from pathlib import Path

from common.parser_registry import mark_parser_run
from common.resolution_detector import canonical_resolution


RENDER_STATS_PATTERN = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}\.\d{3}).*?render_stats.*?"
    r"rnd_w:(?P<width>\d+)\s+rnd_h:(?P<height>\d+)",
    re.IGNORECASE,
)


def extract_resolutions_from_app_render_stats(log_path: str | Path) -> list[dict]:
    events: list[dict] = []
    for line in Path(log_path).read_text(encoding="utf-8").splitlines():
        match = RENDER_STATS_PATTERN.search(line)
        if not match:
            continue
        width = int(match.group("width"))
        height = int(match.group("height"))
        if width <= 0 or height <= 0:
            continue
        resolution = canonical_resolution(width, height)
        if events and events[-1]["resolution"] == resolution:
            continue
        timestamp = datetime.strptime(
            f"{match.group('date')} {match.group('time')}", "%Y-%m-%d %H:%M:%S.%f"
        ).timestamp()
        events.append(
            {
                "timestr": f"{match.group('date')} {match.group('time')}",
                "time": timestamp,
                "resolution": resolution,
                "resolution_raw": f"{width}x{height}",
            }
        )

    mark_parser_run("resolution.app_render_stats")
    return events
