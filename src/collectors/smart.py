"""SMART and NVMe health collector."""

from typing import Any

from core.collector import Collector
from core.shell import run, run_json


class SmartCollector(Collector):
    """Discover disks once and query SMART JSON once per disk."""

    def collect(self) -> dict[str, Any]:
        """Return raw normalized SMART records keyed by device name."""
        devices = run(["lsblk", "-dn", "-o", "NAME,TYPE"]).splitlines()
        disks = [line.split()[0] for line in devices if len(line.split()) > 1 and line.split()[1] == "disk"]
        result: dict[str, Any] = {"error": 0, "devices": {}}
        for disk in disks:
            value = run_json(["smartctl", "-j", f"/dev/{disk}"])
            if isinstance(value, dict):
                result["devices"][disk] = value
        return result