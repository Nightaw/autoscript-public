from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from common.resolution_detector import parse_resolution_log
from common.stall_detector import parse_output_log, parse_timeout_log


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"


@dataclass(frozen=True)
class DemoScenario:
    name: str
    title: str
    description: str
    output_log: str
    timeout_log: str
    resolution_log: str


SCENARIOS: dict[str, DemoScenario] = {
    "baseline_playback": DemoScenario(
        name="baseline_playback",
        title="Baseline Playback Quality Run",
        description=(
            "Mock worker job that simulates a playback task, then combines output-state "
            "stalls, timeout clusters, and resolution transitions into one structured report."
        ),
        output_log="logs/demo_player.log",
        timeout_log="logs/demo_timeout.log",
        resolution_log="logs/demo_resolution.log",
    )
}


def list_scenarios() -> list[dict]:
    return [
        {
            "name": scenario.name,
            "title": scenario.title,
            "description": scenario.description,
        }
        for scenario in SCENARIOS.values()
    ]


def run_demo_scenario(name: str) -> dict:
    if name not in SCENARIOS:
        raise KeyError(f"Unknown scenario: {name}")

    scenario = SCENARIOS[name]
    output_summary = parse_output_log(SAMPLES / scenario.output_log)
    timeout_summary = parse_timeout_log(SAMPLES / scenario.timeout_log)
    resolution_summary = parse_resolution_log(SAMPLES / scenario.resolution_log)

    return {
        "scenario": {
            "name": scenario.name,
            "title": scenario.title,
            "description": scenario.description,
        },
        "metrics": {
            "output_stalls": output_summary,
            "timeout_clusters": timeout_summary,
            "resolution_timeline": resolution_summary,
        },
        "summary": {
            "stall_count": output_summary["count"],
            "timeout_cluster_count": timeout_summary["count"],
            "resolution_change_count": resolution_summary["count"],
            "final_resolution": resolution_summary["last_resolution"],
        },
    }
