from __future__ import annotations

from dataclasses import asdict, dataclass
import json


SYNC_SOURCE = "autoscript@94614e50"


@dataclass(frozen=True)
class AdaptationUpdate:
    area: str
    source_change: str
    public_projection: str
    validation_signal: str
    risk_removed: str

    def to_dict(self) -> dict:
        return asdict(self)


RECENT_ADAPTATIONS: tuple[AdaptationUpdate, ...] = (
    AdaptationUpdate(
        area="live stream entry",
        source_change="A brittle text-based live-room selector was replaced by a stable container id.",
        public_projection="Selector strategy prefers durable resource identifiers over visible creator text.",
        validation_signal="The public model records selector kind, retry budget, and expected screen transition.",
        risk_removed="Real creator names, package ids, and production resource identifiers are not included.",
    ),
    AdaptationUpdate(
        area="gesture compatibility",
        source_change="A scenario-specific drag helper was replaced by the common Android swipe primitive.",
        public_projection="Gestures are represented as normalized coordinates with one shared adapter.",
        validation_signal="The sample plan exposes the same swipe vector through a reusable action object.",
        risk_removed="Device-specific resolution, brand-specific gesture tuning, and private helper names are removed.",
    ),
    AdaptationUpdate(
        area="short video stall guard",
        source_change="The short-video flow now tracks no-audio video state across swipes before classifying stalls.",
        public_projection="The public state machine keeps a no-audio-video flag separate from transient no-audio events.",
        validation_signal="A deterministic sample run shows the guard retaining stall evidence after a no-audio transition.",
        risk_removed="Internal app ids, real title selectors, and production task ids are replaced with demo labels.",
    ),
    AdaptationUpdate(
        area="device inventory rollout",
        source_change="Active device support and historical device support were split during the iOS device update.",
        public_projection="The demo keeps active inventory and rollout history as separate records.",
        validation_signal="The exported snapshot contains active devices plus a dated history entry.",
        risk_removed="Real device serial numbers, IP addresses, and lab host names are not copied.",
    ),
)


def list_recent_adaptations() -> list[dict]:
    return [item.to_dict() for item in RECENT_ADAPTATIONS]


def build_adaptation_snapshot() -> dict:
    return {
        "source": SYNC_SOURCE,
        "theme": "recent compatibility and agent-readiness sync",
        "summary": {
            "update_count": len(RECENT_ADAPTATIONS),
            "covered_layers": [
                "selector strategy",
                "gesture adapter",
                "playback state guard",
                "device rollout inventory",
            ],
        },
        "sample_device_rollout": {
            "active": [
                {"device_id": "demo-ios-01", "platform": "ios", "role": "media-playback"},
                {"device_id": "demo-android-01", "platform": "android", "role": "short-video"},
            ],
            "history": [
                {
                    "date": "2026-05-25",
                    "change": "Moved retired iOS playback devices out of active support and kept a history record.",
                }
            ],
        },
        "sample_action_plan": {
            "entry_selector": {
                "strategy": "resource-id",
                "retry_budget": 10,
                "fallback": "surface transition check",
            },
            "gesture": {
                "adapter": "android_swipe",
                "start": [0.4, 0.8],
                "end": [0.7, 0.8],
                "duration_ms": 100,
            },
            "stall_guard_state": {
                "flag_stall_before_swipe": True,
                "flag_stall": True,
                "noaudio_flag": False,
                "noaudio_video_flag": True,
                "classification": "preserve_stall_evidence",
            },
        },
        "adaptations": list_recent_adaptations(),
    }


def snapshot_to_pretty_json(snapshot: dict) -> str:
    return json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"


def render_adaptation_markdown(snapshot: dict) -> str:
    lines = [
        "# Recent Adaptation Sync",
        "",
        f"- Source snapshot: `{snapshot['source']}`",
        f"- Theme: {snapshot['theme']}",
        f"- Update count: `{snapshot['summary']['update_count']}`",
        "",
        "## Covered Layers",
        "",
    ]
    lines.extend(f"- {item}" for item in snapshot["summary"]["covered_layers"])
    lines.extend(["", "## Updates", ""])

    for item in snapshot["adaptations"]:
        lines.extend(
            [
                f"### {item['area']}",
                "",
                f"- Source change: {item['source_change']}",
                f"- Public projection: {item['public_projection']}",
                f"- Validation signal: {item['validation_signal']}",
                f"- Risk removed: {item['risk_removed']}",
                "",
            ]
        )

    action = snapshot["sample_action_plan"]
    lines.extend(
        [
            "## Sample Action Plan",
            "",
            f"- Entry selector strategy: `{action['entry_selector']['strategy']}`",
            f"- Gesture adapter: `{action['gesture']['adapter']}`",
            f"- Stall classification: `{action['stall_guard_state']['classification']}`",
            "",
            "## Device Rollout Model",
            "",
            f"- Active devices: `{len(snapshot['sample_device_rollout']['active'])}`",
            f"- History entries: `{len(snapshot['sample_device_rollout']['history'])}`",
            "",
        ]
    )
    return "\n".join(lines)
