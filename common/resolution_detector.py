from __future__ import annotations

from collections import defaultdict
from datetime import datetime
import json
import re
from pathlib import Path
from typing import Iterable


RAW_SIZE_PATTERN = re.compile(
    r"(?P<ts>\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*?c2::u32 raw\.size\.(?P<axis>height|width) = (?P<value>\d+)"
)


def _parse_timestamp(timestamp_str: str, year: int | None = None) -> float:
    active_year = year or datetime.now().year
    return datetime.strptime(f"{active_year}-{timestamp_str}", "%Y-%m-%d %H:%M:%S.%f").timestamp()


def canonical_resolution(width: int, height: int) -> str:
    heights = [360, 480, 540, 720, 1080, 2160]
    widths = [640, 854, 960, 1280, 1920, 3840]

    input_max = max(width, height)
    input_min = min(width, height)

    min_diff = float("inf")
    best_index = 0
    for index, (std_width, std_height) in enumerate(zip(widths, heights)):
        diff = min(abs(max(std_width, std_height) - input_max), abs(min(std_width, std_height) - input_min))
        if diff < min_diff or (diff == min_diff and index > best_index):
            min_diff = diff
            best_index = index

    return ["360P", "540P", "540P", "720P", "1080P", "4K"][best_index]


def extract_resolution_events(
    lines: Iterable[str],
    year: int | None = None,
    blacklist: Iterable[str] | None = None,
) -> list[dict]:
    paired: dict[str, dict[str, str]] = defaultdict(dict)
    blocked = set(blacklist or [])

    for line in lines:
        match = RAW_SIZE_PATTERN.search(line)
        if not match:
            continue
        paired[match.group("ts")][match.group("axis")] = match.group("value")

    events: list[dict] = []
    for timestr in sorted(paired.keys()):
        item = paired[timestr]
        if "width" not in item or "height" not in item:
            continue
        width = int(item["width"])
        height = int(item["height"])
        raw = f"{width}x{height}"
        if raw in blocked or f"{height}x{width}" in blocked:
            continue

        resolution = canonical_resolution(width, height)
        if events and events[-1]["resolution"] == resolution:
            continue

        events.append(
            {
                "timestr": timestr,
                "time": _parse_timestamp(timestr, year=year),
                "resolution": resolution,
                "resolution_raw": raw,
            }
        )

    return events


def summarize_resolution_events(events: list[dict]) -> dict:
    return {
        "count": len(events),
        "first_resolution": events[0]["resolution"] if events else None,
        "last_resolution": events[-1]["resolution"] if events else None,
        "events": events,
    }


def parse_resolution_log(
    path: str | Path, year: int | None = None, blacklist: Iterable[str] | None = None
) -> dict:
    file_path = Path(path)
    events = extract_resolution_events(
        file_path.read_text(encoding="utf-8").splitlines(),
        year=year,
        blacklist=blacklist,
    )
    return summarize_resolution_events(events)


def to_pretty_json(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)
