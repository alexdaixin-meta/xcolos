"""The check that the rules text players read says what the numbered rules say."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import SPEC, Models, run_flow, world  # noqa: E402
from gen_game import brief  # noqa: E402

SPEC_WITH_RULES = {**SPEC, "rules": [{"id": "R1", "text": "When a challenge fails, then the challenger loses a card and the action still goes ahead."}]}
GAP = {"rule": "R1", "problem": "the text does not say the action goes ahead after a failed challenge", "add": "A failed challenge does not stop the action."}


class Checker:
    def __init__(self, reply):
        self.reply, self.prompts = reply, []

    def complete(self, prompt, system=""):
        self.prompts.append((prompt, system))
        return json.dumps(self.reply)


def test_the_numbered_rules_and_the_text_are_what_the_model_compares():
    m = Checker({"gaps": []})
    gaps, error = brief.check_brief(m, SPEC_WITH_RULES, "If the claim was true the challenger loses a card.")
    assert gaps == [] and error == ""
    prompt, system = m.prompts[0]
    assert "R1. When a challenge fails" in prompt and "If the claim was true the challenger loses a card." in prompt
    assert "OMITS an outcome a player needs" in system


def test_a_gap_names_the_rule_what_is_missing_and_the_words_to_add():
    gaps, _ = brief.check_brief(Checker({"gaps": [GAP]}), SPEC_WITH_RULES, "text")
    assert gaps[0]["rule"] == "R1" and "A failed challenge does not stop the action." in brief.as_text(gaps)


def test_nothing_to_compare_means_no_call_and_a_bad_reply_is_an_error_not_a_gap():
    m = Checker({"gaps": [GAP]})
    assert brief.check_brief(m, SPEC, "text") == ([], "") and brief.check_brief(m, SPEC_WITH_RULES, "  ") == ([], "") and m.prompts == []
    gaps, error = brief.check_brief(Checker({"nope": 1}), SPEC_WITH_RULES, "text")
    assert gaps == [] and "gaps" in error


def test_with_the_check_on_gaps_in_the_text_go_back_to_the_coder_and_with_it_off_no_call_is_made():
    class WithBrief(Models):
        def complete(self, prompt, system=""):
            if system.startswith("You check that the RULES TEXT"):
                self.calls.append("brief")
                return json.dumps({"gaps": [GAP]} if self.calls.count("brief") == 1 else {"gaps": []})
            return super().complete(prompt, system)

    inv, root = world()
    m = WithBrief(spec={**SPEC, "rules": SPEC_WITH_RULES["rules"]}, scenario_lists=[[]] if False else None)
    run_flow("rps", m, inv, root, adapt=False, check_brief=True)
    assert "brief" in m.calls and m.calls.count("encode") >= 1
    inv2, root2 = world()
    off = WithBrief(spec={**SPEC, "rules": SPEC_WITH_RULES["rules"]})
    run_flow("rps", off, inv2, root2, adapt=False)
    assert "brief" not in off.calls
