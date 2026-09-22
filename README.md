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
  game:     orchestrators/
  record:   log.py, transcript.py
  surfaces: cli.py, web/
design/     design documents and reviews
project/    the product overview
```

## Status

Stage 1a is built: the kernel, the message protocol, the turn loop, visibility, the client and server split, and complete structured logging. One game, Mafia, is hardcoded in Python behind the orchestrator interface.

Stage 1b replaces that with an LLM orchestrator reading a YAML game file. Nothing below the orchestrator interface changes.

See `design/` for the current design and the review that shaped it.
