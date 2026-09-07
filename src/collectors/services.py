"""System service state collector."""

from typing import Any

from core.collector import Collector
from core.shell import run


class ServicesCollector(Collector):
	"""Check all monitored services in one systemctl invocation."""

	services = ("pveproxy", "pvedaemon", "pvestatd", "corosync", "pve-firewall", "chronyd")

	def collect(self) -> dict[str, Any]:
		"""Return active state for each monitored service."""
		output = run(["systemctl", "is-active", *self.services])
		states = output.splitlines()
		result: dict[str, Any] = {"error": 0}
		for index, service in enumerate(self.services):
			result[service] = 1 if index < len(states) and states[index] == "active" else 0
		return result
