from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.resolution_detector import parse_resolution_log
from common.demo_job_runner import build_markdown_report, list_available_devices, run_demo_scenario
from common.parser_registry import list_parsers
from common.stall_detector import parse_output_log, parse_timeout_log
from parsers.resolution.app_log_parser import extract_resolutions_from_app_render_stats
from parsers.stall.sys_log_parser import extract_cloud_game_pid_stalls


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
        self.assertEqual(result["execution"]["status"], "passed")
        self.assertEqual(len(result["execution"]["steps"]), 5)
        self.assertEqual(result["devices"][0]["platform"], "android")

    def test_device_registry(self) -> None:
        devices = list_available_devices(platform="android")
        self.assertGreaterEqual(len(devices), 1)
        self.assertTrue(all(device["platform"] == "android" for device in devices))

    def test_markdown_report(self) -> None:
        report = build_markdown_report("baseline_playback")
        self.assertIn("# Baseline Playback Quality Run", report)
        self.assertIn("## Devices", report)
        self.assertIn("Final resolution: 1080P", report)

    def test_app_log_resolution_parser(self) -> None:
        events = extract_resolutions_from_app_render_stats(self.samples / "demo_rtc_app.log")
        self.assertEqual(len(events), 4)
        self.assertEqual(events[-1]["resolution"], "1080P")

    def test_parser_registry(self) -> None:
        parsers = list_parsers(category="resolution")
        names = {item["name"] for item in parsers}
        self.assertIn("resolution.raw_size", names)
        self.assertIn("resolution.app_render_stats", names)

    def test_cloud_game_pid_parser(self) -> None:
        path = self.samples / "demo_cloud_game.log"
        result = extract_cloud_game_pid_stalls(path, year=2026)
        self.assertEqual(result["pids"], ["1357", "2468"])
        self.assertEqual(len(result["transitions"]["1357"]), 1)



if __name__ == "__main__":
    unittest.main()
