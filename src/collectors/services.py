"""System service state collector."""

from typing import Any

from core.collector import Collector
from core.shell import run_result


class ServicesCollector(Collector):
    """Check all monitored services in one systemctl invocation."""

    services = ("pveproxy", "pvedaemon", "pvestatd", "corosync", "pve-firewall", "chronyd")

    def collect(self) -> dict[str, Any]:
        """Return active state for each monitored service."""
        output, status = run_result(["systemctl", "is-active", *self.services])
        states = output.splitlines()
        result: dict[str, Any] = {"error": int(len(states) != len(self.services) and status != 0)}
        for index, service in enumerate(self.services):
            result[service] = int(index < len(states) and states[index] == "active")
        return result
