# Task: write the XColos game file for "Air, Land and Sea: Three Fronts"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

DECK. There are 18 cards. Each has a theater (Air, Land or Sea) and a strength from 1 to 6, giving exactly one card of each strength per theater (Air 1-6, Land 1-6, Sea 1-6). Both players know the full deck list.

MATCH STRUCTURE. The match lasts at most 36 rounds. It is a sequence of battles, and each battle lasts up to 6 battle rounds. Battle round 1 of the first battle is match round 1. When a battle ends, the next battle begins in the next match round, but only if at least 6 match rounds remain (the next round is 31 or earlier). Otherwise the match ends.

START OF A BATTLE (battle round 1 only). Shuffle all 18 cards. Deal 6 privately to each player; this is the round's one random draw. The remaining 6 stay unseen for this battle. Each player's hand is shown to them in the order dealt. Both players' strength in each theater is set to 0.

EACH BATTLE ROUND, in order:
1. WITHDRAW DECISION (simultaneous). Each player secretly chooses 'Fight' or 'Withdraw'.
   - If exactly one player withdraws in battle round k, the other player gains 2 + floor((k-1)/2) VP. That is 2 VP in rounds 1-2, 3 VP in rounds 3-4 and 4 VP in rounds 5-6. The battle ends immediately.
   - If both withdraw, nobody scores and the battle ends.
2. CARD CHOICE (simultaneous). Each player secretly picks one card from their hand.
3. THEATER CHOICE (simultaneous). Each player secretly names Air, Land or Sea.
4. PLACEMENT. Each chosen card leaves its owner's hand and is placed on its owner's side in the named theater.
   - If the named theater matches the card's own theater, the card is face-up and adds its printed strength.
   - Otherwise it is face-down and adds exactly 3 strength.
5. REVEAL. Both players are told every new placement. Face-up cards show their identity. A face-down card is shown only as 'face-down card (strength 3) in [theater]'. All six theater strengths are announced.
6. If this was battle round 6 (both hands empty), the battle is resolved.

RESOLVING A BATTLE.
- In each theater, the player with the higher strength controls it. A tie means nobody controls it.
- The player controlling more theaters wins the battle. If both control the same number, the player with the higher total strength across all three theaters wins.
- If that is also equal, the battle is drawn and nobody scores.
- The winner gains 4 VP, or 6 VP if they control all three theaters.
- All face-down identities are then revealed to both players.

AFTER EACH ROUND, the match ends if either player has 12 or more VP.

How the winner is decided: The first player to reach 12 VP at the end of a round wins. Only one player can score in any battle, so both can never reach 12 together. If the match ends because the round limit allows no further full battle, the player with more VP wins. Equal VP is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Air, Land and Sea: Three Fronts (2 to 2 players, best with 2)

Two commanders fight a series of 6-round battles over three theaters, placing cards face-up or face-down and deciding each round whether to withdraw; the first to 12 VP wins.

