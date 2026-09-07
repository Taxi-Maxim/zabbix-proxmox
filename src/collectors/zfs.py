"""ZFS pool health collector."""

from typing import Any

from core.collector import Collector
from core.shell import run


class ZfsCollector(Collector):
    """Collect the complete pool status with one zpool invocation."""

    def collect(self) -> dict[str, Any]:
        """Return pool status text and a machine-readable health flag."""
        output = run(["zpool", "status", "-v"])
        pools = []
        for line in output.splitlines():
            fields = line.split()
            if fields and fields[0] == "pool:":
                pools.append(fields[1])
        return {"error": 0, "healthy": int("state: ONLINE" in output), "pools": pools, "status": output}