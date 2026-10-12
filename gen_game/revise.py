"""Revise a game's spec from the findings of a real play, so the coder is told what it must not get wrong.

A reviewed play says where the built game departs from its design. Some of those gaps are the coder's slips; most can be
closed by telling the coder more exactly what the game is: a rule it was never given (what the deck must hold after the
deal), or a question whose options it had to guess (who is offered which block). This asks a model to turn the findings into
additions to the SPEC (new numbered rules, an OFFERS table, a sharper step), keeps the design's own rules as they are, and
leaves the old spec on disk. The coder is then run again on the revised spec.

Findings that are not the game's (`players`) or the platform's (`engine`) are not given to it: no spec can fix those.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Protocol

from gen_game import spec as specmod
from gen_game.repair import refused
from gen_inventory.crawl import first_json

FIXABLE = ("game_file", "design", "prompt")


class Completion(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


SYSTEM = """You revise a game's SPEC after a real play of the built game was reviewed against it. The spec is what a coder reads to build the game file, so
anything the coder got wrong because the spec left it to guess, the spec must now say exactly. You are given the current spec (its numbered rules, its round steps, its state)
and the review's findings: each says what was seen, what was expected, and what would fix it.

Do not change the game: the rules of the DESIGN stay as they are. Add precision where the findings show the coder had to guess:
  - RULES: a numbered rule for each fact the coder got wrong that a test can check, written "when X, then Y" with numbers. Facts about the INITIAL STATE count: for example
    "after the deal the deck holds N cards and every seat holds 2, and each role appears exactly 3 times in the deck and hands together". Do not repeat a rule already there.
  - OFFERS: for EVERY question the round asks, a row saying who is asked and exactly what each seat may be offered in each case. A seat is never offered what it may not do:
    "the target of an assassination: pass, challenge, block as Contessa; any other seat: pass, challenge", "a target: every living seat except the one acting",
    "the action: only the ones the seat can pay for". Write the whole table, not only the rows the findings mention.
  - STEPS: if a round step's effect was ambiguous and the coder resolved it wrongly, give its corrected `effect` text.
Use the spec's own words and attribute names. Do not invent mechanics. A finding that asks for something the design does not say is not yours to add.

Reply with ONE JSON object and nothing else:
  {"rules_add": [{"id": "R37", "text": "..."}],
   "offers": [{"question": "...", "who": "...", "options": "..."}],
   "step_edits": [{"step": 3, "effect": "the corrected effect"}],
   "notes": "one or two sentences on what you changed and why"}"""


def build_prompt(spec: dict, findings: list[dict]) -> str:
    rules = "\n".join(f"{r['id']}. {r['text']}" for r in spec.get("rules") or []) or "(none)"
    steps = "\n".join(f"{i}. [{s['action']}] {s.get('who', '')}: answers {json.dumps(s.get('answer'))[:200]}; effect: {s.get('effect', '')[:300]}"
                      for i, s in enumerate(spec["round"], 1))
    attrs = "; ".join(f"{scope} `{a['key']}` ({a.get('visible')}, {a.get('type')})" for scope in ("player", "game") for a in spec["attributes"][scope])
    found = "\n".join(f"- {f.get('id', '')} [{f['category']}] {f['where']}: observed {f['observed']} | expected {f['expected']} | fix {f['fix']}" for f in findings)
    return (f"SPEC: {spec['name']}, {spec['players']['min']} to {spec['players']['max']} players.\n\nNUMBERED RULES:\n{rules}\n\nROUND STEPS:\n{steps}\n\n"
            f"STATE: {attrs}\n\nSETUP:\n" + "\n".join(f"- {t}" for t in spec["setup"]) +
            f"\n\nCURRENT OFFERS:\n{json.dumps(spec.get('offers') or [], indent=1)}\n\nFINDINGS FROM THE REVIEWED PLAY:\n{found}")


def apply(spec: dict, change: dict) -> dict:
    """The spec with the model's additions merged in. The input is not changed."""
    new = copy.deepcopy(spec)
    have = {r["id"] for r in new.get("rules") or []}
    rules = list(new.get("rules") or [])
    for r in change.get("rules_add") or []:
        rid = str(r.get("id", "")).strip()
        if not rid or rid in have:  # a clashing id takes the next free number
            n = len(rules) + 1
            while f"R{n}" in have:
                n += 1
            rid = f"R{n}"
        have.add(rid)
        rules.append({"id": rid, "text": str(r["text"]).strip()})
    new["rules"] = rules
    if change.get("offers"):
        new["offers"] = change["offers"]
    for e in change.get("step_edits") or []:
        i = int(e["step"]) - 1
        if 0 <= i < len(new["round"]) and str(e.get("effect", "")).strip():
            new["round"][i]["effect"] = str(e["effect"]).strip()
    return new


def problems(change) -> list[str]:
    if not isinstance(change, dict):
        return ["reply with one JSON object"]
    out = []
    for r in change.get("rules_add") or []:
        if not (isinstance(r, dict) and str(r.get("text", "")).strip()):
            out.append('each rules_add needs {"id", "text"} with the text filled in')
    for o in change.get("offers") or []:
        if not (isinstance(o, dict) and all(str(o.get(k, "")).strip() for k in ("question", "who", "options"))):
            out.append('each offers row needs "question", "who" and "options"')
    for e in change.get("step_edits") or []:
        if not (isinstance(e, dict) and isinstance(e.get("step"), int) and str(e.get("effect", "")).strip()):
            out.append('each step_edits row needs a whole-number "step" and an "effect"')
    if not (change.get("rules_add") or change.get("offers") or change.get("step_edits")):
        out.append("nothing was changed: add rules, an offers table or step edits")
    return out


