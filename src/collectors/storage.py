"""Proxmox storage configuration collector."""

from typing import Any

from core.collector import Collector
from core.shell import run_json


class StorageCollector(Collector):
	"""Collect all configured storage definitions in one API request."""

	def collect(self) -> dict[str, Any]:
		"""Return configured storage records."""
		value = run_json(["pvesh", "get", "/storage", "--output-format", "json"])
		return {"error": 0, "storage": value if isinstance(value, list) else []}
