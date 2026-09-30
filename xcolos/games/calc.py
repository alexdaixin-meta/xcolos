"""Arithmetic a game file may write: `{"calc": "high_bid + raise"}`.

The comparison language in a condition is deliberately small, and prose goes
to a judge. Neither can say "the next bid is the current one plus the minimum
raise", or "the player whose cash plus holdings is largest". This can, and the
engine answers it itself, the same way every time.

It is a Python expression, read with `ast` and walked here. Nothing is ever
handed to `eval`: only the node types below are understood, and anything else
is refused when the file loads rather than when the expression runs.

What an expression can name:

  total_value      a table attribute, by its key
  you              the player being asked about, where there is one
  you.cash         one of their attributes; also `you.seat`, `you.status`
  $winner          a binding; `$winner.cash` if it names a seat
  players          every player, for `sum(p.cash for p in players)`
  acting           the players who may still act
  values[3]        indexing a list

Functions: sum, min, max, len, abs, round, int, any, all, sorted, and two that
draw from the match's seed so a replay deals the same numbers:

  uniform(lo, hi)          one number in [lo, hi)
  split(total, n, lo, hi)  n whole numbers in [lo, hi] adding to total
"""

from __future__ import annotations

import ast
import operator
import re
from typing import Any, Callable

#: A `$name` binding, rewritten to a Python name before parsing. The prefix
#: cannot clash with anything a game declares, because keys never start with
#: an underscore pair.
_BINDING = re.compile(r"\$([A-Za-z_]\w*)")
_PREFIX = "__bound_"

_BINARY: dict[type, Callable[[Any, Any], Any]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}
_COMPARE: dict[type, Callable[[Any, Any], Any]] = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.In: lambda a, b: a in b,
    ast.NotIn: lambda a, b: a not in b,
}

#: Pure functions. The seeded two are added per evaluation, because they need
#: the match's generator.
PURE: dict[str, Callable[..., Any]] = {
    "sum": sum, "min": min, "max": max, "len": len, "abs": abs,
    "round": round, "int": int, "any": any, "all": all, "sorted": sorted,
}
SEEDED = ("uniform", "split")
FUNCTIONS = tuple(PURE) + SEEDED

#: Names that mean something in every expression.
BUILTIN_NAMES = ("you", "players", "acting", "True", "False", "None")


class CalcError(Exception):
    """An expression that cannot be read, or cannot be worked out."""


class Expr:
    """A parsed expression. Parse once at load; evaluate as often as needed."""

    def __init__(self, source: str) -> None:
        self.source = source
        rewritten = _BINDING.sub(lambda m: _PREFIX + m.group(1), source)
        try:
            self.tree = ast.parse(rewritten.strip(), mode="eval").body
        except SyntaxError as exc:
            raise CalcError(f"cannot read {source!r}: {exc.msg}") from None
        _vet(self.tree, source)

    def names(self) -> set[str]:
        """Free names: table attributes and builtins. Bindings are separate."""
        bound = {c.target.id for c in ast.walk(self.tree)
                 if isinstance(c, ast.comprehension)}
        return {n.id for n in ast.walk(self.tree)
                if isinstance(n, ast.Name) and not n.id.startswith(_PREFIX)
                and n.id not in bound and n.id not in FUNCTIONS}

    def bindings(self) -> set[str]:
        return {n.id[len(_PREFIX):] for n in ast.walk(self.tree)
                if isinstance(n, ast.Name) and n.id.startswith(_PREFIX)}

    def attributes(self) -> set[str]:
        """Every `.name` read, which can only be a player attribute."""
        return {n.attr for n in ast.walk(self.tree) if isinstance(n, ast.Attribute)}

    def __repr__(self) -> str:
        return f"Expr({self.source!r})"


