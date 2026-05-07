# Agent Collaboration Trace

- Conversation reference: `019e0097-c570-7e53-9d0d-b9859dcd2404`
- Collaboration path: `manualscript -> clawscript -> autoscript -> autoscript-public`
- Demo task: `8088` / `short_video.agent_stall.basic`

## Repo Responsibilities

### manualscript

- Public status: source repo, not published in this demo
- Responsibility: Keeps config-driven task profiles and repeatable scenario definitions.
- Handoff: Scenario name, app profile, device constraints, duration, and metric expectations.

### clawscript

- Public status: planned companion public repo
- Responsibility: Turns a natural-language automation request into an agent-friendly SOP and executable task.
- Handoff: Agent task spec, step guard policy, app entry strategy, debug artifact contract.

### autoscript

- Public status: project represented by this public demo
- Responsibility: Runs worker-side execution, parser registration, metric extraction, and report formatting.
- Handoff: Structured JSON result, Markdown report, parser summaries, and lifecycle state.

## Task Contract

- App profile: `ShortVideoDemo`
- Device: `demo-android-01`
- Watch duration: `60s`
- Swipe interval: `5s`
- Output artifact: `samples/results/agent_short_video_report.json`

## Agent Runtime Shape

- Context model: `AgentContext`
- Strategy interfaces: `PopupHandler`, `PlayEntryHandler`, `PlayValidator`, `ContentClassifier`, `Swiper`, `StallDetector`
- Runtime guards: `step budget`, `debug screenshot/video capture`, `play-state validation`, `stall evidence collection`
- Design point: The runner can change app-specific strategies without rewriting the worker, parser, or report layers.

## Execution Trace

### scenario_contract

- Owner repo: `manualscript`
- Summary: Normalize the target app, duration, swipe cadence, and expected metrics into a stable task contract.
- Artifact: `agent_task_contract.json`

### agent_planning

- Owner repo: `clawscript`
- Summary: Convert the natural-language request into an SOP with popup handling, entry strategy, guard rails, and debug capture.
- Artifact: `agent_sop.md`

### worker_execution

- Owner repo: `autoscript`
- Summary: Execute the task through the worker abstraction, collect logs and video artifacts, then run parser modules.
- Artifact: `samples/results/agent_short_video_report.json`

### public_projection

- Owner repo: `autoscript-public`
- Summary: Publish a sanitized, runnable demo that preserves architecture, contracts, parser outputs, and interview-friendly evidence.
- Artifact: `docs/agent-collaboration.md`

## Public Projection

Kept in this repo:
- repo responsibilities
- handoff contract
- agent strategy shape
- worker/parser/report boundary
- sample JSON and Markdown artifacts

Removed from this repo:
- internal app identifiers
- real device inventory
- private SOP content
- binary artifacts
- company-specific endpoints
