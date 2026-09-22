"""A tiny stand-in for the slice of pytest these tests use.

There is no package index reachable from this machine, so `pip install pytest`
fails. The tests are written in ordinary pytest style and run unchanged under
real pytest; this shim only exists so they can also run offline via
`python run_tests.py`.

Supports exactly what the suite needs: `pytest.mark.parametrize` and
`pytest.raises`.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Callable, Iterable


class _Mark:
    @staticmethod
    def parametrize(names: str, values: Iterable[Any]) -> Callable:
        keys = [n.strip() for n in names.split(",")]

        def decorate(fn: Callable) -> Callable:
            cases = []
            for v in values:
                row = tuple(v) if len(keys) > 1 else (v,)
                cases.append(dict(zip(keys, row)))
            existing = getattr(fn, "_xc_cases", None)
            if existing is None:
                fn._xc_cases = cases  # type: ignore[attr-defined]
            else:
                fn._xc_cases = [  # type: ignore[attr-defined]
                    {**a, **b} for a in existing for b in cases
                ]
            return fn

        return decorate


mark = _Mark()


class Failed(AssertionError):
    pass


class Skipped(Exception):
    """Raised by skip(). The runner reports these separately from failures."""


def skip(reason: str = "") -> None:
    raise Skipped(reason)


@contextmanager
def raises(expected: type[BaseException]):
    try:
        yield
    except expected:
        return
    except BaseException as exc:  # noqa: BLE001
        raise Failed(
            f"expected {expected.__name__}, got {type(exc).__name__}: {exc}"
        ) from exc
    raise Failed(f"expected {expected.__name__}, nothing was raised")
