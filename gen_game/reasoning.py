"""Did winning take reasoning and planning? Read from what the players said in real plays.

A result says a game can be won; it does not say how. This reads the decisions of every play of a game, each with the
options on offer, the answer, the player's own words and what the table had just been told, and asks a model three
things, each scored 0 to 3 with quotes:

  reasoning   do players infer hidden information and weigh options against the state, correctly?
  planning    do they look past the current move: set up later moves, keep resources for later, rely on what others will do?
  luck        how much did chance decide, rather than choices?

The exact facts (choices made, replies that give a reason) are counted by code. Every quote must be found in the reply
it cites, so a review cannot invent the reasoning it praises, and the verdict is worked out from the scores, not
written by the model. Nothing here changes the game.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Protocol

from gen_game.repair import refused
from gen_inventory.crawl import first_json

ASPECTS = ("reasoning", "planning", "luck")
#: A reply with at least this many words before its answer gives a reason; fewer is an answer alone.
REASON_WORDS = 8
#: Fewer choices than this share with a reason, and there is not enough to read: the check says "unmeasured" and asks no model.
MEASURABLE = 0.5
SAID_CHARS = 900
LIMIT = 150000


class Completion(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


SYSTEM = """You judge whether winning a game took REASONING and PLANNING, from what its players said in real plays. You are given the
game's rules, what its designer said a good player must think about, and every decision from the plays: the options on offer, the
answer, the player's own words before it, and what the table had just been told.

Score three things from 0 to 3:
- reasoning: 0 = answers show no thought about the state or the other players; 1 = thought is generic or only restates the rules;
  2 = in most decisions players infer hidden information or weigh options against the state; 3 = most decisions rest on specific,
  correct inference (what others hold or know, what is left, the odds).
- planning: 0 = every move is chosen for now only; 1 = occasional look-ahead; 2 = players set up later moves or keep resources for
  later; 3 = plans over several turns, including plans that rely on what other players will do, are made and carried out.
- luck: 0 = chance decided nothing; 1 = chance moved the result at the margin; 2 = chance decided some results; 3 = chance decided the
  results and choices mattered little.

Judge the decisions, not the result. Restating the rules is not reasoning. A well-reasoned move that turned out badly is still
reasoning; list a weak spot only where the reasoning was wrong, or a clearly better-reasoned option was on offer. Compare what you see
with what the designer said a good player must think about.

Every evidence item quotes the player's own words EXACTLY, copied from that decision (you may skip words with "..."), and names the
match, turn and seat it comes from. Give at least one evidence item for reasoning and for planning unless the score is 0.

