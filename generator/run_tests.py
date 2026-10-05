#!/usr/bin/env python3
"""Run the generator's tests: `python3 generator/run_tests.py`.

Kept apart from the platform's runner, which only looks in `tests/`. The tests
here use plain asserts, so no pytest and no shim are needed.
"""

from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))


def main() -> int:
    passed = 0
    failures: list[tuple[str, str]] = []
    for path in sorted((HERE / "tests").glob("test_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name in sorted(vars(module)):
            fn = getattr(module, name)
            if not name.startswith("test_") or not callable(fn):
                continue
            try:
                fn()
            except (Exception, SystemExit):  # noqa: BLE001 - argparse exits on a bad command line
                failures.append((f"{path.stem}::{name}", traceback.format_exc()))
                print("F", end="", flush=True)
            else:
                passed += 1
                print(".", end="", flush=True)
    print(f"\n\n{passed} passed, {len(failures)} failed")
    for label, tb in failures:
        print(f"\n--- FAILED {label} ---\n{tb}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
