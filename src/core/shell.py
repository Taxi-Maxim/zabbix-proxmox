"""Small, testable wrapper around subprocess."""

import json
import shutil
import subprocess
from typing import Any, Sequence


def run(command: Sequence[str], timeout: int = 30) -> str:
    """Run a command and return stdout, or an empty string on failure."""
    try:
        result = subprocess.run(
            list(command),
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def run_json(command: Sequence[str], timeout: int = 30) -> dict[str, Any] | list[Any] | None:
    """Run a command and decode its JSON stdout."""
    output = run(command, timeout)
    if not output:
        return None
    try:
        value = json.loads(output)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, (dict, list)) else None


def exists(command: str) -> bool:
    """Return whether an executable is available on PATH."""
    return shutil.which(command) is not None