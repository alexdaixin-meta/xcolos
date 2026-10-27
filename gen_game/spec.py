"""Step 2: write a game's rules as a spec.

The spec sits between an inventory game's prose and the platform's game file. It
says the same thing as the rules, but in the platform's terms: which attributes
exist and who may see them, what a round is as a sequence of actions, and how
the game ends, with every number a named parameter. A person can read it to
check the game is the right game, and the encoder and the scenario writer are
both given only this.

Every choice the spec makes that the source rules did not make (a payoff, a
round count, how a tie is broken) is listed under `choices`, and everything it
had to change to fit the platform under `simplifications`, so a reviewer sees
where the converted game departs from the source.
"""

from __future__ import annotations

import json
from typing import Protocol

from gen_game.repair import refused
from gen_inventory.crawl import first_json
from gen_inventory.gates import load_manifest

ACTIONS = ("initialize", "sync", "tell", "ask", "poll", "update", "check", "repeat")
VISIBILITY = ("public", "ally", "others", "none")

#: Every key a spec has, so a missing one is reported by name.
KEYS = ("name", "summary", "players", "parameters", "attributes", "setup", "round", "ending", "choices",
        "simplifications", "unsupported")


class Completion(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


SYSTEM = """You convert a game's rules into a SPEC for a game engine. The engine runs turn-based, text-only
games between language models. It has these actions, and a game is a list of them:

  initialize  fill every player's attributes, then deal   sync   send each player their own state
  tell        send a message and carry on                 ask    address players ONE AT A TIME, each hearing the last
  poll        address everyone AT ONCE and gather; nobody sees an answer until all are in
  update      change state (set, adjust, append, remove) and say what changed
  check       continue, or end the game                   repeat run steps again until a condition holds

Players answer with a choice from a list, a whole number in a range, or short text. Outcomes (scores, eliminations,
the winner) are decided by ARITHMETIC on attributes, never by a model's opinion. A step whose rule check is too complex
for arithmetic may be JUDGED: a referee model answers one stated sentence true or false at play time. Attributes belong to each player or to the whole table,
and each is visible to: public (everyone), ally (own side only), others (everyone but the owner), or none
(hidden; the engine keeps it). A round is a list of steps run in order, repeated until a check ends the game.
The engine is turn-based and has no board, grid, map or movement.

Reply with ONE JSON object and nothing else, with exactly these keys:

  name            the game's name
  summary         one line
  players         {"min": n, "max": n, "suggested": n}: chosen by the PLAYER COUNT rule below, not copied from the source; `suggested` is the size it plays best at
  parameters      {"name": number, ...}: EVERY number in the rules (payoffs, rounds, budgets, ...). If the
                  source leaves a number open (it says "a > c >= d > b"), choose concrete values that satisfy
                  what it says and list the choice under `choices`.
  attributes      {"player": [{"key", "type": "number|text|list|bool", "visible", "initial", "meaning", "observable": true|false}],
                   "game":   [same]}: use snake_case. Mark `observable: true` ONLY for what someone watching the game from outside
                  would read: each player's score and anything the rules reveal. Anything the RULES talk about (a hand of cards, a deck, a pile, a
                  hidden type, who holds what) MUST be declared here with its visibility, even though it is not observable: a game
                  whose rules say "deal two cards" needs a hand and a deck to deal them into and from. A player's own hidden state is
                  `ally` (a PLAYER attribute is never `none`); a table's hidden state, such as a deck, is `none`. Only scratch
                  counters and codes the rules never mention may be left out.
                  Tests may assert only on observable attributes, so keep them few and put the score among them.
  setup           a list of plain sentences: what happens before round one
  round           a list of steps in order. Each: {"action": one of the actions above, "who": "all players | each
                  player in turn | seat 1 | ...", "answer": what a player may reply (or null), "effect": what
                  changes, in terms of attribute keys, "judged": optional, the one sentence a referee answers true or
                  false, for a step whose rule check is too complex for arithmetic}
  ending          {"condition": an arithmetic condition on attributes that ends the game,
                   "rank_by": each player's standing as ONE arithmetic expression over `you.<attribute>` (`you` is the player
                              being ranked) and table attributes, e.g. "you.score" or "you.cards * 1000 + you.coins" (cards first,
                              then coins as the tie-break). It is worked out for every player when the game ends: the highest
                              value wins and players level at the top share the win, so there is no separate draw,
                   "min_to_win": optional, a number or an expression over table attributes (no `you`): the value a player's
                              rank_by must reach to win. Use it when a player must reach a bar to win, so that "nobody qualified"
                              ends with no winner; leave it out otherwise,
                   "decided_by": that ranking in words: what a player's standing is, and who wins}
  rules           (optional but wanted) a list of {"id": "R1", "text": "..."}: EVERY rule of the game as one sentence a test can check, with its numbers: each
                  action's cost and gain, each block, each challenge (a true claim and a bluff), each forced action, each way the game ends. Tests are written
                  one per rule, and a failing test names the rule, so write each as "when X, then Y" with concrete values.
  offers          (optional but wanted) a list of {"question": the round step or question, "who": which seats are asked, "options": exactly what each seat may be offered,
                  in each situation}: for EVERY question, the options by case, such as "the target of an assassination: pass, challenge, block as Contessa; any other
                  seat: pass, challenge", or "a target: every living seat except the one acting". A seat is never offered what it may not do.
  choices         a list of {"what", "why"}: every decision you made that the source rules did not
  simplifications a list of {"what", "why"}: everything you changed to fit the engine
  unsupported     a list of strings: anything the game NEEDS that the actions above cannot do (a board, hidden
                  rules that depend on a prior branch, trading, real time). Empty if nothing. Do not hide a
                  gap by changing the game: say it here.

Be faithful to the source rules. Do not add mechanics. Reply with the JSON object only."""


ENGINE_OVERVIEW = """HOW XCOLOS WORKS, in plain words (design the game, then describe it, in these terms).
A match is a table of seats. The game is a script: some SETUP steps run once, then ROUND steps run in order again and again until an ending
is reached. State lives in attributes: a number, a text, a list or a yes/no, kept for each player or for the whole table. Each attribute has an
owner and a visibility (public, the owner's own, everyone but the owner, or hidden from all), and a player only ever sees what they are entitled to.
What the engine does well:
  - Ask players questions: one player at a time (each hears the answers before), or everyone at once, with nobody seeing an answer until all are in.
    A question takes a choice from a list, a whole number in a range, or a short free-text message. A choice can name another player.
  - Hidden information: a secret dealt to each player at random (a type, a role, a hand), a hidden table (a deck, a discard pile), and revealing one
    player's secret to chosen players. Randomness is seeded, so a match replays exactly.
  - Cards and decks: a shared deck is a list on the table. DRAWING a card is picking one at random from the list, putting it in a player's hand
    list and taking it out of the deck list; RETURNING is the reverse; shuffling is just drawing at random. Dealing N cards to everyone is N draws each.
  - Arithmetic: counters, scores, costs, comparisons, sums over players, counting how many players did something; all decided by calculation, never by opinion.
  - A referee model can rule whether a complex rule applies at a step (true or false), from one sentence; scores and the winner are still calculated.
  - Elimination of players, a fixed number of rounds or "until a condition", and a winner picked by calculation from the final state: each player's
    standing is worked out by one expression, the highest wins, and players level at the top share the win.
  - Talk: players write short messages, one at a time or all at once, that are shown to everyone or to some.
  - Announcements: fixed sentences filled with the current numbers, or a short summary a model writes.
What it cannot do: a board, grid, map or movement; real time or time pressure; a model deciding the outcome (a game's outcome is calculated);
more than the platform's size limits. A game that needs one of these is changed to avoid it, or listed under `unsupported`.
Whatever the rules say happens must happen to a stated piece of state: if a card is dealt, say where it goes; if a card is challenged, say which list it is
checked against; if a player is out, say which number says so."""

PLAYER_COUNT_GUIDE = """PLAYER COUNT. Before anything else, decide how many players the game needs, and put it in `players`. The count in the
source is where to start, not an answer: a source written for two players may play better with more, and the count
you set is the one the game is built and played with.
  - Ask what the game is about (coordination, bluffing, trust, bidding, deduction) and the SMALLEST table where that
    thing really happens. Coordination needs enough players that agreeing is hard and a few who hold out can break a
    group: with two players there is nothing to coordinate, only one other to guess, so a coordination game wants
    at least 3, and a threshold ("enough of us must commit") wants a threshold that is neither everyone nor one.
    A hidden-role game needs enough seats for a minority to hide in; an auction needs rivals to bid against.
  - If the source names a suggested table size (the designer already chose it), keep it as `suggested` and give its reason.
  - Otherwise set `suggested` to the size it plays best at: enough players for the point of the game to work with room to spare, few enough that a turn is short and
    each choice still matters. Real models are tested at that size.
  - Say in one line why the minimum is that number, and why the maximum is not larger (a table so big that one
    player's choice no longer matters, or a conversation too long to follow).
  - Then think as a PLAYER at that table: what is the strategy? What does a thoughtful player do that a thoughtless one
    does not (read the others, bargain, bluff, build trust, hold back)? If you cannot name one, the table or the rules
    need changing before they are written down.
  - With three or more players, decide whether talk before the choice each round earns its place: it does when it gives players
    something to reason about AND they disagree about something, so that following a proposal could cost them; it does not when
    everyone wants the same outcome (the first speaker proposes, the rest copy) or when it only adds words. If the rules keep it,
    build it as a simultaneous `poll` for one short text message from every player, shown to everyone with `broadcast` (`{"to": "all", "text": "Seat {seat} says: {value}"}`), and then the
    `poll` for the choice. Use `ask`, one player at a time, only when the rules say the order of speaking matters. Say which you chose, and
    why, in `choices`.
Put the reasoning in `choices` (for example {"what": "3 to 5 players", "why": "..."}). Every number in the rules that
depends on the count (a threshold, a pot, a share) is written as a rule over the count, so it holds at each size."""



def system_with_engine_facts(manifest: dict | None = None) -> str:
    """The spec prompt plus what the platform can and cannot do, from the capability manifest,
    so a spec is written inside the supported infrastructure and a gap is declared, not hidden."""
    m = (manifest or load_manifest())["needs"]
    group = lambda *v: "; ".join(f"{k} ({e['note']})" for k, e in m.items() if e["verdict"] in v)  # noqa: E731
    return (SYSTEM + "\n\nWhat the engine supports, from its capability list:\n"
            f"- supported: {', '.join(k for k, e in m.items() if e['verdict'] == 'ok')}\n"
            f"- supported with a workaround (works, but costs extra steps): {group('workaround')}\n"
            f"- NOT supported (list it under `unsupported`): {group('blocked')}\n"
            f"- out of scope, never wanted (list it under `unsupported`): {group('excluded')}\n"
            "Where the source rules say a choice is made simultaneously, use `poll`, not `ask`: with `ask` a later "
            "player hears the earlier answer.\n\n" + ENGINE_OVERVIEW + "\n\n" + PLAYER_COUNT_GUIDE)


def problems(spec: dict) -> list[str]:
    """What is wrong with a spec, in words a model can act on."""
    out = [f"missing key {k!r}" for k in KEYS if k not in spec]
    if out:
        return out
    pl = spec["players"]
    if not (isinstance(pl, dict) and isinstance(pl.get("min"), int) and isinstance(pl.get("max"), int) and 1 <= pl["min"] <= pl["max"]):
        out.append("players must be {\"min\": n, \"max\": n, \"suggested\": n} with 1 <= min <= max")
    elif "suggested" in pl and not (isinstance(pl["suggested"], int) and pl["min"] <= pl["suggested"] <= pl["max"]):
        out.append(f"players.suggested must be a whole number from {pl['min']} to {pl['max']}")
    if not isinstance(spec["parameters"], dict) or not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in spec["parameters"].values()):
        out.append("parameters must map each name to a number")
    attrs = spec["attributes"]
    if not (isinstance(attrs, dict) and set(attrs) == {"player", "game"}):
        out.append("attributes must have exactly the keys 'player' and 'game'")
    else:
        for scope in ("player", "game"):
            for a in attrs[scope]:
                if isinstance(a, dict) and "observable" in a and not isinstance(a["observable"], bool):
                    out.append(f"attribute {a.get('key')!r}: observable must be true or false")
                if not isinstance(a, dict) or not a.get("key"):
                    out.append(f"an attribute in {scope!r} has no key")
                elif a.get("visible") not in VISIBILITY:
                    out.append(f"attribute {a['key']!r}: visible must be one of {', '.join(VISIBILITY)}")
                elif scope == "player" and a["visible"] == "none":
                    out.append(f"player attribute {a['key']!r}: a player's attribute is never `none`; use `ally` for the owner's own hidden state")
    if not isinstance(spec["round"], list) or not spec["round"]:
        out.append("round must be a non-empty list of steps")
    else:
        for i, step in enumerate(spec["round"]):
            if not isinstance(step, dict) or step.get("action") not in ACTIONS:
                out.append(f"round step {i + 1}: action must be one of {', '.join(ACTIONS)}")
            elif step.get("judged") is not None and not (isinstance(step["judged"], str) and step["judged"].strip()):
                out.append(f"round step {i + 1}: judged must be one non-empty sentence")
    end = spec["ending"]
    if not (isinstance(end, dict) and end.get("condition")):
        out.append("ending needs a condition")
    if not (isinstance(end, dict) and isinstance(end.get("rank_by"), str) and end["rank_by"].strip()):
        out.append("ending needs a rank_by: one expression over `you.<attribute>` worked out for every player; the highest wins")
    bar = end.get("min_to_win") if isinstance(end, dict) else None
    if isinstance(end, dict) and "min_to_win" in end and not (
            (isinstance(bar, (int, float)) and not isinstance(bar, bool)) or (isinstance(bar, str) and bar.strip())):
        out.append("ending min_to_win, when given, is a number or an expression over table attributes")
    rules = spec.get("rules")
    if rules is not None:
        ids = [r.get("id") for r in rules if isinstance(r, dict)] if isinstance(rules, list) else []
        if not (isinstance(rules, list) and all(isinstance(r, dict) and str(r.get("id", "")).strip() and str(r.get("text", "")).strip() for r in rules)):
            out.append('rules must be a list of {"id": "R1", "text": "..."} with both filled in')
        elif len(set(ids)) != len(ids):
            out.append("rules: each id must be used once")
    offers = spec.get("offers")
    if offers is not None and not (isinstance(offers, list) and all(isinstance(o, dict) and all(str(o.get(k, "")).strip() for k in ("question", "who", "options")) for o in offers)):
        out.append('offers must be a list of {"question", "who", "options"} with all three filled in')
    for k in ("choices", "simplifications", "unsupported"):
        if not isinstance(spec[k], list):
            out.append(f"{k} must be a list")
    for k in ("choices", "simplifications"):
        for i, item in enumerate(spec[k] if isinstance(spec[k], list) else []):
            if not (isinstance(item, str) and item.strip()) and not (isinstance(item, dict) and str(item.get("what", "")).strip() and str(item.get("why", "")).strip()):
                out.append(f"{k}[{i + 1}] must be {{\"what\": ..., \"why\": ...}} with both filled in")
    return out


