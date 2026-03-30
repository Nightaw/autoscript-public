# Baseline Playback Quality Run

Mock worker job that simulates a playback task, then combines output-state stalls, timeout clusters, and resolution transitions into one structured report.

## Summary

- Stall intervals: 2
- Timeout clusters: 2
- Resolution changes: 4
- Final resolution: 1080P

## Devices

- `android-pixel7-01` | android 14 | Pixel 7 | main
- `android-galaxy-s22-aux` | android 13 | Galaxy S22 | auxiliary

## Execution Steps

- `launch_app` | passed | 2.4s | Bootstrapped app session and confirmed player landing page.
- `warmup_playback` | passed | 5.2s | Started baseline playback and collected initial player telemetry.
- `background_foreground` | passed | 4.8s | Sent app to background and restored playback session.
- `seek_forward` | passed | 3.1s | Performed forward seek to trigger decoder and rendering transitions.
- `quality_switch` | passed | 3.9s | Changed playback quality and tracked resulting resolution timeline.

## Metric Outputs

- Output-state stalls: 2 intervals
- Timeout clusters: 2 windows
- Resolution timeline points: 4 changes
