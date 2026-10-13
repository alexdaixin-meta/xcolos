# Logging for manual UI play (built)

## Problem
A match played in the web console lives only in the server's memory (`MatchLog(match_id)` in `MatchManager._new_game`
is built with no path). A restart, or a closed table, loses it, so a manual play cannot be reviewed later.

## What already exists
- `MatchLog` takes an optional `path`. With one it appends every record as a JSON line and flushes at once, so a
  half-played or crashed game is still on disk up to its last record. Nothing new is needed in the log itself.
- A table (`w0001`) hosts a sequence of games. Game 1 is logged as `w0001`, later games as `w0001-g2`, `-g3`.
  Each game has its own `MatchLog`, so one file per game falls out naturally.
- Model calls are already records in the same log (`LLMAgent.log = log`), so seat model calls, refusals and
  fallbacks are in the file too.

## Proposal
1. **One file per game**, written as it is played: `<log_dir>/<run>/<game_id>/<match_id>.jsonl`.
2. **Table ids are not unique across restarts** (the counter restarts at `w0001`), so a restarted server would
   overwrite or mix files. Name the folder by server start time: `runs/web/2026-10-12T23-24-39/`, and inside it
   `w0001.jsonl`, `w0001-g2.jsonl`. Each file name is then unique, and a session is one folder.
3. **Where:** `runs/web/` by default (already git-ignored). `--log-dir PATH` on `python3 -m xcolos.web` changes it,
   `--no-log` turns it off. Tests keep using in-memory logs (no path), so they write nothing.
4. **A small index per game**: when a game ends (or the table closes), write `<match_id>.summary.json` beside the log with game id,
   seats and who was behind each (human, bot, model name), seed, result, round count, start/end time. Without it, finding
   "the Coup game I played at 3pm" means opening files.
5. **Unfinished games** keep their log; the summary says `"status": "abandoned"` if the server stops mid-game
   (written on shutdown if possible; otherwise the log simply has no `game_over` record, which is what marks it).
6. **Human moves**: they are `turn/move` records already (the same as bots), with the seat, so no extra capture.
   A seat's `host`/`profile` is in `setup/register_seat`, which tells human from model.

## Change surface
- `xcolos/web/server.py`: `MatchManager(log_dir=None)`; `_new_game` passes `path` to `MatchLog`; call a
  `_write_summary` when `game_over` fires; `serve(port, log_dir)` creates the session folder; two CLI flags.
- No change to `log.py`, the engine, or any game file.
- Tests: with a `log_dir`, a played game leaves `<id>.jsonl` whose records equal `game.log.records`; two games on one table give
  two files; no `log_dir` writes nothing; summary has the result.

## Open questions
1. Keep `runs/web/` forever, or prune old sessions? (Proposed: keep, they are small; ~50 KB per Coup game of 18 turns.)
2. Should the model prompts/replies be logged in full? Today the log has them for model seats; for human seats there is
   only the move. Proposed: leave as is.
3. Should a finished game's review (`result/review`) be in the same file? It already is a record in the log, so yes
   once it is written (it comes after `game_over`, so the file keeps growing a little after the end).

## Decisions (2026-10-12) and what was built
- Old sessions are ignored (kept, never pruned). Human seats are logged as moves only.
- **Seat to model is logged:** a `setup/seat_model` record per seat (`seat, name, kind, model`; `model` is null for a person
  or a plain bot, `offline-stub` for an `llm` seat with no model named) and the same in the summary.
- **The post-game review is in the log.** The runner closes the log when the match concludes, before the review is written, so
  `MatchLog.record` now appends to the file when it has been closed. The summary file is written after the review.
- Size: a Coup game of 18 turns is about 0.9 MB, not 50 KB (most of it `delivery/*` records).
- Flags: `python3 -m xcolos.web --log-dir runs/web` (the default; one dated folder per start) and `--no-log`.
- Tests: `tests/test_server_logging.py`.
