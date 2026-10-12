"""The arithmetic Mafia, a fixture for the tests.

It is Mafia with every rule as arithmetic, so a match needs no model: the engine tests and the kernel tests play it. It lives with the
tests, not in the game library; importing this module makes the platform offer it (unlisted, by its id) for the rest of the run.
"""

from __future__ import annotations

import os
from pathlib import Path

from xcolos.games.loader import EXTRA_GAMES

DATA = Path(__file__).resolve().parent / "data"
ORACLE_PATH = DATA / "mafia_oracle.json"
ORACLE_ID = "mafia-oracle"

_paths = [p for p in os.environ.get(EXTRA_GAMES, "").split(os.pathsep) if p]
if str(DATA) not in _paths:
    os.environ[EXTRA_GAMES] = os.pathsep.join(_paths + [str(DATA)])
