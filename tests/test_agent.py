"""Focused tests for the collector contract and CLI serialization."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from collectors.services import ServicesCollector
from proxmox_agent import main


class AgentTests(unittest.TestCase):
    """Verify stdout remains valid JSON and service calls stay batched."""

    @patch("collectors.services.run", return_value="active\ninactive\nfailed\n")
    def test_services_payload(self, run_command: object) -> None:
        with patch("sys.stdout") as stdout:
            ServicesCollector().collect()
        self.assertEqual(run_command.call_count, 1)

    @patch("proxmox_agent.create")
    def test_main_writes_json(self, create: object) -> None:
        create.return_value.collect.return_value = {"health": 1}
        with patch("sys.stdout") as stdout:
            main(["api"])
            output = "".join(call.args[0] for call in stdout.write.call_args_list)
        self.assertEqual(json.loads(output), {"health": 1})


if __name__ == "__main__":
    unittest.main()