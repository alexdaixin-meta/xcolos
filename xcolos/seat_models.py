"""A real model in a seat.

`LLMAgent` takes any `completion(messages, env) -> text`. This turns a model spec, the same strings the
rest of the platform uses, into one:

    claude[:model]       the `claude` command in print mode (no key to handle)
    muse[:model]         Meta's Model API
    anthropic[:model]    the Anthropic API (needs ANTHROPIC_API_KEY)
    command:<program>    any program: prompt on stdin, reply on stdout
    offline              the built-in stub, for checking the wiring
    muse|gateway         either, the first preferred: whichever answers

Each decision sends the seat's whole session again: nothing is kept on the provider's side, so a seat sees
only what its own session holds.
"""

from __future__ import annotations

import time
from typing import Callable

from xcolos.flow.backends import CommandCompletion, CompletionError, FallbackCompletion, MuseCompletion, from_spec, split_alternatives

#: Said to every model seat. The game's own rules arrive as the first message, so this says only what a
#: player is and how to answer; it must fit any game, and must not say what kind of game it is. Reasons are invited before
#: the answer, so a play can be read for how its players thought (gen_game's reasoning check), but never demanded: told to
#: give them, Claude refused some moves as reasoning extraction and the plays stopped.
SEAT_SYSTEM = (
    "You are one player in a game on the XColos platform, played by turns. You know only what the game tells you; "
    "other players' hidden information is hidden from you as yours is from them. Your goal is to win. "
    "Think about the rules, the other players and what they have done, then act. "
    "When you are asked to act, reply with exactly one legal answer in the form the question asks for, "
    "and keep any reasoning short and before the answer. Do not ask questions back."
)


def _seat_model(spec: str, timeout_s: int):
    kind, _, rest = spec.partition(":")
    kind = kind.strip().lower()
    if kind == "claude":
        return CommandCompletion(["claude", "-p", "--bare", "--model", rest.strip() or "claude-opus-5-5"], timeout_s=timeout_s)
    if kind == "muse":
        from xcolos.flow.backends import MUSE_FALLBACKS, muse_first_choice

        return MuseCompletion(model=rest.strip()) if rest.strip() else MuseCompletion(model=muse_first_choice(), fallbacks=MUSE_FALLBACKS)
    return from_spec(spec)


def seat_completion(spec: str, timeout_s: int = 300, retries: int = 2, pause: Callable[[float], None] = time.sleep):
    """The `completion(messages, env)` a model seat calls, for a model spec. `muse|gateway` is whichever of the two answers."""
    if spec.partition(":")[0].strip().lower() == "offline":
        from xcolos.agents import offline_model

        return offline_model(0)
    alternatives = split_alternatives(spec)
    inner = FallbackCompletion([_seat_model(p, timeout_s) for p in alternatives]) if len(alternatives) > 1 else _seat_model(spec, timeout_s)

    def complete(messages: list[dict[str, str]], env) -> str:
        system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
        talk = "\n\n".join(f"[{m['role']}]\n{m['content']}" for m in messages if m["role"] != "system")
        for attempt in range(retries + 1):
            try:
                return inner.complete(talk, system=system)
            except CompletionError:
                if attempt == retries:
                    raise
                pause(5 * 2 ** attempt)
        raise AssertionError("unreachable")

    return complete
