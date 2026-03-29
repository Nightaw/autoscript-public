from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.resolution_detector import parse_resolution_log
from common.demo_job_runner import run_demo_scenario
from common.stall_detector import parse_output_log, parse_timeout_log


class MediaMetricsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.samples = ROOT / "samples" / "logs"

    def test_output_stalls(self) -> None:
        result = parse_output_log(self.samples / "demo_player.log")
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["max_duration"], 1.75)
        self.assertEqual(result["stalls"][0]["sources"], ["output_state"])

    def test_timeout_clusters(self) -> None:
        result = parse_timeout_log(self.samples / "demo_timeout.log")
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["input_event_count"], 6)
        self.assertEqual(
            result["stalls"][0]["sources"],
            ["audio_timeout", "display_idle", "video_timeout"],
        )

    def test_resolution_timeline(self) -> None:
        result = parse_resolution_log(self.samples / "demo_resolution.log")
        self.assertEqual(result["count"], 4)
        self.assertEqual(result["first_resolution"], "360P")
        self.assertEqual(result["last_resolution"], "1080P")

    def test_demo_job_runner(self) -> None:
        result = run_demo_scenario("baseline_playback")
        self.assertEqual(result["scenario"]["name"], "baseline_playback")
        self.assertEqual(result["summary"]["stall_count"], 2)
        self.assertEqual(result["summary"]["final_resolution"], "1080P")



if __name__ == "__main__":
    unittest.main()
