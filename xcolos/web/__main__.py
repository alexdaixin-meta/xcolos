"""`python -m xcolos.web` starts the operator console."""

from __future__ import annotations

import argparse

from xcolos.web.server import serve


def main() -> None:
    ap = argparse.ArgumentParser(
        prog="xcolos.web", description="Serve the XColos operator console."
    )
    ap.add_argument("--port", type=int, default=8000)
    serve(ap.parse_args().port)


if __name__ == "__main__":
    main()
