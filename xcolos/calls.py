"""Every call the server makes to a language model, written to the match log.

One record per call, whatever it was for and however it ended:

    for       what asked: "review", "seat 2", ...
    model     which model answered
    system    the standing half of the prompt
    prompt    the half that changes every call
    raw       the model's reply, unparsed
    error     why there was no reply, instead of `raw`
    seconds   how long it took

The point of logging the call here, rather than its result wherever the
result is used, is that nothing can call a model without passing through
`call()`. Anything added later is logged without anyone remembering to.

The referee is the one exception: its `judge_call` record already carries all
of this and the ruling beside it, so it is not written twice.

Prompts can hold every hidden role and value. That is safe because this goes
to the log, which is the operator's view, and never into a fact.
"""

from __future__ import annotations

import time
from typing import Any, Callable

from xcolos.log import MatchLog


def call(
    log: MatchLog | None,
    purpose: str,
    model: str,
    system: str,
    prompt: str,
    send: Callable[[], Any],
) -> Any:
    """Make one model call through `send()`, and log it however it ends."""
    if log is None:
        return send()
    started = time.time()
    fields = {"for": purpose, "model": model, "system": system, "prompt": prompt}
    try:
        raw = send()
    except Exception as error:
        log.record("model", "model_call", **fields, error=str(error),
                   seconds=round(time.time() - started, 2))
        raise
    log.record("model", "model_call", **fields, raw=str(raw),
               seconds=round(time.time() - started, 2))
    return raw


class Logged:
    """A completion whose every call is logged. Same shape as what it wraps."""

    def __init__(self, completion: Any, log: MatchLog, purpose: str) -> None:
        self.completion = completion
        self.log = log
        self.purpose = purpose
        self.model = getattr(completion, "model", "") or ""

    def complete(self, prompt: str, system: str = "") -> str:
        return call(self.log, self.purpose, self.model, system, prompt,
                    lambda: self.completion.complete(prompt, system=system))
