# gen_game

Turns a game from the inventory (`../gen_inventory/`) into a game file for the XColos platform, and tests it.
Design: `design/2026-10-05-game-generation-pipeline.md`.

```bash
.venv/bin/python -m gen_game convert ID                       # the idea is designed into rules (players, numbers, winner), then spec, build, scenarios, checks
.venv/bin/python -m gen_game convert ID --model muse          # Muse only, never Claude (plain python3 works for Muse)
.venv/bin/python -m gen_game convert ID --encoder claude      # a coding agent writes it (claude, metacode, command:...)
.venv/bin/python -m gen_game convert ID --redo adapt          # run a step again (adapt, spec, encode, scenarios)
.venv/bin/python -m gen_game convert ID --judge               # also gate the design (critic, balance checks; can drop a game)
.venv/bin/python -m gen_game convert ID --no-adapt            # the entry is finished rules: convert them as written
python3 -m gen_game verify ID variation|spec|game|scenarios    # check a file written by hand or by an agent
python3 -m gen_game show ID                                    # the report
python3 -m gen_game evaluate ID                                # tiers 0 and 1 on an existing game.json
.venv/bin/python -m gen_game simulate ID --players 'muse|gateway'   # real model players (installed game), logs under <game>/sim/, then the reasoning check
.venv/bin/python -m gen_game reasoning ID                      # did winning take reasoning and planning? REASONING.md, with quotes from the plays (also run by simulate and by every loop iteration)
.venv/bin/python -m gen_game batch --name NAME --ids-file ids.txt   # many games side by side on pinned code (8 at a time), play-tested; BATCH.md; same name resumes

python3 gen_game/run_tests.py
```

## The flow

```
inventory game
 A design    A designer works out rules from the XColos goal and the platform's RESTRICTIONS (what it can and
             cannot do, and its complexity limits), not from its file format. A separate critic must then find
             them BALANCED, PLAYABLE and rewarding REASONING OVER LUCK, showing its arithmetic, before they go on.
             They go back and forth up to 3 times.                          variation.json  VARIATION.md
 B spec      The rules' interface (attribute names, parameters, the `rank_by` that picks the winner, and an
             optional `min_to_win` bar below which no player wins) as a contract.
                                                                               spec.json  SPEC.md
 C build     A coder writes the game file from a prompt that carries the platform's API (design/actions.md,
             example games, the mistakes the loader has refused, a `verify` command that says when it is done).
             The coder is a model in a repair loop (`--encoder completion`) or a coding agent with tools
             (`--encoder claude|metacode|command:...`). An independent model writes scenario tests from the
             spec alone. The pipeline re-checks the file itself; it never takes the coder's word.
 D evaluate  Tier 0: valid, ends with a winner and its standings, same seed replays the same. Tier 1: does a
             thoughtless policy always win?
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

Every game that does not pass is marked in both places. The inventory record's `not_passed` says why
(`needs_review: 25/27 scenarios`, `play_failed: 2 of 3 plays ended; ...`, a failed step, a drop, a platform limit),
and `gen_inventory`'s index lists it as `not passed` unless it is dropped or blocked. The game folder has
`DROPPED.md`, `PLATFORM_LIMIT.md`, or, for everything else, `NOT_PASSED.md` with the reason and what to do next.
The status is left alone, so a game that needs review or failed a step is converted again. Passing clears
`not_passed` and moves an earlier run's file into `history/`. `convert` marks a game when it ends; `batch` also marks crashes and failed installs or play-tests.

## Models

The default is `gateway|muse`: Claude, or Muse when Claude cannot be reached. Specs joined by `|` are tried in turn;
the one that answers goes first from then on, so a model that is down costs one failed call, and the switch is printed
(`note: ... using <model> instead`). Muse needs the corporate network (off the VPN it answers 403
`network_access_required`); Claude needs the `anthropic` package (under plain `python3` the gateway is left out and
Muse is used alone). Model seats default to `muse|gateway`: Muse, or Claude when Muse cannot be reached.

`gateway` is Claude (`claude-opus-5-5` unless you name one, `gateway:<model>`) through Meta's AI Gateway,
the sanctioned route to third-party models for internal tools. There is no key: the local proxy (`localhost:10054`)
vouches for your Meta identity, and requests are labelled `x-meta-ai-gateway-calling-product: xcolos`, not sensitive.
It needs the `anthropic` package, which is installed in `.venv` only (`.venv/bin/pip install anthropic` from a normal
terminal; pip cannot reach PyPI from inside a Claude Code sandbox), so run the pipeline with `.venv/bin/python`.
`--effort minimal|low|medium|high` becomes the API's `low|low|medium|high`. This runs under your own identity, which
suits experiments; a team workload should register its own gateway with an access list and rate limits
(https://www.internalfb.com/intern/staticdocs/ai-gateway/docs/owning/onboarding). The `.venv` skips the base Python's
`sitecustomize`, which points `SSL_CERT_FILE` at Meta's CA bundle; the command line does the same at start-up, so
Muse's HTTPS calls verify under `.venv` too.

`muse` uses `rl-muse-spark-1-2-playground` unless you name a model (`muse:<model>`). The platform's default
(`...-1-1-playground`) sheds load with 503s for long stretches, and `...-1-3-sglang-playground` is slow and drops
the connection; `MuseCompletion().models()` lists what a key holds. `--effort` sets the reasoning effort (default
`medium`; at `minimal` the games came out wrong). Every model call is retried with growing waits when the connection
fails. `claude[:model]` is the `claude` CLI in print mode; it needs a terminal where `claude` can start (not a shell inside a
Claude Code session: macOS refuses the nested sandbox).

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
                            DROPPED.md, PLATFORM_LIMIT.md or NOT_PASSED.md when the game did not pass
```

A converted game stays here until a person copies it into `xcolos/games/library/`.

## Not built yet

Tiers that need models (a skill ladder, a reasoning check). A spec review that pauses the flow for a person. Running
a coding agent from inside this sandbox.