def write_spec(completion: Completion, record: dict, repairs: int = 2) -> tuple[dict | None, str]:
    """Ask a model for the spec of one inventory game. Returns (spec, error).

    A reply that is not a valid spec goes back with the reasons, up to `repairs`
    times. The error is empty when a spec came back.
    """
    chosen = record.get("players_suggested")
    prompt = (f"Game: {record['name']}\n"
              f"Players in the source: {record['players_min']} to {record['players_max']}\n"
              + (f"Suggested table size, chosen by the designer of these rules (keep it): {chosen}\n" if chosen else "")
              + f"\nRules, as filed in the inventory:\n{record['rules_text']}")
    base, error, reply = prompt, "", ""
    system = system_with_engine_facts()
    for _ in range(repairs + 1):
        try:
            reply = completion.complete(prompt, system=system)
            spec = first_json(reply)
            found = problems(spec)
        except ValueError as exc:
            spec, found = None, [str(exc)]
        except Exception as exc:  # noqa: BLE001 - a backend that is down is not a bad spec
            return None, f"the model call failed: {str(exc)[:200]}"
        if not found:
            return spec, ""
        error = "; ".join(found)
        prompt = refused(base, reply, error)
    return None, error


def render(spec: dict) -> str:
    """The spec as a page a person can review."""
    out = [f"# {spec['name']}", "", spec["summary"], "",
           f"Players: {spec['players']['min']} to {spec['players']['max']}, best with {spec['players'].get('suggested', spec['players']['min'])}", "", "## Parameters", ""]
    out += [f"- `{k}` = {v}" for k, v in spec["parameters"].items()]
    out += ["", "## Round", ""]
    out += [f"{i}. **{s['action']}** ({s.get('who', '')}): {s.get('effect', '')}" + (f' (judged: "{s["judged"]}")' if s.get("judged") else "")
            for i, s in enumerate(spec["round"], 1)]
    out += ["", "## Ending", "", f"- ends when: {spec['ending']['condition']}",
            f"- ranked by: `{spec['ending']['rank_by']}` (the highest wins; players level at the top share the win)"]
    if "min_to_win" in spec["ending"]:
        out += [f"- min_to_win: `{spec['ending']['min_to_win']}` (a player below it cannot win; if none reaches it, nobody wins)"]
    out += [f"- decided by: {spec['ending'].get('decided_by', '')}"]
    for title, key in (("Choices the source did not make", "choices"), ("Simplifications", "simplifications"),
                       ("Unsupported (needs engine work)", "unsupported")):
        out += ["", f"## {title}", ""]
        items = spec[key]
        out += [f"- {i.get('what', i)}: {i.get('why', '')}" if isinstance(i, dict) else f"- {i}" for i in items] or ["- none"]
    return "\n".join(out) + "\n"


