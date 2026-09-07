"""Single-pass systemd journal counters."""

import json
from typing import Any

from core.collector import Collector
from core.shell import run_result


class JournalCollector(Collector):
    """Scan the recent journal once and count relevant error patterns."""

    journal_window = "10 minutes ago"

    def collect(self) -> dict[str, Any]:
        """Return counters for kernel, filesystem, package, and service errors."""
        text, status = run_result(
            ["journalctl", "-b", "--since", self.journal_window, "--no-pager", "-o", "json"]
        )
        result = {"error": int(status != 0 and not text), "oom": 0, "kernel_panic": 0, "segfault": 0,
                  "apt_failed": 0, "filesystem_error": 0, "kernel_error": 0, "proxmox_error": 0}
        for line in text.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            message = str(event.get("MESSAGE", "")).lower()
            identifier = str(event.get("SYSLOG_IDENTIFIER", "")).lower()
            unit = str(event.get("_SYSTEMD_UNIT", "")).lower()
            priority = int(event.get("PRIORITY", 7)) if str(event.get("PRIORITY", "7")).isdigit() else 7
            result["oom"] += int(any(value in message for value in ("out of memory", "oom-killer", "killed process")))
            result["kernel_panic"] += int(any(value in message for value in ("kernel panic", "not syncing:")))
            result["segfault"] += int(any(value in message for value in ("segfault", "general protection fault")))
            result["apt_failed"] += int(any(value in message for value in ("apt error", "dpkg: error", "failed to fetch")))
            result["filesystem_error"] += int(any(value in message for value in ("i/o error", "ext4-fs error", "xfs (", "zfs: error")))
            result["kernel_error"] += int(priority <= 3 and (identifier == "kernel" or "call trace:" in message or "kernel error" in message))
            proxmox_units = {"pveproxy.service", "pvedaemon.service", "pvestatd.service"}
            proxmox_names = ("pveproxy", "pvedaemon", "pvestatd")
            result["proxmox_error"] += int(priority <= 3 and (unit in proxmox_units or any(name in message for name in proxmox_names)))
        return result