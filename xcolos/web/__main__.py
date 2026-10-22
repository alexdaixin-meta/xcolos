"""`python -m xcolos.web` starts the operator console."""

from __future__ import annotations

import argparse
from pathlib import Path

from xcolos.web.server import serve


def main() -> None:
    ap = argparse.ArgumentParser(
        prog="xcolos.web", description="Serve the XColos operator console."
    )
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--log-dir", type=Path, default=Path("runs/web"), help="where game logs are written (a folder per start)")
    ap.add_argument("--no-log", action="store_true", help="keep game logs in memory only")
    args = ap.parse_args()
    serve(args.port, None if args.no_log else args.log_dir)


if __name__ == "__main__":
    main()
