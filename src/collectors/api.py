"""Proxmox node API collector."""

from typing import Any

from core.collector import Collector
from core.shell import run_json


class ApiCollector(Collector):
    """Collect node data with one pvesh request."""

    def collect(self) -> dict[str, Any]:
        """Return the node list payload from the local Proxmox API."""
        value = run_json(["pvesh", "get", "/nodes", "--output-format", "json"])
        if not isinstance(value, list):
            return {"error": 1, "nodes": []}
        return {"error": 0, "nodes": value}