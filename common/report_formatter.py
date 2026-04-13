from __future__ import annotations

from common.models import JobReport


def render_markdown_report(report: dict) -> str:
    scenario = report["scenario"]
    summary = report["summary"]
    lines = [
        f"# {scenario['title']}",
        "",
        scenario["description"],
        "",
        "## Summary",
        "",
        f"- Stall intervals: {summary['stall_count']}",
        f"- Timeout clusters: {summary['timeout_cluster_count']}",
        f"- Resolution changes: {summary['resolution_change_count']}",
        f"- Final resolution: {summary['final_resolution']}",
        "",
        "## Devices",
        "",
    ]
    for device in report["devices"]:
        lines.append(
            f"- `{device['device_id']}` | {device['platform']} {device['os_version']} | {device['model']} | {device['role']}"
        )

    lines.extend(["", "## Execution Steps", ""])
    for step in report["execution"]["steps"]:
        lines.append(
            f"- `{step['name']}` | {step['status']} | {step['duration_sec']}s | {step['details']}"
        )

    lines.extend(["", "## Metric Outputs", ""])
    lines.append(
        f"- Output-state stalls: {report['metrics']['output_stalls']['count']} intervals"
    )
    lines.append(
        f"- Timeout clusters: {report['metrics']['timeout_clusters']['count']} windows"
    )
    lines.append(
        f"- Resolution timeline points: {report['metrics']['resolution_timeline']['count']} changes"
    )
    lines.append(
        f"- App-log resolution points: {report['metrics']['app_log_resolution_timeline']['count']} changes"
    )
    return "\n".join(lines)
