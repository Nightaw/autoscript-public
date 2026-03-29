from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app


class WorkerApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = create_app().test_client()

    def test_health(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "ok")

    def test_scenarios(self) -> None:
        response = self.client.get("/demo/scenarios")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["scenarios"][0]["name"], "baseline_playback")

    def test_run_demo(self) -> None:
        response = self.client.post("/demo/run", json={"scenario": "baseline_playback"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["summary"]["stall_count"], 2)
        self.assertEqual(data["summary"]["final_resolution"], "1080P")
