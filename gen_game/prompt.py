"""The prompt a coding agent is given to write one game file.

Everything the agent needs and nothing it should not have: the game's final rules, the interface
the file must use, where the platform's file format is documented, what the loader has refused
before, the one file to write, and the command that tells it whether it is done. The designer never
sees the file format; this is the first place it appears.
"""

from __future__ import annotations

from pathlib import Path

from gen_game import complexity
from gen_game import spec as specmod
from gen_game.encode import MISTAKES, REFERENCES

ROOT = Path(__file__).resolve().parent.parent
RECIPE_FILE = Path(__file__).resolve().parent / "recipes" / "match_or_miss.json"


def recipe() -> str:
    """The tested pattern for "each player chooses in private, then the choices decide the score", with the game itself.

    Coders kept declaring attributes and scoring steps that never took effect, because they did not know how an answer reaches
    the state. This complete game passes every check the pipeline applies (a test keeps it that way), so it is shown whole.
    """
    return f"""## A pattern that works (this complete game is tested: it loads, ends, and every attribute it declares is updated)

For "each player chooses in private, then the choices decide the score":
1. One `ask` per seat, addressed with `{{"where": "you.seat == N"}}`, with `"verify": {{"bind": "aN"}}`. The answer exists only because it is bound.
2. One `update` after both. It `set`s the bound answers into table attributes with `"$aN"`, and `adjust`s each player's score with a
   `calc` that may use `$aN` and `if ... else`.
3. A `check` with `when` and `against`, and ONE ending in `end` whose `rank_by` is `you.score`: the engine ranks the players by it.
Every attribute is set by a step that runs. Adapt this; do not invent another way to store answers.

```json
{RECIPE_FILE.read_text().strip()}
```
"""


def interface(spec: dict) -> str:
    """The names the file must use: what an outside observer reads, which the independent tests are written against.

    Everything else (counters, scratch values, codes) is the coder's own design, and is left out on purpose: listing the
    spec writer's bookkeeping made coders clone it and made the tests depend on it.
    """
    out = []
    for scope, label in (("player", "each player"), ("game", "the table")):
        for a in spec["attributes"][scope]:
            if a.get("observable", True):
                out.append(f"- {label}: `{a['key']}` ({a.get('type', 'number')}, visible: {a.get('visible')}, starts {a.get('initial')!r}): {a.get('meaning', '')}")
    out.append("- parameters (each must be an attribute holding this value, never a number buried in a step): "
               + ", ".join(f"{k} = {v}" for k, v in spec["parameters"].items()))
    out.append(f"- the game ends with ONE ending whose `rank_by` is `{spec['ending']['rank_by']}`: worked out for every player (`you` is that "
               "player), the highest wins and players level at the top share the win")
    if "min_to_win" in spec["ending"]:
        out.append(f"- that ending's `min_to_win` is `{spec['ending']['min_to_win']}`: a player below it cannot win, and if nobody reaches it "
                   "the match ends with no winner")
    out.append("- anything else the game needs to keep track of is yours to design: name it as you like.")
    return "\n".join(out)



DECK_RECIPE = """## Recipe: a shared deck and hidden hands (tested on the engine)

When the script has a deck and hands, both must exist as attributes, and setup must really deal. Declare the hand as a PLAYER attribute
`{"key": "hand", "visible": "ally", "type": "list", "initial": []}` (only its owner sees it; a player attribute is never `none`) and the
deck as a TABLE attribute `{"key": "deck", "visible": "none", "type": "list", "initial": [every card, one entry per copy]}`, plus a table text
attribute `pick` (visible `none`, initial `""`) to hold the card just drawn. Then ONE draw, of a random card into seat N's hand, is three operations
in an `update`'s `do` list, in this order:

  {"set":    {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
  {"append": {"player": N, "key": "hand", "value": {"calc": "pick"}}},
  {"remove": {"key": "deck", "value": {"calc": "pick"}}}

Dealing two cards to three seats is that block repeated twice for each seat (6 draws), never a fixed list written into `initial`: the deal
is random and different each match, and every player's hand must differ. A card coming back is `{"append": {"key": "deck", ...}}` and
`{"remove": {"player": N, "key": "hand", ...}}`. "Has a card of role R" is `"R" in you.hand`. Use `{"if": {"calc": ...}}` on an operation to make
it conditional. Never declare `hand` or `deck` and then leave them unchanged: the rules would then claim cards that do not exist.
"""

