"""Per-agent sessions.

Every seat has its own session. Sessions are never shared, never merged, and
never read by anything but the agent that owns them. Two seats hosted by the
same client still hold two entirely separate objects.

This matters for more than tidiness. The kernel guarantees that a seat is only
ever *sent* what it is entitled to. The session is what guarantees a seat only
ever *remembers* what it was sent. A shared buffer, or a prompt cache keyed
across seats, would leak past a kernel that is doing its job perfectly.

A session holds the conversation in the standard chat shape, so handing it to a
model provider is a direct mapping rather than a translation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

from xcolos.protocol import RESPONSE_REQUIRED, Action, Envelope, MsgType

#: Rough characters per token. No tokeniser is installed and none is reachable,
#: so budgets are approximate and deliberately conservative.
CHARS_PER_TOKEN = 4


@dataclass
class Turn:
    """One entry in a seat's conversation."""

    role: str  # "system" | "game" | "agent"
    content: str
    kind: str = ""  # the message type, for game turns
    turn_seq: int | None = None
    #: Pinned turns are never dropped by compaction. The setup block is pinned,
    #: because a seat that forgets its own role is not playing the game.
    pinned: bool = False

    @property
    def chat_role(self) -> str:
        return {"system": "system", "game": "user", "agent": "assistant"}[self.role]

    def to_json(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "kind": self.kind,
            "turn_seq": self.turn_seq,
            "pinned": self.pinned,
            "content": self.content,
        }


class Session:
    """One seat's whole memory.

    Created per seat per match. The identifier is stable and unique, which is
    what any provider-side session or prompt cache must be keyed by.
    """

    def __init__(
        self,
        seat: int,
        match_id: str,
        system: str = "",
        token_budget: int = 8000,
        owner: str = "",
    ) -> None:
        self.seat = seat
        self.match_id = match_id
        self.session_id = f"{match_id}:seat{seat}"
        self.token_budget = token_budget
        #: The player this session belongs to. A session holds a seat's
        #: secrets, so it is never anonymous and never reassigned.
        self.owner = owner

        self.turns: list[Turn] = []
        self.dropped = 0
        #: Everything before the seat's first turn is setup, and stays pinned.
        self._seen_own_turn = False

        if system:
            self.turns.append(Turn(role="system", content=system, pinned=True))

    # ------------------------------------------------------------------
    # Writing
    # ------------------------------------------------------------------

    def observe(self, env: Envelope) -> Turn:
        """Record something the server sent this seat."""
        turn = Turn(
            role="game",
            content=env.body,
            kind=env.type.value,
            turn_seq=env.turn_seq,
            pinned=not self._seen_own_turn,
        )
        if env.type in RESPONSE_REQUIRED:
            self._seen_own_turn = True
        self.turns.append(turn)
        self.compact()
        return turn

    def record_action(self, action: Action) -> Turn:
        """Record what this seat said back."""
        content = action.text or f"{action.type} -> {action.target}"
        turn = Turn(role="agent", content=content, kind=action.type)
        self.turns.append(turn)
        self.compact()
        return turn

    def note(self, content: str) -> Turn:
        """Record a private thought. Never leaves the client."""
        turn = Turn(role="agent", content=content, kind="note")
        self.turns.append(turn)
        return turn

    # ------------------------------------------------------------------
    # Budget
    # ------------------------------------------------------------------

    @property
    def estimated_tokens(self) -> int:
        return sum(len(t.content) for t in self.turns) // CHARS_PER_TOKEN

    def compact(self) -> int:
        """Drop the oldest unpinned turns until the session fits its budget.

        Deterministic and free. No model call sits in the memory path, so two
        runs of a seed compact identically. A summarising policy would be an
        improvement and a source of nondeterminism, so it stays opt-in.
        """
        removed = 0
        while self.estimated_tokens > self.token_budget:
            index = next(
                (i for i, t in enumerate(self.turns) if not t.pinned), None
            )
            if index is None:
                break  # everything left is pinned; nothing more can go
            self.turns.pop(index)
            removed += 1
        self.dropped += removed
        return removed

    # ------------------------------------------------------------------
    # Reading
    # ------------------------------------------------------------------

    def messages(self) -> list[dict[str, str]]:
        """The conversation in chat shape, ready for a provider."""
        out: list[dict[str, str]] = []
        if self.dropped:
            out.append(
                {
                    "role": "system",
                    "content": f"[{self.dropped} earlier messages were dropped to fit the context window]",
                }
            )
        for t in self.turns:
            out.append({"role": t.chat_role, "content": t.content})
        return out

    def transcript(self) -> str:
        return "\n".join(
            f"[{t.kind or t.role}] {t.content}" for t in self.turns
        )

    def living_seats(self) -> list[int]:
        """Seats this agent believes are alive, from what it was told.

        Parsed from the kernel's own wording. An agent knows nothing it was not
        sent, and that includes this.
        """
        import re

        for turn in reversed(self.turns):
            match = re.search(r"Living seats: \[([\d, ]*)\]", turn.content)
            if match:
                return [int(x) for x in match.group(1).split(",") if x.strip()]
        return []

    def snapshot(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "seat": self.seat,
            "owner": self.owner,
            "turns": len(self.turns),
            "dropped": self.dropped,
            "estimated_tokens": self.estimated_tokens,
            "token_budget": self.token_budget,
            "history": [t.to_json() for t in self.turns],
        }

    def __iter__(self) -> Iterator[Turn]:
        return iter(self.turns)

    def __len__(self) -> int:
        return len(self.turns)
