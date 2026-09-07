"""Proxmox storage configuration collector."""

from typing import Any

from core.collector import Collector
from core.shell import run_json_result


class StorageCollector(Collector):
	"""Collect all configured storage definitions in one API request."""

	def collect(self) -> dict[str, Any]:
		"""Return configured storage records."""
		value, status = run_json_result(["pvesh", "get", "/storage", "--output-format", "json"])
		return {"error": int(not isinstance(value, list)), "storage": value if isinstance(value, list) else [], "command_status": status}
