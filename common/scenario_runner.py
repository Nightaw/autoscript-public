from __future__ import annotations

from common.models import ScenarioDefinition, StepResult


STEP_LIBRARY: dict[str, StepResult] = {
    "launch_app": StepResult(
        name="launch_app",
        status="passed",
        duration_sec=2.4,
        details="Bootstrapped app session and confirmed player landing page.",
    ),
    "warmup_playback": StepResult(
        name="warmup_playback",
        status="passed",
        duration_sec=5.2,
        details="Started baseline playback and collected initial player telemetry.",
    ),
    "background_foreground": StepResult(
        name="background_foreground",
        status="passed",
        duration_sec=4.8,
        details="Sent app to background and restored playback session.",
    ),
    "seek_forward": StepResult(
        name="seek_forward",
        status="passed",
        duration_sec=3.1,
        details="Performed forward seek to trigger decoder and rendering transitions.",
    ),
    "quality_switch": StepResult(
        name="quality_switch",
        status="passed",
        duration_sec=3.9,
        details="Changed playback quality and tracked resulting resolution timeline.",
    ),
}


def run_scenario_steps(scenario: ScenarioDefinition) -> dict:
    steps = [STEP_LIBRARY[name] for name in scenario.steps]
    total_duration = round(sum(step.duration_sec for step in steps), 2)
    return {
        "status": "passed",
        "total_duration_sec": total_duration,
        "steps": [step.to_dict() for step in steps],
    }