Reply with one JSON object and nothing else:
{"reasoning": {"score": 0-3, "notes": "two sentences", "evidence": [{"match": 1, "turn": 5, "seat": 2, "quote": "...", "shows": "what it shows"}]},
 "planning": {"score": 0-3, "notes": "...", "evidence": [...]},
 "luck": {"score": 0-3, "notes": "...", "evidence": [...]},
 "weak_spots": [{"match": 1, "turn": 7, "seat": 1, "what": "what was wrong or missed, and the better option"}],
 "summary": "two sentences: does winning this game take reasoning and planning, and what would make it take more?"}"""


def _seat(value) -> int | None:
    m = re.search(r"\d+", str(value or ""))
    return int(m.group(0)) if m else None


def _answer_removed(raw: str, chose: str) -> str:
    """The reply without its final answer line: what the player said before answering."""
    text = raw.strip()
    lines = text.splitlines()
    if lines and chose and chose.strip() in lines[-1]:
        text = "\n".join(lines[:-1]).strip()
    return text


def decisions(sim: dict) -> list[dict]:
    """Every choice in one play, with the player's words and what the table was told since the previous choice. A move with only
    one option on offer was not a choice and is left out."""
    out, said, news = [], {}, []
    for r in sim["events"]["records"]:
        if r.get("category") == "fact" and (r.get("audience") or {}).get("kind") == "all":
            text = str((r.get("payload") or {}).get("rendered") or "").strip()
            if text:
                news.append(text[:300])
        elif r.get("type") == "model_call" and r.get("raw"):
            said[(str(r.get("turn_seq")), _seat(r.get("for")))] = str(r["raw"])
        elif r.get("category") == "turn" and r.get("type") == "move":
            options = [str(o) for o in r.get("legal_targets") or []]  # options may be numbers or seats
            chose = str((r.get("action") or {}).get("target") or "")
            if len(options) > 1:
                raw = said.get((str(r.get("turn_seq")), _seat(r.get("seat"))), "")
                out.append({"turn": int(r.get("turn_seq") or 0), "round": r.get("round"), "seat": _seat(r.get("seat")), "options": options,
                            "chose": chose, "said": _answer_removed(raw, chose), "before": news})
            news = []
    return out


def stats(sims: list[dict]) -> dict:
    """What can be counted exactly: plays, choices, replies that give a reason, results."""
    found = [decisions(s) for s in sims]
    flat = [d for ds in found for d in ds]
    words = [len(d["said"].split()) for d in flat]
    return {
        "matches": len(sims), "decisions": len(flat),
        "with_reasons": sum(w >= REASON_WORDS for w in words),
        "reason_words_avg": round(sum(words) / len(words), 1) if words else 0,
        "results": dict(Counter(str((s.get("snapshot") or {}).get("winner")) for s in sims)),
    }


def transcript(sims: list[dict], limit: int = LIMIT) -> str:
    parts = []
    for n, sim in enumerate(sims, 1):
        snap = sim.get("snapshot") or {}
        parts.append(f"=== match {n}: result {snap.get('winner')!r}. {str(snap.get('summary') or '')[:300]}")
        for d in decisions(sim):
            parts += [f"  table: {line}" for line in d["before"]]
            shown = ", ".join(d["options"][:24]) + (f", ... ({len(d['options'])} in all)" if len(d["options"]) > 24 else "")
            parts.append(f"- match {n}, turn {d['turn']}, seat {d['seat']}: offered [{shown}]; chose {d['chose']!r}.")
            parts.append(f"  said: {d['said'][:SAID_CHARS] or '(nothing but the answer)'}")
    text = "\n".join(parts)
    return text if len(text) <= limit else text[:limit] + "\n... (cut: the rest of the plays are not shown)"


def build_prompt(sims: list[dict], design: dict) -> str:
    v = design.get("variation") or design
    return (f"GAME: {v.get('name', '')}\n\nRULES:\n{v.get('rules', '')}\n\nWHAT A GOOD PLAYER MUST THINK ABOUT (the designer's words):\n"
            f"{v.get('expected_effect', '(not given)')}\n\nTHE DECISIONS:\n{transcript(sims)}")


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("’", "'")).strip().lower()


def _quoted(quote: str, said: str) -> bool:
    """Every piece of the quote, between any "..." skips, is in what the player said, in order."""
    pieces = [p.strip(" \"'") for p in re.split(r"\.\.\.|…", _norm(quote))]
    pieces = [p for p in pieces if p]
    at, hay = 0, _norm(said)
    for p in pieces:
        at = hay.find(p, at)
        if at < 0:
            return False
        at += len(p)
    return bool(pieces)


def problems(result, found: list[list[dict]]) -> list[str]:
    """What is wrong with a check: missing parts, scores out of range, and quotes that are not in the reply they cite."""
    if not isinstance(result, dict):
        return ["reply with one JSON object"]
    out = []
    for a in ASPECTS:
        part = result.get(a)
        if not isinstance(part, dict):
            out.append(f"{a} must be an object with score, notes and evidence")
            continue
        score = part.get("score")
        if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 3:
            out.append(f"{a}.score must be a whole number from 0 to 3")
        evidence = part.get("evidence")
        if not isinstance(evidence, list):
            out.append(f"{a}.evidence must be a list")
            continue
        if a != "luck" and isinstance(score, int) and score > 0 and not evidence:
            out.append(f"{a} needs at least one evidence item when its score is above 0")
        for i, e in enumerate(evidence, 1):
            where = f"{a}.evidence {i}"
            try:
                said = next(d["said"] for d in found[int(e["match"]) - 1] if d["turn"] == int(e["turn"]) and d["seat"] == int(e["seat"]))
            except (KeyError, IndexError, StopIteration, TypeError, ValueError):
                out.append(f"{where}: no decision at match {e.get('match')!r}, turn {e.get('turn')!r}, seat {e.get('seat')!r}" if isinstance(e, dict)
                           else f"{where} must be an object")
                continue
            if not _quoted(str(e.get("quote") or ""), said):
                out.append(f"{where}: the quote {str(e.get('quote'))[:80]!r} was not found in what seat {e['seat']} said at match {e['match']}, turn {e['turn']}; copy their words exactly")
    if not isinstance(result.get("weak_spots", []), list):
        out.append("weak_spots must be a list")
    if not str(result.get("summary") or "").strip():
        out.append("summary is missing")
    return out


def verdict(result: dict) -> str:
    """strong: reasoning and planning both 2 or more, and chance at most at the margin. weak: either is 1 or less, or chance decided the results."""
    r, p, luck = (result[a]["score"] for a in ASPECTS)
    if r <= 1 or p <= 1 or luck >= 3:
        return "weak"
    return "strong" if luck <= 1 else "adequate"


def unmeasured(facts: dict) -> dict:
    """The check when the players gave too few reasons to read: no scores, and nothing for the loop to act on."""
    return {"verdict": "unmeasured", "weak_spots": [], **{a: {"score": None, "notes": "", "evidence": []} for a in ASPECTS},
            "summary": f"Only {facts['with_reasons']} of {facts['decisions']} choices came with a reason, so how the players thought cannot be "
                       "read. Play it with players that say why they choose (the seats are asked to)."}


def check(completion: Completion, sims: list[dict], design: dict, repairs: int = 2) -> tuple[dict | None, str]:
    facts = stats(sims)
    if facts["decisions"] and facts["with_reasons"] < MEASURABLE * facts["decisions"]:
        return unmeasured(facts), ""
    found = [decisions(s) for s in sims]
    base = prompt = build_prompt(sims, design)
    error = ""
    for _ in range(repairs + 1):
        try:
            reply = completion.complete(prompt, system=SYSTEM)
        except Exception as exc:  # noqa: BLE001 - a backend that is down is not a bad check
            return None, f"the model call failed: {str(exc)[:200]}"
        try:
            result = first_json(reply)
            wrong = problems(result, found)
        except ValueError as exc:
            result, wrong = None, [str(exc)]
        if not wrong:
            return {**result, "verdict": verdict(result)}, ""
        error = "; ".join(wrong)
        prompt = refused(base, reply, error, what="check")
    return None, error


def play_logs(folder: Path) -> list[Path]:
    """The game's plays, oldest first; reviews of a play sit beside it and are not plays."""
    return sorted((p for p in (folder / "sim").glob("*.json") if not p.name.endswith(".review.json")), key=lambda p: p.stat().st_mtime)


