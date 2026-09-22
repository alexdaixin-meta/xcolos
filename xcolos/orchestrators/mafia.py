"""Mafia, hardcoded.

Stage 1a deliberately hardcodes one game so the kernel can be proven without any
nondeterminism in the system. Every rule here moves into a YAML file plus prose
in stage 1b, and this file is deleted. Nothing below the orchestrator interface
knows the difference.
"""

from __future__ import annotations

from collections import Counter

from xcolos.game import Game
from xcolos.orchestrators.base import ActionRequest, GameBrief, Play
from xcolos.protocol import ActionSchema
from xcolos.state import Audience, Seat

SPEAK = ActionSchema(id="speak", target="text", default="pass")
KILL = ActionSchema(id="kill", target="seat", default="random")
INVESTIGATE = ActionSchema(id="investigate", target="seat", default="random")
VOTE = ActionSchema(id="vote", target="seat", default="random")


MIN_SEATS = 4
MAX_SEATS = 12


def role_plan(seats: int) -> list[tuple[str, str]]:
    """Roles for a table of this size.

    The mafia count is kept low deliberately. Too many and the first night kill
    makes the factions equal, so the match ends before anyone speaks and the
    discussion and voting paths never execute.
    """
    if not MIN_SEATS <= seats <= MAX_SEATS:
        raise ValueError(f"mafia needs between {MIN_SEATS} and {MAX_SEATS} seats")
    mafia = 1 if seats <= 6 else 2 if seats <= 9 else 3
    villagers = seats - mafia - 1  # one detective
    return (
        [("mafia", "evil")] * mafia
        + [("detective", "good")]
        + [("villager", "good")] * villagers
    )


RULES = """Mafia is a hidden-role game. Every player is secretly either mafia or a
member of the town. The mafia know each other. Nobody else knows anything.

Each round has three parts.

  Night     The mafia privately choose one player to kill. The detective
            privately investigates one player and learns whether they are
            evil. Everyone knows night has fallen; only the mafia and the
            detective act, and only they see what they did.
  Day       The death is announced to everyone, then every living player
            speaks once, in seat order, to the whole table.
  Voting    Every living player names someone to eliminate. Votes are
            private until all are in, then the tally is announced and the
            player with the most votes is eliminated and their role revealed.
            A tie eliminates nobody.

The town wins when every mafia is dead. The mafia win when they equal or
outnumber the town. Eliminated players see everything public that follows, but
never act again."""


