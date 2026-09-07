"""Consistent JSON serialization for Zabbix master items."""

import json
import sys
from typing import Any


def dumps(payload: dict[str, Any]) -> str:
	"""Serialize a payload deterministically without human-readable noise."""
	return json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def write(payload: dict[str, Any]) -> None:
	"""Write one JSON document to stdout."""
	sys.stdout.write(dumps(payload) + "\n")
