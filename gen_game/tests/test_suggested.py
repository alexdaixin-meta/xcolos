"""The suggested table size: designed first, carried through, and what the real-model run plays at."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import PLAN, SPEC  # noqa: E402
from gen_game import adapt, simulate, spec as specmod  # noqa: E402


def with_players(plan, **players):
    out = copy.deepcopy(plan)
    out["variation"]["players"] = {"min": 3, "max": 5, **players}
    return out


def test_the_designer_is_asked_for_the_best_size_and_a_suggestion_outside_the_range_is_refused():
    assert "`suggested` is the table size the game plays BEST at" in adapt.IDEA_MODE
    assert not [p for p in adapt.problems(with_players(PLAN, suggested=4)) if "suggested" in p]
    bad = adapt.problems(with_players(PLAN, suggested=7))
    assert any("suggested must be a whole number from 3 to 5" in p for p in bad)


def test_the_spec_carries_it_and_the_script_and_source_record_say_it():
    spec = {**SPEC, "players": {"min": 3, "max": 5, "suggested": 4}}
    assert specmod.problems(spec) == [] and "best with 4" in specmod.script(spec)
    assert any("suggested" in p for p in specmod.problems({**SPEC, "players": {"min": 3, "max": 5, "suggested": 9}}))
    assert adapt.source_record(with_players(PLAN, suggested=4))["players_suggested"] == 4
    assert adapt.source_record(with_players(PLAN))["players_suggested"] == 3  # not given: the minimum


def test_one_model_named_for_the_table_is_repeated_to_the_suggested_size_and_a_list_is_used_as_given():
    game = {"min_seats": 3, "max_seats": 5, "suggested_seats": 4}
    assert simulate.fill_table(["muse"], game) == ["muse"] * 4
    assert simulate.fill_table(["muse", "claude", "muse"], game) == ["muse", "claude", "muse"]
    assert simulate.fill_table(["muse"], {"min_seats": 2, "max_seats": 2}) == ["muse", "muse"]


def test_the_designers_suggested_size_reaches_the_spec_prompt_so_it_is_not_decided_twice():
    class Capture:
        def __init__(self):
            self.prompts = []

        def complete(self, prompt, system=""):
            self.prompts.append(prompt)
            import json

            return json.dumps({**SPEC, "players": {"min": 3, "max": 5, "suggested": 4}})

    record = adapt.source_record(with_players(PLAN, suggested=4))
    m = Capture()
    spec, error = specmod.write_spec(m, record)
    assert error == "" and spec["players"]["suggested"] == 4
    assert "Suggested table size, chosen by the designer of these rules (keep it): 4" in m.prompts[0]
    assert "keep it as `suggested`" in specmod.system_with_engine_facts()
