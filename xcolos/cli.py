"""Command line entry point: run matches, then read what happened."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

from xcolos.agents import ScriptedAgent
from xcolos.game import Game
from xcolos.host import LocalAgentHost, Registry
from xcolos.log import MatchLog, validate_log
from xcolos.orchestrators.mafia import MafiaOrchestrator
from xcolos.runner import MatchResult, Runner
from xcolos.transcript import seat_transcript, summarize, timeline

SEAT_NAMES = ["Ada", "Blaise", "Curie", "Dirac", "Euler", "Fermi", "Gauss"]
SEATS = 5


def build_match(seed: int, out_dir: Path | None = None, agent_factory=None):
    """Wire up one match, including the client registration handshake.

    The client offers the seats it owns. The server assigns the indices and
    records which host speaks for each one. A local run is the same handshake
    with one in-process host holding every seat.
    """
    agent_factory = agent_factory or (lambda i, name: ScriptedAgent(name=name))

    match_id = f"m_{seed:08d}"
    path = out_dir / f"{match_id}.jsonl" if out_dir else None
    log = MatchLog(match_id, path)
    game = Game(match_id=match_id, game_id=MafiaOrchestrator.game_id, seed=seed, log=log)

    host = LocalAgentHost(
        [agent_factory(i, name) for i, name in enumerate(SEAT_NAMES[:SEATS])]
    )
    registry = Registry(match_id)
    for binding in host.register():
        index = game.register_seat(binding.name, host.host_id, binding.profile)
        registry.attach(index, host, binding)

    return game, MafiaOrchestrator(), registry, host


def run_match(seed: int, out_dir: Path | None = None) -> tuple[MatchResult, Game]:
    game, orchestrator, registry, _host = build_match(seed, out_dir)
    return Runner(game, orchestrator, registry).run(), game


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="xcolos", description="Run XColos matches.")
    parser.add_argument("--seed", type=int, default=1, help="starting seed")
    parser.add_argument("--matches", type=int, default=1, help="how many to run")
    parser.add_argument("--out", type=Path, default=None, help="directory for match logs")
    parser.add_argument(
        "--timeline", action="store_true", help="print the full match timeline"
    )
    parser.add_argument(
        "--seat", type=int, default=None, help="print one seat's whole world"
    )
    parser.add_argument(
        "--messages", action="store_true", help="include every message in the timeline"
    )
    parser.add_argument(
        "--check", action="store_true", help="structurally validate each log"
    )
    args = parser.parse_args(argv)

    winners: Counter[str] = Counter()
    problems_found = 0

    for i in range(args.matches):
        result, game = run_match(args.seed + i, args.out)
        winners[result.winner or result.status] += 1
        records = game.log.records

        if args.check:
            problems = validate_log(records)
            problems_found += len(problems)
            status = "ok" if not problems else "PROBLEMS"
            print(f"{result.match_id} log: {status}")
            for p in problems:
                print(f"  - {p}")

        if args.matches == 1:
            print(f"=== {result.match_id} ===")
            print(f"{result.status}: {result.winner} ({result.reason})")
            print(
                f"turns={result.turns} rounds={result.rounds} "
                f"degraded={result.degraded_turns} records={len(records)}"
            )
            if args.timeline:
                show = {"process", "fact", "orchestrator", "turn", "result"}
                if args.messages:
                    show.add("message")
                print("\n" + timeline(records, show))
            if args.seat is not None:
                print(f"\n--- everything seat {args.seat} ever saw ---")
                print(seat_transcript(records, args.seat))
            if not args.timeline and args.seat is None:
                print(summarize(records)["counts"])

    if args.matches > 1:
        print(f"\n{args.matches} matches from seed {args.seed}:")
        for winner, count in winners.most_common():
            print(f"  {winner}: {count} ({count / args.matches:.0%})")

    return 1 if problems_found else 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
