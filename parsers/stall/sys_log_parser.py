from __future__ import annotations

from datetime import datetime
import re
from pathlib import Path
from typing import Iterable

from common.parser_registry import mark_parser_run
from common.stall_detector import (
    cluster_timeout_events,
    extract_output_stalls,
    extract_timeout_events,
)


CODEC_STATE_PATTERN = re.compile(
    r"(?P<ts>\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*?getCodecState : (?P<state>\d).*?getpid : (?P<pid>\d+)"
)


def _to_timestamp(ts: str, year: int | None = None) -> float:
    active_year = year or datetime.now().year
    return datetime.strptime(f"{active_year}-{ts}", "%Y-%m-%d %H:%M:%S.%f").timestamp()


def extract_stalls_by_output(log_path: str | Path, year: int | None = None) -> list[dict]:
    lines = Path(log_path).read_text(encoding="utf-8").splitlines()
    stalls = extract_output_stalls(lines, year=year)
    mark_parser_run("stall.output_state")
    return [
        {"start": stall.start, "end": stall.end, "duration": stall.duration}
        for stall in stalls
    ]


def extract_stalls_by_timeout_cluster(
    log_path: str | Path, year: int | None = None, max_gap: float = 1.0, min_events: int = 3
) -> list[dict]:
    lines = Path(log_path).read_text(encoding="utf-8").splitlines()
    events = extract_timeout_events(lines, year=year)
    clusters = cluster_timeout_events(events, max_gap=max_gap, min_events=min_events)
    mark_parser_run("stall.timeout_cluster")
    return [
        {
            "start": stall.start,
            "end": stall.end,
            "duration": stall.duration,
            "sources": list(stall.sources),
            "event_count": stall.event_count,
        }
        for stall in clusters
    ]


def extract_cloud_game_pid_stalls(log_path: str | Path, year: int | None = None) -> dict:
    transitions: dict[str, list[dict]] = {}
    states: dict[str, float | None] = {}
    lines = Path(log_path).read_text(encoding="utf-8").splitlines()

    for line in lines:
        match = CODEC_STATE_PATTERN.search(line)
        if not match:
            continue
        pid = match.group("pid")
        state = match.group("state")
        ts = _to_timestamp(match.group("ts"), year=year)
        transitions.setdefault(pid, [])
        states.setdefault(pid, None)

        if state == "0" and states[pid] is None:
            states[pid] = ts
        elif state == "1" and states[pid] is not None:
            transitions[pid].append({"start": states[pid], "end": ts, "pid": pid})
            states[pid] = None

    mark_parser_run("stall.cloud_game_pid")
    return {"pids": sorted(transitions.keys()), "transitions": transitions}
