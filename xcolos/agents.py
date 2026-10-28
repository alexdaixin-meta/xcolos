"""Agents: what actually sits in a seat.

Agents live on the client. Every one of them owns a Session, and no two agents
ever share one. A client hosting five seats holds five separate conversations
that never touch.

The interface is synchronous because the turn model is strictly sequential, one
seat acting at a time. Nothing is ever in flight concurrently.
"""

from __future__ import annotations

import re
from typing import Any, Callable, Protocol

from xcolos import calls
from xcolos.log import MatchLog
from xcolos.protocol import RESPONSE_REQUIRED, Action, ActionSchema, Envelope, MsgType
from xcolos.session import Session
from xcolos.state import Rng

DEFAULT_SYSTEM = (
    "You are a player in a multi-player game. "
    "You know only what you are told. "
    "When asked to act, answer with exactly one legal action."
)


class Agent(Protocol):
    """Everything a seat must implement."""

    name: str
    session: Session

    def bind(self, seat: int, match_id: str, owner: str = "") -> None:
        """Open this agent's session. Called once, when the seat is assigned."""
        ...

    def handle(self, env: Envelope) -> Action | None:
        """Handle one message. Returns an Action only for YOUR_TURN."""
        ...


class BaseAgent:
    """Session handling, shared by every agent.

    Subclasses implement `decide`. They never touch the session directly, which
    is what keeps the isolation guarantee in one place.
    """

    def __init__(
        self,
        name: str,
        system: str = DEFAULT_SYSTEM,
        token_budget: int = 8000,
    ) -> None:
        self.name = name
        self.system = system
        self.token_budget = token_budget
        # A placeholder until the server assigns a seat. Replaced on bind, so
        # the real session is always seat-specific from its first message.
        self.session = Session(-1, "unbound", system, token_budget)

    def bind(self, seat: int, match_id: str, owner: str = "") -> None:
        self.session = Session(
            seat, match_id, self.system, self.token_budget, owner=owner
        )

    def handle(self, env: Envelope) -> Action | None:
        self.session.observe(env)
        if env.type not in RESPONSE_REQUIRED:
            return None
        action = self.decide(env)
        if action is not None:
            self.session.record_action(action)
        return action

    def decide(self, env: Envelope) -> Action | None:
        raise NotImplementedError

    def transcript(self) -> str:
        return self.session.transcript()

    # -- helpers for subclasses ----------------------------------------

    @staticmethod
    def _schema(env: Envelope) -> ActionSchema:
        assert env.schema is not None, "YOUR_TURN always carries a schema"
        return env.schema


class ScriptedAgent(BaseAgent):
    """Always takes the first legal move. Fully deterministic.

    Fast, free and reproducible: the cheapest check that the runtime works end
    to end. It also makes a useful probe, because it cannot infer anything. If
    a scripted seat's session contains a secret, the kernel leaked it.
    """

    def __init__(self, name: str = "scripted", **kw: Any) -> None:
        super().__init__(name, **kw)
        self._spoken = 0

    def decide(self, env: Envelope) -> Action:
        schema = self._schema(env)
        if schema.target == "text":
            self._spoken += 1
            return Action(type=schema.id, text=f"Seat {env.seat} statement {self._spoken}.")
        if schema.target == "none":
            return Action(type=schema.id)
        if env.legal_targets:
            return Action(type=schema.id, target=env.legal_targets[0])
        return Action(type=schema.id)


class RandomAgent(BaseAgent):
    """Picks uniformly among the legal moves it was offered.

    Its generator is seeded from the match and its own seat, never from the
    kernel's, so it is reproducible without perturbing the game's own draws.
    """

    LINES = [
        "I am not convinced by seat {other}.",
        "Seat {other} has been very quiet.",
        "I have nothing solid yet. Watching seat {other}.",
        "Seat {other} is the obvious read.",
        "Nothing from seat {other} adds up.",
    ]

    def __init__(self, name: str = "random", seed: int = 0, **kw: Any) -> None:
        super().__init__(name, **kw)
        self._rng = Rng(seed)

    def decide(self, env: Envelope) -> Action:
        schema = self._schema(env)

        if schema.target == "text":
            others = [s for s in self.session.living_seats() if s != env.seat]
            other = self._rng.choice(others) if others else env.seat
            return Action(
                type=schema.id, text=self._rng.choice(self.LINES).format(other=other)
            )

        if schema.target == "none":
            return Action(type=schema.id)

        if schema.target == "number":
            low, high = schema.minimum, schema.maximum
            can_bid = low is not None and high is not None and low <= high
            if schema.choices and (not can_bid or self._rng.below(3) == 0):
                return Action(type=schema.id, target=schema.choices[0])
            if can_bid:
                return Action(type=schema.id, target=low + self._rng.below(high - low + 1))
            return Action(type=schema.id, target=low if low is not None else 0)

        if env.legal_targets:
            return Action(type=schema.id, target=self._rng.choice(list(env.legal_targets)))

        return Action(type=schema.id)


