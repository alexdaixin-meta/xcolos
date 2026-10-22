# xcolos

The AI Colosseum. A runtime for hidden-role social deduction games played by LLM agents.

## Layers

| Layer | Role |
|---|---|
| **Kernel** | Deterministic, game-agnostic. Owns state, visibility, turn order, and the log. The only component trusted with secrets |
| **Orchestrator** | Game-aware. Decides what happens next. Never touches an agent, never writes state directly |
| **Client** | Hosts the agents that occupy seats. Relays messages. Decides nothing |

There is no broadcast channel. The orchestrator emits facts with an explicit audience, and the kernel pushes each entitled seat its own view. A seat cannot receive something that was never selected for it.

## Running it

No third-party packages. Python 3.11 or newer.

```bash
# The operator console: build a table, pick a game, press play
python3 -m xcolos.web --port 8000

# One match, with the full timeline
python3 -m xcolos.cli --seed 7 --timeline

# A batch, with log validation
python3 -m xcolos.cli --seed 1 --matches 50 --check --out runs

# Everything one seat ever saw
python3 -m xcolos.cli --seed 7 --seat 3

# Tests
python3 run_tests.py
```

`run_tests.py` prefers real pytest and falls back to a small shim in `tests/`, because no package index is reachable from this machine.

## Layout

```
xcolos/
  kernel:   state.py, game.py, protocol.py, render.py
  client:   host.py, agents.py
  game:     orchestrators/, flow/ (the flow engine that runs game files)
  games:    games/library/ (one JSON file per game)
  record:   log.py, transcript.py
  surfaces: cli.py, web/
gen_inventory/  find candidate games and keep an inventory of them
gen_game/       turn an inventory game into a game file, and test it
design/         design documents and reviews
project/        the product overview
```

## Games are data

No game is hard-coded in Python. Each game is a JSON file in `xcolos/games/library/`, run by the flow
engine: `assurance_game`, `auction`, `battle_of_wits`, `mafia`, `mafia_oracle` and `rps` on this branch.
A game file declares its `attributes`, `deal`, `setup`, `steps`, `end`, `reveal` and `limits`. Every
attribute says who may see it:

```json
"attributes": {
  "player": [
    {"key": "role",    "visible": "ally",   "type": "text", "values": ["mafia", "detective", "villager"]},
    {"key": "faction", "visible": "ally",   "type": "text", "values": ["good", "evil"]}
  ]
}
```

`visible` is `public`, `ally` or `none`; `type` is `number`, `list`, `bool` or `text`. The kernel uses it
to decide what each seat is shown.

## Generating games

Two tools beside the platform produce new games. Nothing in `xcolos/` imports them.

- `gen_inventory/` finds candidate games from curated sources, rates each one's fit with what the
  engine can express, extracts its rules into a fixed vocabulary and runs gates. Anything a game needs
  that the engine lacks is recorded, which is how missing engine features are found. See
  `gen_inventory/README.md`.
- `gen_game/` turns an inventory game into a game file. A designer model works out the rules and a
  separate critic must find them balanced, playable and rewarding reasoning over luck. A coder writes
  the game file, an independent model writes scenario tests from the spec, and automatic checks test
  that the game is valid, ends, replays the same from the same seed, is not always won by a thoughtless
  policy and is not decided by chance. Failures are triaged back to the coder, back to the designer, or
  recorded as engine work. See `gen_game/README.md`.

A generated game stays in `gen_game/data/` until a person copies it into `xcolos/games/library/`.

## Status

Built: the kernel, the message protocol, the turn loop, visibility, the client and server split,
complete structured logging, the flow engine that runs games from JSON files, the game library above,
and the generation tools.

See `design/` for the current design and the review that shaped it.
