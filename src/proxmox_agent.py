import argparse
from typing import Sequence

from core.command import COLLECTORS, create
from core.jsonutil import write
from core.logger import configure


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Zabbix Proxmox monitoring agent")
    parser.add_argument("collector", choices=sorted(COLLECTORS))
    parser.add_argument("--debug", action="store_true", help="enable diagnostics on stderr")
    args = parser.parse_args(argv)
    configure(args.debug)
    try:
        payload = create(args.collector).collect()
    except Exception:
        payload = {"error": 1, "collector": args.collector}
    write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())