from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
import re
from pathlib import Path
from typing import Iterable


EVENT_PATTERN = re.compile(
    r"(?P<ts>\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*?(?P<event>startOutput|stopOutput)\(\)"
)


@dataclass
class StallEvent:
    start: float
    end: float

    @property
    def duration(self) -> float:
        return round(self.end - self.start, 3)


def _parse_timestamp(timestamp_str: str, year: int | None = None) -> float:
    active_year = year or datetime.now().year
    full = f"{active_year}-{timestamp_str}"
    return datetime.strptime(full, "%Y-%m-%d %H:%M:%S.%f").timestamp()


def extract_stalls(lines: Iterable[str], year: int | None = None) -> list[StallEvent]:
    pending_stop: float | None = None
    stalls: list[StallEvent] = []

    for line in lines:
        match = EVENT_PATTERN.search(line)
        if not match:
            continue

        current_time = _parse_timestamp(match.group("ts"), year=year)
        event = match.group("event")

        if event == "stopOutput":
            pending_stop = current_time
            continue

        if event == "startOutput" and pending_stop is not None and current_time >= pending_stop:
            stalls.append(StallEvent(start=pending_stop, end=current_time))
            pending_stop = None

    return stalls


def summarize_stalls(stalls: list[StallEvent]) -> dict:
    if not stalls:
        return {
            "count": 0,
            "total_duration": 0.0,
            "max_duration": 0.0,
            "stalls": [],
        }

    durations = [stall.duration for stall in stalls]
    return {
        "count": len(stalls),
        "total_duration": round(sum(durations), 3),
        "max_duration": round(max(durations), 3),
        "stalls": [
            {
                "start": stall.start,
                "end": stall.end,
                "duration": stall.duration,
            }
            for stall in stalls
        ],
    }


def parse_log_file(path: str | Path, year: int | None = None) -> dict:
    file_path = Path(path)
    stalls = extract_stalls(file_path.read_text(encoding="utf-8").splitlines(), year=year)
    return summarize_stalls(stalls)


def to_pretty_json(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)
