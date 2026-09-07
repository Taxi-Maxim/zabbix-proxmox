"""ZFS pool health collector."""

from typing import Any

from core.collector import Collector
from core.shell import run_result


class ZfsCollector(Collector):
    """Collect the complete pool status with one zpool invocation."""

    def collect(self) -> dict[str, Any]:
        """Return pool status text and a machine-readable health flag."""
        output, status = run_result(["zpool", "status", "-v"])
        pool_states: dict[str, str] = {}
        current_pool = ""
        for line in output.splitlines():
            fields = line.split()
            if len(fields) >= 2 and fields[0] == "pool:":
                current_pool = fields[1]
            elif len(fields) >= 2 and fields[0] == "state:" and current_pool:
                pool_states[current_pool] = fields[1]
        return {
            "error": int(not output and status != 0),
            "healthy": int(bool(pool_states) and all(state == "ONLINE" for state in pool_states.values())),
            "pools": list(pool_states),
            "pool_states": pool_states,
            "status": output,
        }