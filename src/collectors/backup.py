"""Recent vzdump task collector."""

from typing import Any

from core.collector import Collector
from core.shell import run_json_result


class BackupCollector(Collector):
    """Read recent backup tasks from the local API in one request."""

    def collect(self) -> dict[str, Any]:
        """Return the most recent backup task records."""
        value, status = run_json_result(["pvesh", "get", "/cluster/tasks", "--typefilter", "vzdump", "--limit", "50", "--output-format", "json"])
        return {"error": int(not isinstance(value, list)), "tasks": value if isinstance(value, list) else [], "command_status": status}
