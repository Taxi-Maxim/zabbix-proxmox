"""Proxmox certificate expiry collector."""

import datetime
import ssl
from pathlib import Path
from typing import Any

from core.collector import Collector


class CertificatesCollector(Collector):
	"""Read local Proxmox certificate files without external commands."""

	def collect(self) -> dict[str, Any]:
		"""Return days remaining for each discovered certificate."""
		result: dict[str, Any] = {"error": 0, "certificates": {}}
		for path in Path("/etc/pve/nodes").glob("*/pve-ssl.pem"):
			try:
				data = ssl._ssl._test_decode_cert(str(path))
				expiry = datetime.datetime.strptime(data["notAfter"], "%b %d %H:%M:%S %Y %Z")
				result["certificates"][str(path)] = (expiry - datetime.datetime.utcnow()).days
			except (OSError, KeyError, ValueError):
				result["certificates"][str(path)] = None
		return result
