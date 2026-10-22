# xcolos

The AI Colosseum. A runtime for multi-player games of hidden information, played by LLM agents.

## Layers

| Layer | Role |
|---|---|
| **Kernel** | Deterministic, game-agnostic. Owns state, visibility, turn order, and the log. The only component trusted with secrets |
| **Orchestrator** | Game-aware. Decides what happens next. Never touches an agent, never writes state directly |
| **Client** | Hosts the agents that occupy seats. Relays messages. Decides nothing |

There is no broadcast channel. The orchestrator emits facts with an explicit audience, and the kernel
pushes each entitled seat its own view. A seat cannot receive something that was never selected for it.

## Games are data

A game is a JSON file, not Python. Each one declares its state in an `attributes` block, where every
field carries a visibility and a type:

```json
{"key": "coins",        "visible": "public", "type": "number", "initial": 2}
{"key": "hidden_cards", "visible": "ally",   "type": "list",   "initial": []}
{"key": "deck",         "visible": "none",   "type": "list",   "initial": [...]}
```

`visible` is one of `public`, `ally` or `none`, and the kernel enforces it. Because visibility is a
kernel concept rather than a per-game convention, "which facts are hidden from seat N" is an engine
query that works the same way for every game.

The library holds seven games: `coup`, `mafia`, `auction`, `agram`, `assurance_game`,
`battle_of_wits` and `rps`. The agent's playing guide is identical for all of them — the server
sends each game's rules at the start of play, so nothing in the client names a game.

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

`run_tests.py` prefers real pytest and falls back to a small shim in `tests/`, because no package
index is reachable from this machine.

## Generating games

`gen_inventory/` crawls curated sources and rates each candidate against what the engine can express,
then gates the survivors. Anything a game needs that the engine lacks is recorded, which is how
missing engine features get found.

`gen_game/` takes a candidate through design, spec, build and evaluation: a designer model works the
idea into concrete rules, an independent critic must find them balanced and playable, a coder writes
the game file against a spec, a separate model writes scenario tests from the spec alone, and the
pipeline re-checks the file rather than trusting the coder. Tier 0 asks whether the game is valid,
terminates, and replays identically from the same seed. Tier 1 asks whether a thoughtless strategy
loses sometimes, whether chance decides too much, and whether the game stays inside the engine's
complexity limits. Every failure is triaged into one of three outcomes: fix the file, revise the
rules, or log a platform limit as engine work.

## Layout

```
xcolos/
  kernel:   state.py, game.py, protocol.py, render.py
  client:   host.py, agents.py
  game:     orchestrators/
  record:   log.py, transcript.py
  surfaces: cli.py, web/

gen_inventory/   candidate discovery and gating
gen_game/        design -> spec -> build -> evaluate
design/          design documents and reviews
project/         the product overview
```

## Status

The kernel, message protocol, turn loop, visibility model, client/server split and structured logging
are built. Games are JSON files run by the flow engine; no game is hard-coded in Python. Seven
games are in the library and the generation pipeline has produced game files of its own.

See `design/` for the current design and the review that shaped it.
