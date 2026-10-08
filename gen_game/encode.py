"""Step 3: encode a spec as a platform game file.

A model writes the whole game file from the spec. Three things check it, each
sending its findings back to the model until the file passes or the attempts run
out:

  1 the platform's loader, which refuses misspelled keys, bad selectors and the
    rest of what `design/actions.md` lists
  2 a rule this pipeline adds: a generated game is decided by arithmetic, with no
    prose condition and no model-written text, so its outcome is a fact
  3 smoke play: random seats play it at the smallest and largest table, and it
    must end, give a result, write a valid log and never leave a seat unable to
    answer

None of these says the game is the right game. That is the scenarios' job.
"""

from __future__ import annotations

import dataclasses
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from gen_game import harness
from gen_game.repair import refused
from gen_inventory.crawl import first_json
from xcolos.games.definition import Condition, DefinitionError, GameDefinition
from xcolos.games.loader import load

ROOT = Path(__file__).resolve().parent.parent
ACTIONS_DOC = ROOT / "design" / "actions.md"
#: Shipped games shown to the model as complete examples of the file format.
REFERENCES = ("rps", "auction")
LIBRARY = ROOT / "xcolos" / "games" / "library"


class Completion(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


#: What the loader has refused before. Shown to anything that writes a game file, human-readable.
MISTAKES = """- Mistakes the loader has refused before, so avoid them:
  * A PLAYER attribute's `visible` is one of public, ally or others, never `none`. (`none` is only for table
    attributes.) For something only its owner should see, use `ally`.
  * A `poll` step has no `each` key, and no key the format reference does not list for `poll`. `each` belongs to `ask`.
  * Do not write a `deal` block unless it has the `into` it requires. Set starting values with `initial` on
    attributes, or with `set` operations in `setup`, instead.
  * Every key must be one the reference lists for that action; a misspelled or invented key is refused.
  * An answer to an `ask` or a `poll` exists ONLY if the step binds it with `verify: {"bind": "name"}`; a later `update`
    stores it with `"value": "$name"` (see the `rps` example, `card1`). A step that asks and binds nothing throws the
    answers away, and every score that depends on them stays at its starting value.
  * An attribute declared `"mutable": false` is set once, by an `initialize` step, and any other step that sets it crashes the game
    ("declared static and has already been dealt"). To set a hidden type or a starting value at setup, either use an `initialize`
    step or leave the attribute mutable.
  * Do not write steps that do nothing (for example an `if` of `{"calc": "False"}`), or two polls where one will do.
  * Reply with one complete JSON object: double-quoted keys and strings, no comments, no trailing commas. WRITE IT INDENTED,
    two spaces per level and one key per line, so you can see the nesting and count the brackets; do not put it on one line."""


def system_prompt() -> str:
    refs = "\n\n".join(f"### Example game: {r}\n```json\n{(LIBRARY / (r + '.json')).read_text()}\n```" for r in REFERENCES)
    return f"""You write game files for a turn-based, text-only game engine. Below is the complete reference for
the file format, then two complete example games. The user gives you a SPEC; write the game file for it.

Reply with the complete game file as ONE JSON object and nothing else.

Rules for this task:
- Use exactly the attribute keys the spec declares, with its visibility. Put every spec parameter in the file
  as an attribute with its value, never as a number buried in a step, so a number is written once.
- The outcome must follow from arithmetic. Every ending's `when` is a {{"calc": ...}} condition and its
  `result` is one of the spec's result names exactly. Do not use `winner` or prose conditions, and no step uses
  `llm`: every step uses `text`. An ENDING is the one place `llm` belongs (see ENDING STATEMENT below).
- ENDING STATEMENT. The end screen must say more than who won. Every ending's `text` states the final figures that
  decided it, written with placeholders over the final state, such as "Seat 1 wins. Final scores: Seat 1
  {{players[0].score}}, Seat 2 {{players[1].score}}, Seat 3 {{players[2].score}}; target {{target}}." Also give each ending
  an `llm` that asks a model for a short summary of how the game went and why that result came out (what each player did,
  the turning point), `text` stays as the fallback and must be complete on its own. The model only words the
  announcement; the `result` is still decided by the calc.
- meta.id and meta.name come from the spec; give `meta.blurb` one line and write `rules` as the rules a
  player reads, using {{key}} for public attributes.
- Do what the spec says, in its order. Do not add mechanics.
- The `auction` example ends with a model-decided `winner`. Do NOT copy that: end with `result` and a calc
  condition, as the `rps` example does.
{MISTAKES}

# THE FORMAT

{ACTIONS_DOC.read_text()}

# EXAMPLES

{refs}
"""


def mend_json(text: str, tries: int = 12) -> tuple[str, int]:
    """Parse a reply as JSON, mending the slip a long minified file most often has: a missing closing bracket or brace.

    A model cannot count braces in a file written on one line, and it made the same one-brace slip five times in a row
    while being shown the error. Each time parsing fails at a position, a closing `}` or `]` is tried there, and the
    mend is kept only if parsing then gets further. Nothing is guessed about meaning: whatever comes out is still checked
    by the loader and every other check. Returns (text, mends); the text is unchanged if it could not be mended.
    """
    import json as _json

    start = text.find("{")
    if start < 0:
        return text, 0
    body, mends = text[start:], 0

    def whole(candidate: str) -> bool:
        """Parses with nothing but whitespace or a closing code fence left over: a mend that stops early has dropped the rest."""
        try:
            _, end = _json.JSONDecoder().raw_decode(candidate)
        except _json.JSONDecodeError:
            return False
        return candidate[end:].strip().strip("`").strip() == ""

    for _ in range(tries):
        try:
            _json.JSONDecoder().raw_decode(body)
            return body, mends  # it parses as it stands; whatever follows is for the caller to judge
        except _json.JSONDecodeError as exc:
            pos = exc.pos
            best = None
            # a missing closer belongs just before the comma that the parser trips over, or where it stopped
            comma = body.rfind(",", 0, pos)
            for at in dict.fromkeys(a for a in (comma, pos) if a >= 0):
                for ch in ("}", "]"):
                    trial = body[:at] + ch + body[at:]
                    if whole(trial):
                        return trial, mends + 1
                    try:
                        _json.JSONDecoder().raw_decode(trial)
                    except _json.JSONDecodeError as exc2:
                        if exc2.pos > pos and (best is None or exc2.pos > best[1]):
                            best = (trial, exc2.pos)
            if best is None:
                return text, 0
            body, mends = best[0], mends + 1
    return text, 0


def syntax_context(text: str, width: int = 90) -> str:
    """Where a JSON reply stops parsing, with the text around it, for a repair message."""
    import json as _json

    start = text.find("{")
    body = text[start:] if start >= 0 else text
    try:
        _json.JSONDecoder().raw_decode(body)
        return ""
    except _json.JSONDecodeError as exc:
        a, b = max(0, exc.pos - width), exc.pos + width
        return f"{exc.msg} at character {exc.pos}. The text there is: ...{body[a:exc.pos]}<<HERE>>{body[exc.pos:b]}..."


def lint(game: dict) -> list[str]:
    """The known mistakes, all at once.

    The loader stops at the first thing wrong, so a model that makes four of the known mistakes sees one
    per attempt and burns four attempts. These are the ones the loader has refused before, checked
    together so they are fixed together.
    """
    found = []
    attrs = (game.get("attributes") or {}) if isinstance(game.get("attributes"), dict) else {}
    for a in attrs.get("player") or []:
        if isinstance(a, dict) and a.get("visible") == "none":
            found.append(f"player attribute {a.get('key')!r} has visible: none; a player attribute is public, ally or others (use ally for owner-only)")

    def walk(steps, where):
        for i, st in enumerate(steps if isinstance(steps, list) else []):
            if not isinstance(st, dict):
                continue
            label = f"{where}[{i}] ({st.get('label') or st.get('use')})"
            if st.get("use") == "poll" and "each" in st:
                found.append(f"{label}: a poll has no `each` key; `each` belongs to an `ask`")
            walk(st.get("steps"), label + ".steps")
    walk(game.get("setup"), "setup")
    walk(game.get("steps"), "steps")
    deal = game.get("deal")
    if isinstance(deal, dict) and "into" not in deal:
        found.append("the `deal` block has no `into`; remove the block and set starting values with `initial` or `set` operations")
    return found


def steps_mentioning(game: dict, key: str) -> list[str]:
    """Labels of the steps that name an attribute key, however deep: the places that were meant to set it."""
    found: list[str] = []

    def walk(steps):
        for st in steps if isinstance(steps, list) else []:
            if isinstance(st, dict):
                if f'"key": "{key}"' in json.dumps(st.get("do", []), sort_keys=False).replace('"key":"', '"key": "'):
                    found.append(str(st.get("label") or st.get("use")))
                walk(st.get("steps"))
    walk(game.get("setup"))
    walk(game.get("steps"))
    return found


def explain_dead(dead: list[str], game: dict) -> str:
    """What to do about attributes nothing changes: name the steps that were meant to, or say none exists."""
    import re

    lines = []
    for d in dead[:4]:
        m = re.search(r"attribute `([^`]+)`", d)
        key = m.group(1) if m else ""
        where = steps_mentioning(game, key)
        lines.append(d + (f". Steps that name it: {', '.join(where)}. They never change it: their `when`/`if` may never be true, the `key` may be "
                          f"spelled differently from the attribute, or the value written may equal what it already holds."
                          if where else ". No step sets it. Either remove the attribute from the file, or add the update that sets it."))
    return "; ".join(lines)


def dead_attributes(defn: GameDefinition, constants: set[str] = frozenset(), matches: int = 3) -> list[str]:
    """Attributes that are never given a different value in random play: the update that should move them does not work.

    A game whose scoring steps are written but never take effect loads, ends and plays cleanly (the file that scored
    every round at zero did all three), so this is what says so. It watches every write during the matches, not the
    end state, so a scratch attribute that is set and reset each round counts as alive. Parameters are meant to stay
    put and are passed in as `constants`.
    """
    from xcolos.flow.state import FlowState

    touched: set[tuple[str, str]] = set()
    original = FlowState.set_attribute

    def spy(self, player, key, value, *, dealing=False):
        now = self.game_attributes.get(key) if player is None else self.player_attributes[player].get(key)
        if now != value:
            touched.add(("game" if player is None else "player", key))
        return original(self, player, key, value, dealing=dealing)

    FlowState.set_attribute = spy
    try:
        for seed in range(1, matches + 1):
            try:
                harness.play(defn, harness.random_agents(defn.min_players, seed), seed)
            except Exception:  # noqa: BLE001 - smoke play reports crashes; this is not the place
                return []
    finally:
        FlowState.set_attribute = original
    declared = [("player", a.key) for a in defn.player_attributes] + [("game", a.key) for a in defn.game_attributes]
    return [f"{scope} attribute `{key}` is never changed in {matches} random matches, so nothing updates it"
            for scope, key in declared if key not in constants and (scope, key) not in touched]


def model_use(defn: GameDefinition) -> list[str]:
    """Where a definition lets a model, not arithmetic, decide or speak."""
    found: list[str] = []
    for rule in defn.end:
        if rule.when.kind != "calc":
            found.append(f"ending {rule.name!r} has a prose condition; write it as a calc")
        if rule.winner:
            found.append(f"ending {rule.name!r} uses `winner`; use `result` with a calc condition")
        if rule.llm and not rule.text:
            found.append(f"ending {rule.name!r} uses `llm` with no `text`; the `text` (final scores and the deciding figures) is the fallback and is required")

    def walk(steps, where):
        for s in steps:
            for f in dataclasses.fields(s):
                v = getattr(s, f.name)
                if isinstance(v, Condition) and v.kind == "prose":
                    found.append(f"step {s.label or s.use!r}: `{f.name}` is prose; write it as a calc")
            if getattr(s, "llm", ""):
                found.append(f"step {s.label or s.use!r} uses `llm`; use `text`")
            walk(getattr(s, "steps", ()) or (), where)

    walk(defn.setup, "setup")
    walk(defn.steps, "steps")
    return found


@dataclass
class Encoded:
    game: dict | None = None
    definition: GameDefinition | None = None
    #: One entry per attempt: what was wrong with it, or "" for the one that passed.
    attempts: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.definition is not None


def check(text_or_obj, game_id: str, constants: set[str] = frozenset(), tests: list[dict] | None = None) -> tuple[dict | None, GameDefinition | None, str]:
    """Load and vet one reply. Returns (game, definition, problem); problem is '' if it passed.

    `constants` are the spec's parameter keys, which are meant never to change. `tests` are independent
    scenarios written from the spec; when given, the game must also pass them, and each failure comes
    back as a concrete difference ("seat 1 total_score: expected 30, got 0").
    """
    try:
        if isinstance(text_or_obj, dict):
            obj = text_or_obj
        else:
            mended, _ = mend_json(text_or_obj)
            try:
                obj = first_json(mended)
            except ValueError:
                hint = syntax_context(text_or_obj)
                raise ValueError(f"the JSON did not parse. {hint or 'No JSON object was found in the reply.'} "
                                 "A closing } or ] is usually missing or extra there; count the brackets of what you wrote.") from None
        obj.setdefault("meta", {})["id"] = game_id  # the id is the inventory's, not the model's
        if (mistakes := lint(obj)):
            return None, None, "known mistakes, all of them: " + " | ".join(mistakes)
        defn = load(json.dumps(obj), source=game_id)
    except (ValueError, DefinitionError) as exc:
        return None, None, f"the game file was refused by the loader: {exc}"
    except Exception as exc:  # noqa: BLE001 - a loader crash is still a finding for the model
        return None, None, f"the loader crashed on it: {type(exc).__name__}: {exc}"
    if (used := model_use(defn)):
        return obj, None, "a generated game must be decided by arithmetic: " + "; ".join(used[:4])
    for n in sorted({defn.min_players, defn.max_players}):
        if (found := harness.smoke(defn, players=n)):
            return obj, None, "playing it with random seats failed: " + "; ".join(found[:3])
    a = harness.play(defn, harness.random_agents(defn.min_players, 1), 1)
    b = harness.play(defn, harness.random_agents(defn.min_players, 1), 1)
    if a.comparable_log() != b.comparable_log():
        return obj, None, "playing the same seed twice gave different logs: something in the game is not deterministic (a clock, an unseeded draw)"
    if (dead := dead_attributes(defn, set(constants))):
        return obj, None, ("it plays, but part of it does nothing: " + explain_dead(dead, obj) +
                           ". Declare only attributes the game uses, and make sure each one is set by a step that actually runs.")
    if tests:
        from gen_game import scenarios

        failed = [o for o in scenarios.run_all(defn, tests) if not o.passed]
        if failed:
            first = failed[0]
            return obj, None, ("tests written independently from the rules disagree with the game: " +
                               " | ".join(f"{o.name}: " + "; ".join(o.failures)[:240] for o in failed[:4]) +
                               (f". What YOUR game did on the first of them ({first.name}): {first.trace}" if first.trace else ""))
    return obj, defn, ""


def encode(completion: Completion, spec: dict, game_id: str, repairs: int = 4, outage_retries: int = 3,
           pause=time.sleep, guidance: str = "", tests: list[dict] | None = None, prompt_text: str | None = None) -> Encoded:
    """Ask for the game file, repair it from the checks, and ride out a dropped connection.

    A whole game file is a long generation and the connection to a model sometimes closes in the
    middle of one. That says nothing about the game, so such a call is retried (without using up a
    repair) before the encoding is given up as failed. Only outages in a row count: a reply that
    arrives, even a bad one, starts the count again.
    """
    out = Encoded()
    # the prompt is the generated one (rules, interface, task) when given; the bare spec only as a fallback
    prompt = prompt_text if prompt_text is not None else "SPEC:\n" + json.dumps(spec, indent=2)
    if guidance and prompt_text is None:
        prompt += "\n\nA PREVIOUS ATTEMPT at this game file had problems. Guidance on fixing them:\n" + guidance
    system = system_prompt()
    base = prompt
    # A model that can hold a conversation gets real turns: its refused file as its own turn, then the problem.
    chat = [{"role": "user", "content": prompt}] if hasattr(completion, "converse") else None
    outages = 0
    attempt = 0
    while attempt <= repairs:
        try:
            reply = completion.converse(chat, system=system) if chat is not None else completion.complete(prompt, system=system)
        except Exception as exc:  # noqa: BLE001 - a backend that is down is not a bad game
            outages += 1
            out.attempts.append(f"the model call failed: {str(exc)[:200]}")
            if outages > outage_retries:
                return out
            pause(5 * 2 ** (outages - 1))
            continue
        outages = 0
        attempt += 1
        obj, defn, problem = check(reply, game_id, set(spec.get("parameters", {})), tests)
        out.attempts.append(problem)
        if not problem:
            out.game, out.definition = obj, defn
            return out
        if chat is not None:
            chat += [{"role": "assistant", "content": reply},
                     {"role": "user", "content": f"That game file was refused. Why: {problem}\nCorrect it: change what the problem requires and "
                                                 "keep the rest. Reply with the complete corrected game file as one JSON object, and nothing else."}]
        else:
            prompt = refused(base, reply, problem, what="game file")
    return out
