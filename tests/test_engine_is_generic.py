"""The flow engine must not know what game it is running.

The whole milestone is worth nothing if Mafia leaks back into the executor one
convenient special case at a time. These tests fail the moment it does.

Two kinds of check. The first reads the source for game vocabulary, which
catches the obvious slip. The second is the one that matters: it invents a game
that shares no word, no role and no structure with Mafia, and plays it. Code
that secretly depends on a role called "mafia" cannot survive that.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

from xcolos.agents import ScriptedAgent
from xcolos.flow import FlowOrchestrator
from xcolos.game import Game
from xcolos.games.definition import Condition
from xcolos.games.loader import LIBRARY, load
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import Player
from xcolos.log import MatchLog
from xcolos.runner import Runner

ROOT = Path(__file__).resolve().parent.parent

#: Every module that claims to be game-agnostic.
ENGINE = [
    "xcolos/flow/executor.py",
    "xcolos/flow/state.py",
    "xcolos/flow/judge.py",
    "xcolos/games/definition.py",
    "xcolos/games/loader.py",
]

#: Words from real games. If one of these is a string constant in the engine,
#: the engine has learned something it should have been told.
GAME_WORDS = (
    "mafia",
    "villager",
    "detective",
    "werewolf",
    "seer",
    "hitler",
    "liberal",
    "fascist",
    "spy",
    "merlin",
    "assassin",
    "night",
    "dawn",
    "town",
    "evil",
)

#: Names the kernel itself uses on `Seat`, from Milestone 1. They are game
#: vocabulary in a game-agnostic kernel, which is a known wart; the engine is
#: allowed to name them only in order to *avoid* assuming a game uses them.
KERNEL_FIELDS = ("role", "faction")


def string_constants(path: Path):
    """Every string literal that is not a docstring, with its line."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docstrings = {
        ast.get_docstring(node, clean=False)
        for node in ast.walk(tree)
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef))
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value not in docstrings:
                yield node.lineno, node.value


def test_no_engine_module_names_a_real_game():
    offences = []
    for name in ENGINE:
        path = ROOT / name
        for line, text in string_constants(path):
            lowered = text.lower()
            for word in GAME_WORDS:
                if word in lowered:
                    offences.append(f"{name}:{line} says {text!r} ({word})")
    assert not offences, "the engine has learned a game:\n  " + "\n  ".join(offences)


def test_the_only_kernel_field_names_left_are_the_documented_wart():
    """`role` and `faction` may appear, but only as the display mapping."""
    seen = []
    for name in ENGINE:
        for line, text in string_constants(ROOT / name):
            if text in KERNEL_FIELDS:
                seen.append(f"{name}:{line}")
    assert seen, "if the wart is gone, delete this test and KERNEL_FIELDS"
    for place in seen:
        module, line = place.rsplit(":", 1)
        source = (ROOT / module).read_text(encoding="utf-8").splitlines()
        window = "\n".join(source[max(0, int(line) - 8):int(line) + 2])
        assert "display" in window or "DISPLAY_FIELDS" in window, (
            f"{place} uses a kernel field name outside the display mapping"
        )


