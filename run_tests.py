#!/usr/bin/env python3
"""Run the test suite without a pytest install.

Prefers real pytest when it is importable. Falls back to the shim in
tests/_minipytest.py, which supports the subset of pytest the suite uses.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))


def _install_shim() -> bool:
    try:
        import pytest  # noqa: F401

        return False
    except ImportError:
        pass
    spec = importlib.util.spec_from_file_location(
        "pytest", ROOT / "tests" / "_minipytest.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["pytest"] = module
    spec.loader.exec_module(module)
    return True


# No test may reach a model. A key on the developer's machine must not
# change what the suite does, or the suite means something different for
# them than it does in review.
os.environ["XCOLOS_NO_MODEL"] = "1"


def main() -> int:
    shimmed = _install_shim()
    if shimmed:
        print("pytest not installed; using the offline shim\n")

    passed = failed = skipped = 0
    failures: list[tuple[str, str]] = []
    skip_exc = getattr(sys.modules["pytest"], "Skipped", None)

    for path in sorted((ROOT / "tests").glob("test_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name in sorted(vars(module)):
            if not name.startswith("test_"):
                continue
            fn = getattr(module, name)
            if not callable(fn):
                continue
            cases = getattr(fn, "_xc_cases", [{}])
            for case in cases:
                label = f"{path.stem}::{name}"
                if case:
                    label += "[" + ",".join(f"{k}={v}" for k, v in case.items()) + "]"
                try:
                    fn(**case)
                except Exception as exc:  # noqa: BLE001
                    if skip_exc is not None and isinstance(exc, skip_exc):
                        skipped += 1
                        print("s", end="", flush=True)
                        continue
                    failed += 1
                    failures.append((label, traceback.format_exc()))
                    print("F", end="", flush=True)
                else:
                    passed += 1
                    print(".", end="", flush=True)

    tail = f", {skipped} skipped" if skipped else ""
    print(f"\n\n{passed} passed, {failed} failed{tail}")
    for label, tb in failures:
        print(f"\n--- FAILED {label} ---\n{tb}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
