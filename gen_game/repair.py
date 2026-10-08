"""Asking a model to correct what it just wrote.

A model call here is stateless: it gets one prompt and one system prompt, and nothing of what it
said before. So a repair request that names the problem but does not include the refused reply asks
the model to rewrite from nothing, and a long answer rewritten blind trades the old mistake for new
ones. A repair prompt therefore carries the previous reply as well as the complaint.
"""

from __future__ import annotations

MAX_PREVIOUS = 24000


def refused(base_prompt: str, reply: str, error: str, what: str = "reply") -> str:
    """The original request, the refused reply, the reason, and what to do about it.

    Built from the original every time, not appended to the last repair, so the prompt does not
    grow with each attempt and the model sees only the latest version and the latest complaint.
    """
    shown = reply if len(reply) <= MAX_PREVIOUS else reply[:MAX_PREVIOUS] + "\n... (cut)"
    return (f"{base_prompt}\n\nYOUR PREVIOUS {what.upper()} WAS REFUSED. Here it is:\n{shown}\n\n"
            f"Why it was refused: {error}\n"
            "Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.")
