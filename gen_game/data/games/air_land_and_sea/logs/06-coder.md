# 06 coder

- time: 2026-10-27T17:26:27+00:00 (163.3s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 d3744fd8a1504ba5, reply sha256 c50cd6963838d02f

## Sent

````
# Task: write the XColos game file for "Three Fronts"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

COMPONENTS
- The deck has 18 cards: Air 1–6, Land 1–6 and Sea 1–6.
- There are three theaters: Air, Land and Sea. Each player has their own side of each theater.
- Each player has a VP score starting at 0.

STRUCTURE
- The match has 4 battles of 6 rounds each, 24 rounds in total.
- Player A is first player in battles 1 and 3. Player B is first player in battles 2 and 4.

START OF EACH BATTLE (rounds 1, 7, 13 and 19)
- Shuffle all 18 cards and deal 6 privately to each player.
- The remaining 6 cards are set aside unseen for the whole battle.
- All theaters start empty.

EACH ROUND
If the battle has not ended by withdrawal, the first player takes one action, then the second player takes one action. Both players see the result of each action before the next one.

The three possible actions are:
1. DEPLOY: place a card from your hand face-up on your side of the theater matching its suit (an Air card to Air, and so on). It counts its printed strength (1–6).
2. IMPROVISE: place a card from your hand face-down on your side of any theater. It counts strength 2. The opponent sees only that a face-down card was placed there; the owner knows what the card is.
3. WITHDRAW: concede the battle immediately. You may withdraw only while you still hold at least 1 card. The opponent scores VP by the number of cards you still hold:
   - 4 or more cards: 2 VP.
   - 2 or 3 cards: 3 VP.
   - 1 card: 4 VP.
   After a withdrawal, no further actions are taken in that battle, and the remaining rounds of the battle pass with no actions.

Cards placed later stack on earlier ones. Every card on your side counts, whether or not it is covered.

END OF A BATTLE FOUGHT TO THE END (after round 6 of the battle, when both players have played all 6 cards)
- For each theater, add up each player's strength on their side.
- The higher sum controls the theater. On an equal sum, including 0–0, the first player of that battle controls it.
- The player controlling 2 or 3 theaters wins the battle and scores 6 VP.
- The face-down cards are then revealed for the record.

END OF MATCH
After round 24, compare VP totals.

How the winner is decided: After 4 battles, the player with more VP wins. Equal VP is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Three Fronts (2 to 2 players, best with 2)

Two players fight 4 battles of 6 rounds over three theaters (Air, Land, Sea). Each round a player deploys a card face-up, improvises it face-down for strength 2, or withdraws to give up fewer VP; winning 2 of 3 theaters scores 6 VP.

STATE (every item below must exist in the file):
  - each player: vp (number, starts 0); everyone sees it. Victory points scored in the match so far.
  - each player: hand (list, starts []); only its owner sees it. The cards the player holds in the current battle, such as 'Air 4'.
  - each player: air_strength (number, starts 0); everyone sees it. Total strength on this player's side of Air this battle: face-up cards count their rank, face-down cards count 2.
  - each player: land_strength (number, starts 0); everyone sees it. Total strength on this player's side of Land this battle.
  - each player: sea_strength (number, starts 0); everyone sees it. Total strength on this player's side of Sea this battle.
  - each player: face_up_cards (list, starts []); everyone sees it. Cards deployed face-up this battle. Each card sits in the theater of its own suit.
  - each player: face_down_theaters (list, starts []); everyone sees it. The theater of each face-down card placed this battle. Both players see this.
  - each player: face_down_cards (list, starts []); only its owner sees it. The identity and theater of each face-down card this player placed, such as 'Land 5 in Sea'. Only the owner knows it until the battle is fought to the end.
  - the table: deck (list, starts ['Air 1', 'Air 2', 'Air 3', 'Air 4', 'Air 5', 'Air 6', 'Land 1', 'Land 2', 'Land 3', 'Land 4', 'Land 5', 'Land 6', 'Sea 1', 'Sea 2', 'Sea 3', 'Sea 4', 'Sea 5', 'Sea 6']); hidden from all players. The 18-card deck that is dealt from at the start of each battle.
  - the table: set_aside (list, starts []); hidden from all players. The 6 undealt cards, set aside unseen for the battle.
  - the table: battle (number, starts 1); everyone sees it. The current battle, from 1 to 4. A value of 5 means the match is over.
  - the table: round_in_battle (number, starts 1); everyone sees it. The current round within the battle, from 1 to 6.
  - the table: first_player (number, starts 1); everyone sees it. The seat that is first player this battle: seat 1 (A) in battles 1 and 3, seat 2 (B) in battles 2 and 4.
  - the table: battle_over (bool, starts False); everyone sees it. True once someone has withdrawn from the current battle.
  - the table: seat1_theaters (number, starts 0); everyone sees it. Scratch value: the number of theaters seat 1 controls at the end of a battle fought to the end (the workaround for comparing players).
  - the table: seat2_theaters (number, starts 0); everyone sees it. Scratch value: the number of theaters seat 2 controls at the end of a battle fought to the end.
  - parameters, each kept as a table attribute: deck_size = 18, suits = 3, ranks_per_suit = 6, min_rank = 1, max_rank = 6, battles = 4, rounds_per_battle = 6, total_rounds = 24, hand_size = 6, set_aside_cards = 6, improvise_strength = 2, withdraw_min_cards_held = 1, withdraw_vp_4_or_more_cards = 4, withdraw_vp_value_4_or_more = 2, withdraw_vp_value_2_or_3 = 3, withdraw_vp_value_1 = 4, theaters_to_win_battle = 2, battle_win_vp = 6, starting_vp = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 is Player A and seat 2 is Player B.
  2. Each player's vp is 0.
  3. battle is 1, round_in_battle is 1 and first_player is 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When round_in_battle == 1: the deck is reset to all 18 cards. Each player's hand, face_up_cards, face_down_theaters and face_down_cards are emptied, and air_strength, land_strength and sea_strength are set to 0. battle_over is set to false. Each player then draws 6 cards at random: each card is removed from deck and appended to that player's hand. The remaining 6 deck cards are moved to set_aside, unseen.
  2. [sync] all players. What happens: Each player is sent their own hand and the public state: strengths, face-up cards, face-down theaters, vp, battle, round_in_battle and first_player.
  3. [ask] the seat equal to first_player answers: one choice: 'deploy <card>' for a card in hand, 'improvise <card> to <Air|Land|Sea>' for a card in hand, or 'withdraw'. What happens: Only when battle_over == false. DEPLOY: the card is removed from hand and appended to face_up_cards, and the strength attribute of the card's suit rises by its rank. IMPROVISE: the card is removed from hand, '<card> in <theater>' is appended to face_down_cards, the theater is appended to face_down_theaters, and that theater's strength rises by 2. WITHDRAW: with n = the number of cards in the withdrawer's hand, the opponent's vp rises by 2 if n >= 4, by 3 if n is 2 or 3, and by 4 if n == 1; battle_over is set to true.
  4. [tell] all players. What happens: Only when that action was taken: everyone is told the result. A deploy names the card and its theater. An improvise names only the theater ('a face-down card was placed in X'). A withdraw states the VP awarded. The updated strengths are shown.
  5. [ask] the seat not equal to first_player answers: one choice: 'deploy <card>' for a card in hand, 'improvise <card> to <Air|Land|Sea>' for a card in hand, or 'withdraw'. What happens: Only when battle_over == false. The effects are the same as for the first player's action.
  6. [tell] all players. What happens: Only when that action was taken: everyone is told the result in the same way, with face-down card identities hidden.
  7. [update] all players. What happens: When round_in_battle == 6 and battle_over == false: for each theater, seat 1 controls it if seat 1's strength > seat 2's strength. On an equal sum, including 0-0, the seat equal to first_player controls it. Otherwise seat 2 controls it. seat1_theaters and seat2_theaters are set to these counts. The seat with 2 or more theaters gains 6 vp.
  8. [tell] all players. What happens: When round_in_battle == 6 and battle_over == false: the control of each theater and the battle winner are announced, and each player's face_down_cards are revealed to everyone for the record.
  9. [update] all players. What happens: If round_in_battle == 6: battle rises by 1, round_in_battle becomes 1 and first_player becomes 3 - first_player. Otherwise round_in_battle rises by 1.
  10. [check] all players. What happens: The game ends if battle > 4, which is after round 24. Otherwise play continues.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a battle starts (rounds 1, 7, 13 and 19), then all 18 cards are shuffled, 6 are dealt privately to each player's hand, and the remaining 6 go to set_aside unseen.
  R2. When a battle starts, then all strengths, face-up cards and face-down cards of both players are reset to empty or 0.
  R3. When it is battle 1 or 3, then seat 1 (A) is first player; when it is battle 2 or 4, then seat 2 (B) is first player.
  R4. When a round is played and the battle has not ended by withdrawal, then the first player takes one action, then the second player takes one action, and both see each result.
  R5. When a player deploys a card, then it leaves the hand, is shown face-up, and adds its rank (1 to 6) to that player's strength in the theater of its suit.
  R6. When a player improvises a card to a theater, then it leaves the hand, adds 2 to that player's strength in the chosen theater, and the opponent learns only the theater.
  R7. When a player withdraws holding 4 or more cards, then the opponent gains 2 VP.
  R8. When a player withdraws holding 2 or 3 cards, then the opponent gains 3 VP.
  R9. When a player withdraws holding 1 card, then the opponent gains 4 VP.
  R10. When a player holds 0 cards, then they may not withdraw.
  R11. When a player withdraws, then no further actions are taken in that battle and its remaining rounds pass with no actions.
  R12. When a later card is placed on a theater, then every card on that side still counts, covered or not.
  R13. When a battle is fought to the end (after its round 6, with no withdrawal), then for each theater the player with the higher strength sum controls it.
  R14. When the strength sums in a theater are equal, including 0-0, then the first player of that battle controls it.
  R15. When a player controls 2 or 3 theaters at the end of a battle fought to the end, then that player gains 6 VP.
  R16. When a battle is fought to the end, then all face-down cards are revealed for the record.
  R17. When round 24 is over, then the game ends and the player with more VP wins; equal VP is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - First player's action for the round | asked: the seat equal to first_player, only while battle_over is false | options: 'deploy <card>' for each card in hand; 'improvise <card> to Air', 'improvise <card> to Land' and 'improvise <card> to Sea' for each card in hand; and 'withdraw', which is always offered because the player always holds at least 1 card on their turn.
  - Second player's action for the round | asked: the seat not equal to first_player, only while battle_over is false | options: 'deploy <card>' for each card in hand; 'improvise <card> to Air', 'improvise <card> to Land' and 'improvise <card> to Sea' for each card in hand; and 'withdraw' (the player holds at least 1 card on their turn).

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: battle > 4
  - each player's standing: you.vp (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After 4 battles (24 rounds), the player with more VP wins. Equal VP is a draw, in which both players share the win.
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

- each player: `vp` (number, visible: public, starts 0): Victory points scored in the match so far.
- each player: `air_strength` (number, visible: public, starts 0): Total strength on this player's side of Air this battle: face-up cards count their rank, face-down cards count 2.
- each player: `land_strength` (number, visible: public, starts 0): Total strength on this player's side of Land this battle.
- each player: `sea_strength` (number, visible: public, starts 0): Total strength on this player's side of Sea this battle.
- the table: `battle` (number, visible: public, starts 1): The current battle, from 1 to 4. A value of 5 means the match is over.
- the table: `first_player` (number, visible: public, starts 1): The seat that is first player this battle: seat 1 (A) in battles 1 and 3, seat 2 (B) in battles 2 and 4.
- the table: `battle_over` (bool, visible: public, starts False): True once someone has withdrawn from the current battle.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 18, suits = 3, ranks_per_suit = 6, min_rank = 1, max_rank = 6, battles = 4, rounds_per_battle = 6, total_rounds = 24, hand_size = 6, set_aside_cards = 6, improvise_strength = 2, withdraw_min_cards_held = 1, withdraw_vp_4_or_more_cards = 4, withdraw_vp_value_4_or_more = 2, withdraw_vp_value_2_or_3 = 3, withdraw_vp_value_1 = 4, theaters_to_win_battle = 2, battle_win_vp = 6, starting_vp = 0
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
    "id": "three_fronts",
    "name": "Three Fronts",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two commanders fight 4 battles over Air, Land and Sea: deploy face-up, improvise face-down, or withdraw to cut your losses."
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
        "key": "air_strength",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "land_strength",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sea_strength",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "face_up_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "face_down_theaters",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "face_down_cards",
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
        "key": "full_deck",
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
        "key": "first_player",
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
        "key": "seat1_theaters",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "seat2_theaters",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "control",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "revealed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "cur_act",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "cur_actor",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cur_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "cur_theater",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "cur_gain",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cur_award",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "report",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "ranks_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "min_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_rank",
        "visible": "public",
        "type": "number",
        "initial": 6
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
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "set_aside_cards",
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
        "key": "withdraw_min_cards_held",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "withdraw_vp_4_or_more_cards",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "withdraw_vp_value_4_or_more",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "withdraw_vp_value_2_or_3",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "withdraw_vp_value_1",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "theaters_to_win_battle",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "battle_win_vp",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "starting_vp",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the match begins",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "vp",
            "value": {
              "calc": "starting_vp"
            }
          }
        },
        {
          "set": {
            "key": "battle",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_in_battle",
            "value": 1
          }
        },
        {
          "set": {
            "key": "first_player",
            "value": 1
          }
        }
      ],
      "text": "Seat 1 is Player A and seat 2 is Player B. Battle 1 begins with seat 1 as first player."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "a new battle",
      "when": {
        "calc": "round_in_battle == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[c for c in full_deck]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "face_up_cards",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "face_down_theaters",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "face_down_cards",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "air_strength",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "land_strength",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "sea_strength",
            "value": 0
          }
        },
        {
          "set": {
            "key": "battle_over",
            "value": false
          }
        },
        {
          "set": {
            "key": "seat1_theaters",
            "value": 0
          }
        },
        {
          "set": {
            "key": "seat2_theaters",
            "value": 0
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "[c for c in deck]"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": ""
          }
        }
      ],
      "text": "Battle {battle} of {battles} begins. All {deck_size} cards are shuffled; each player is dealt {hand_size} cards in secret and {set_aside_cards} are set aside unseen. All theaters are empty. Seat {first_player} is first player."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your position",
      "mode": "self",
      "to": "all",
      "text": "Battle {battle}, round {round_in_battle} of {rounds_per_battle}. First player: seat {first_player}. Your position:"
    },
    {
      "use": "update",
      "phase": "orders",
      "label": "the options",
      "do": [
        {
          "set": {
            "key": "cur_act",
            "value": ""
          }
        },
        {
          "set": {
            "key": "cur_actor",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['deploy ' + c for c in you.hand] + ['improvise ' + c + ' to Air' for c in you.hand] + ['improvise ' + c + ' to Land' for c in you.hand] + ['improvise ' + c + ' to Sea' for c in you.hand] + (['withdraw'] if len(you.hand) >= withdraw_min_cards_held else [])"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "orders",
      "label": "first player acts",
      "when": {
        "calc": "not battle_over"
      },
      "to": {
        "where": "you.seat == first_player"
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
      "text": "Battle {battle}, round {round_in_battle}: you are first player. Choose one action: 'deploy <card>' places it face-up in the theater of its suit at its printed strength; 'improvise <card> to <theater>' places it face-down in any theater at strength {improvise_strength} (your opponent sees only the theater); 'withdraw' concedes this battle now and your opponent scores VP by the cards you still hold."
    },
    {
      "use": "update",
      "phase": "orders",
      "label": "first player's action resolves",
      "when": {
        "calc": "not battle_over"
      },
      "do": [
        {
          "set": {
            "key": "cur_act",
            "value": "$a1"
          }
        },
        {
          "set": {
            "key": "cur_actor",
            "value": {
              "calc": "first_player"
            }
          }
        },
        {
          "set": {
            "key": "cur_card",
            "value": {
              "calc": "([c for c in players[cur_actor - 1].hand if cur_act in ['deploy ' + c, 'improvise ' + c + ' to Air', 'improvise ' + c + ' to Land', 'improvise ' + c + ' to Sea']] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "cur_theater",
            "value": {
              "calc": "'' if cur_act == 'withdraw' else ((('Air' if cur_card[0] == 'A' else ('Land' if cur_card[0] == 'L' else 'Sea'))) if cur_act[0] == 'd' else ('Air' if cur_act == 'improvise ' + cur_card + ' to Air' else ('Land' if cur_act == 'improvise ' + cur_card + ' to Land' else 'Sea')))"
            }
          }
        },
        {
          "set": {
            "key": "cur_gain",
            "value": {
              "calc": "0 if cur_act == 'withdraw' else (int(cur_card[len(cur_card) - 1]) if cur_act[0] == 'd' else improvise_strength)"
            }
          }
        },
        {
          "set": {
            "key": "cur_award",
            "value": {
              "calc": "0 if cur_act != 'withdraw' else (withdraw_vp_value_4_or_more if len(players[cur_actor - 1].hand) >= withdraw_vp_4_or_more_cards else (withdraw_vp_value_2_or_3 if len(players[cur_actor - 1].hand) > withdraw_min_cards_held else withdraw_vp_value_1))"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "hand",
            "value": {
              "calc": "cur_card"
            },
            "if": {
              "calc": "cur_act != 'withdraw'"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "face_up_cards",
            "value": {
              "calc": "cur_card"
            },
            "if": {
              "calc": "cur_act != 'withdraw' and cur_act[0] == 'd'"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "face_down_cards",
            "value": {
              "calc": "cur_card + ' in ' + cur_theater"
            },
            "if": {
              "calc": "cur_act != 'withdraw' and cur_act[0] == 'i'"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "face_down_theaters",
            "value": {
              "calc": "cur_theater"
            },
            "if": {
              "calc": "cur_act != 'withdraw' and cur_act[0] == 'i'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "air_strength",
            "value": {
              "calc": "cur_gain"
            },
            "if": {
              "calc": "cur_theater == 'Air'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "land_strength",
            "value": {
              "calc": "cur_gain"
            },
            "if": {
              "calc": "cur_theater == 'Land'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "sea_strength",
            "value": {
              "calc": "cur_gain"
            },
            "if": {
              "calc": "cur_theater == 'Sea'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "[p.seat for p in players if p.seat != cur_actor][0]"
            },
            "key": "vp",
            "value": {
              "calc": "cur_award"
            },
            "if": {
              "calc": "cur_act == 'withdraw'"
            },
            "text": "Seat {cur_actor} withdraws. Seat {player} gains {cur_award} VP."
          }
        },
        {
          "set": {
            "key": "battle_over",
            "value": true,
            "if": {
              "calc": "cur_act == 'withdraw'"
            }
          }
        },
        {
          "set": {
            "key": "report",
            "value": {
              "calc": "'withdraws from the battle; no further actions are taken in it' if cur_act == 'withdraw' else (('deploys ' + cur_card + ' face-up to ' + cur_theater) if cur_act[0] == 'd' else ('places a face-down card in ' + cur_theater))"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "orders",
      "label": "first player's result",
      "when": {
        "calc": "cur_act != '' and cur_actor == first_player"
      },
      "to": "all",
      "text": "Seat {cur_actor} {report}. Strengths (Air/Land/Sea): seat 1 {players[0].air_strength}/{players[0].land_strength}/{players[0].sea_strength}, seat 2 {players[1].air_strength}/{players[1].land_strength}/{players[1].sea_strength}. VP: seat 1 {players[0].vp}, seat 2 {players[1].vp}."
    },
    {
      "use": "ask",
      "phase": "orders",
      "label": "second player acts",
      "when": {
        "calc": "not battle_over"
      },
      "to": {
        "where": "you.seat != first_player"
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
      "text": "Battle {battle}, round {round_in_battle}: you are second player. Choose one action: 'deploy <card>' places it face-up in the theater of its suit at its printed strength; 'improvise <card> to <theater>' places it face-down in any theater at strength {improvise_strength} (your opponent sees only the theater); 'withdraw' concedes this battle now and your opponent scores VP by the cards you still hold."
    },
    {
      "use": "update",
      "phase": "orders",
      "label": "second player's action resolves",
      "when": {
        "calc": "not battle_over"
      },
      "do": [
        {
          "set": {
            "key": "cur_act",
            "value": "$a2"
          }
        },
        {
          "set": {
            "key": "cur_actor",
            "value": {
              "calc": "[p.seat for p in players if p.seat != first_player][0]"
            }
          }
        },
        {
          "set": {
            "key": "cur_card",
            "value": {
              "calc": "([c for c in players[cur_actor - 1].hand if cur_act in ['deploy ' + c, 'improvise ' + c + ' to Air', 'improvise ' + c + ' to Land', 'improvise ' + c + ' to Sea']] + [''])[0]"
            }
          }
        },
        {
          "set": {
            "key": "cur_theater",
            "value": {
              "calc": "'' if cur_act == 'withdraw' else ((('Air' if cur_card[0] == 'A' else ('Land' if cur_card[0] == 'L' else 'Sea'))) if cur_act[0] == 'd' else ('Air' if cur_act == 'improvise ' + cur_card + ' to Air' else ('Land' if cur_act == 'improvise ' + cur_card + ' to Land' else 'Sea')))"
            }
          }
        },
        {
          "set": {
            "key": "cur_gain",
            "value": {
              "calc": "0 if cur_act == 'withdraw' else (int(cur_card[len(cur_card) - 1]) if cur_act[0] == 'd' else improvise_strength)"
            }
          }
        },
        {
          "set": {
            "key": "cur_award",
            "value": {
              "calc": "0 if cur_act != 'withdraw' else (withdraw_vp_value_4_or_more if len(players[cur_actor - 1].hand) >= withdraw_vp_4_or_more_cards else (withdraw_vp_value_2_or_3 if len(players[cur_actor - 1].hand) > withdraw_min_cards_held else withdraw_vp_value_1))"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "hand",
            "value": {
              "calc": "cur_card"
            },
            "if": {
              "calc": "cur_act != 'withdraw'"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "face_up_cards",
            "value": {
              "calc": "cur_card"
            },
            "if": {
              "calc": "cur_act != 'withdraw' and cur_act[0] == 'd'"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "face_down_cards",
            "value": {
              "calc": "cur_card + ' in ' + cur_theater"
            },
            "if": {
              "calc": "cur_act != 'withdraw' and cur_act[0] == 'i'"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "face_down_theaters",
            "value": {
              "calc": "cur_theater"
            },
            "if": {
              "calc": "cur_act != 'withdraw' and cur_act[0] == 'i'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "air_strength",
            "value": {
              "calc": "cur_gain"
            },
            "if": {
              "calc": "cur_theater == 'Air'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "land_strength",
            "value": {
              "calc": "cur_gain"
            },
            "if": {
              "calc": "cur_theater == 'Land'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "cur_actor"
            },
            "key": "sea_strength",
            "value": {
              "calc": "cur_gain"
            },
            "if": {
              "calc": "cur_theater == 'Sea'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "[p.seat for p in players if p.seat != cur_actor][0]"
            },
            "key": "vp",
            "value": {
              "calc": "cur_award"
            },
            "if": {
              "calc": "cur_act == 'withdraw'"
            },
            "text": "Seat {cur_actor} withdraws. Seat {player} gains {cur_award} VP."
          }
        },
        {
          "set": {
            "key": "battle_over",
            "value": true,
            "if": {
              "calc": "cur_act == 'withdraw'"
            }
          }
        },
        {
          "set": {
            "key": "report",
            "value": {
              "calc": "'withdraws from the battle; no further actions are taken in it' if cur_act == 'withdraw' else (('deploys ' + cur_card + ' face-up to ' + cur_theater) if cur_act[0] == 'd' else ('places a face-down card in ' + cur_theater))"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "orders",
      "label": "second player's result",
      "when": {
        "calc": "cur_act != '' and cur_actor != first_player and cur_actor != 0"
      },
      "to": "all",
      "text": "Seat {cur_actor} {report}. Strengths (Air/Land/Sea): seat 1 {players[0].air_strength}/{players[0].land_strength}/{players[0].sea_strength}, seat 2 {players[1].air_strength}/{players[1].land_strength}/{players[1].sea_strength}. VP: seat 1 {players[0].vp}, seat 2 {players[1].vp}."
    },
    {
      "use": "update",
      "phase": "resolution",
      "label": "the battle is decided",
      "when": {
        "calc": "round_in_battle == rounds_per_battle and not battle_over"
      },
      "do": [
        {
          "set": {
            "key": "seat1_theaters",
            "value": {
              "calc": "(1 if (players[0].air_strength > players[1].air_strength or (players[0].air_strength == players[1].air_strength and first_player == 1)) else 0) + (1 if (players[0].land_strength > players[1].land_strength or (players[0].land_strength == players[1].land_strength and first_player == 1)) else 0) + (1 if (players[0].sea_strength > players[1].sea_strength or (players[0].sea_strength == players[1].sea_strength and first_player == 1)) else 0)"
            }
          }
        },
        {
          "set": {
            "key": "seat2_theaters",
            "value": {
              "calc": "suits - seat1_theaters"
            }
          }
        },
        {
          "set": {
            "key": "control",
            "value": {
              "calc": "'Air: seat ' + ('1' if (players[0].air_strength > players[1].air_strength or (players[0].air_strength == players[1].air_strength and first_player == 1)) else '2') + ', Land: seat ' + ('1' if (players[0].land_strength > players[1].land_strength or (players[0].land_strength == players[1].land_strength and first_player == 1)) else '2') + ', Sea: seat ' + ('1' if (players[0].sea_strength > players[1].sea_strength or (players[0].sea_strength == players[1].sea_strength and first_player == 1)) else '2')"
            }
          }
        },
        {
          "set": {
            "key": "revealed",
            "value": {
              "calc": "['Seat 1: ' + c for c in players[0].face_down_cards] + ['Seat 2: ' + c for c in players[1].face_down_cards]"
            }
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "vp",
            "value": {
              "calc": "battle_win_vp"
            },
            "if": {
              "calc": "seat1_theaters >= theaters_to_win_battle"
            },
            "text": "Seat 1 wins battle {battle} and gains {battle_win_vp} VP."
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "vp",
            "value": {
              "calc": "battle_win_vp"
            },
            "if": {
              "calc": "seat2_theaters >= theaters_to_win_battle"
            },
            "text": "Seat 2 wins battle {battle} and gains {battle_win_vp} VP."
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolution",
      "label": "the battle report",
      "when": {
        "calc": "round_in_battle == rounds_per_battle and not battle_over"
      },
      "to": "all",
      "text": "Battle {battle} is fought to the end. Control: {control}. Theaters held: seat 1 {seat1_theaters}, seat 2 {seat2_theaters}. Face-down cards revealed for the record: {revealed}. VP: seat 1 {players[0].vp}, seat 2 {players[1].vp}."
    },
    {
      "use": "update",
      "phase": "resolution",
      "label": "advance the round",
      "do": [
        {
          "adjust": {
            "key": "battle",
            "value": 1,
            "if": {
              "calc": "round_in_battle == rounds_per_battle"
            }
          }
        },
        {
          "set": {
            "key": "first_player",
            "value": {
              "calc": "3 - first_player"
            },
            "if": {
              "calc": "round_in_battle == rounds_per_battle"
            }
          }
        },
        {
          "set": {
            "key": "round_in_battle",
            "value": {
              "calc": "1 if round_in_battle == rounds_per_battle else round_in_battle + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "resolution",
      "label": "after the last battle",
      "when": {
        "calc": "battle > battles"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "battle > battles"
      },
      "rank_by": "you.vp",
      "text": "Winner: {result}. Final VP: Seat 1 {players[0].vp}, Seat 2 {players[1].vp}."
    }
  },
  "limits": {
    "rounds": 24,
    "rounds_max": 30,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "Three Fronts is played by two players: seat 1 is Player A and seat 2 is Player B. The deck has {deck_size} cards: Air 1-6, Land 1-6 and Sea 1-6. There are three theaters, Air, Land and Sea, and each player has their own side of each theater. Each player has a VP score starting at {starting_vp}.\n\nThe match has {battles} battles of {rounds_per_battle} rounds each, {total_rounds} rounds in total. Player A is first player in battles 1 and 3; Player B is first player in battles 2 and 4.\n\nAt the start of each battle (rounds 1, 7, 13 and 19), all {deck_size} cards are shuffled and {hand_size} are dealt privately to each player. The remaining {set_aside_cards} cards are set aside unseen for the whole battle. All theaters start empty.\n\nEach round, if the battle has not ended by withdrawal, the first player takes one action, then the second player takes one action. Both players see the result of each action before the next one. The three possible actions are:\n1. DEPLOY: place a card from your hand face-up on your side of the theater matching its suit (an Air card to Air, and so on). It counts its printed strength (1-6).\n2. IMPROVISE: place a card from your hand face-down on your side of any theater. It counts strength {improvise_strength}. The opponent sees only that a face-down card was placed there; the owner knows what the card is.\n3. WITHDRAW: concede the battle immediately. You may withdraw only while you still hold at least {withdraw_min_cards_held} card (you always do on your turn). The opponent scores VP by the number of cards you still hold: {withdraw_vp_4_or_more_cards} or more cards: {withdraw_vp_value_4_or_more} VP; 2 or 3 cards: {withdraw_vp_value_2_or_3} VP; 1 card: {withdraw_vp_value_1} VP. After a withdrawal, no further actions are taken in that battle, the remaining rounds of the battle pass with no actions, and nobody scores the {battle_win_vp} VP for that battle. If nobody withdraws, the battle is fought to the end.\n\nCards placed later stack on earlier ones. Every card on your side counts, whether or not it is covered.\n\nEnd of a battle fought to the end (after round 6 of the battle, when both players have played all 6 cards): for each theater, add up each player's strength on their side. The higher sum controls the theater. On an equal sum, including 0-0, the first player of that battle controls it. The player controlling {theaters_to_win_battle} or 3 theaters wins the battle and scores {battle_win_vp} VP; the other player scores nothing for the battle. The face-down cards are then revealed for the record.\n\nEnd of match: after round {total_rounds}, compare VP totals. The player with more VP wins. Equal VP is a draw, and both players share the win."
}
```
````
