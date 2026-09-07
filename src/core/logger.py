"""Debug logging kept separate from the JSON stdout channel."""

import logging
import sys


def configure(debug: bool = False) -> None:
	"""Configure optional diagnostics on stderr."""
	logging.basicConfig(
		level=logging.DEBUG if debug else logging.WARNING,
		stream=sys.stderr,
		format="%(levelname)s %(name)s: %(message)s",
	)