STATE (every item below must exist in the file):
  - each player: vp (number, starts 0); everyone sees it. Victory points; the score
  - each player: hand (list, starts []); only its owner sees it. Cards in hand, e.g. 'Air 4', in the order dealt
  - each player: air (number, starts 0); everyone sees it. This player's total strength in Air this battle
  - each player: land (number, starts 0); everyone sees it. This player's total strength in Land this battle
  - each player: sea (number, starts 0); everyone sees it. This player's total strength in Sea this battle
  - each player: faceup_played (list, starts []); everyone sees it. Cards this player has placed face-up this battle, with their theater
  - each player: facedown_played (list, starts []); only its owner sees it. Identities of cards this player has placed face-down this battle, with the theater each was placed in; the opponent sees only 'face-down card (strength 3) in [theater]'
  - each player: withdraw_choice (text, starts ''); only its owner sees it. This round's secret Fight/Withdraw choice
  - each player: card_choice (text, starts ''); only its owner sees it. This round's secret card choice
  - each player: theater_choice (text, starts ''); only its owner sees it. This round's secret theater choice
  - the table: deck (list, starts []); hidden from all players. Undealt cards of the current battle; the 6 left after dealing stay unseen
  - the table: match_round (number, starts 1); everyone sees it. Current match round, 1 to 36
  - the table: battle_round (number, starts 1); everyone sees it. Current round within the battle, 1 to 6
  - the table: battle_over (bool, starts False); everyone sees it. True once the current battle has ended by withdrawal or resolution
  - the table: match_over (bool, starts False); everyone sees it. True when not enough match rounds remain for another full battle
  - parameters, each kept as a table attribute: deck_size = 18, theaters = 3, min_strength = 1, max_strength = 6, hand_size = 6, max_match_rounds = 36, battle_rounds = 6, last_battle_start_round = 31, withdraw_base_vp = 2, facedown_strength = 3, battle_win_vp = 4, sweep_vp = 6, target_vp = 12

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Both players start with 0 vp.
  2. The table sets match_round to 1, battle_round to 1, battle_over to false and match_over to false.
  3. Both players are told the full 18-card deck list: Air 1-6, Land 1-6 and Sea 1-6.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When battle_round == 1: deck is set to all 18 cards; each player's hand, faceup_played and facedown_played are emptied and air, land and sea are set to 0; then 6 random cards are moved from deck to each player's hand (6 draws each). The 6 cards left in deck stay unseen.
  2. [sync] all players. What happens: Each player sees their own hand in the order dealt, their facedown_played, and all public state.
  3. [poll] all players answers: Fight or Withdraw. What happens: Sets withdraw_choice for each player; nobody sees the other's answer until both are in.
  4. [update] all players. What happens: If exactly one player's withdraw_choice is Withdraw, the other player's vp += 2 + floor((battle_round - 1) / 2). If at least one player withdrew, battle_over = true. Both choices are announced.
  5. [poll] all players answers: one card from own hand. What happens: When battle_over is false: sets card_choice for each player; it stays secret until placement.
  6. [poll] all players answers: Air, Land or Sea. What happens: When battle_over is false: sets theater_choice for each player; it stays secret until placement.
  7. [update] all players. What happens: When battle_over is false: card_choice is removed from each player's hand. If its theater equals theater_choice, it is appended to faceup_played and its printed strength is added to that player's attribute for theater_choice (air, land or sea). Otherwise it is appended to facedown_played and 3 is added to that attribute.
  8. [tell] all players. What happens: When battle_over is false: both new placements are announced. A face-up card shows its identity and theater. A face-down card shows only as 'face-down card (strength 3) in [theater]'. All six theater strengths are announced (each player's air, land and sea).
  9. [update] all players. What happens: When battle_round == 6 and battle_over is false: in each theater the player with the higher strength controls it, and a tie means nobody does. The player controlling more theaters wins. If both control the same number, the player with the higher air+land+sea wins. If that is also equal, the battle is drawn and nobody scores. The winner's vp += 6 if they control all 3 theaters, otherwise += 4. battle_over = true.
  10. [tell] all players. What happens: When the battle was just resolved at battle_round 6: the battle result is announced and every card in both players' facedown_played is revealed to both players.
  11. [update] all players. What happens: match_round += 1. If battle_over is true: battle_round = 1 and battle_over = false, and if match_round > 31 then match_over = true. Otherwise battle_round += 1.
  12. [check] all players. What happens: End the game if any player's vp >= 12, or match_over is true, or match_round > 36. Otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a battle starts (battle_round 1), then all 18 cards are shuffled, 6 are dealt into each player's hand, the remaining 6 stay unseen in the deck, and every theater strength is set to 0.
  R2. When each battle round starts, then both players choose Fight or Withdraw simultaneously, and neither sees the other's choice before both are in.
  R3. When exactly one player withdraws in battle round 1 or 2, then the other player gains 2 VP and the battle ends immediately.
  R4. When exactly one player withdraws in battle round 3 or 4, then the other player gains 3 VP and the battle ends immediately.
  R5. When exactly one player withdraws in battle round 5 or 6, then the other player gains 4 VP and the battle ends immediately.
  R6. When both players withdraw, then nobody scores and the battle ends immediately.
  R7. When a battle ends by withdrawal, then no card or theater choice is made that round.
  R8. When both players fight, then each secretly picks one card from their own hand and then secretly names Air, Land or Sea.
  R9. When a card is placed in its own theater, then it is face-up and adds its printed strength (1 to 6) to its owner's strength in that theater.
  R10. When a card is placed in a theater other than its own, then it is face-down and adds exactly 3 strength to its owner's strength in that theater.
  R11. When cards are placed, then each card leaves its owner's hand and both players are told every placement: face-up cards by identity, face-down cards only as 'face-down card (strength 3) in [theater]'. All six theater strengths are announced.
  R12. When battle round 6 is completed without a withdrawal, then in each theater the player with the higher strength controls it, and a tie means nobody controls it.
  R13. When a battle is resolved, then the player controlling more theaters wins the battle.
  R14. When both players control the same number of theaters, then the player with the higher total strength across all three theaters wins the battle.
  R15. When both players also have equal total strength, then the battle is drawn and nobody scores.
  R16. When a player wins a battle controlling fewer than 3 theaters, then they gain 4 VP.
  R17. When a player wins a battle controlling all 3 theaters, then they gain 6 VP.
  R18. When a battle is resolved, then all face-down card identities are revealed to both players.
  R19. When a battle ends and the next match round is 31 or earlier, then a new battle begins in the next match round.
  R20. When a battle ends and the next match round would be 32 or later, then the match ends.
  R21. When any player has 12 or more VP at the end of a round, then the match ends and that player wins.
  R22. When the match ends on the round limit, then the player with more VP wins, and equal VP is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Withdraw decision | asked: both seats, every battle round | options: Fight, Withdraw
  - Card choice | asked: both seats, only when neither player withdrew this round | options: each card currently in that seat's own hand, and nothing else
  - Theater choice | asked: both seats, only when neither player withdrew this round | options: Air, Land, Sea

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: any player's vp >= 12 OR match_over == true OR match_round > 36
  - each player's standing: you.vp (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: A player's standing is their VP. The first player to reach 12 VP wins; only one player can score in a battle, so both cannot reach 12 together. If the match ends on the round limit, the player with more VP wins, and equal VP is a draw (both share the result).
  - the end screen states the final scores or deciding figures, and a short model-written summary of how the game went

## Recipe: a shared deck and hidden hands (tested on the engine)

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

## Pattern: offer each seat only what it may do (tested on the engine)

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

## Rounds and the safety cap

If the script ends when someone wins (the last player standing, a target reached) and not after a set number of rounds, do not add a fixed
round count to the rules. The game file still has a `limits` block: set `limits.rounds` to the generous cap the script gives (the number of
rounds it says a match may run at most) and `limits.rounds_max` to at least that. The ending's `when` holds for the real ending AND when the cap
is reached, and its `rank_by` also ranks the players as the script says at the cap, so a match that hits the cap still ends with a winner.

## The interface the file must use

Independent tests were written against these names and you cannot see them, so use them exactly.

- each player: `vp` (number, visible: public, starts 0): Victory points; the score
- each player: `air` (number, visible: public, starts 0): This player's total strength in Air this battle
- each player: `land` (number, visible: public, starts 0): This player's total strength in Land this battle
- each player: `sea` (number, visible: public, starts 0): This player's total strength in Sea this battle
- the table: `match_round` (number, visible: public, starts 1): Current match round, 1 to 36
- the table: `battle_round` (number, visible: public, starts 1): Current round within the battle, 1 to 6
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 18, theaters = 3, min_strength = 1, max_strength = 6, hand_size = 6, max_match_rounds = 36, battle_rounds = 6, last_battle_start_round = 31, withdraw_base_vp = 2, facedown_strength = 3, battle_win_vp = 4, sweep_vp = 6, target_vp = 12
- the game ends with ONE ending whose `rank_by` is `you.vp`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
- anything else the game needs to keep track of is yours to design: name it as you like.

## How the platform works

The complete file format reference and two example games are in your system prompt. Follow them exactly: every key an
action accepts is listed there, and the loader refuses any other. The outcome must be decided by arithmetic: write ONE
ending, whose `when` is a calc condition and whose `rank_by` is the ranking in the interface below; no `result`, no `winner`, no prose
ending, no `llm` in an ending. Use calc for any rule that is arithmetic. For a spec step marked `judged`, make that step's `when` `{"prose": "<the judged sentence, verbatim>"}`: a referee answers it
true or false at play time. You may add `llm` wording to a tell, sync or update (never an ask or poll, never an outcome branch), but always keep its `text`, which is used when no
model answers. Choices made at the same moment are a `poll`. The end screen announces only the result: the ending's `text` says who won (`{result}`) and the final scores or deciding figures with
placeholders such as `{players[0].score}`, in a line or two, with no retelling of how the game went. End with `rank_by` as both examples do.

- Mistakes the loader has refused before, so avoid them:
  * A PLAYER attribute's `visible` is one of public, ally or others, never `none`. (`none` is only for table
    attributes.) For something only its owner should see, use `ally`.
  * A `poll` step has no `each` key, and no key the format reference does not list for `poll`. `each` belongs to `ask`.
  * Do not write a `deal` block unless it has the `into` it requires. Set starting values with `initial` on
    attributes, or with `set` operations in `setup`, instead.
  * Every key must be one the reference lists for that action; a misspelled or invented key is refused.
  * TALK that everyone hears is a `poll` with a free-text answer and `"broadcast": {"to": "all", "text": "Seat {seat} says: {value}"}`
    (or `"broadcast": "all"` with no `text`, which shows each message word for word). A broadcast may use ONLY `{value}` (what that
    player answered), `{seat}` (who) and table attributes: a name bound by `verify` is not set yet, so `{talk_msg}` reaches players as
    the literal braces, and the loader refuses it.
  * WHO answered what (who challenged, who blocked, who raised a hand) is `"store": "attr"` on the `poll` or `ask`, naming a PLAYER
    attribute declared under `attributes.player` (a `text` attribute for a choice). Each player's own answer is written to it and a calc reads
    them all: `count(p.said == 'Challenge' for p in players)`, `min([p.seat for p in players if p.said == 'Challenge'])`. A `verify`
    tally gives ONE winning value and loses who gave which: one "Challenge" against three "Pass" tallies to "Pass". Never write a seat
    number into a calc by guessing (`2 if active_seat == 1 else 1`); read it from a stored answer. Reset the stored attribute with a `set`
    to `""` (`players: "all"`) before each poll, so last round's answers do not count.
  * `meta.players` carries `min`, `max` and `suggested`, exactly as the task gives them: the console fills a table to the suggested size and the real-model tests play at it.
  * THE RULES TEXT SAYS BOTH OUTCOMES. For every decision point (a challenge, a block, a claim, a cost), say what happens when it is true AND when it is false,
    and whether the action still goes ahead; a player decides on this text and nothing else, and a check compares it with each numbered rule.
  * THE RULES TEXT PLAYERS READ IS THE DESIGN'S. `meta.rules` (the brief) says each mechanic in the design's own words and in its order: how a challenge is resolved,
    what a block costs, who counts when several answer. Do not paraphrase a mechanic: a reordered sentence is a different rule.
  * BOOKKEEPING IS HIDDEN. An attribute that only the game's own steps read (a scratch value, a counter, a copy of an option list, who is blocking) is declared
    hidden (`none` on the table, `ally` on a player), not `public`: every public attribute is printed into every player's prompt on every turn.
  * THE DEAL REMOVES WHAT IT DEALS. Every card put into a hand is taken out of the deck in the same step (see the deck recipe); after setup, deck plus hands holds
    exactly the cards the rules start with, and no card appears more often than the rules say.
  * OFFER ONLY WHAT A SEAT MAY DO. Build each seat's option list from its own state (see the offer pattern) and never refuse an answer afterwards
    and ask again: an option that is offered, taken and then taken back fails the pipeline's check.
  * A QUESTION WITH ONE POSSIBLE ANSWER IS NEVER WORTH ASKING ("pass" and nothing else): the engine answers it itself, but write the step so
    it is not asked at all, and never announce a seat's answer when the seat was not asked (eliminated players).
  * ASK ONLY WHAT IS NEEDED. Put a `when` on a question that applies only sometimes: a target is asked only for the actions that take one
    (`"when": {"calc": "chosen_action in ['Steal', 'Assassinate', 'Coup']"}`), a block only when something can be blocked.
  * A counter must not go below what the rules allow. Guard every payment and loss with an `if` (`"if": {"calc": "you.coins >= cost"}`,
    or check it before the action is allowed), and treat an action the player cannot afford as the cheapest legal one, as the rules say.
  * An answer to an `ask` or a `poll` exists ONLY if the step binds it with `verify: {"bind": "name"}`; a later `update`
    stores it with `"value": "$name"` (see the `rps` example, `card1`). A step that asks and binds nothing throws the
    answers away, and every score that depends on them stays at its starting value.
  * An attribute declared `"mutable": false` is set once, by an `initialize` step, and any other step that sets it crashes the game
    ("declared static and has already been dealt"). To set a hidden type or a starting value at setup, either use an `initialize`
    step or leave the attribute mutable.
  * Do not write steps that do nothing (for example an `if` of `{"calc": "False"}`), or two polls where one will do.
  * Reply with one complete JSON object: double-quoted keys and strings, no comments, no trailing commas. WRITE IT INDENTED,
    two spaces per level and one key per line, so you can see the nesting and count the brackets; do not put it on one line.
