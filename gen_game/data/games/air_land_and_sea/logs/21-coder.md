# 21 coder

- time: 2026-10-27T17:50:35+00:00 (136.0s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 3001f26e87ecd004, reply sha256 ab13559f8f5e19fd

## Sent

````
# Task: write the XColos game file for "Air, Land and Sea: Four Battles"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. There are 18 cards: Air 1–6, Land 1–6 and Sea 1–6. A card's strength is its number.

MATCH. The match has 24 rounds, grouped into 4 battles of 6 rounds:
- Battle 1 is rounds 1–6.
- Battle 2 is rounds 7–12.
- Battle 3 is rounds 13–18.
- Battle 4 is rounds 19–24.

START OF EVERY ROUND (bookkeeping, no choices).
- Set battle = floor((round−1)/6)+1.
- Set round_in_battle = round − 6×(battle−1).
- Set first player = seat 1 if battle is 1 or 3, seat 2 if battle is 2 or 4.
- These values come only from the round number. Nothing else changes them.

BATTLE START (only when round_in_battle = 1).
- Set battle_over to false.
- Reset every player's Air, Land and Sea strength to 0 and clear all played cards.
- Shuffle all 18 cards.
- Deal 6 privately to each player's hand.
- Put the remaining 6 aside unseen. They are out of play for this battle.
- This is the only random event in a round.

ACTIONS. If battle_over is false, the first player takes one action. Then, if battle_over is still false, the second player takes one action. An action is exactly one of:
(a) DEPLOY: play a card from your hand face-up to the theater named on it. Add its number to your strength there.
(b) IMPROVISE: play a card from your hand face-down to any theater. Add 2 to your strength there. The opponent sees only the theater and the +2, not the card.
(c) WITHDRAW: concede the battle.

All theater strengths and face-up cards are public. Hands, the set-aside cards and the identity of face-down cards are hidden.

WITHDRAWAL.
- When a player withdraws, count the cards left in their hand.
- The opponent immediately gains VP as follows: 4 or more cards gives 2 VP; 2 or 3 cards gives 3 VP; 1 card gives 4 VP.
- battle_over becomes true at once.
- If the first player withdrew, the second player does not act that round.
- Every remaining round of the battle passes with no actions and no scoring.
- The next battle starts at its fixed round as usual.

BATTLE END (only when round_in_battle = 6 and battle_over is false, after both actions).
- Both hands are now empty.
- In each theater, the player with the higher strength controls it. A tie goes to that battle's first player.
- The player who controls 2 or more theaters wins the battle and gains 6 VP.
- Set battle_over to true.

END.
- After round 24 the game ends.

How the winner is decided: After round 24, the player with more VP wins. Equal VP is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Air, Land and Sea: Four Battles (2 to 2 players, best with 2)

Two commanders fight 4 battles of 6 rounds over three theaters, playing cards face-up for their strength or face-down for 2, and may withdraw early to limit the VP the opponent gains.

STATE (every item below must exist in the file):
  - each player: vp (number, starts 0); everyone sees it. victory points earned so far
  - each player: hand (list, starts []); only its owner sees it. cards held this battle, such as 'Air 3'
  - each player: air (number, starts 0); everyone sees it. this player's strength in the Air theater this battle
  - each player: land (number, starts 0); everyone sees it. this player's strength in the Land theater this battle
  - each player: sea (number, starts 0); everyone sees it. this player's strength in the Sea theater this battle
  - each player: face_up (list, starts []); everyone sees it. cards this player deployed face-up this battle
  - each player: face_down (list, starts []); only its owner sees it. identities of cards this player improvised face-down this battle, with their theater; the opponent sees only the +2 in that theater's strength
  - the table: round (number, starts 1); everyone sees it. current round, 1 to 24
  - the table: battle (number, starts 1); everyone sees it. current battle, floor((round-1)/6)+1
  - the table: round_in_battle (number, starts 1); everyone sees it. round - 6*(battle-1)
  - the table: first_seat (number, starts 1); everyone sees it. first player: seat 1 in battles 1 and 3, seat 2 in battles 2 and 4
  - the table: battle_over (bool, starts False); everyone sees it. true once the current battle has been decided by withdrawal or by the battle end
  - the table: deck (list, starts ['Air 1', 'Air 2', 'Air 3', 'Air 4', 'Air 5', 'Air 6', 'Land 1', 'Land 2', 'Land 3', 'Land 4', 'Land 5', 'Land 6', 'Sea 1', 'Sea 2', 'Sea 3', 'Sea 4', 'Sea 5', 'Sea 6']); hidden from all players. the 18 cards to be shuffled and dealt at each battle start
  - the table: set_aside (list, starts []); hidden from all players. the 6 undealt cards, out of play this battle
  - parameters, each kept as a table attribute: total_cards = 18, theaters = 3, min_strength = 1, max_strength = 6, total_rounds = 24, battles = 4, rounds_per_battle = 6, hand_size = 6, set_aside_count = 6, improvise_strength = 2, withdraw_vp_4_plus_cards = 2, withdraw_vp_2_or_3_cards = 3, withdraw_vp_1_card = 4, battle_win_vp = 6, theaters_to_win_battle = 2

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat both players. Each player's vp is 0.
  2. round is set to 1 and battle_over to false.
  3. The deck holds all 18 cards: Air 1-6, Land 1-6 and Sea 1-6.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Set battle = floor((round-1)/6)+1. Set round_in_battle = round - 6*(battle-1). Set first_seat = 1 if battle is 1 or 3, and 2 if battle is 2 or 4. Announce the round, the battle and the first player.
  2. [update] all players. What happens: Only when round_in_battle = 1 (battle start): set battle_over = false. Set every player's air, land and sea to 0. Return every card in each hand, face_up, face_down and set_aside to deck, so deck holds all 18 cards. Draw 6 cards at random from deck into each player's hand, removing each from deck. Move the remaining 6 deck cards to set_aside.
  3. [sync] all players. What happens: Each player privately sees their own hand and face_down, plus every public attribute: all air, land and sea strengths, all face_up cards, vp, round, battle, first_seat and battle_over.
  4. [ask] the seat named by first_seat, only when battle_over is false answers: one choice: 'deploy <card>' for a card in hand, 'improvise <card> to <Air|Land|Sea>' for a card in hand and any theater, or 'withdraw'. What happens: Deploy: remove the card from hand, append it to face_up, and add its number to the player's strength in the theater named on the card. Improvise: remove the card from hand, append it with the chosen theater to face_down, and add 2 to the player's strength in the chosen theater; only the theater and the +2 are announced. Withdraw: let n = length of the player's hand; the opponent's vp += 4 if n = 1, 3 if n is 2 or 3, and 2 if n >= 4; set battle_over = true.
  5. [ask] the seat that is not first_seat, only when battle_over is false answers: one choice: 'deploy <card>' for a card in hand, 'improvise <card> to <Air|Land|Sea>' for a card in hand and any theater, or 'withdraw'. What happens: Same effects as the first player's action, applied to this player.
  6. [update] all players. What happens: Only when round_in_battle = 6 and battle_over is false (battle end): in each of air, land and sea, the player with the higher strength controls that theater, and a tie goes to the first_seat player. The player who controls 2 or more theaters gains vp += 6. Set battle_over = true. Announce the strengths and the battle winner.
  7. [check] all players. What happens: If round = 24, end the game. Otherwise continue.
  8. [update] all players. What happens: round += 1.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The deck has 18 cards, Air 1-6, Land 1-6 and Sea 1-6, and a card's strength is its number.
  R2. The match has 24 rounds, and battle = floor((round-1)/6)+1, so rounds 1-6 are battle 1, rounds 7-12 battle 2, rounds 13-18 battle 3 and rounds 19-24 battle 4.
  R3. When the battle is 1 or 3, then seat 1 is the first player; when the battle is 2 or 4, then seat 2 is the first player.
  R4. When round_in_battle = 1, then battle_over becomes false, every air, land and sea strength becomes 0, and all played cards are cleared.
  R5. When round_in_battle = 1, then all 18 cards are shuffled, each player is dealt 6 cards privately into hand, and the remaining 6 go to set_aside, out of play and unseen.
  R6. When battle_over is false, then the first player takes exactly one action, and the second player then takes one action if battle_over is still false.
  R7. When a player deploys a card such as Land 5, then it leaves their hand face-up and their land strength rises by 5.
  R8. When a player improvises a card to a chosen theater, then it leaves their hand face-down and their strength in that theater rises by 2, whatever the card's number or suit.
  R9. When a card is improvised, then the opponent sees only the theater and the +2, never the card's identity.
  R10. When a player withdraws with 4 or more cards in hand, then the opponent gains 2 VP.
  R11. When a player withdraws with 2 or 3 cards in hand, then the opponent gains 3 VP.
  R12. When a player withdraws with 1 card in hand, then the opponent gains 4 VP.
  R13. When a player withdraws, then battle_over becomes true at once, and if the first player withdrew, then the second player does not act that round.
  R14. When battle_over is true, then the remaining rounds of that battle pass with no actions and no scoring, and the next battle starts at its fixed round.
  R15. When round_in_battle = 6 and battle_over is false after both actions, then in each theater the player with the higher strength controls it, and a tie goes to the battle's first player.
  R16. When a player controls 2 or more of the 3 theaters at a battle end, then they gain 6 VP and battle_over becomes true.
  R17. When round 24 ends, then the game ends, the player with more VP wins, and equal VP is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - First player's action (when battle_over is false) | asked: the seat named by first_seat | options: 'deploy <card>' for each card in their hand; 'improvise <card> to Air', 'improvise <card> to Land' and 'improvise <card> to Sea' for each card in their hand; 'withdraw'.
  - Second player's action (when battle_over is still false) | asked: the seat that is not first_seat | options: 'deploy <card>' for each card in their hand; 'improvise <card> to Air', 'improvise <card> to Land' and 'improvise <card> to Sea' for each card in their hand; 'withdraw'. Not asked at all if the first player withdrew this round.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round = 24 after that round's steps have run
  - each player's standing: you.vp (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total VP after round 24. The player with more VP wins. Equal VP is a draw, and both players share the win.
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

- each player: `vp` (number, visible: public, starts 0): victory points earned so far
- each player: `air` (number, visible: public, starts 0): this player's strength in the Air theater this battle
- each player: `land` (number, visible: public, starts 0): this player's strength in the Land theater this battle
- each player: `sea` (number, visible: public, starts 0): this player's strength in the Sea theater this battle
- the table: `round` (number, visible: public, starts 1): current round, 1 to 24
- the table: `battle` (number, visible: public, starts 1): current battle, floor((round-1)/6)+1
- parameters (each must be an attribute holding this value, never a number buried in a step): total_cards = 18, theaters = 3, min_strength = 1, max_strength = 6, total_rounds = 24, battles = 4, rounds_per_battle = 6, hand_size = 6, set_aside_count = 6, improvise_strength = 2, withdraw_vp_4_plus_cards = 2, withdraw_vp_2_or_3_cards = 3, withdraw_vp_1_card = 4, battle_win_vp = 6, theaters_to_win_battle = 2
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

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "air_land_sea_four_battles",
    "name": "Air, Land and Sea: Four Battles",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two commanders fight 4 battles of 6 rounds over Air, Land and Sea, playing cards face-up for strength or face-down for 2, or withdrawing to limit losses."
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
        "key": "vp",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "air",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "land",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sea",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "face_up",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "face_down",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "battle",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_in_battle",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "battle_over",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Air 1",
          "Air 2",
          "Air 3",
          "Air 4",
          "Air 5",
          "Air 6",
          "Land 1",
          "Land 2",
          "Land 3",
          "Land 4",
          "Land 5",
          "Land 6",
          "Sea 1",
          "Sea 2",
          "Sea 3",
          "Sea 4",
          "Sea 5",
          "Sea 6"
        ]
      },
      {
        "key": "all_cards",
        "visible": "none",
        "type": "list",
        "initial": [
          "Air 1",
          "Air 2",
          "Air 3",
          "Air 4",
          "Air 5",
          "Air 6",
          "Land 1",
          "Land 2",
          "Land 3",
          "Land 4",
          "Land 5",
          "Land 6",
          "Sea 1",
          "Sea 2",
          "Sea 3",
          "Sea 4",
          "Sea 5",
          "Sea 6"
        ]
      },
      {
        "key": "set_aside",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "act_kind",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "act_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "act_theater",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "act_gain",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "s1_theaters",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "battle_winner",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_cards",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "theaters",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "min_strength",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_strength",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "battles",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rounds_per_battle",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "set_aside_count",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "improvise_strength",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "withdraw_vp_4_plus_cards",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "withdraw_vp_2_or_3_cards",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "withdraw_vp_1_card",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "battle_win_vp",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "theaters_to_win_battle",
        "visible": "public",
        "type": "number",
        "initial": 2
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "seat the players",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "vp",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "start the clock",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "battle_over",
            "value": false
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "build the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_cards"
            }
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "bookkeeping",
      "label": "the round",
      "do": [
        {
          "set": {
            "key": "battle",
            "value": {
              "calc": "int((round - 1) / rounds_per_battle) + 1"
            }
          }
        },
        {
          "set": {
            "key": "round_in_battle",
            "value": {
              "calc": "round - rounds_per_battle * (battle - 1)"
            }
          }
        },
        {
          "set": {
            "key": "first_seat",
            "value": {
              "calc": "1 if battle in [1, 3] else 2"
            }
          }
        }
      ],
      "text": "Round {round} of {total_rounds}: battle {battle}, round {round_in_battle} of {rounds_per_battle}. First player: seat {first_seat}."
    },
    {
      "use": "update",
      "phase": "battle start",
      "label": "battle start",
      "when": {
        "calc": "round_in_battle == 1"
      },
      "do": [
        {
          "set": {
            "key": "battle_over",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "air",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "land",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "sea",
            "value": 0
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_cards"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "face_up",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "face_down",
            "value": []
          }
        },
        {
          "set": {
            "key": "set_aside",
            "value": []
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "set_aside",
            "value": {
              "calc": "deck"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": []
          }
        }
      ],
      "text": "Battle {battle} begins. All strengths are 0. The {total_cards} cards are shuffled; each player is dealt {hand_size} cards in secret and {set_aside_count} are set aside unseen."
    },
    {
      "use": "sync",
      "phase": "bookkeeping",
      "label": "your state",
      "mode": "self",
      "to": "all",
      "text": "Your state:"
    },
    {
      "use": "update",
      "phase": "actions",
      "label": "the offers",
      "when": {
        "calc": "not battle_over"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['deploy ' + c for c in you.hand] + ['improvise ' + c + ' to Air' for c in you.hand] + ['improvise ' + c + ' to Land' for c in you.hand] + ['improvise ' + c + ' to Sea' for c in you.hand] + ['withdraw']"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "actions",
      "label": "first player acts",
      "when": {
        "calc": "not battle_over"
      },
      "to": {
        "where": "you.seat == first_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "a1"
      },
      "text": "You are the first player this round. Choose one action: 'deploy <card>' plays it face-up to its own theater for its number; 'improvise <card> to <theater>' plays it face-down to any theater for +{improvise_strength}; 'withdraw' concedes the battle (your opponent gains {withdraw_vp_4_plus_cards} VP if you hold 4+ cards, {withdraw_vp_2_or_3_cards} VP if 2 or 3, {withdraw_vp_1_card} VP if 1)."
    },
    {
      "use": "update",
      "phase": "actions",
      "label": "first player's action resolves",
      "when": {
        "calc": "not battle_over"
      },
      "do": [
        {
          "set": {
            "key": "act_kind",
            "value": {
              "calc": "'withdraw' if $a1 == 'withdraw' else ('deploy' if $a1 in ['deploy ' + c for c in players[first_seat - 1].hand] else 'improvise')"
            }
          }
        },
        {
          "set": {
            "key": "act_card",
            "value": {
              "calc": "([c for c in players[first_seat - 1].hand if $a1 in ['deploy ' + c, 'improvise ' + c + ' to Air', 'improvise ' + c + ' to Land', 'improvise ' + c + ' to Sea']] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "act_theater",
            "value": {
              "calc": "(('Air' if act_card[0] == 'A' else ('Land' if act_card[0] == 'L' else 'Sea')) if act_kind == 'deploy' else ('Air' if $a1 == 'improvise ' + act_card + ' to Air' else ('Land' if $a1 == 'improvise ' + act_card + ' to Land' else 'Sea')))"
            },
            "if": {
              "calc": "act_kind != 'withdraw'"
            }
          }
        },
        {
          "set": {
            "key": "act_gain",
            "value": {
              "calc": "int(act_card[-1]) if act_kind == 'deploy' else improvise_strength"
            },
            "if": {
              "calc": "act_kind != 'withdraw'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "3 - first_seat"
            },
            "key": "vp",
            "value": {
              "calc": "withdraw_vp_1_card if len(players[first_seat - 1].hand) == 1 else (withdraw_vp_2_or_3_cards if len(players[first_seat - 1].hand) <= 3 else withdraw_vp_4_plus_cards)"
            },
            "if": {
              "calc": "act_kind == 'withdraw'"
            },
            "text": "Seat {first_seat} withdraws from battle {battle}. Seat {player} gains VP for the withdrawal."
          }
        },
        {
          "set": {
            "key": "battle_over",
            "value": true,
            "if": {
              "calc": "act_kind == 'withdraw'"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "first_seat"
            },
            "key": "hand",
            "value": {
              "calc": "act_card"
            },
            "if": {
              "calc": "act_kind != 'withdraw'"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "first_seat"
            },
            "key": "face_up",
            "value": {
              "calc": "act_card"
            },
            "if": {
              "calc": "act_kind == 'deploy'"
            },
            "text": "Seat {player} deploys {act_card} face-up to {act_theater} (+{act_gain})."
          }
        },
        {
          "append": {
            "player": {
              "calc": "first_seat"
            },
            "key": "face_down",
            "value": {
              "calc": "act_card + ' to ' + act_theater"
            },
            "if": {
              "calc": "act_kind == 'improvise'"
            },
            "text": "Seat {player} improvises a face-down card to {act_theater} (+{improvise_strength})."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "first_seat"
            },
            "key": "air",
            "value": {
              "calc": "act_gain"
            },
            "if": {
              "calc": "act_kind != 'withdraw' and act_theater == 'Air'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "first_seat"
            },
            "key": "land",
            "value": {
              "calc": "act_gain"
            },
            "if": {
              "calc": "act_kind != 'withdraw' and act_theater == 'Land'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "first_seat"
            },
            "key": "sea",
            "value": {
              "calc": "act_gain"
            },
            "if": {
              "calc": "act_kind != 'withdraw' and act_theater == 'Sea'"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "actions",
      "label": "second player acts",
      "when": {
        "calc": "not battle_over"
      },
      "to": {
        "where": "you.seat != first_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "a2"
      },
      "text": "You are the second player this round. Choose one action: 'deploy <card>' plays it face-up to its own theater for its number; 'improvise <card> to <theater>' plays it face-down to any theater for +{improvise_strength}; 'withdraw' concedes the battle (your opponent gains {withdraw_vp_4_plus_cards} VP if you hold 4+ cards, {withdraw_vp_2_or_3_cards} VP if 2 or 3, {withdraw_vp_1_card} VP if 1)."
    },
    {
      "use": "update",
      "phase": "actions",
      "label": "second player's action resolves",
      "when": {
        "calc": "not battle_over"
      },
      "do": [
        {
          "set": {
            "key": "act_kind",
            "value": {
              "calc": "'withdraw' if $a2 == 'withdraw' else ('deploy' if $a2 in ['deploy ' + c for c in players[2 - first_seat].hand] else 'improvise')"
            }
          }
        },
        {
          "set": {
            "key": "act_card",
            "value": {
              "calc": "([c for c in players[2 - first_seat].hand if $a2 in ['deploy ' + c, 'improvise ' + c + ' to Air', 'improvise ' + c + ' to Land', 'improvise ' + c + ' to Sea']] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "act_theater",
            "value": {
              "calc": "(('Air' if act_card[0] == 'A' else ('Land' if act_card[0] == 'L' else 'Sea')) if act_kind == 'deploy' else ('Air' if $a2 == 'improvise ' + act_card + ' to Air' else ('Land' if $a2 == 'improvise ' + act_card + ' to Land' else 'Sea')))"
            },
            "if": {
              "calc": "act_kind != 'withdraw'"
            }
          }
        },
        {
          "set": {
            "key": "act_gain",
            "value": {
              "calc": "int(act_card[-1]) if act_kind == 'deploy' else improvise_strength"
            },
            "if": {
              "calc": "act_kind != 'withdraw'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "first_seat"
            },
            "key": "vp",
            "value": {
              "calc": "withdraw_vp_1_card if len(players[2 - first_seat].hand) == 1 else (withdraw_vp_2_or_3_cards if len(players[2 - first_seat].hand) <= 3 else withdraw_vp_4_plus_cards)"
            },
            "if": {
              "calc": "act_kind == 'withdraw'"
            },
            "text": "The second player withdraws from battle {battle}. Seat {player} gains VP for the withdrawal."
          }
        },
        {
          "set": {
            "key": "battle_over",
            "value": true,
            "if": {
              "calc": "act_kind == 'withdraw'"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "3 - first_seat"
            },
            "key": "hand",
            "value": {
              "calc": "act_card"
            },
            "if": {
              "calc": "act_kind != 'withdraw'"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "3 - first_seat"
            },
            "key": "face_up",
            "value": {
              "calc": "act_card"
            },
            "if": {
              "calc": "act_kind == 'deploy'"
            },
            "text": "Seat {player} deploys {act_card} face-up to {act_theater} (+{act_gain})."
          }
        },
        {
          "append": {
            "player": {
              "calc": "3 - first_seat"
            },
            "key": "face_down",
            "value": {
              "calc": "act_card + ' to ' + act_theater"
            },
            "if": {
              "calc": "act_kind == 'improvise'"
            },
            "text": "Seat {player} improvises a face-down card to {act_theater} (+{improvise_strength})."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "3 - first_seat"
            },
            "key": "air",
            "value": {
              "calc": "act_gain"
            },
            "if": {
              "calc": "act_kind != 'withdraw' and act_theater == 'Air'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "3 - first_seat"
            },
            "key": "land",
            "value": {
              "calc": "act_gain"
            },
            "if": {
              "calc": "act_kind != 'withdraw' and act_theater == 'Land'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "3 - first_seat"
            },
            "key": "sea",
            "value": {
              "calc": "act_gain"
            },
            "if": {
              "calc": "act_kind != 'withdraw' and act_theater == 'Sea'"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "battle end",
      "label": "battle end",
      "when": {
        "calc": "round_in_battle == rounds_per_battle and not battle_over"
      },
      "do": [
        {
          "set": {
            "key": "s1_theaters",
            "value": {
              "calc": "(1 if (players[0].air > players[1].air or (players[0].air == players[1].air and first_seat == 1)) else 0) + (1 if (players[0].land > players[1].land or (players[0].land == players[1].land and first_seat == 1)) else 0) + (1 if (players[0].sea > players[1].sea or (players[0].sea == players[1].sea and first_seat == 1)) else 0)"
            }
          }
        },
        {
          "set": {
            "key": "battle_winner",
            "value": {
              "calc": "1 if s1_theaters >= theaters_to_win_battle else 2"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "battle_winner"
            },
            "key": "vp",
            "value": {
              "calc": "battle_win_vp"
            },
            "text": "Seat {player} controls {theaters_to_win_battle} or more theaters, wins battle {battle} and gains {battle_win_vp} VP."
          }
        },
        {
          "set": {
            "key": "battle_over",
            "value": true
          }
        }
      ],
      "text": "Battle {battle} ends. Seat 1: Air {players[0].air}, Land {players[0].land}, Sea {players[0].sea}. Seat 2: Air {players[1].air}, Land {players[1].land}, Sea {players[1].sea}. Ties go to seat {first_seat}."
    },
    {
      "use": "check",
      "phase": "end",
      "label": "after the last round",
      "when": {
        "calc": "round >= total_rounds"
      },
      "against": [
        "over"
      ]
    },
    {
      "use": "update",
      "phase": "end",
      "label": "next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        }
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= total_rounds"
      },
      "rank_by": "you.vp",
      "text": "Winner: {result}. Final VP: Seat 1 {players[0].vp}, Seat 2 {players[1].vp}."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 30,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "CARDS. There are {total_cards} cards: Air 1-6, Land 1-6 and Sea 1-6. A card's strength is its number ({min_strength} to {max_strength}).\n\nMATCH. The match has {total_rounds} rounds, grouped into {battles} battles of {rounds_per_battle} rounds: battle 1 is rounds 1-6, battle 2 rounds 7-12, battle 3 rounds 13-18, battle 4 rounds 19-24. Seat 1 is the first player in battles 1 and 3; seat 2 is the first player in battles 2 and 4.\n\nBATTLE START (first round of each battle). All Air, Land and Sea strengths reset to 0 and all played cards are cleared. All {total_cards} cards are shuffled; each player is dealt {hand_size} cards privately, and the remaining {set_aside_count} are put aside unseen, out of play for this battle.\n\nACTIONS. If the battle is not over, the first player takes one action. Then, if the battle is still not over, the second player takes one action. An action is exactly one of:\n(a) DEPLOY: play a card from your hand face-up to the theater named on it. Add its number to your strength there.\n(b) IMPROVISE: play a card from your hand face-down to any theater. Add {improvise_strength} to your strength there, whatever the card's number or suit. The opponent sees only the theater and the +{improvise_strength}, not the card.\n(c) WITHDRAW: concede the battle.\nAll theater strengths and face-up cards are public. Hands, the set-aside cards and the identity of face-down cards are hidden.\n\nWITHDRAWAL. When a player withdraws, count the cards left in their hand. The opponent immediately gains VP: 4 or more cards gives {withdraw_vp_4_plus_cards} VP; 2 or 3 cards gives {withdraw_vp_2_or_3_cards} VP; 1 card gives {withdraw_vp_1_card} VP. The battle is over at once. If the first player withdrew, the second player does not act that round. Every remaining round of the battle passes with no actions and no scoring; the next battle starts at its fixed round as usual. If nobody withdraws, the battle goes to its end.\n\nBATTLE END (last round of a battle, after both actions, if nobody withdrew). Both hands are now empty. In each theater, the player with the higher strength controls it; a tie goes to that battle's first player. The player who controls {theaters_to_win_battle} or more of the {theaters} theaters wins the battle and gains {battle_win_vp} VP; the other gains nothing.\n\nEND. After round {total_rounds} the game ends. The player with more VP wins. Equal VP is a draw, and both players share the win."
}
```
````
