from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class JobState:
    status: str = "idle"
    current_scenario: str | None = None
    completed_steps: int = 0
    last_report_path: str | None = None


@dataclass
class ParserState:
    available_parsers: list[str] = field(default_factory=list)
    last_parser_run: str | None = None


JOB_STATE = JobState()
PARSER_STATE = ParserState()
