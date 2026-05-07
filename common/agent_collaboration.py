from __future__ import annotations

from dataclasses import asdict, dataclass
import json


CONVERSATION_ID = "019e0097-c570-7e53-9d0d-b9859dcd2404"


@dataclass(frozen=True)
class RepoRole:
    name: str
    public_status: str
    responsibility: str
    handoff: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class AgentTaskSpec:
    task_id: str
    natural_language: str
    device_id: str
    app_name: str
    scenario: str
    watch_duration_sec: int
    swipe_interval_sec: int
    output_path: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CollaborationEvent:
    stage: str
    owner_repo: str
    summary: str
    artifact: str

    def to_dict(self) -> dict:
        return asdict(self)


REPO_ROLES: tuple[RepoRole, ...] = (
    RepoRole(
        name="clawscript-public",
        public_status="published companion public repo",
        responsibility="Turns a natural-language automation request into an agent-friendly SOP and executable task.",
        handoff="Agent task spec, step guard policy, app entry strategy, debug artifact contract.",
    ),
    RepoRole(
        name="autoscript-public",
        public_status="project represented by this public demo",
        responsibility="Runs worker-side execution, parser registration, metric extraction, and report formatting.",
        handoff="Structured JSON result, Markdown report, parser summaries, and lifecycle state.",
    ),
    RepoRole(
        name="autoSampler-public",
        public_status="published companion public repo",
        responsibility="Packages post-capture review evidence, storyboards, manifests, and static portfolio artifacts.",
        handoff="Review score, storyboard images, artifact manifest, and GitHub Pages bundle.",
    ),
)


SAMPLE_AGENT_TASKS: dict[str, AgentTaskSpec] = {
    "8088": AgentTaskSpec(
        task_id="8088",
        natural_language=(
            "Open a short-video app, enter playback, swipe every 5 seconds, "
            "watch for 60 seconds, detect stalls, and export a structured result."
        ),
        device_id="demo-android-01",
        app_name="ShortVideoDemo",
        scenario="short_video.agent_stall.basic",
        watch_duration_sec=60,
        swipe_interval_sec=5,
        output_path="samples/results/agent_short_video_report.json",
    ),
    "8099": AgentTaskSpec(
        task_id="8099",
        natural_language=(
            "Run a short-video playback smoke test with agent-controlled entry, "
            "popup handling, swipe actions, and post-run quality parsing."
        ),
        device_id="demo-android-02",
        app_name="ShortVideoDemo",
        scenario="short_video.agent_smoke.basic",
        watch_duration_sec=45,
        swipe_interval_sec=5,
        output_path="samples/results/agent_smoke_report.json",
    ),
}


def list_repo_roles() -> list[dict]:
    return [role.to_dict() for role in REPO_ROLES]


def list_agent_tasks() -> list[dict]:
    return [task.to_dict() for task in SAMPLE_AGENT_TASKS.values()]