#: A model call. Takes the seat's own conversation and returns raw text.
#: Swapping in a real provider is a matter of supplying one of these.
Completion = Callable[[list[dict[str, str]], Envelope], str]


class LLMAgent(BaseAgent):
    """A seat backed by a language model.

    The model is injected rather than constructed here, so the transport is not
    this class's business. A real provider, a local endpoint, and the offline
    stub below all satisfy the same signature.

    The prompt is built from this seat's session alone. Nothing else is in
    scope, so the model physically cannot condition on another seat's view.
    """

    def __init__(
        self,
        name: str,
        completion: Completion,
        persona: str = "",
        model: str = "unspecified",
        **kw: Any,
    ) -> None:
        system = kw.pop("system", DEFAULT_SYSTEM)
        if persona:
            system = f"{system}\n\nYour manner: {persona}"
        super().__init__(name, system=system, **kw)
        self.completion = completion
        self.persona = persona
        self.model = model
        self.calls = 0
        #: Where this seat's model calls are written. Set by whoever runs the
        #: table, once per game, because the agent outlives any one game's log.
        self.log: MatchLog | None = None

    def decide(self, env: Envelope) -> Action | None:
        schema = self._schema(env)
        self.calls += 1
        messages = self.session.messages()
        system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
        talk = "\n\n".join(f"[{m['role']}]\n{m['content']}"
                            for m in messages if m["role"] != "system")
        raw = calls.call(self.log, f"seat {env.seat}", self.model, system, talk,
                         lambda: self.completion(messages, env))
        return parse_action(raw, schema, env.legal_targets)


def parse_action(
    raw: str, schema: ActionSchema, legal_targets: tuple[Any, ...]
) -> Action | None:
    """Turn model output into an action.

    Deliberately forgiving about form and strict about content. A model that
    wraps a number in prose should not lose the game, but one that names an
    illegal target must be rejected so the repair ladder can correct it.
    """
    import json

    text = (raw or "").strip()
    if not text:
        return None

    if schema.target == "text":
        # Seats are told to keep any reasoning before the answer, so a reply in several paragraphs is reasons, then the
        # message: only the last paragraph goes to the table, and the reasons stay private (a note no other seat is told).
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        if len(paragraphs) > 1:
            return Action(type=schema.id, text=paragraphs[-1], notes={"reason": "\n\n".join(paragraphs[:-1])})
        return Action(type=schema.id, text=text)

    # A well-formed object, possibly inside a fenced block.
    block = re.search(r"\{.*\}", text, re.DOTALL)
    if block:
        try:
            data = json.loads(block.group(0))
            target = data.get("target", data.get("seat"))
            if target is not None:
                return Action(type=schema.id, target=_coerce(target, legal_targets))
        except (ValueError, TypeError):
            pass

    # Seats are told to reason first and answer last, so the reasoning names
    # other options, numbers and seats. The answer is the last line when that
    # line is one legal answer; otherwise the last legal answer the reply
    # mentions. Never the first option in the game's own order.
    words = tuple(schema.choices) if schema.target in ("number", "enum") else ()
    if schema.target == "enum" and not words:
        words = tuple(legal_targets)
    final = _final_answer(text, schema.target, words)
    if final is not None:
        return Action(type=schema.id, target=_coerce(final, legal_targets))

    best, at = None, -1
    for choice in words:
        for m in re.finditer(_word_pattern(choice), text, re.IGNORECASE):
            if m.start() > at:
                best, at = choice, m.start()
    if schema.target != "enum":
        # A minus only after a non-word: the 400 of "240-400" is 400, not -400.
        # Matched on `text` itself, so positions compare with the words above.
        for m in re.finditer(r"(?:(?<![\w-])-)?(?<!\d)\d+(?:,\d{3})*(?!\d)", text):
            if m.start() > at:
                best, at = m.group(0).replace(",", ""), m.start()
        if best is not None and schema.target == "number" and best not in words:
            best = int(best)
    if best is None:
        return None
    return Action(type=schema.id, target=_coerce(best, legal_targets))


