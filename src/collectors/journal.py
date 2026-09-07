"""Single-pass systemd journal counters."""

from typing import Any

from core.collector import Collector
from core.shell import run


class JournalCollector(Collector):
    """Scan the recent journal once and count relevant error patterns."""

    def collect(self) -> dict[str, Any]:
        """Return counters for kernel, filesystem, package, and service errors."""
        text = run(["journalctl", "-b", "--no-pager", "-o", "cat"])
        lowered = text.lower()
        patterns = {
            "oom": ("out of memory", "oom-killer", "killed process"),
            "kernel_panic": ("kernel panic", "not syncing:"),
            "segfault": ("segfault", "general protection fault"),
            "apt_failed": ("apt error", "dpkg: error", "failed to fetch"),
            "filesystem_error": ("i/o error", "ext4-fs error", "xfs (", "zfs: error"),
            "kernel_error": ("kernel error", "call trace:"),
            "proxmox_error": ("pveproxy", "pvedaemon", "pvestatd"),
        }
        return {"error": 0, **{name: int(any(item in lowered for item in values)) for name, values in patterns.items()}}