def script(spec: dict) -> str:
    """The spec as a script in plain language: what the game is, what state it keeps, how it starts, what happens in each step, and how it ends.

    This is what the coder converts into the game file, so every piece of state the rules need is named here, hidden ones included.
    """
    out = [f"GAME: {spec['name']} ({spec['players']['min']} to {spec['players']['max']} players, best with {spec['players'].get('suggested', spec['players']['min'])})", "", spec["summary"], "",
           "STATE (every item below must exist in the file):"]
    for scope, label in (("player", "each player"), ("game", "the table")):
        for a in spec["attributes"][scope]:
            who = {"public": "everyone sees it", "ally": "only its owner sees it", "others": "everyone but its owner sees it",
                   "none": "hidden from all players"}.get(a.get("visible"), a.get("visible", ""))
            start = f", starts {a['initial']!r}" if a.get("initial") is not None else ""
            out.append(f"  - {label}: {a['key']} ({a.get('type', 'number')}{start}); {who}. {a.get('meaning', '')}")
    out += ["  - parameters, each kept as a table attribute: " + ", ".join(f"{k} = {v}" for k, v in spec["parameters"].items()), "",
            "INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):"]
    out += [f"  {i}. {t}" for i, t in enumerate(spec["setup"], 1)]
    out += ["", "EACH ROUND (steps in order; the round repeats until an ending):"]
    for i, st in enumerate(spec["round"], 1):
        out.append(f"  {i}. [{st['action']}] {st.get('who', '')}" + (f" answers: {st['answer']}" if st.get("answer") else "") + f". What happens: {st.get('effect', '')}"
                   + (f' JUDGED: a referee rules true or false on "{st["judged"]}"; write this step\'s `when` as {{"prose": that sentence, verbatim}}.'
                      if st.get("judged") else ""))
    if spec.get("rules"):
        out += ["", "RULES (each is tested by an independent scenario; the game must play every one exactly):"]
        out += [f"  {r['id']}. {r['text']}" for r in spec["rules"]]
    if spec.get("offers"):
        out += ["", "OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):"]
        out += [f"  - {o['question']} | asked: {o['who']} | options: {o['options']}" for o in spec["offers"]]
    end = spec["ending"]
    out += ["", "EVALUATION (how the game ends and who wins; decided by calculation):",
            f"  - the game ends when: {end['condition']}",
            f"  - each player's standing: {end['rank_by']} (worked out for every player, `you` being that player; the highest "
            "wins and players level at the top share the win)"]
    if "min_to_win" in end:
        out += [f"  - min_to_win: {end['min_to_win']} (a player whose standing is below it cannot win; if none reaches it, the "
                "match ends with no winner)"]
    out += [f"  - how the result is decided: {end.get('decided_by', '')}",
            "  - the end screen states the final scores or deciding figures, and a short model-written summary of how the game went"]
    return "\n".join(out) + "\n"


def dumps(spec: dict) -> str:
    return json.dumps(spec, indent=2) + "\n"


def observable(spec: dict) -> dict[str, list[str]]:
    """The attributes tests may assert on: those marked observable (all of them in a spec that does not say)."""
    return {scope: [a["key"] for a in spec["attributes"][scope] if a.get("observable", True)] for scope in ("player", "game")}
