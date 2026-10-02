"""A scripted referee that decides `winner` endings by a score the test names.

The oracle for a model-decided winner: the test states in Python the rule the
game states in words, and the referee answers by it, reading the same full
table the model would be shown.
"""

from __future__ import annotations

from typing import Callable

from xcolos.flow.judge import ScriptedJudge


def referee(score: Callable[[dict], float], highest: bool = True) -> ScriptedJudge:
    """Names the players whose `score(attributes)` is best; level ones share."""

    def answer(call):
        assert call.where.tag == "winner", call.where.tag
        scores = {p["id"]: score(p["attributes"]) for p in call.table["players"]}
        best = (max if highest else min)(scores.values())
        return [seat for seat, s in scores.items() if s == best]

    return ScriptedJudge(answer)