- Keep a round to at most 20 steps. Put several operations in one `update`'s `do` list, and use one `tell` for the
  reveal. A game with more steps than that is flagged as too large in the report, however well it plays, and `verify` tells you the count.

## A pattern that works (this complete game is tested: it loads, ends, and every attribute it declares is updated)

For "each player chooses in private, then the choices decide the score":
1. One `ask` per seat, addressed with `{"where": "you.seat == N"}`, with `"verify": {"bind": "aN"}`. The answer exists only because it is bound.
2. One `update` after both. It `set`s the bound answers into table attributes with `"$aN"`, and `adjust`s each player's score with a
   `calc` that may use `$aN` and `if ... else`.
3. A `check` with `when` and `against`, and ONE ending in `end` whose `rank_by` is `you.score`: the engine ranks the players by it.
Every attribute is set by a step that runs. Adapt this; do not invent another way to store answers.

```json
{
  "schema": 1,
  "meta": {
    "id": "match_or_miss",
    "name": "Match or Miss",
    "players": {
      "min": 2,
      "max": 2
    },
    "blurb": "Two players choose A or B in secret; seat 1 scores when they match, seat 2 when they differ."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "rounds_left",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "last_a1",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_a2",
        "visible": "public",
        "type": "text",
        "initial": ""
      }
    ]
  },
  "rules": "Three rounds. Each round both players secretly choose A or B. If the choices match, seat 1 scores a point; if they differ, seat 2 does. The higher score wins.",
  "setup": [
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "ask",
      "label": "seat 1 chooses",
      "to": {
        "where": "you.seat == 1"
      },
      "answer": {
        "type": "choice",
        "options": [
          "A",
          "B"
        ]
      },
      "verify": {
        "bind": "a1"
      },
      "text": "Choose A or B. Your opponent will not see it."
    },
    {
      "use": "ask",
      "label": "seat 2 chooses",
      "to": {
        "where": "you.seat == 2"
      },
      "answer": {
        "type": "choice",
        "options": [
          "A",
          "B"
        ]
      },
      "verify": {
        "bind": "a2"
      },
      "text": "Choose A or B. Your opponent will not see it."
    },
    {
      "use": "update",
      "label": "score the round",
      "do": [
        {
          "set": {
            "key": "last_a1",
            "value": "$a1"
          }
        },
        {
          "set": {
            "key": "last_a2",
            "value": "$a2"
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "score",
            "value": {
              "calc": "1 if $a1 == $a2 else 0"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "score",
            "value": {
              "calc": "0 if $a1 == $a2 else 1"
            }
          }
        },
        {
          "adjust": {
            "key": "rounds_left",
            "value": -1
          }
        }
      ],
      "text": "Seat 1 chose {last_a1}, seat 2 chose {last_a2}."
    },
    {
      "use": "check",
      "label": "is it over",
      "when": {
        "calc": "rounds_left <= 0"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "rounds_left <= 0"
      },
      "rank_by": "you.score",
      "text": "{result} wins."
    }
  }
}
```

Your file is checked by the platform's loader, a rule that the outcome is arithmetic, random play, a check that every
attribute is actually updated, and tests written independently from the rules. If it is refused you will be told why and
shown your file again; fix what is wrong and keep the rest.
