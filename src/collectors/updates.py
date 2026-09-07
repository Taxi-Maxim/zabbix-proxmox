"""Available package updates collector."""

from typing import Any

from core.collector import Collector
from core.shell import run


class UpdatesCollector(Collector):
	"""Inspect package metadata without modifying it or running apt update."""

	def collect(self) -> dict[str, Any]:
		"""Return simulated upgrade lines and reboot requirement."""
		output = run(["apt-get", "-s", "--quiet", "upgrade"])
		packages = sum(1 for line in output.splitlines() if line.startswith("Inst "))
		return {
			"error": 0,
			"updates": packages,
			"repository_error": int("E:" in output or "Err:" in output),
			"gpg_error": int("NO_PUBKEY" in output or "GPG error" in output),
			"reboot_required": int(__import__("os").path.exists("/var/run/reboot-required")),
		}
