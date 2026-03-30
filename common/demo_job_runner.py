from __future__ import annotations

from pathlib import Path

from common.device_registry import list_devices as registry_list_devices
from common.device_registry import select_devices
from common.models import JobReport, ScenarioDefinition
from common.resolution_detector import parse_resolution_log
from common.report_formatter import render_markdown_report
from common.scenario_runner import run_scenario_steps
from common.stall_detector import parse_output_log, parse_timeout_log


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"


SCENARIOS: dict[str, ScenarioDefinition] = {
    "baseline_playback": ScenarioDefinition(
        name="baseline_playback",
        title="Baseline Playback Quality Run",
        description=(
            "Mock worker job that simulates a playback task, then combines output-state "
            "stalls, timeout clusters, and resolution transitions into one structured report."
        ),
        steps=(
            "launch_app",
            "warmup_playback",
            "background_foreground",
            "seek_forward",
            "quality_switch",
        ),
        preferred_platforms=("android", "ios"),
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
            "steps": list(scenario.steps),
            "preferred_platforms": list(scenario.preferred_platforms),
        }
        for scenario in SCENARIOS.values()
    ]


def list_available_devices(platform: str | None = None, role: str | None = None) -> list[dict]:
    return registry_list_devices(platform=platform, role=role)


def run_demo_scenario(name: str) -> dict:
    if name not in SCENARIOS:
        raise KeyError(f"Unknown scenario: {name}")

    scenario = SCENARIOS[name]
    devices = select_devices(scenario.preferred_platforms)
    execution = run_scenario_steps(scenario)
    output_summary = parse_output_log(SAMPLES / scenario.output_log)
    timeout_summary = parse_timeout_log(SAMPLES / scenario.timeout_log)
    resolution_summary = parse_resolution_log(SAMPLES / scenario.resolution_log)

    report = JobReport(
        scenario={
            "name": scenario.name,
            "title": scenario.title,
            "description": scenario.description,
            "steps": list(scenario.steps),
        },
        devices=devices,
        execution=execution,
        metrics={
            "output_stalls": output_summary,
            "timeout_clusters": timeout_summary,
            "resolution_timeline": resolution_summary,
        },
        summary={
            "stall_count": output_summary["count"],
            "timeout_cluster_count": timeout_summary["count"],
            "resolution_change_count": resolution_summary["count"],
            "final_resolution": resolution_summary["last_resolution"],
        },
        artifacts={
            "sample_payload": "samples/payloads/baseline_playback.json",
            "sample_markdown_report": "samples/results/baseline_playback_report.md",
            "sample_json_report": "samples/results/baseline_playback_report.json",
        },
    )
    return report.to_dict()


def build_markdown_report(name: str) -> str:
    return render_markdown_report(run_demo_scenario(name))