def build_collaboration_trace(task_id: str = "8088") -> dict:
    if task_id not in SAMPLE_AGENT_TASKS:
        raise KeyError(f"Unknown agent task: {task_id}")

    task = SAMPLE_AGENT_TASKS[task_id]
    events = (
        CollaborationEvent(
            stage="agent_planning",
            owner_repo="clawscript-public",
            summary="Normalize the target app family, duration, swipe cadence, validation gates, and downstream repo contracts into an agent task spec.",
            artifact="agent_task_contract.json",
        ),
        CollaborationEvent(
            stage="sop_generation",
            owner_repo="clawscript-public",
            summary="Convert the natural-language request into an SOP with popup handling, entry strategy, guard rails, and debug capture.",
            artifact="agent_sop.md",
        ),
        CollaborationEvent(
            stage="worker_execution",
            owner_repo="autoscript-public",
            summary="Execute the task through the worker abstraction, collect logs and video artifacts, then run parser modules.",
            artifact=task.output_path,
        ),
        CollaborationEvent(
            stage="evidence_packaging",
            owner_repo="autoSampler-public",
            summary="Package worker output into review evidence, storyboards, manifests, and portfolio-facing static artifacts.",
            artifact="docs/agent-handoffs.json",
        ),
    )

    return {
        "conversation_id": CONVERSATION_ID,
        "collaboration": "clawscript-public -> autoscript-public -> autoSampler-public",
        "repos": list_repo_roles(),
        "task": task.to_dict(),
        "handoff_contract": {
            "task_id": task.task_id,
            "device_id": task.device_id,
            "app": task.app_name,
            "scenario": task.scenario,
            "watch_duration_sec": task.watch_duration_sec,
            "swipe_interval_sec": task.swipe_interval_sec,
            "output_path": task.output_path,
        },
        "agent_framework": {
            "context_model": "AgentContext",
            "strategy_interfaces": [
                "PopupHandler",
                "PlayEntryHandler",
                "PlayValidator",
                "ContentClassifier",
                "Swiper",
                "StallDetector",
            ],
            "runtime_guards": [
                "step budget",
                "debug screenshot/video capture",
                "play-state validation",
                "stall evidence collection",
            ],
            "why_it_matters": (
                "The runner can change app-specific strategies without rewriting the worker, "
                "parser, or report layers."
            ),
        },
        "events": [event.to_dict() for event in events],
        "public_projection": {
            "kept": [
                "repo responsibilities",
                "handoff contract",
                "agent strategy shape",
                "worker/parser/report boundary",
                "sample JSON and Markdown artifacts",
            ],
            "removed": [
                "internal app identifiers",
                "real device inventory",
                "private SOP content",
                "binary artifacts",
                "company-specific endpoints",
            ],
        },
    }


def trace_to_pretty_json(trace: dict) -> str:
    return json.dumps(trace, ensure_ascii=False, indent=2) + "\n"


def render_collaboration_markdown(trace: dict) -> str:
    task = trace["task"]
    lines = [
        "# Agent Collaboration Trace",
        "",
        f"- Conversation reference: `{trace['conversation_id']}`",
        f"- Collaboration path: `{trace['collaboration']}`",
        f"- Demo task: `{task['task_id']}` / `{task['scenario']}`",
        "",
        "## Repo Responsibilities",
        "",
    ]

    for repo in trace["repos"]:
        lines.extend(
            [
                f"### {repo['name']}",
                "",
                f"- Public status: {repo['public_status']}",
                f"- Responsibility: {repo['responsibility']}",
                f"- Handoff: {repo['handoff']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Task Contract",
            "",
            f"- App profile: `{task['app_name']}`",
            f"- Device: `{task['device_id']}`",
            f"- Watch duration: `{task['watch_duration_sec']}s`",
            f"- Swipe interval: `{task['swipe_interval_sec']}s`",
            f"- Output artifact: `{task['output_path']}`",
            "",
            "## Agent Runtime Shape",
            "",
            f"- Context model: `{trace['agent_framework']['context_model']}`",
            "- Strategy interfaces: "
            + ", ".join(f"`{item}`" for item in trace["agent_framework"]["strategy_interfaces"]),
            "- Runtime guards: "
            + ", ".join(f"`{item}`" for item in trace["agent_framework"]["runtime_guards"]),
            f"- Design point: {trace['agent_framework']['why_it_matters']}",
            "",
            "## Execution Trace",
            "",
        ]
    )

    for event in trace["events"]:
        lines.extend(
            [
                f"### {event['stage']}",
                "",
                f"- Owner repo: `{event['owner_repo']}`",
                f"- Summary: {event['summary']}",
                f"- Artifact: `{event['artifact']}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Public Projection",
            "",
            "Kept in this repo:",
        ]
    )
    lines.extend(f"- {item}" for item in trace["public_projection"]["kept"])
    lines.extend(["", "Removed from this repo:"])
    lines.extend(f"- {item}" for item in trace["public_projection"]["removed"])
    lines.append("")
    return "\n".join(lines)
