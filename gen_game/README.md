# gen_game

Turns a game from the inventory (`../gen_inventory/`) into a game file for the XColos platform, and tests it.
Design: `design/2026-10-05-game-generation-pipeline.md`.

```bash
python3 -m gen_game convert ID --model muse                    # the idea is designed into rules (players, numbers, winner), then spec, build, scenarios, checks
python3 -m gen_game convert ID --model muse --encoder claude   # a coding agent writes it (claude, metacode, command:...)
python3 -m gen_game convert ID --model muse --redo adapt       # run a step again (adapt, spec, encode, scenarios)
python3 -m gen_game convert ID --model muse --judge            # also gate the design (critic, balance checks; can drop a game)
python3 -m gen_game convert ID --model muse --no-adapt         # the entry is finished rules: convert them as written
python3 -m gen_game verify ID variation|spec|game|scenarios    # check a file written by hand or by an agent
python3 -m gen_game show ID                                    # the report
python3 -m gen_game evaluate ID                                # tiers 0 and 1 on an existing game.json

python3 gen_game/run_tests.py
```

## The flow

```
inventory game
 A design    A designer works out rules from the XColos goal and the platform's RESTRICTIONS (what it can and
             cannot do, and its complexity limits), not from its file format. A separate critic must then find
             them BALANCED, PLAYABLE and rewarding REASONING OVER LUCK, showing its arithmetic, before they go on.
             They go back and forth up to 3 times.                          variation.json  VARIATION.md
 B spec      The rules' interface (attribute names, parameters, result names) as a contract.   spec.json  SPEC.md
 C build     A coder writes the game file from a prompt that carries the platform's API (design/actions.md,
             example games, the mistakes the loader has refused, a `verify` command that says when it is done).
             The coder is a model in a repair loop (`--encoder completion`) or a coding agent with tools
             (`--encoder claude|metacode|command:...`). An independent model writes scenario tests from the
             spec alone. The pipeline re-checks the file itself; it never takes the coder's word.
 D evaluate  Tier 0: valid, ends, same seed replays the same. Tier 1: does a thoughtless policy always win?
             does chance decide everything? is the built game within the complexity limits?
 E triage    Whenever C or D finds a problem a model decides whose it is:
               fix_game        the file is wrong: the coder tries again with guidance (up to 2 times)
               revise_rules    the rules are the problem: back to A with guidance (up to 3 designs)
               platform_limit  the rules are sound and need what the platform cannot do: STOP
```

`platform_limit` is not a drop. `PLATFORM_LIMIT.md` says exactly what is missing, and the inventory records the
game as `blocked` on that need, so `gen_inventory gaps` counts it as engine work and the game is converted again
once the engine can do it.

A game is **dropped, with a reason**, when the designer recommends it (`too_simple`, or `too_complex`), when no
design gets past the critic, or when the last design still cannot be built to behave as designed or still has a
design flaw. A drop writes `DROPPED.md` and sets `dropped` on the inventory record, which no recheck revives; clear
`dropped` to convert it again. A backend outage never drops a game.

`ported` in the inventory means the game passed its scenarios and validity checks; `evaluated` means nothing was
left to flag as well; `accepted` is a person's.

## Models

`muse` uses `rl-muse-spark-1-2-playground` unless you name a model (`muse:<model>`). The platform's default
(`...-1-1-playground`) sheds load with 503s for long stretches, and `...-1-3-sglang-playground` is slow and drops
the connection; `MuseCompletion().models()` lists what a key holds. `--effort` sets the reasoning effort (default
`medium`; at `minimal` the games came out wrong). Every model call is retried with growing waits when the connection
fails. `claude[:model]` is the `claude` CLI in print mode; it needs a terminal where `claude` can start.

The coding agents (`claude`, `metacode`) are run with the prompt on stdin, in the repository, with permission to
read, write, edit and run commands. Those flags have not been exercised: the CLIs refuse to start inside the
sandbox this was built in.

## Complexity

The platform builds a game from rules only when it is simple enough (`complexity.py`: at most 12 steps a round, 4
choice steps, 20 attributes, 3 hidden elements, one chance event a round, 15 rounds). The designer is given the
limits and must report its numbers; the built game is measured against them too.

## Where things go

```
gen_game/data/games/<id>/   variation.json VARIATION.md  spec.json SPEC.md  AGENT_PROMPT.md  game.json
                            encode_notes.md  scenarios.json  report.json REPORT.md  history/round_N/
                            DROPPED.md or PLATFORM_LIMIT.md when the flow stops
```

A converted game stays here until a person copies it into `xcolos/games/library/`.

## Not built yet

Tiers that need models (a skill ladder, a reasoning check). A spec review that pauses the flow for a person. Running
a coding agent from inside this sandbox.
