"""Game definitions: the schema, the loader, and the files themselves."""

from xcolos.games.definition import (
    DefinitionError,
    GameDefinition,
    SCHEMA_VERSION,
    KINDS,
    parse,
)
from xcolos.games.loader import available, load, load_file

__all__ = [
    "DefinitionError",
    "GameDefinition",
    "SCHEMA_VERSION",
    "KINDS",
    "available",
    "load",
    "load_file",
    "parse",
]