class Player:
    """A seat, as an expression sees it: its attributes by name."""

    __slots__ = ("seat", "_read")

    def __init__(self, seat: int, read: Callable[[int, str], Any]) -> None:
        self.seat = seat
        self._read = read

    def get(self, name: str) -> Any:
        if name == "seat":
            return self.seat
        return self._read(self.seat, name)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Player):
            return other.seat == self.seat
        return other == self.seat

    def __hash__(self) -> int:
        return hash(self.seat)

    def __repr__(self) -> str:
        return f"seat {self.seat}"


class Scope:
    """What an evaluation may read.

    `lookup` answers a bare name (a table attribute), `binding` a `$name`,
    `player` turns a seat number into something with attributes, and `rng`
    feeds the seeded functions. The engine builds one of these per call.
    """

    def __init__(
        self,
        lookup: Callable[[str], Any],
        binding: Callable[[str], Any],
        player: Callable[[int], Player | None],
        rng: Any = None,
    ) -> None:
        self.lookup = lookup
        self.binding = binding
        self.player = player
        self.rng = rng


def evaluate(expr: Expr, scope: Scope) -> Any:
    functions = dict(PURE)
    functions["uniform"] = lambda lo, hi: _uniform(scope.rng, lo, hi)
    functions["split"] = lambda total, n, lo, hi: split(scope.rng, total, n, lo, hi)
    try:
        return _Walk(scope, functions).value(expr.tree, {})
    except CalcError:
        raise
    except (TypeError, ValueError, ZeroDivisionError, IndexError, KeyError) as exc:
        raise CalcError(f"{expr.source!r}: {exc}") from None


# ----------------------------------------------------------------------
# Seeded draws
# ----------------------------------------------------------------------


def _uniform(rng: Any, lo: float, hi: float) -> float:
    if rng is None:
        raise CalcError("uniform() needs the match's generator")
    return lo + (hi - lo) * rng.random()


def split(rng: Any, total: int, n: int, lo: int, hi: int) -> list[int]:
    """n whole numbers, each in [lo, hi], adding up to exactly total.

    Drawn independently and then pulled toward the total, clamped at the
    bounds, rather than handed out one unit at a time: that way the spread
    comes from the draws, where unit-by-unit settles every value near the
    mean.
    """
    total, n, lo, hi = int(total), int(n), int(lo), int(hi)
    if n <= 0 or lo > hi or not n * lo <= total <= n * hi:
        raise CalcError(
            f"split({total}, {n}, {lo}, {hi}): {n} values between {lo} and "
            f"{hi} cannot add up to {total}"
        )
    values = [_uniform(rng, lo, hi) for _ in range(n)]
    for _ in range(200):
        gap = total - sum(values)
        if abs(gap) < 1e-9:
            break
        room = [i for i, v in enumerate(values) if (v < hi if gap > 0 else v > lo)]
        share = gap / len(room)
        for i in room:
            values[i] = min(hi, max(lo, values[i] + share))
    whole = [int(round(v)) for v in values]
    # Rounding leaves the sum a few units out. Nudged one unit at a time, at
    # seeded positions that still have room.
    while sum(whole) != total:
        step = 1 if sum(whole) < total else -1
        room = [i for i, v in enumerate(whole) if lo <= v + step <= hi]
        whole[room[rng.below(len(room))]] += step
    return whole


# ----------------------------------------------------------------------
# Reading and walking
# ----------------------------------------------------------------------


_ALLOWED = (
    ast.Constant, ast.Name, ast.Attribute, ast.Subscript, ast.Call,
    ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare, ast.IfExp,
    ast.List, ast.Tuple, ast.ListComp, ast.GeneratorExp, ast.comprehension,
    ast.Load, ast.Store, ast.And, ast.Or, ast.Not, ast.USub, ast.UAdd,
    *_BINARY, *_COMPARE,
)