PATTERNS = """## Pattern: offer each seat only what it may do (tested on the engine)

A question's options may come from state, and the state can differ for every player. So make who may do what part of the OFFER, never a check
afterwards. Declare a PLAYER list attribute (say `offer`, visible `ally`), and set it for everyone in one `update` just before the question,
from each player's own attributes and the table's:

  {"set": {"players": "all", "key": "offer",
           "value": {"calc": "['wait'] + (['buy'] if you.coins >= price else []) + (['block'] if you.seat == target else [])"}}}

then ask with `"answer": {"type": "choice", "options": {"attribute": "offer"}}` and `to` naming who is asked. `you` is each player in turn, and a
list can be built with `+` and `(... if ... else [])`. Whatever a seat may not do is not in its list: a seat that cannot pay is not offered the
paid action, only the target of an action is offered a block against it, a player already out is not asked. Do the same for a target: put the
legal seats in a list attribute.

When a player is eliminated, set the PLATFORM status as well as your own counters: declare a status for it (`{"id": "out", "acts": false}`) next to `playing` and
run `{"set_status": {"player": N, "to": "out", "text": "Seat {player} is out."}}`. Without it the platform and the console show the player as still in the game, and the
prompts list them as playing, whatever your own `alive` attribute says. Name the cards it reveals in the same announcement.

Do NOT offer a broad list and then refuse illegal answers and ask again (a `repeat` that asks, checks, and asks again, or an update that removes
an option the player just picked). It costs a model call, it lets a model choose something illegal, and the pipeline reports it as a failure:
"an option is offered and then refused". If you find yourself writing a step called "refuse...", "check the answer is legal" or "not allowed",
you are filling the wrong list: fix the offer.
"""


