from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.adaptation_updates import build_adaptation_snapshot, render_adaptation_markdown


class AdaptationUpdatesTest(unittest.TestCase):
    def test_snapshot_covers_recent_sync_layers(self) -> None:
        snapshot = build_adaptation_snapshot()

        self.assertEqual(snapshot["source"], "autoscript@94614e50")
        self.assertEqual(snapshot["summary"]["update_count"], 4)
        self.assertIn("gesture adapter", snapshot["summary"]["covered_layers"])

    def test_public_projection_does_not_copy_private_identifiers(self) -> None:
        snapshot_text = render_adaptation_markdown(build_adaptation_snapshot())

        self.assertIn("Recent Adaptation Sync", snapshot_text)
        self.assertIn("no-audio-video flag", snapshot_text)
        self.assertNotIn("com.smile.gifmaker", snapshot_text)
        self.assertNotIn("com.ss.android.article.video", snapshot_text)


if __name__ == "__main__":
    unittest.main()