def _vet(tree: ast.AST, source: str) -> None:
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED):
            raise CalcError(f"{source!r}: {type(node).__name__} is not allowed")
        if isinstance(node, ast.Attribute) and node.attr.startswith("_"):
            raise CalcError(f"{source!r}: .{node.attr} is not allowed")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in FUNCTIONS:
                raise CalcError(
                    f"{source!r}: only these functions exist: {', '.join(FUNCTIONS)}"
                )
            if node.keywords:
                raise CalcError(f"{source!r}: functions take no keyword arguments")
        if isinstance(node, ast.comprehension):
            if not isinstance(node.target, ast.Name) or node.is_async:
                raise CalcError(f"{source!r}: loop over one name, as in `p for p in players`")


class _Walk:
    def __init__(self, scope: Scope, functions: dict[str, Callable[..., Any]]) -> None:
        self.scope = scope
        self.functions = functions

    def value(self, node: ast.AST, local: dict[str, Any]) -> Any:
        method = getattr(self, "_" + type(node).__name__)
        return method(node, local)

    def _Constant(self, node: ast.Constant, local: dict[str, Any]) -> Any:
        return node.value

    def _Name(self, node: ast.Name, local: dict[str, Any]) -> Any:
        name = node.id
        if name in local:
            return local[name]
        if name.startswith(_PREFIX):
            return self.scope.binding(name[len(_PREFIX):])
        return self.scope.lookup(name)

    def _Attribute(self, node: ast.Attribute, local: dict[str, Any]) -> Any:
        owner = self.value(node.value, local)
        if not isinstance(owner, Player):
            seat = owner if isinstance(owner, int) and not isinstance(owner, bool) else None
            owner = self.scope.player(seat) if seat is not None else None
        if owner is None:
            raise CalcError(f".{node.attr} read from something that is not a player")
        return owner.get(node.attr)

    def _Subscript(self, node: ast.Subscript, local: dict[str, Any]) -> Any:
        return self.value(node.value, local)[self.value(node.slice, local)]

    def _Call(self, node: ast.Call, local: dict[str, Any]) -> Any:
        args = [self.value(a, local) for a in node.args]
        return self.functions[node.func.id](*args)

    def _BinOp(self, node: ast.BinOp, local: dict[str, Any]) -> Any:
        return _BINARY[type(node.op)](self.value(node.left, local),
                                      self.value(node.right, local))

    def _UnaryOp(self, node: ast.UnaryOp, local: dict[str, Any]) -> Any:
        operand = self.value(node.operand, local)
        if isinstance(node.op, ast.Not):
            return not operand
        return -operand if isinstance(node.op, ast.USub) else +operand

    def _BoolOp(self, node: ast.BoolOp, local: dict[str, Any]) -> Any:
        last: Any = None
        for part in node.values:
            last = self.value(part, local)
            if isinstance(node.op, ast.And) and not last:
                return last
            if isinstance(node.op, ast.Or) and last:
                return last
        return last

    def _Compare(self, node: ast.Compare, local: dict[str, Any]) -> bool:
        left = self.value(node.left, local)
        for op, right_node in zip(node.ops, node.comparators):
            right = self.value(right_node, local)
            if not _COMPARE[type(op)](left, right):
                return False
            left = right
        return True

    def _IfExp(self, node: ast.IfExp, local: dict[str, Any]) -> Any:
        if self.value(node.test, local):
            return self.value(node.body, local)
        return self.value(node.orelse, local)

    def _List(self, node: ast.List, local: dict[str, Any]) -> list[Any]:
        return [self.value(e, local) for e in node.elts]

    _Tuple = _List

    def _ListComp(self, node: ast.ListComp, local: dict[str, Any]) -> list[Any]:
        return list(self._generate(node.elt, node.generators, local))

    _GeneratorExp = _ListComp

    def _generate(self, elt: ast.AST, generators: list[ast.comprehension],
                  local: dict[str, Any]):
        first, rest = generators[0], generators[1:]
        for item in self.value(first.iter, local):
            inner = {**local, first.target.id: item}
            if all(self.value(test, inner) for test in first.ifs):
                if rest:
                    yield from self._generate(elt, rest, inner)
                else:
                    yield self.value(elt, inner)