def render(result: dict, facts: dict, game_name: str) -> str:
    out = [f"# Reasoning and planning: {game_name}", "", f"**Verdict: {result['verdict']}.** {result.get('summary', '')}", "",
           f"From {facts['matches']} play(s): {facts['decisions']} choices, {facts['with_reasons']} with a reason given "
           f"(about {facts['reason_words_avg']} words each); results {facts['results']}.", ""]
    for a in ASPECTS:
        part = result[a]
        if part.get("score") is None:
            continue
        out += [f"## {a.capitalize()}: {part['score']} of 3", "", part.get("notes", ""), ""]
        out += [f"- match {e['match']}, turn {e['turn']}, seat {e['seat']}: \"{e['quote']}\" ({e.get('shows', '')})" for e in part.get("evidence") or []]
        out.append("")
    out += ["## Weak spots", ""]
    out += [f"- match {w.get('match')}, turn {w.get('turn')}, seat {w.get('seat')}: {w.get('what', '')}" for w in result.get("weak_spots") or []] or ["- none"]
    return "\n".join(out) + "\n"


def write(folder: Path, result: dict, facts: dict, game_name: str) -> Path:
    (folder / "reasoning.json").write_text(json.dumps({**result, "stats": facts}, indent=1) + "\n")
    path = folder / "REASONING.md"
    path.write_text(render(result, facts, game_name))
    return path