def revise_spec(completion: Completion, spec: dict, review: dict, drop: tuple[str, ...] = (), repairs: int = 2) -> tuple[dict | None, dict, str]:
    """(the revised spec, what the model changed, an error). Findings named in `drop` were judged wrong by a person and are not shown."""
    findings = [f for f in review.get("findings") or [] if f.get("category") in FIXABLE and f.get("id") not in drop]
    if not findings:
        return None, {}, "no finding is one a spec can fix"
    prompt = build_prompt(spec, findings)
    base, error, reply = prompt, "", ""
    for _ in range(repairs + 1):
        try:
            reply = completion.complete(prompt, system=SYSTEM)
            change = first_json(reply)
            found = problems(change)
            if not found:
                revised = apply(spec, change)
                found = specmod.problems(revised)
        except ValueError as exc:
            change, found = {}, [str(exc)]
        except Exception as exc:  # noqa: BLE001 - a backend that is down is not a bad revision
            return None, {}, f"the model call failed: {str(exc)[:200]}"
        if not found:
            return revised, change, ""
        error = "; ".join(found)
        prompt = refused(base, reply, error)
    return None, {}, error


DESIGN_FEEDBACK_HEAD = """THE DESIGN AS IT STANDS. Revise it: keep everything that works, and keep it faithful to the idea. Do not make the game simpler to make it easier.

{design}

WHAT A REAL PLAY OF THIS DESIGN SHOWED. Each finding says what was seen, what it should have been and what would fix it. Rewrite the rules so that none of these can happen again.
Where a finding shows the coder or the players had to GUESS, write the missing fact into the rules itself, in numbers and in order: the initial state (what each seat holds after setup, how many items a deck holds),
what each seat may be offered in each situation (and never anything it may not do), the order of steps inside a resolution, what a player is told and when, and the outcome in BOTH cases of every decision
(true and false, success and failure, whether the action still goes ahead). Rules the earlier version already had stay unless a finding shows they are wrong.

{findings}"""


def design_text(plan: dict) -> str:
    """The design as the designer wrote it, for the designer to revise."""
    v = plan["variation"]
    kept = "\n".join(f"- {k}" for k in plan.get("keeps") or [])
    changed = "\n".join(f"- {c.get('what')} (because: {c.get('fixes', '')})" for c in plan.get("changes") or [])
    p = v["players"]
    return (f"{v['name']}, {p['min']} to {p['max']} players, best with {p.get('suggested', p['min'])}.\n\nRULES:\n{v['rules']}\n\nHOW THE WINNER IS DECIDED: {v['objective']}\n\n"
            f"WHY THE TABLE SIZE: {v.get('expected_effect', '')}\n\nWHAT IT KEPT OF THE IDEA:\n{kept or '(not listed)'}\n\nWHAT IT CHANGED FROM THE IDEA, AND WHY:\n{changed or '(not listed)'}")


def compose_design_feedback(plan: dict, findings: list[dict]) -> str:
    """What the designer is given to improve the design: the design itself, then the confirmed findings and the minor ones to fix in the same pass."""
    def line(f: dict) -> str:
        return f"- [{f.get('severity', 'minor')}, {f.get('category')}] {f.get('where')}: {f.get('observed')} | should be: {f.get('expected')} | fix: {f.get('fix')}"

    severe = [f for f in findings if f.get("severity") in ("critical", "major")]
    minor = [f for f in findings if f.get("severity") not in ("critical", "major")]
    parts = ["CONFIRMED (critical or major):\n" + "\n".join(line(f) for f in severe) if severe else "",
             "MINOR (fix them in this pass too):\n" + "\n".join(line(f) for f in minor) if minor else ""]
    return DESIGN_FEEDBACK_HEAD.format(design=design_text(plan), findings="\n\n".join(p for p in parts if p))


KEPT = ("variation.json", "VARIATION.md", "spec.json", "SPEC.md", "game.json", "scenarios.json", "report.json")


def prepare_redesign(folder: Path, findings: list[dict], iteration: int) -> tuple[str, Path]:
    """Keep every artifact of this version under history/iteration-N, and write the feedback the designer is given. Returns (feedback, where they were kept)."""
    import shutil

    plan = json.loads((folder / "variation.json").read_text())
    feedback = compose_design_feedback(plan, findings)
    keep = folder / "history" / f"iteration-{iteration}"
    keep.mkdir(parents=True, exist_ok=True)
    for name in KEPT:
        if (folder / name).exists():
            shutil.copy2(folder / name, keep / name)
    return feedback, keep


def save(folder: Path, revised: dict) -> Path:
    """Keep the old spec, write the new one and its page."""
    old = folder / "spec.json"
    history = folder / "history"
    history.mkdir(exist_ok=True)
    n = len(list(history.glob("spec.before-revision-*.json"))) + 1
    backup = history / f"spec.before-revision-{n}.json"
    backup.write_text(old.read_text())
    old.write_text(specmod.dumps(revised))
    (folder / "SPEC.md").write_text(specmod.render(revised))
    return backup
