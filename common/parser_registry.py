from __future__ import annotations

from common.state import PARSER_STATE


PARSER_REGISTRY: dict[str, dict] = {
    "stall.output_state": {
        "category": "stall",
        "source": "sys_log",
        "description": "Pair startOutput/stopOutput events into stall intervals.",
    },
    "stall.timeout_cluster": {
        "category": "stall",
        "source": "sys_log",
        "description": "Cluster timeout-like events into higher-confidence stall windows.",
    },
    "stall.cloud_game_pid": {
        "category": "stall",
        "source": "sys_log",
        "description": "Track codec state transitions per pid for cloud-game-like logs.",
    },
    "resolution.raw_size": {
        "category": "resolution",
        "source": "sys_log",
        "description": "Extract decoder raw width/height changes into a normalized timeline.",
    },
    "resolution.app_render_stats": {
        "category": "resolution",
        "source": "app_log",
        "description": "Extract render_stats width/height changes from RTC-style app logs.",
    },
}

PARSER_STATE.available_parsers = sorted(PARSER_REGISTRY.keys())


def list_parsers(category: str | None = None) -> list[dict]:
    items = []
    for name, meta in sorted(PARSER_REGISTRY.items()):
        if category and meta["category"] != category:
            continue
        items.append({"name": name, **meta})
    return items


def mark_parser_run(name: str) -> None:
    PARSER_STATE.last_parser_run = name
