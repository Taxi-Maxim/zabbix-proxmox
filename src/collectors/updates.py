"""Available package updates collector."""

from typing import Any

from core.collector import Collector
import os

from core.shell import run_result


class UpdatesCollector(Collector):
	"""Inspect package metadata without modifying it or running apt update."""

	def collect(self) -> dict[str, Any]:
		"""Return simulated upgrade lines and reboot requirement."""
		output, status = run_result(["apt-get", "-s", "--quiet", "upgrade"])
		packages = sum(1 for line in output.splitlines() if line.startswith("Inst "))
		return {
			"error": int(status != 0),
			"command_status": status,
			"updates": packages,
			"repository_error": int("E:" in output or "Err:" in output),
			"gpg_error": int("NO_PUBKEY" in output or "GPG error" in output),
			"reboot_required": int(os.path.exists("/var/run/reboot-required")),
		}
