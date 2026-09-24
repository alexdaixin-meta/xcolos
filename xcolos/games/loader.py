"""Loading a game definition from disk.

Definitions are JSON. The design writes them in YAML because it reads better,
and the two have an identical shape, but no YAML parser is available here and
none can be installed. When one is, this module grows a branch on the file
extension and nothing else changes.
"""

from __future__ import annotations

import json
from pathlib import Path

from xcolos.games.definition import DefinitionError, GameDefinition, parse

#: Definitions that ship with the runtime.
LIBRARY = Path(__file__).parent / "library"


def load(text: str, *, source: str = "<string>") -> GameDefinition:
    try:
        raw = json.loads(text)
    except ValueError as exc:
        raise DefinitionError(f"{source}: not valid JSON: {exc}") from None
    try:
        return parse(raw)
    except DefinitionError as exc:
        raise DefinitionError(f"{source}: {exc}") from None


def load_file(path: str | Path) -> GameDefinition:
    p = Path(path)
    if not p.is_file():
        raise DefinitionError(f"no definition at {p}")
    return load(p.read_text(encoding="utf-8"), source=str(p))


def available() -> dict[str, GameDefinition]:
    """Every definition in the library, by id.

    Loaded eagerly so a broken file is a startup error rather than a surprise
    when somebody opens a table.
    """
    out: dict[str, GameDefinition] = {}
    for path in sorted(LIBRARY.glob("*.json")):
        definition = load_file(path)
        if definition.id in out:
            raise DefinitionError(f"{path}: duplicate game id {definition.id!r}")
        out[definition.id] = definition
    return out
