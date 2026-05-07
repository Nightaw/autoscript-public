# Agent Collaboration Trace

- Conversation reference: `019e0097-c570-7e53-9d0d-b9859dcd2404`
- Collaboration path: `clawscript-public -> autoscript-public -> autoSampler-public`
- Demo task: `8088` / `short_video.agent_stall.basic`

## Repo Responsibilities

### clawscript-public

- Public status: published companion public repo
- Responsibility: Turns a natural-language automation request into an agent-friendly SOP and executable task.
- Handoff: Agent task spec, step guard policy, app entry strategy, debug artifact contract.

### autoscript-public

- Public status: project represented by this public demo
- Responsibility: Runs worker-side execution, parser registration, metric extraction, and report formatting.
- Handoff: Structured JSON result, Markdown report, parser summaries, and lifecycle state.

### autoSampler-public

- Public status: published companion public repo
- Responsibility: Packages post-capture review evidence, storyboards, manifests, and static portfolio artifacts.
- Handoff: Review score, storyboard images, artifact manifest, and GitHub Pages bundle.

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

### agent_planning

- Owner repo: `clawscript-public`
- Summary: Normalize the target app family, duration, swipe cadence, validation gates, and downstream repo contracts into an agent task spec.
- Artifact: `agent_task_contract.json`

### sop_generation

- Owner repo: `clawscript-public`
- Summary: Convert the natural-language request into an SOP with popup handling, entry strategy, guard rails, and debug capture.
- Artifact: `agent_sop.md`

### worker_execution

- Owner repo: `autoscript-public`
- Summary: Execute the task through the worker abstraction, collect logs and video artifacts, then run parser modules.
- Artifact: `samples/results/agent_short_video_report.json`

### evidence_packaging

- Owner repo: `autoSampler-public`
- Summary: Package worker output into review evidence, storyboards, manifests, and portfolio-facing static artifacts.
- Artifact: `docs/agent-handoffs.json`

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
