"""Review a real play of a built game against what it was meant to be.

After the game file is final, `simulate` plays it with a model in every seat and keeps the whole log. This reads that log
against the four things the game answers to:

  the IDEA     the inventory entry: what the game is, in the source's words
  the DESIGN   the rules the designer wrote from it, and what it changed and why
  the SPEC     the rule table (R1, R2...) and the state the game keeps
  the PROMPT   what each player was actually shown: the system prompt, the rules brief, the question

and says whether the play matched, and where it did not: what was seen (round and seat), what it should have been
and by which authority, whose fault the gap is (the game file, the design, the prompt the players see, the engine, or the
players' own play), and what would fix it. Nothing here edits the game.

The cheap, exact facts (model errors, refused answers, unfilled text, how many rules were seen at work) are worked out
by code and handed to the reviewer, so it spends its attention on what only reading can find.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Protocol

from gen_game import lint
from gen_game.repair import refused
from gen_inventory.crawl import first_json

SKIP_FACTS = ("the_table",)
CATEGORIES = ("game_file", "design", "prompt", "infra", "players", "none")
SEVERITIES = ("critical", "major", "minor")
#: Older wording the reviewer may still use, read as the new one.
ALIASES = {"engine": "infra", "high": "major", "medium": "major", "low": "minor"}


class Completion(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


SYSTEM = """You review ONE real play of a game against what the game was meant to be. You are given the game's IDEA (the source's own description),
the DESIGN (the rules a designer wrote from it, and the changes it made and why), the SPEC (a table of numbered rules, and the state the game keeps),
the PROMPT every player was shown (the system prompt, the rules brief, a question), and the PLAY: a transcript of the whole match (what every player
answered, what the table was told, each round's state) plus some measured facts.

Your job is to say whether the play matched, and where it did not. Check:
  1. RULES. Does every change of state in the transcript follow the DESIGN's rules and the SPEC's numbered rules (costs, gains, who may do what, challenges,
     blocks, eliminations, the ending)? Recompute coins, cards and counts yourself from the state lines. Cite the round and seat.
  2. IDEA. Is the play the game the IDEA describes, or has something that makes it that game been lost? (A change the DESIGN lists with a reason is not a gap;
     a change it does not list is.)
  3. PROMPT. Did the players have what they needed to play: the rules, their own state, their legal options, what happened? Was anything missing, wrong, contradictory,
     unfilled (`{name}`), empty, repeated, or leaking another player's hidden information? Did a player's reply show it misread the prompt?
  4. INTERFACE. Was each seat offered only what it may do, and asked only what needs deciding? (A seat offered an illegal option, or asked twice for the same decision,
     is a gap in the game file even when the outcome is right.)
  5. COVERAGE. Which numbered rules were seen at work in this play, and which were not exercised (so this play says nothing about them).

Be exact and honest. Report only what the transcript shows; do not invent events and do not assume a rule is broken because the players played badly (poor or
odd play by the players is `players`, not a gap in the game). If everything matched, say so plainly: an empty list of findings is a valid answer.
For each gap say whose fault it is:
  game_file  the game file does not do what the DESIGN/SPEC says (the coder's)
  design     the DESIGN/SPEC itself is wrong, unclear or departs from the IDEA without saying so
  prompt     what the players are shown is missing, unclear or misleading
  infra      the platform, the harness or the tools did something they should not (an unfilled placeholder, an announcement about nobody, a call that failed)
  players    the players' own play (not a defect)

Give each finding a severity:
  critical   the game cannot be played correctly: a crash, a hang, no ending, a wrong winner, corrupted state (cards or coins that should not exist), hidden information leaked
  major      a rule or an offer differs from the DESIGN/SPEC, or the prompt hides or misstates something a player decides on (would a typical player's choice change if they read it?)
  minor      display, wording, noise or efficiency that does not change play

Reply with ONE JSON object and nothing else:

  {"verdict": "aligned" or "gaps",
   "summary": "two or three sentences",
   "findings": [{"id": "F1", "where": "round 8, seat 1", "observed": "what the transcript shows",
                 "expected": "what it should have been, and which of IDEA / DESIGN / SPEC R# / PROMPT says so",
                 "category": "game_file|design|prompt|infra|players",
                 "severity": "critical|major|minor", "fix": "what would fix it, in the game file / design / prompt / engine"}],
   "rules_seen": ["R1", ...], "rules_not_seen": ["R7", ...],
   "idea_alignment": "one sentence: is it still the game in the IDEA, and what was changed"}"""


def load_sim(path: Path) -> dict:
    return json.loads(Path(path).read_text())


def stats(sim: dict) -> dict:
    """What can be counted exactly from the log."""
    recs = sim["events"]["records"]
    moves = [r for r in recs if r.get("category") == "turn" and r.get("type") == "move"]
    calls = [r for r in recs if r.get("type") == "model_call"]
    found = Counter(lint.scan(recs))
    # What each seat was sent is a message in a played match, not a logged fact: the same checks on the text itself.
    sent = [(r.get("msg_type") or "message", r["body"]) for r in recs if r.get("category") == "message" and r.get("type") == "offered" and r.get("body")]
    found.update(lint.scan_bodies(sent))
    return {
        "players": sim.get("players"), "seed": sim.get("seed"),
        "status": (sim.get("snapshot") or {}).get("status"), "winner": (sim.get("snapshot") or {}).get("winner"),
        "rounds": (sim.get("snapshot") or {}).get("round"),
        "decisions": len(moves), "degraded_turns": sum(1 for r in moves if r.get("degraded")),
        "auto_answers": sum(1 for r in recs if r.get("type") == "auto_answer"),
        "model_calls": len(calls), "model_errors": sum(1 for r in calls if r.get("error")),
        "model_seconds_avg": round(sum(r.get("seconds", 0) for r in calls) / len(calls), 1) if calls else 0,
        "replies_over_80_chars": sum(1 for r in calls if len(str(r.get("raw", ""))) > 80),
        "trace_lint": [f"{f} (x{n})" if n > 1 else f for f, n in found.most_common(10)],
    }


def compact_trace(sim: dict, limit: int = 60000) -> str:
    """The match, round by round: state lines, what each seat answered, what the table was told, and how it ended.

    What only some seats were told (their own private view) is cut short and not repeated, so the middle of a long match
    is not what gets thrown away.
    """
    recs = sim["events"]["records"]
    lines: list[str] = []
    current = None
    private_seen: set = set()
    endings = 0
    for r in recs:
        rnd, cat = r.get("round"), r.get("category")
        if rnd != current and cat in ("fact", "turn"):
            current = rnd
            private_seen = set()
            lines.append(f"\n== round {rnd} ==")
        if cat == "fact" and r.get("type") not in SKIP_FACTS:
            p = r.get("payload") or {}
            text = str(p.get("rendered") or "").strip()
            if not text:
                continue
            if r.get("type") == "game_over":
                endings += 1
                if endings == 1:
                    lines.append(f"  [THE ENDING, as announced to the table] {text[:700]}")
                continue
            who = (r.get("audience") or {}).get("kind", "")
            entitled = r.get("entitled")
            if who == "all":
                lines.append(f"  [ALL] {text[:420]}")
            else:
                key = (str(entitled), text[:90])
                if key not in private_seen:
                    private_seen.add(key)
                    lines.append(f"  [to {entitled}] {text[:230]}")
        elif cat == "turn" and r.get("type") == "move":
            a = r.get("action") or {}
            value = a.get("target") if a.get("target") is not None else a.get("text")
            lines.append(f"  seat {r.get('seat')} answers `{r.get('action_schema')}`: {str(value)[:140]}" + ("  (DEGRADED)" if r.get("degraded") else ""))
        elif cat == "orchestrator" and r.get("type") == "action_request":
            lines.append(f"  seat {r.get('seat')} asked `{r.get('action_schema')}` with options {str(r.get('legal_targets'))[:160]}")
        elif r.get("type") == "auto_answer":
            lines.append(f"  (engine answered for seat {r.get('seat')} `{r.get('step')}`: {r.get('value')!r})")
    status = (sim.get("snapshot") or {}).get("seats")
    if status:
        lines.append("\nFINAL SEAT STATUS AS THE PLATFORM SHOWS IT: " + ", ".join(f"seat {x['index']} {x['name']}: {x['status']}" for x in status))
    text = "\n".join(lines)
    return text if len(text) <= limit else text[:limit // 2] + "\n... (the middle is cut) ...\n" + text[-limit // 2:]


def shown_prompts(sim: dict) -> str:
    """What a seat was actually shown: the system prompt and the first question in full, and a later one cut short.

    A play with model seats logs each call's prompt. A play whose seats were connected from outside (a person's own assistant)
    has no such calls, so the messages the server offered the seats are used instead.
    """
    recs = sim["events"]["records"]
    calls = [r for r in recs if r.get("type") == "model_call" and str(r.get("for", "")).startswith("seat")]
    if calls:
        first, later = calls[0], calls[len(calls) // 2]
        return (f"SYSTEM PROMPT:\n{first.get('system', '')}\n\nFIRST QUESTION, seat {first.get('for')} (everything it was shown):\n{first.get('prompt', '')}\n\n"
                f"A LATER QUESTION, {later.get('for')} (cut):\n{str(later.get('prompt', ''))[:2600]}\n...")
    offered = [r for r in recs if r.get("category") == "message" and r.get("type") == "offered" and r.get("body")]
    if not offered:
        return "(the log holds no prompts)"
    brief = next((r for r in recs if r.get("category") == "message" and r.get("type") == "delivered" and r.get("msg_type") == "GAME_START" and r.get("body")), None)
    first, later = offered[0], offered[len(offered) // 2]
    return ((f"THE RULES BRIEF every seat was sent before its first turn (GAME_START, seat {brief.get('seat')}):\n{brief['body']}\n\n" if brief else "") +
            f"FIRST QUESTION, seat {first.get('seat')} (everything the server offered it):\n{first['body']}\n\n"
            f"A LATER QUESTION, seat {later.get('seat')} (cut):\n{str(later['body'])[:2600]}\n...")


def build_prompt(sim: dict, idea: str, design: dict, spec: dict) -> str:
    v = design["variation"]
    rules = "\n".join(f"{r['id']}. {r['text']}" for r in spec.get("rules") or []) or "(the spec lists no numbered rules)"
    changes = "\n".join(f"- {c['what']} (fixes: {c.get('fixes', '')})" for c in design.get("changes", []))
    attrs = "; ".join(f"{scope} `{a['key']}` ({a.get('visible')})" for scope in ("player", "game") for a in spec["attributes"][scope])
    return (f"THE IDEA (the source's description of the game):\n{idea}\n\n"
            f"THE DESIGN: {v['name']}, {v['players']['min']} to {v['players']['max']} players.\n{v['rules']}\nHow the winner is decided: {v['objective']}\n"
            f"What the design changed from the idea, and why:\n{changes or '(none listed)'}\n\n"
            f"THE SPEC's numbered rules:\n{rules}\nState the game keeps: {attrs}\n\n"
            f"THE PROMPT the players were shown:\n{shown_prompts(sim)}\n\n"
            f"MEASURED FACTS about this play:\n{json.dumps(stats(sim), indent=1)}\n\n"
            f"THE PLAY (a transcript of the whole match; [ALL] was told to everyone, [to [..]] only to those seats):\n{compact_trace(sim)}")


def problems(review) -> list[str]:
    if not isinstance(review, dict):
        return ["reply with one JSON object"]
    out = []
    if review.get("verdict") not in ("aligned", "gaps"):
        out.append('verdict must be "aligned" or "gaps"')
    if not isinstance(review.get("findings"), list):
        out.append("findings must be a list (empty when everything matched)")
    else:
        for i, f in enumerate(review["findings"], 1):
            if not isinstance(f, dict) or not all(str(f.get(k, "")).strip() for k in ("where", "observed", "expected", "fix")):
                out.append(f"finding {i} needs where, observed, expected and fix")
            elif ALIASES.get(f.get("category"), f.get("category")) not in CATEGORIES[:-1]:
                out.append(f"finding {i}: category must be one of {', '.join(CATEGORIES[:-1])}")
            elif f.get("severity") is not None and ALIASES.get(f.get("severity"), f.get("severity")) not in SEVERITIES:
                out.append(f"finding {i}: severity must be one of {', '.join(SEVERITIES)}")
    for k in ("rules_seen", "rules_not_seen"):
        if not isinstance(review.get(k, []), list):
            out.append(f"{k} must be a list")
    if review.get("verdict") == "aligned" and review.get("findings"):
        out.append('a verdict of "aligned" cannot come with findings')
    return out


def normalize(review: dict) -> dict:
    """The review with the old words read as the new ones, and every finding carrying a severity."""
    for f in review.get("findings") or []:
        f["category"] = ALIASES.get(f.get("category"), f.get("category"))
        f["severity"] = ALIASES.get(f.get("severity"), f.get("severity")) or "minor"
    return review


def review_play(completion: Completion, sim: dict, idea: str, design: dict, spec: dict, repairs: int = 2) -> tuple[dict | None, str]:
    prompt = build_prompt(sim, idea, design, spec)
    base, error, reply = prompt, "", ""
    for _ in range(repairs + 1):
        try:
            reply = completion.complete(prompt, system=SYSTEM)
            review = first_json(reply)
            found = problems(review)
        except ValueError as exc:
            review, found = None, [str(exc)]
        except Exception as exc:  # noqa: BLE001 - a backend that is down is not a bad review
            return None, f"the model call failed: {str(exc)[:200]}"
        if not found:
            return normalize(review), ""
        error = "; ".join(found)
        prompt = refused(base, reply, error)
    return None, error


CONFIRM_SYSTEM = """You verify ONE claim about a played game, from the evidence only. You are given a finding (what was observed, what was expected, by which rule) and the
part of the transcript it points to, and the numbered rules. Decide whether the evidence shows what the finding says. Recompute any coins, cards or counts yourself.
Do not give the finding the benefit of the doubt: if the evidence does not show it, or shows something that explains it as correct play, it is not confirmed.

Reply with ONE JSON object and nothing else:  {"confirmed": true or false, "evidence": "one or two sentences: what in the transcript shows it, or what refutes it"}"""


def rounds_named(where: str) -> list[int]:
    """The round numbers a finding's `where` names: "round 8, seat 1", "rounds 3, 4 and 10", "rounds 17-21"."""
    import re

    m = re.search(r"rounds?\s+([\d][\d,\s\-\u2013and]*)", where or "", re.I)
    if not m:
        return []
    out: list[int] = []
    for part in re.split(r",|\band\b", m.group(1)):
        part = part.strip()
        if r := re.fullmatch(r"(\d+)\s*[-\u2013]\s*(\d+)", part):
            out += list(range(int(r.group(1)), min(int(r.group(2)), int(r.group(1)) + 12) + 1))
        elif part.isdigit():
            out.append(int(part))
    return out


def evidence_for(sim: dict, finding: dict, spec: dict, window: int = 1) -> str:
    """The transcript around the rounds a finding names (or what the players were shown, for a finding about the prompt)."""
    rounds = rounds_named(finding.get("where", ""))
    trace = compact_trace(sim, limit=200000)
    if finding.get("category") == "prompt" or not rounds:
        return shown_prompts(sim) + ("\n\nTRANSCRIPT (the part around the finding):\n" + _slice(trace, rounds, window) if rounds else "")
    return _slice(trace, rounds, window)


def _slice(trace: str, rounds: list[int], window: int) -> str:
    import re

    if not rounds:
        return trace[:6000]
    keep = {r + d for r in rounds for d in range(-window, window + 1)}
    parts = re.split(r"(?=\n== round \d+ ==)", trace)
    chosen = [p for p in parts if (m := re.match(r"\n== round (\d+) ==", p)) and int(m.group(1)) in keep]
    return "".join(chosen)[:14000] or trace[:6000]


def confirm(completion: Completion, sim: dict, finding: dict, spec: dict) -> tuple[bool | None, str]:
    """(confirmed, why). None when the verifier could not be reached or answered nothing usable: unconfirmed, not refuted."""
    rules = "\n".join(f"{r['id']}. {r['text']}" for r in spec.get("rules") or [])
    prompt = (f"FINDING ({finding.get('id', '')}, {finding.get('category')}, {finding.get('severity')}) at {finding.get('where')}:\n"
              f"observed: {finding.get('observed')}\nexpected: {finding.get('expected')}\n\nTHE NUMBERED RULES:\n{rules}\n\n"
              f"EVIDENCE:\n{evidence_for(sim, finding, spec)}")
    try:
        reply = first_json(completion.complete(prompt, system=CONFIRM_SYSTEM))
    except Exception as exc:  # noqa: BLE001 - a verifier that cannot answer leaves the finding unconfirmed
        return None, f"the verifier could not answer: {str(exc)[:120]}"
    if not isinstance(reply, dict) or not isinstance(reply.get("confirmed"), bool):
        return None, "the verifier gave no usable answer"
    return reply["confirmed"], str(reply.get("evidence", ""))[:300]


def render(review: dict, sim: dict, game_name: str) -> str:
    s = stats(sim)
    out = [f"# Play review: {game_name}", "",
           f"Verdict: **{review['verdict'].upper()}**", "", review.get("summary", ""), "",
           "## The play", "",
           f"- players {s['players']}, seed {s['seed']}; {s['status']}, winner {s['winner']}, {s['rounds']} rounds, {s['decisions']} decisions",
           f"- model calls {s['model_calls']} (errors {s['model_errors']}, average {s['model_seconds_avg']}s); degraded turns {s['degraded_turns']}; answered by the engine {s['auto_answers']}"]
    out += [f"- trace check: {f}" for f in s["trace_lint"]] or ["- trace checks: clean"]
    out += ["", "## Alignment with the idea", "", review.get("idea_alignment", "")]
    out += ["", "## Gaps", ""]
    findings = review.get("findings") or []
    if not findings:
        out.append("- none: the play matched the design")
    for f in findings:
        out += [f"### {f.get('id', '')} [{f['category']}, {f.get('severity', 'minor')}] {f['where']}", "",
                f"- observed: {f['observed']}", f"- expected: {f['expected']}", f"- fix: {f['fix']}", ""]
    by = Counter(f["category"] for f in findings)
    out += ["## Where the fixes belong", ""] + [f"- {k}: {n}" for k, n in by.most_common()] if findings else []
    out += ["", "## Rules", "", f"- seen at work: {', '.join(review.get('rules_seen') or []) or 'none named'}",
            f"- not exercised by this play: {', '.join(review.get('rules_not_seen') or []) or 'none'}"]
    return "\n".join(out) + "\n"