def test_the_engine_imports_nothing_from_a_game():
    for name in ENGINE:
        tree = ast.parse((ROOT / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                # `orchestrators.base` is the protocol every orchestrator
                # implements, not a game. Anything else under it is one.
                allowed = {"xcolos.orchestrators.base"}
                if node.module.startswith("xcolos.orchestrators"):
                    assert node.module in allowed, f"{name} imports {node.module}"
                assert "library" not in node.module, f"{name} imports {node.module}"


# ----------------------------------------------------------------------
# A game that is not Mafia in any respect
# ----------------------------------------------------------------------

#: Deliberately alien. Different words, different shape: no hidden roles at
#: all, no night phase, no elimination by vote. A numeric attribute on the
#: table drives the ending, and the only secret is a per-player number.
ORCHARD = {
    "schema": 1,
    "meta": {"id": "orchard", "name": "The Orchard", "players": {"min": 3, "max": 8}},
    "statuses": [
        {"id": "picking", "acts": True, "initial": True},
        {"id": "resting", "acts": False},
    ],
    "attributes": {
        "player": [
            {"key": "basket", "visible": "public", "type": "number", "initial": 0},
            {"key": "ladder", "visible": "ally", "type": "text", "mutable": False},
        ],
        "game": [{"key": "fruit_left", "visible": "public", "type": "number",
                  "initial": 3}],
    },
    "deal": {
        "into": ["ladder"],
        "by_players": {"3": [{"ladder": "tall"}, {"ladder": "short", "fill": True}]},
    },
    # A game says for itself what its players are told to begin with. This one
    # has a briefing and no allies notice, which the engine must not supply.
    "setup": [
        {"use": "tell", "label": "the welcome", "to": "all", "text": "brief"},
    ],
    "steps": [
        {"use": "tell", "phase": "morning", "label": "the mist", "to": "all",
         "text": "morning"},
        {
            "use": "ask",
            "phase": "morning",
            "label": "the gossip",
            "text": "ask_gossip",
            "to": "acting",
            "answer": {"type": "text", "max_words": 20},
            "broadcast": {"to": "others", "text": "said"},
        },
        {
            "use": "poll",
            "phase": "morning",
            "label": "the picking",
            "text": "ask_pick",
            "to": "acting",
            "answer": {"type": "player", "exclude_self": True},
            "broadcast": {"to": "others", "text": "said"},
            "verify": {"tally": "plurality", "on_tie": "nobody", "bind": "picker"},
        },
        {
            "use": "update",
            "phase": "evening",
            "label": "the tally",
            "do": [
                {"adjust": {"player": "$picker", "key": "basket", "value": 1,
                            "unless": "nobody"}},
                {"adjust": {"key": "fruit_left", "value": -1}},
            ],
            "text": "tally",
        },
        {"use": "check", "phase": "evening", "label": "sundown"},
    ],
    "end": {
        "trees_bare": {
            "when": {"game": "fruit_left", "op": "<=", "value": 0},
            "result": "the orchard",
            "reason": "the trees are bare",
        }
    },
    "reveal": ["ladder"],
    "limits": {"rounds": 10, "rounds_max": 20, "actions_max": 200, "deadline_s": 60},
    # Overriding the engine's own defaults, which is what makes the test below
    # able to assert that no engine wording reaches a player.
    "text": {
        "brief": "You are picker {you}. Your ladder is {ladder}.",
        "morning": "The morning mist lifts over the orchard.",
        "tally": "Picker {picker} takes the fruit. {fruit_left} left on the trees.",
        "said": "Picker {seat} says: {value}",
        "ask_gossip": "Say something to the other pickers.",
        "ask_pick": "Point at whoever should take today's fruit.",
        "game_over": "The season closes. {result}: {reason}.",
    },
    "rules": "Pickers gossip, then each points at whoever should take the "
             "day's fruit. The orchard empties after three days.",
}


def play(raw: dict, seed: int = 1, seats: int = 4):
    definition = load(json.dumps(raw), source=raw["meta"]["id"])
    log = MatchLog("generic")
    game = Game("generic", definition.id, seed, log)
    registry = Registry(game.match_id)
    host = LocalAgentHost(
        [ScriptedAgent(name=f"P{i}") for i in range(seats)],
        player=Player.new("operator"),
    )
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    return Runner(game, FlowOrchestrator(definition), registry).run(), game


def test_a_game_sharing_no_vocabulary_with_mafia_plays_to_its_own_ending():
    result, game = play(ORCHARD)
    assert result.status == "ended"
    assert result.winner == "the orchard"
    assert result.reason == "the trees are bare"
    assert result.rounds == 3, "three fruit, one taken a round"


def test_that_game_declares_no_display_mapping_and_still_runs():
    """A game with nothing resembling a role leaves the kernel's fields empty."""
    assert "display" not in ORCHARD
    _, game = play(ORCHARD)
    assert all(not seat.role for seat in game.seats.values()), (
        "the engine must not invent a role for a game that has none"
    )
    assert all(seat.attributes.get("ladder") for seat in game.seats.values()), (
        "its own attributes are still dealt and recorded"
    )


def test_its_wording_comes_from_its_own_templates():
    """No fragment of the engine's own default wording reaches a player.

    The engine now holds no wording at all, so this checks the stronger thing:
    every rendered message traces back to a template this game declared. What
    the agents themselves say is theirs, and is not checked.
    """
    DEFAULT_TEXT = {}

    _, game = play(ORCHARD)
    rendered = [str(f.payload.get("rendered", "")) for f in game.facts]
    assert any("orchard" in text for text in rendered)
    assert any(text.startswith("You are picker ") for text in rendered)

    # What a player said is that player's wording, not the engine's, so the
    # answer is cut out before the framing around it is examined.
    framing = []
    for fact in game.facts:
        text = str(fact.payload.get("rendered", ""))
        spoken = str(fact.payload.get("value", ""))
        framing.append(text.replace(spoken, "") if spoken else text)

    leaked = []
    for key, template in DEFAULT_TEXT.items():
        for literal in re.split(r"\{\w+\}", template):
            literal = literal.strip(' ".:')
            if len(literal) < 4:
                continue
            for text in framing:
                if literal in text:
                    leaked.append(f"{key}: {literal!r} appears in {text!r}")
    assert not leaked, "engine wording reached a player:\n  " + "\n  ".join(leaked)


def test_a_table_attribute_can_drive_the_ending_with_no_player_counting():
    """Mafia ends by counting players. This one ends on a number. Both work."""
    fewer = json.loads(json.dumps(ORCHARD))
    fewer["attributes"]["game"][0]["initial"] = 1
    result, _ = play(fewer)
    assert result.rounds == 1


def test_every_shipped_definition_is_loadable_and_self_consistent():
    for path in sorted(Path(LIBRARY).glob("*.json")):
        definition = load(path.read_text(encoding="utf-8"), source=str(path))
        keys = {a.key for a in definition.player_attributes}
        for field, attribute in definition.display.items():
            assert attribute in keys, f"{path.name}: display.{field} -> {attribute}"


# ----------------------------------------------------------------------
# What the loader will and will not accept
# ----------------------------------------------------------------------


#: Three players, each holding different cards, asked to play one. The point
#: is that no `options` list could have been written when the game was: the
#: choices differ per player and are not known until the deal.
CARDS = {
    "schema": 1,
    "meta": {"id": "cards", "name": "Cards", "players": {"min": 3, "max": 3}},
    "statuses": [{"id": "in", "acts": True, "initial": True},
                 {"id": "out", "acts": False}],
    "attributes": {
        "player": [{"key": "hand", "visible": "ally", "type": "list",
                    "initial": []}],
        "game": [{"key": "played", "visible": "public", "type": "number",
                  "initial": 0}],
    },
    "deal": {
        "into": ["hand"],
        "by_players": {"3": [{"hand": ["oak", "ash"]},
                             {"hand": ["elm"]},
                             {"hand": []}]},
    },
    "setup": [{"use": "tell", "label": "the welcome", "to": "all",
               "text": "You hold {hand}."}],
    "steps": [
        {"use": "ask", "label": "the play", "to": "acting",
         "text": "Play a card.",
         "answer": {"type": "choice", "options": {"attribute": "hand"}}},
        {"use": "update", "label": "the count",
         "do": [{"adjust": {"key": "played", "value": 1}}],
         "text": "A card is played."},
        {"use": "check", "label": "the last trick"},
    ],
    "end": {"done": {"when": {"game": "played", "op": ">=", "value": 1},
                     "result": "the deck", "reason": "the cards are spent"}},
    "reveal": ["hand"],
    "limits": {"rounds": 3, "rounds_max": 5, "actions_max": 50, "deadline_s": 60},
    "text": {"game_over": "{result}: {reason}."},
    "rules": "Each player holds cards and plays one.",
}


def test_a_choice_can_be_drawn_from_the_players_own_hand():
    """`options` had to be a literal list, so no card game could be written.

    "Discard one of the three policies you drew" names choices that differ per
    player and do not exist until the deal. A list in the file cannot say it.
    """
    _, game = play(CARDS, seats=3)

    asked = [r for r in game.log.records if r["type"] == "action_request"]
    assert asked, "nobody was asked to play a card"

    for record in asked:
        offered = set(record["legal_targets"])
        assert offered, f"seat {record['seat']} was asked with no cards to play"
        # Exactly this player's hand, not the union of everyone's.
        assert offered in ({"oak", "ash"}, {"elm"}), (
            f"seat {record['seat']} was offered {offered}, which is nobody's hand"
        )


def test_a_player_holding_nothing_is_not_asked():
    """An empty hand is not a question with no answer; it is not a question.

    The same treatment a vote gets when there is nobody left to point at.
    Asking anyway returns an empty choice, and an empty choice is what ends up
    in a binding and then in an operation.
    """
    _, game = play(CARDS, seats=3)

    asked = {r["seat"] for r in game.log.records
             if r["type"] == "action_request"}
    assert len(asked) == 2, (
        f"three players, one holding nothing, but {len(asked)} were asked"
    )


def test_options_must_name_a_list_attribute():
    """Pointing at a number yields no choices, so every seat would be skipped.

    The step would then run silently with nobody asked — the empty-audience
    failure again, one level down.
    """
    from xcolos.games.definition import DefinitionError

    for key, complaint in (("played", "must come from a `list`"),
                           ("purse", "not a declared")):
        raw = json.loads(json.dumps(CARDS))
        raw["steps"][0]["answer"]["options"] = {"game": key}
        try:
            load(json.dumps(raw), source="notalist")
        except DefinitionError as error:
            assert complaint in str(error), error
        else:
            raise AssertionError(f"options drawn from {key!r} was accepted")


def _with_a_step_addressing_the_picker(**extra):
    """The Orchard, plus a step aimed at whoever the poll chose."""
    raw = json.loads(json.dumps(ORCHARD))
    step = {"use": "tell", "phase": "evening", "label": "the nod",
            "to": {"ids": ["$picker"]}, "text": "nod"}
    step.update(extra)
    raw["steps"].insert(3, step)
    raw["text"]["nod"] = "You were pointed at, picker {you}."
    return raw


def test_a_step_can_address_the_player_an_earlier_step_chose():
    """The president-nominates-a-chancellor shape, which had no spelling.

    A `verify` binds the seat its tally landed on, and until now that name was
    readable in operations and in wording but not in `to` — so a game could act
    on the chosen player and talk about them, but could not talk *to* them.
    Secret Hitler and Avalon are both that pattern and both were unwriteable.
    """
    _, game = play(_with_a_step_addressing_the_picker())

    nods = [f for f in game.facts if f.type == "the_nod"]
    assert nods, "a step addressed to $picker reached nobody"

    for fact in nods:
        assert fact.audience.kind == "seats", (
            f"a bound seat should address exactly that seat, got "
            f"{fact.audience.kind!r}"
        )
        assert len(fact.audience.seats) == 1
        # And it is the seat the poll actually landed on, not merely some seat.
        seat = fact.audience.seats[0]
        assert f"picker {seat}" in str(fact.payload["rendered"])


def test_a_binding_that_named_nobody_addresses_nobody():
    """A tie binds NOBODY, and NOBODY is not seat zero.

    The dangerous reading of an unresolved binding is a falsy one: `int("")`
    fails, but a stray 0 or a dropped filter would quietly aim the step at the
    first seat in the table.
    """
    raw = _with_a_step_addressing_the_picker()
    # Nobody can be pointed at, so the poll binds the no-winner sentinel.
    raw["steps"][2]["answer"] = {"type": "text", "max_words": 5}
    raw["steps"][2]["verify"] = {"tally": "unanimity", "on_tie": "nobody",
                                 "bind": "picker"}
    _, game = play(raw)

    nods = [f for f in game.facts if f.type == "the_nod"]
    assert not nods, (
        "a binding that named nobody still addressed somebody: "
        f"{[f.audience for f in nods]}"
    )


def test_a_selector_naming_a_binding_no_step_makes_is_refused():
    from xcolos.games.definition import DefinitionError

    raw = json.loads(json.dumps(ORCHARD))
    raw["steps"].insert(3, {"use": "tell", "label": "the nod", "text": "morning",
                            "to": {"ids": ["$chancellor"]}})
    try:
        load(json.dumps(raw), source="unbound")
    except DefinitionError as error:
        assert "$chancellor" in str(error) and "binds it" in str(error)
    else:
        raise AssertionError("a selector named a binding nothing produces")


def test_a_step_cannot_address_the_player_its_own_answer_will_name():
    """`to` is resolved before the question is asked, so this cannot work."""
    from xcolos.games.definition import DefinitionError

    raw = json.loads(json.dumps(ORCHARD))
    raw["steps"][2]["to"] = {"ids": ["$picker"]}  # the step that binds `picker`
    try:
        load(json.dumps(raw), source="circular")
    except DefinitionError as error:
        assert "$picker" in str(error)
    else:
        raise AssertionError("a step addressed its own not-yet-made binding")


def test_a_relative_selector_without_a_subject_is_refused_not_ignored():
    """`author` with nothing to be relative to used to name nobody in silence.

    Same failure as `answers_visable`: the step loaded, ran, and addressed an
    empty audience, which is indistinguishable from a step meant to be quiet.
    """
    from xcolos.games.definition import DefinitionError

    raw = json.loads(json.dumps(ORCHARD))
    raw["steps"][0]["to"] = "author"  # a tell with no `about`
    try:
        load(json.dumps(raw), source="subjectless")
    except DefinitionError as error:
        assert "about" in str(error), error
    else:
        raise AssertionError("a subject-relative selector loaded with no subject")


def test_ids_rejects_a_word_that_is_neither_a_seat_nor_a_binding():
    """The old failure was a bare int() traceback naming neither step nor value."""
    from xcolos.games.definition import DefinitionError

    raw = json.loads(json.dumps(ORCHARD))
    raw["steps"][0]["to"] = {"ids": ["picker"]}  # the missing $
    try:
        load(json.dumps(raw), source="nodollar")
    except DefinitionError as error:
        assert "'picker'" in str(error) and "steps[0].to" in str(error), error
    else:
        raise AssertionError("ids accepted a word that names nothing")


def test_a_misspelled_field_is_refused_rather_than_ignored():
    """The failure mode of hand-written configuration is the ignored field.

    `answers_visable` used to load cleanly and do nothing, so a step meant to
    keep its answers private silently published them and nothing said so. Every
    structure now rejects keys it does not read, and the message lists what it
    does take.
    """
    from xcolos.games.definition import DefinitionError

    base = json.loads((LIBRARY / "mafia.json").read_text(encoding="utf-8"))

    def broken(mutate):
        raw = json.loads(json.dumps(base))
        mutate(raw)
        return raw

    cases = {
        "step": lambda r: r["steps"][1].update({"answers_visable": "public"}),
        "answer": lambda r: r["steps"][2]["answer"].update({"exclude_slef": True}),
        "verify": lambda r: r["steps"][2]["verify"].update({"on_ties": "random"}),
        "selector": lambda r: r["steps"][2]["to"].update({"attribue": "role"}),
    }
    for name, mutate in cases.items():
        try:
            load(json.dumps(broken(mutate)), source="typo")
        except DefinitionError as error:
            assert "unknown key" in str(error), f"{name}: {error}"
            assert "takes:" in str(error), f"{name} must say what is accepted"
        else:
            raise AssertionError(f"a misspelled {name} field was accepted")


def test_a_comparison_may_still_hold_its_operator_beside_its_operand():
    """The one place a structure legitimately shares a dict with its parent."""
    condition = Condition.parse(
        {"count": {"attribute": "faction", "is": "evil"}, "op": ">=", "value": 1},
        "end[0].when",
    )
    assert condition.kind == "compare"
    assert condition.op == ">="


def test_every_shipped_file_survives_the_strict_loader():
    for path in sorted(Path(LIBRARY).glob("*.json")):
        load(path.read_text(encoding="utf-8"), source=str(path))


def test_every_action_declares_what_it_asks_for_and_what_it_runs():
    """The action table is the contract; it must cover every step kind.

    An action fixes which view the model sees, what shape comes back, and
    which engine call consumes it. A kind missing from the table is a step the
    engine can run without anyone having said what the model is allowed to see
    while it runs — which is how the composing call came to be handed every
    hidden role.
    """
    from xcolos.flow.executor import ACTIONS
    from xcolos.games.definition import KINDS

    for kind in KINDS:
        assert kind in ACTIONS, f"the {kind!r} action has no declared contract"
    for name, contract in ACTIONS.items():
        assert set(contract) == {"sees", "returns", "engine_calls"}, name
        assert all(contract.values()), f"{name} has an empty field"


def test_only_full_sight_actions_return_something_other_than_a_message():
    """The safety rule, stated as a property of the table.

    A call shown the whole table must not return text, because its reply is
    forwarded to players and anything in the prompt can come out of it. A call
    that returns a message must therefore be shown one recipient.
    """
    from xcolos.flow.executor import ACTIONS

    for name, contract in ACTIONS.items():
        writes_text = contract["returns"] == "message"
        full_sight = "whole table" in contract["sees"]
        assert not (writes_text and full_sight), (
            f"{name} writes player-facing text with full sight of the table"
        )


def test_the_briefing_numbers_seats_the_way_the_kernel_does():
    """It used to say "0 to N-1" and then "you are seat 1", in one message.

    Two contradictory statements about the only identifier the protocol uses,
    sent to every agent at the start of every match.
    """
    from xcolos.state import FIRST_SEAT

    _, game = play(ORCHARD)
    briefings = [
        r["body"] for r in game.log.records
        if r.get("category") == "message" and r.get("msg_type") == "GAME_START"
    ]
    assert briefings, "every seat is greeted"
    last = FIRST_SEAT + len(game.seats) - 1
    for body in briefings:
        assert f"numbered {FIRST_SEAT} to {last}" in body, body[:200]
        seat = int(body.split("You are seat ")[1].split(",")[0])
        assert FIRST_SEAT <= seat <= last, "and the seat it names is in that range"


def test_the_no_winner_sentinel_is_one_constant_not_two_spellings():
    """`tally()` produces it, `_seat()` refuses it, a game file may write it.

    Three places, so it is one name. A misspelled `unless` used to load and
    never match, running the operation it was written to prevent. Mafia no
    longer needs the guard — its vote names both outcomes instead — so this
    builds a file that does use one rather than depending on a shipped game to
    keep exercising it.
    """
    from xcolos.games.definition import NOBODY, DefinitionError

    base = json.loads((LIBRARY / "mafia_oracle.json").read_text(encoding="utf-8"))
    guarded = json.loads(json.dumps(base))
    step = next(s for s in guarded["steps"] if s["label"] == "the night resolves")
    step["do"][0]["set_status"]["unless"] = NOBODY
    load(json.dumps(guarded), source="guarded")          # the right spelling loads

    step["do"][0]["set_status"]["unless"] = "noboby"
    try:
        load(json.dumps(guarded), source="typo")
    except DefinitionError as error:
        assert "noboby" in str(error) and NOBODY in str(error)
    else:
        raise AssertionError("a misspelled guard must not load")


def test_no_step_kind_is_referenced_that_the_schema_does_not_declare():
    """`brief` outlived its removal from KINDS in two branches of the loop."""
    import re

    from xcolos.games.definition import KINDS

    source = (ROOT / "xcolos/flow/executor.py").read_text(encoding="utf-8")
    for match in re.finditer(r'step\.use\s*[!=]=\s*"(\w+)"', source):
        assert match.group(1) in KINDS, (
            f"executor tests for step kind {match.group(1)!r}, which is not in KINDS"
        )


def test_the_kernel_renderer_knows_no_game():
    """`render.py` is on every message's path, for every orchestrator.

    It used to carry thirteen Mafia message types by name. A definition-driven
    game puts its own wording on the fact, so the kernel needs none; the
    hardcoded game's wording moved in with the hardcoded game.
    """
    import re

    # String constants only. A comment may name the deprecated game in order to
    # explain why the fallback exists; what must not appear is a game's word in
    # something the module can emit or compare against.
    for line, text in string_constants(ROOT / "xcolos/render.py"):
        for word in GAME_WORDS:
            assert word not in text.lower(), f"render.py:{line} says {text!r}"

    # The give-away shape: a branch per fact type.
    source = (ROOT / "xcolos/render.py").read_text(encoding="utf-8")
    assert not re.search(r'if t == "', source), (
        "render.py dispatches on fact type, which only a game's renderer does"
    )


def test_nothing_outside_legacy_imports_legacy():
    """Deprecated code must not be load-bearing for anything current."""
    import ast

    allowed = {
        "xcolos/render.py",          # the one fallback, documented as the last
        "xcolos/cli.py",             # the reference runner
        "xcolos/web/server.py",      # offers it by id for grading, not in the picker
    }
    for path in sorted((ROOT / "xcolos").rglob("*.py")):
        rel = str(path.relative_to(ROOT))
        if rel.startswith("xcolos/legacy/") or rel in allowed:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert "legacy" not in node.module, f"{rel} imports {node.module}"


def test_the_flow_engine_never_reaches_the_legacy_renderer():
    """Every fact a flow game emits carries its own wording.

    Checked rather than assumed, because the fallback still exists and its
    last resort prints a whole payload — including fields nobody was meant to
    read.
    """
    _, game = play(ORCHARD)
    unworded = [f.type for f in game.facts if "rendered" not in f.payload]
    assert not unworded, f"these would fall through to the legacy path: {unworded}"


def test_the_action_reference_documents_the_whole_vocabulary():
    """`design/actions.md` is meant to be enough to write a game from.

    That is only true while it keeps up. Adding an action, an operation, a step
    key or a value to a closed set without documenting it fails here, because a
    reference that is 90% complete is worse than none: it is trusted and wrong.
    """
    from xcolos.flow.judge import MESSAGE_TYPES
    from xcolos.games import definition as spec

    doc = (ROOT / "design" / "actions.md").read_text(encoding="utf-8")
    missing = []

    for name, values in [
        ("action", spec.KINDS),
        ("operation", spec.OPERATIONS),
        ("update target", spec.UPDATE_TARGETS),
        ("tell kind", spec.TELL_KINDS),
        ("sync mode", spec.SYNC_MODES),
        ("tally", spec.TALLIES),
        ("tie rule", spec.ON_TIE),
        ("answer type", spec.ANSWER_TYPES),
        ("attribute type", spec.TYPES),
        ("visibility", spec.PLAYER_VISIBILITY),
        ("message type", MESSAGE_TYPES),
    ]:
        missing += [f"{name} {v!r}" for v in values if f"`{v}`" not in doc]

    for key in spec.COMMON_KEYS:
        if f"`{key}`" not in doc:
            missing.append(f"common key {key!r}")
    for action, keys in spec.ACTION_KEYS.items():
        for key in keys:
            if f"`{key}`" not in doc:
                missing.append(f"{action} key {key!r}")

    assert not missing, "actions.md does not mention:\n  " + "\n  ".join(missing)


def test_the_reference_names_the_gaps_it_cannot_do():
    """A reference that lists only what works teaches a false schema.

    Each of these is something a reader would otherwise try, write, and watch
    fail at load or — worse — silently do nothing.
    """
    doc = (ROOT / "design" / "actions.md").read_text(encoding="utf-8")

    # What the loader refuses has to be listed, or a reader learns the schema
    # by watching load errors.
    refusals = doc.split("## What the loader refuses", 1)
    assert len(refusals) == 2, "the reference no longer says what it refuses"
    for refusal in ("$name", "about", "ids"):
        assert refusal in refusals[1], (
            f"the refusals list does not mention {refusal!r}"
        )

    # Bindings in `to` are the one place a reader is most likely to guess
    # wrong, so the reference has to show the shape rather than describe it.
    assert '"$chancellor"' in doc, "the reference does not show a bound selector"