def build(game_id: str, plan: dict, spec: dict, guidance: str = "", agent: bool = True) -> str:
    """The prompt the coder is given, for a coding agent (`agent=True`) or a model answering in one reply.

    Both get the same game, interface and rules. They differ only in how the platform's API reaches them.
    An agent is told where `design/actions.md` and the examples are, and how to run `verify`. A model in a
    reply cannot read files, so the format reference and the examples are put in front of it as its system
    prompt (`encode.system_prompt()`), and this message says so.
    """
    v = plan["variation"]
    folder = f"gen_game/data/games/{game_id}"
    examples = "\n".join(f"  * xcolos/games/library/{r}.json" for r in REFERENCES)
    if agent:
        how = f"""## How the platform works

- The complete file format is documented in `design/actions.md`. Read all of it: every key an action accepts is listed there,
  and the loader refuses any other.
- Complete example games to imitate, in `xcolos/games/library/`:
{examples}
- The outcome must be decided by arithmetic: write ONE ending, whose `when` is a calc condition and whose `rank_by` is the
  ranking in the interface below, as both examples do; no `result`, no `winner`, no prose ending, no `llm` in an ending. Use
  calc for any rule that is arithmetic. For a spec step marked `judged`, make that step's `when`
  `{{"prose": "<the judged sentence, verbatim>"}}`: a referee answers it true or false at play time. You may add `llm` wording to a
  tell, sync or update (never an ask or poll, never an outcome branch), but always keep its `text`, which is used when no model answers. Choices made at the same moment
  are a `poll`.
- ENDING STATEMENT: the end screen announces the result only: who won (`{{result}}` names the winning seat, or seats when they
  share the win) and the final figures that decided it, using placeholders such as `{{players[0].score}}` and `{{target}}`. Keep it
  to a line or two. Do NOT retell the game, and do NOT use
  `llm` in an ending: no summary of what each player did or of the turning points.

{MISTAKES}
- Keep a round to at most {complexity.LIMITS['steps_per_round']} steps. Put several operations in one `update`'s `do` list, and use one `tell` for the
  reveal. A game with more steps than that is flagged as too large in the report, however well it plays, and `verify` tells you the count.

{recipe()}
## Check your work

Run this from the repository root, and keep fixing `game.json` until it prints `ok` (give up after about 8 attempts and say
what blocks you):

    python3 -m gen_game verify {game_id} game

It runs the loader, checks the outcome is arithmetic, and plays the game with random seats. It tells you the problem when it
fails. Then check that the game plays the RULES in the script:

    python3 -m gen_game verify {game_id} rules

It plays the game through independent scenarios, one per rule, and names each rule that is broken, in its own words, with what it
expected and what the game did. Fix the game until it prints `ok` too. (If it says no scenarios have been written yet, skip it.)
The scenarios are written by someone else from the rules alone, so the rules list is your checklist: read it, and do not guess.

Do NOT read `{folder}/scenarios.json` or anything under `{folder}/history/`, and do not edit code. When you are done, write
`{folder}/encode_notes.md`: where the rules were ambiguous or the platform could not do what they ask, and what you chose.
If the platform genuinely cannot express something the rules REQUIRE, say so there plainly instead of faking it.
"""
        task = f"""You are a coding agent working in the repository at {ROOT}. Write ONE file, `{folder}/game.json`: the game
below as a game definition for the XColos engine. Do not write any other file except `{folder}/encode_notes.md`."""
    else:
        how = f"""## How the platform works

The complete file format reference and two example games are in your system prompt. Follow them exactly: every key an
action accepts is listed there, and the loader refuses any other. The outcome must be decided by arithmetic: write ONE
ending, whose `when` is a calc condition and whose `rank_by` is the ranking in the interface below; no `result`, no `winner`, no prose
ending, no `llm` in an ending. Use calc for any rule that is arithmetic. For a spec step marked `judged`, make that step's `when` `{{"prose": "<the judged sentence, verbatim>"}}`: a referee answers it
true or false at play time. You may add `llm` wording to a tell, sync or update (never an ask or poll, never an outcome branch), but always keep its `text`, which is used when no
model answers. Choices made at the same moment are a `poll`. The end screen announces only the result: the ending's `text` says who won (`{{result}}`) and the final scores or deciding figures with
placeholders such as `{{players[0].score}}`, in a line or two, with no retelling of how the game went. End with `rank_by` as both examples do.

{MISTAKES}
- Keep a round to at most {complexity.LIMITS['steps_per_round']} steps. Put several operations in one `update`'s `do` list, and use one `tell` for the
  reveal. A game with more steps than that is flagged as too large in the report, however well it plays, and `verify` tells you the count.

{recipe()}
Your file is checked by the platform's loader, a rule that the outcome is arithmetic, random play, a check that every
attribute is actually updated, and tests written independently from the rules. If it is refused you will be told why and
shown your file again; fix what is wrong and keep the rest.
"""
        task = "Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else."
    text = f"""# Task: write the XColos game file for "{v['name']}"

{task}

## The game

Players: {v['players']['min']} to {v['players']['max']}; set `meta.players` to {{"min": {spec['players']['min']}, "max": {spec['players']['max']}, "suggested": {spec['players'].get('suggested', spec['players']['min'])}}} (the suggested size is the one the game plays best at).

{v['rules']}

How the winner is decided: {v['objective']}

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

{specmod.script(spec)}
{DECK_RECIPE}
{PATTERNS}
## Rounds and the safety cap

If the script ends when someone wins (the last player standing, a target reached) and not after a set number of rounds, do not add a fixed
round count to the rules. The game file still has a `limits` block: set `limits.rounds` to the generous cap the script gives (the number of
rounds it says a match may run at most) and `limits.rounds_max` to at least that. The ending's `when` holds for the real ending AND when the cap
is reached, and its `rank_by` also ranks the players as the script says at the cap, so a match that hits the cap still ends with a winner.

## The interface the file must use

Independent tests were written against these names and you cannot see them, so use them exactly.

{interface(spec)}

{how}"""
    if guidance:
        text += f"\n## Guidance from the last attempt\n\nThe previous attempt had problems:\n\n{guidance}\n"
    return text