def _norm(value: Any) -> str:
    """An answer as compared: lower case, `_` and spaces alike."""
    return re.sub(r"[\s_]+", " ", str(value).strip().lower())


def _word_pattern(choice: Any) -> str:
    """Matches `choice` as a whole word, with `_` and spaces interchangeable."""
    parts = [re.escape(p) for p in re.split(r"[\s_]+", str(choice).strip()) if p]
    return r"(?<![\w])" + r"[\s_]+".join(parts) + r"(?![\w])"


def _final_answer(text: str, target: str, words: tuple[Any, ...]) -> Any:
    """The reply's last line, if it is exactly one answer of this kind."""
    line = text.strip().splitlines()[-1]
    line = _norm(line.strip().strip("*`\"'.").strip())
    line = re.sub(r"^(?:final answer|answer|my answer|i choose|i bid)\s*[:\-]?\s*", "", line)
    line = line.strip("*`\"'.").strip()
    for choice in words:
        if line == _norm(choice) or line == "seat " + _norm(choice):
            return choice
    if target in ("number", "seat"):
        m = re.fullmatch(r"(?:seat\s*)?(-?\d+)", line.replace(",", ""))
        if m:
            return int(m.group(1))
    return None


def _coerce(value: Any, legal_targets: tuple[Any, ...]) -> Any:
    """Match the type of the legal targets, so validation compares like for like."""
    if legal_targets and isinstance(legal_targets[0], int):
        try:
            return int(value)
        except (ValueError, TypeError):
            return value
    # A number for an answer the game lists as text ("10" among a hand of cards): that text,
    # so it matches. Only an answer that would otherwise be refused changes.
    if (isinstance(value, int) and not isinstance(value, bool)
            and value not in legal_targets and str(value) in legal_targets):
        return str(value)
    return value


def offline_model(seed: int = 0) -> Completion:
    """A stand-in for a real provider.

    No network is reachable from this machine, so this exists to exercise the
    full model-backed path: session in, raw text out, parsed and validated like
    anything else. It reads the prompt the way a model would, from the
    conversation alone, and answers in the loose formats a model actually emits.
    """
    rng = Rng(seed)

    def complete(messages: list[dict[str, str]], env: Envelope) -> str:
        schema = env.schema
        assert schema is not None

        if schema.target == "text":
            seen = sum(1 for m in messages if m["role"] == "user")
            return rng.choice(
                [
                    f"Going on what I have heard across {seen} updates, I am unsure.",
                    "I would rather hear from someone who has said nothing yet.",
                    "Nothing in the last round changed my read.",
                ]
            )

        if schema.target == "number":
            low, high = schema.minimum, schema.maximum
            if low is not None and high is not None and low <= high and rng.below(2):
                return f"I bid {low + rng.below(high - low + 1)}."
            return f"I {schema.choices[0]}." if schema.choices else f"{low or 0}"

        if env.legal_targets:
            target = rng.choice(list(env.legal_targets))
            # Deliberately varied, loose formats, to exercise the parser.
            return rng.choice(
                [
                    f'{{"target": {target}}}',
                    f"I choose seat {target}.",
                    f"```json\n{{\"target\": {target}}}\n```",
                ]
            )

        return "{}"

    return complete


class BrokenAgent(BaseAgent):
    """Always answers invalidly. Exercises the repair ladder."""

    def __init__(self, name: str = "broken", mode: str = "bad_type", **kw: Any) -> None:
        super().__init__(name, **kw)
        self.mode = mode

    def decide(self, env: Envelope) -> Action | None:
        if self.mode == "silent":
            return None
        if self.mode == "bad_target":
            return Action(type=self._schema(env).id, target=9999)
        return Action(type="not_a_real_action")


class SilentAgent(BaseAgent):
    """Never answers. Should be carried by the declared default action."""

    def __init__(self, name: str = "silent", **kw: Any) -> None:
        super().__init__(name, **kw)

    def decide(self, env: Envelope) -> Action | None:
        return None
