from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
import re
from pathlib import Path
from typing import Iterable


OUTPUT_EVENT_PATTERN = re.compile(
    r"(?P<ts>\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*?(?P<event>startOutput|stopOutput)\(\)"
)

TIMEOUT_EVENT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "video_timeout",
        re.compile(
            r"(?P<ts>\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{3})?).*?"
            r"VideoRecorder.*?dequeueOutputBuffer timeout"
        ),
    ),
    (
        "audio_timeout",
        re.compile(
            r"(?P<ts>\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{3})?).*?"
            r"NativeAudioRecorder.*?dequeueOutputBuffer timeout"
        ),
    ),
    (
        "display_idle",
        re.compile(
            r"(?P<ts>\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{3})?).*?"
            r"DisplayBase::CommitThread: Received idle timeout"
        ),
    ),
    (
        "render_timeout",
        re.compile(
            r"(?P<ts>\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{3})?).*?"
            r"RenderInspector.*?(DequeueBuffer|QueueBuffer) time out"
        ),
    ),
)


@dataclass(frozen=True)
class StallInterval:
    start: float
    end: float
    sources: tuple[str, ...] = ()
    event_count: int = 0

    @property
    def duration(self) -> float:
        return round(self.end - self.start, 3)


def _parse_timestamp(timestamp_str: str, year: int | None = None) -> float:
    active_year = year or datetime.now().year
    full = f"{active_year}-{timestamp_str}"
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(full, fmt).timestamp()
        except ValueError:
            continue
    raise ValueError(f"Unsupported timestamp format: {timestamp_str}")


def extract_output_stalls(lines: Iterable[str], year: int | None = None) -> list[StallInterval]:
    pending_stop: float | None = None
    stalls: list[StallInterval] = []

    for line in lines:
        match = OUTPUT_EVENT_PATTERN.search(line)
        if not match:
            continue

        current_time = _parse_timestamp(match.group("ts"), year=year)
        event = match.group("event")

        if event == "stopOutput":
            pending_stop = current_time
            continue

        if event == "startOutput" and pending_stop is not None and current_time >= pending_stop:
            stalls.append(StallInterval(start=pending_stop, end=current_time, sources=("output_state",), event_count=2))
            pending_stop = None

    return stalls


def extract_timeout_events(
    lines: Iterable[str], year: int | None = None, allowed_sources: Iterable[str] | None = None
) -> list[dict]:
    allowed = set(allowed_sources or [name for name, _ in TIMEOUT_EVENT_PATTERNS])
    events: list[dict] = []

    for line in lines:
        for source, pattern in TIMEOUT_EVENT_PATTERNS:
            if source not in allowed:
                continue
            match = pattern.search(line)
            if not match:
                continue
            events.append(
                {
                    "ts": _parse_timestamp(match.group("ts"), year=year),
                    "source": source,
                    "raw": line.strip(),
                }
            )
            break

    events.sort(key=lambda item: item["ts"])
    return events


def cluster_timeout_events(events: list[dict], max_gap: float = 1.0, min_events: int = 3) -> list[StallInterval]:
    if not events:
        return []

    clusters: list[list[dict]] = [[events[0]]]
    for event in events[1:]:
        if event["ts"] - clusters[-1][-1]["ts"] <= max_gap:
            clusters[-1].append(event)
        else:
            clusters.append([event])

    windows: list[StallInterval] = []
    for cluster in clusters:
        if len(cluster) < min_events:
            continue
        windows.append(
            StallInterval(
                start=cluster[0]["ts"],
                end=cluster[-1]["ts"],
                sources=tuple(sorted({item["source"] for item in cluster})),
                event_count=len(cluster),
            )
        )
    return windows


def summarize_stalls(stalls: list[StallInterval]) -> dict:
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
                "sources": list(stall.sources),
                "event_count": stall.event_count,
            }
            for stall in stalls
        ],
    }


def parse_output_log(path: str | Path, year: int | None = None) -> dict:
    file_path = Path(path)
    stalls = extract_output_stalls(file_path.read_text(encoding="utf-8").splitlines(), year=year)
    return summarize_stalls(stalls)


def parse_timeout_log(
    path: str | Path,
    year: int | None = None,
    max_gap: float = 1.0,
    min_events: int = 3,
) -> dict:
    file_path = Path(path)
    events = extract_timeout_events(file_path.read_text(encoding="utf-8").splitlines(), year=year)
    stalls = cluster_timeout_events(events, max_gap=max_gap, min_events=min_events)
    summary = summarize_stalls(stalls)
    summary["input_event_count"] = len(events)
    return summary


def to_pretty_json(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)