class MafiaOrchestrator:
    """Mafia, hardcoded, for any table between four and twelve seats."""

    game_id = "mafia"

    def __init__(self, discussion_rounds: int = 1) -> None:
        self.discussion_rounds = discussion_rounds

    # ------------------------------------------------------------------

    def setup(self, game: Game) -> None:
        indices = sorted(game.seats)
        order = role_plan(len(indices))
        game.rng.shuffle(order)
        for seat, (role, faction) in zip(indices, order):
            game.set_role(seat, role, faction)
            game.emit_fact(
                "role_assigned",
                {"role": role, "faction": faction},
                Audience.only(seat),
            )

        mafia = self._by_role(game, "mafia")
        game.emit_fact("allies", {"seats": mafia}, Audience.only(*mafia))

    def brief(self, game: Game) -> GameBrief:
        """The game content of the briefing. Identical for every seat.

        Nothing here is seat-specific. A seat's own role reaches it through its
        entitled setup facts, not through this, so the orchestrator has no way
        to write a secret into someone's briefing.
        """
        return GameBrief(
            name="Mafia",
            rules=RULES,
            seat_count=len(game.seats),
            round_shape=["night", "day_reveal", "day_discussion", "day_voting"],
            actions=[KILL, INVESTIGATE, SPEAK, VOTE],
        )

    # ------------------------------------------------------------------

    def play(self, game: Game) -> Play:
        while True:
            game.advance_round()

            victim = yield from self._night(game)
            if self._resolve_and_check(game, victim):
                return

            yield from self._discussion(game)

            voted = yield from self._vote(game)
            if self._resolve_vote_and_check(game, voted):
                return

    # ------------------------------------------------------------------
    # Phases
    # ------------------------------------------------------------------

    def _night(self, game: Game) -> object:
        game.set_phase("night")
        # Everyone knows the phase. Only the night actions are secret, so this
        # is broadcast; the kill and the investigation below are not.
        game.emit_fact("phase", {"phase": "night"}, Audience.all())
        mafia = self._by_role(game, "mafia", alive_only=True)

        targets: list[int] = []
        for seat in mafia:
            legal = tuple(s for s in game.active_seats() if game.seats[s].faction != "evil")
            if not legal:
                break
            action = yield ActionRequest(
                seat=seat,
                schema=KILL,
                prompt="It is night. Choose a seat for your side to kill.",
                legal_targets=legal,
                reason="night_action:mafia",
            )
            targets.append(int(action.target))

        victim = None
        if targets:
            # First mafia's choice decides ties, so the outcome never depends
            # on response timing.
            victim = Counter(targets).most_common(1)[0][0]
            game.emit_fact("kill_target", {"seat": victim}, Audience.only(*mafia))

        for seat in self._by_role(game, "detective", alive_only=True):
            legal = tuple(s for s in game.active_seats() if s != seat)
            if not legal:
                continue
            action = yield ActionRequest(
                seat=seat,
                schema=INVESTIGATE,
                prompt="Choose a seat to investigate.",
                legal_targets=legal,
                reason="night_action:detective",
            )
            target = int(action.target)
            result = "evil" if game.seats[target].faction == "evil" else "not evil"
            game.emit_fact(
                "investigation",
                {"seat": target, "result": result},
                Audience.only(seat),
            )

        return victim

    def _discussion(self, game: Game) -> Play:
        game.set_phase("day_discussion")
        game.emit_fact("phase", {"phase": "day_discussion"}, Audience.all())

        for _ in range(self.discussion_rounds):
            # One pass in index order. The cursor is kernel-owned, so speaking
            # order never depends on model output or on latency.
            for seat in game.eligible_seats():
                action = yield ActionRequest(
                    seat=seat,
                    schema=SPEAK,
                    prompt="Say something to the town.",
                    reason="discussion_rotation",
                )
                game.emit_fact(
                    "speech", {"seat": seat, "text": action.text}, Audience.all()
                )

    def _vote(self, game: Game) -> object:
        game.set_phase("day_voting")
        game.emit_fact("phase", {"phase": "day_voting"}, Audience.all())

        votes: dict[int, int] = {}
        for seat in game.eligible_seats():
            legal = tuple(s for s in game.active_seats() if s != seat)
            if not legal:
                continue
            action = yield ActionRequest(
                seat=seat,
                schema=VOTE,
                prompt="Vote for a seat to eliminate.",
                legal_targets=legal,
                reason="voting",
            )
            target = int(action.target)
            votes[seat] = target
            # Private until everyone has voted. A sequential run of turns with
            # results withheld is how this design does a simultaneous vote.
            game.emit_fact(
                "vote_cast", {"seat": seat, "target": target}, Audience.only(seat)
            )

        tally = Counter(votes.values())
        # String keys: the log must round trip through JSON, which has no
        # integer keys.
        game.emit_fact(
            "vote_tally",
            {"tally": {str(k): v for k, v in sorted(tally.items())}},
            Audience.all(),
        )
        if not tally:
            return None
        top = tally.most_common()
        if len(top) > 1 and top[0][1] == top[1][1]:
            return None
        return top[0][0]

    # ------------------------------------------------------------------
    # Resolution
    # ------------------------------------------------------------------

    def _resolve_and_check(self, game: Game, victim: object) -> bool:
        game.set_phase("day_reveal")
        game.emit_fact("phase", {"phase": "day_reveal"}, Audience.all())
        if victim is None:
            game.emit_fact("no_death", {}, Audience.all())
        else:
            seat = int(victim)
            role = game.seats[seat].role
            game.eliminate(seat)
            game.emit_fact("death", {"seat": seat, "role": role}, Audience.all())
        return self._check_win(game)

    def _resolve_vote_and_check(self, game: Game, voted: object) -> bool:
        if voted is None:
            game.emit_fact("no_elimination", {}, Audience.all())
        else:
            seat = int(voted)
            role = game.seats[seat].role
            game.eliminate(seat)
            game.emit_fact("eliminated", {"seat": seat, "role": role}, Audience.all())
        return self._check_win(game)

    def _check_win(self, game: Game) -> bool:
        evil = sum(1 for s in game.seats.values() if s.alive and s.faction == "evil")
        good = sum(1 for s in game.seats.values() if s.alive and s.faction == "good")
        if evil == 0:
            self._finish(game, "good", "all mafia are dead")
            return True
        if evil >= good:
            self._finish(game, "evil", "mafia equal or outnumber the town")
            return True
        return False

    def _finish(self, game: Game, winner: str, reason: str) -> None:
        game.emit_fact(
            "game_over", {"winner": winner, "reason": reason}, Audience.all()
        )
        game.end_game(winner, reason)

    # ------------------------------------------------------------------

    @staticmethod
    def _by_role(game: Game, role: str, alive_only: bool = False) -> list[int]:
        return [
            i
            for i, s in sorted(game.seats.items())
            if s.role == role and (s.alive or not alive_only)
        ]
