from __future__ import annotations

from pathlib import Path

from common.device_registry import list_devices as registry_list_devices
from common.device_registry import select_devices
from common.models import JobReport, ScenarioDefinition
from common.parser_registry import list_parsers
from common.report_formatter import render_markdown_report
from common.scenario_runner import run_scenario_steps
from common.resolution_detector import parse_resolution_log
from common.stall_detector import parse_output_log, parse_timeout_log
from parsers.resolution.app_log_parser import extract_resolutions_from_app_render_stats


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
    ),
    "rtc_app_log_validation": ScenarioDefinition(
        name="rtc_app_log_validation",
        title="RTC App Log Resolution Validation",
        description=(
            "Mock scenario focused on RTC-style render_stats app logs to demonstrate "
            "parser modularization between system logs and application logs."
        ),
        steps=(
            "launch_app",
            "warmup_playback",
            "quality_switch",
        ),
        preferred_platforms=("ios", "android"),
        output_log="logs/demo_player.log",
        timeout_log="logs/demo_timeout.log",
        resolution_log="logs/demo_resolution.log",
    ),
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
    app_log_resolution_summary = {
        "count": 0,
        "first_resolution": None,
        "last_resolution": None,
        "events": [],
    }
    app_log_path = SAMPLES / "logs" / "demo_rtc_app.log"
    if app_log_path.exists():
        app_events = extract_resolutions_from_app_render_stats(app_log_path)
        app_log_resolution_summary = {
            "count": len(app_events),
            "first_resolution": app_events[0]["resolution"] if app_events else None,
            "last_resolution": app_events[-1]["resolution"] if app_events else None,
            "events": app_events,
        }

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
            "app_log_resolution_timeline": app_log_resolution_summary,
        },
        summary={
            "stall_count": output_summary["count"],
            "timeout_cluster_count": timeout_summary["count"],
            "resolution_change_count": resolution_summary["count"],
            "app_log_resolution_change_count": app_log_resolution_summary["count"],
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


def describe_architecture() -> dict:
    return {
        "scenario_count": len(SCENARIOS),
        "available_parsers": list_parsers(),
        "device_count": len(registry_list_devices()),
    }
