from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.agent_collaboration import build_collaboration_trace, render_collaboration_markdown


class AgentCollaborationTest(unittest.TestCase):
    def test_trace_contains_three_repo_handoff(self) -> None:
        trace = build_collaboration_trace("8088")
        repo_names = [repo["name"] for repo in trace["repos"]]

        self.assertEqual(trace["conversation_id"], "019e0097-c570-7e53-9d0d-b9859dcd2404")
        self.assertEqual(repo_names, ["manualscript", "clawscript", "autoscript"])
        self.assertEqual(trace["collaboration"], "manualscript -> clawscript -> autoscript -> autoscript-public")

    def test_task_contract_keeps_agent_runtime_parameters(self) -> None:
        trace = build_collaboration_trace("8088")
        contract = trace["handoff_contract"]

        self.assertEqual(contract["task_id"], "8088")
        self.assertEqual(contract["watch_duration_sec"], 60)
        self.assertEqual(contract["swipe_interval_sec"], 5)
        self.assertEqual(contract["scenario"], "short_video.agent_stall.basic")
        self.assertTrue((ROOT / contract["output_path"]).exists())

    def test_markdown_is_readable_as_project_evidence(self) -> None:
        markdown = render_collaboration_markdown(build_collaboration_trace("8088"))

        self.assertIn("# Agent Collaboration Trace", markdown)
        self.assertIn("manualscript -> clawscript -> autoscript -> autoscript-public", markdown)
        self.assertIn("AgentContext", markdown)
        self.assertIn("Public Projection", markdown)


if __name__ == "__main__":
    unittest.main()
