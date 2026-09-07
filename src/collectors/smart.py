"""SMART and NVMe health collector."""

import json
from pathlib import Path
from typing import Any

from core.collector import Collector
from core.shell import run_result


class SmartCollector(Collector):
    """Discover disks once and query SMART JSON once per disk."""

    @staticmethod
    def _physical_disks(lines: list[str]) -> list[str]:
        """Keep physical disks and exclude virtual block devices."""
        disks = [line.split()[0] for line in lines if len(line.split()) > 1 and line.split()[1] == "disk"]
        sys_block = Path("/sys/block")
        if not sys_block.exists():
            return disks
        return [disk for disk in disks if (sys_block / disk / "device").exists()]

    def collect(self) -> dict[str, Any]:
        """Return normalized SMART records keyed by device name."""
        device_output, device_status = run_result(["lsblk", "-dn", "-o", "NAME,TYPE"])
        if device_status != 0:
            return {"error": 1, "devices": {}}
        devices = device_output.splitlines()
        disks = self._physical_disks(devices)
        result: dict[str, Any] = {"error": 0, "data": [], "devices": {}}
        for disk in disks:
            result["data"].append({"{#DEVICE}": disk})
            output, status = run_result(["smartctl", "--all", "--json", f"/dev/{disk}"])
            try:
                value = json.loads(output)
            except (json.JSONDecodeError, TypeError):
                result["devices"][disk] = {"error": 1}
                continue
            if not isinstance(value, dict):
                result["devices"][disk] = {"error": 1}
                continue
            smart_status = value.get("smart_status", {})
            temperature = value.get("temperature", {})
            nvme_log = value.get("nvme_smart_health_information_log", {})
            result["devices"][disk] = {
                "error": int(status not in (0, 2)),
                "health": int(smart_status["passed"]) if isinstance(smart_status, dict) and "passed" in smart_status else None,
                "temperature": temperature.get("current") if isinstance(temperature, dict) else None,
                "percentage_used": nvme_log.get("percentage_used") if isinstance(nvme_log, dict) else None,
                "media_errors": nvme_log.get("media_errors") if isinstance(nvme_log, dict) else None,
                "model": value.get("model_name") or value.get("model_family"),
                "serial": value.get("serial_number"),
            }
        return result