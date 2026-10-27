# 29 coder

- time: 2026-10-27T18:22:02+00:00 (79.0s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 10c8aa16efe8375c, reply sha256 cd9e2af0c0413028

## Sent

````
# Task: write the XColos game file for "Skull King: Three-Card Bids"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP
- Every player's score starts at 0. The round counter starts at 0.
- Table parameters: hand_size = 3, tricks_per_round = 3, rounds = 8, bid_min = 0, bid_max = 3.
- The deck has 18 cards, each identified by its power:
  - number cards 1 to 12 (one of each);
  - two Escapes, each of power 0;
  - one Mermaid, power 20;
  - Pirate A, power 30;
  - Pirate B, power 31;
  - the Skull King, power 40.

EACH ROUND (8 rounds)
1. Add 1 to the round counter. Set every player's tricks_won to 0 and bonus to 0. Empty every hand.
2. Gather all 18 cards into the deck and shuffle it. This is the round's only random event.
3. Deal 3 cards from the deck to each player, one at a time in seat order. Each hand is private: only its owner sees it. The undealt cards stay in the deck and are never revealed that round.
4. BID, as one simultaneous poll of all players:
   - The options are exactly the whole numbers from bid_min to bid_max, which are 0, 1, 2 and 3.
   - Each player picks one option without seeing anyone else's choice.
   - Each player's chosen number is stored as that player's bid.
5. Once every bid is in, announce all bids to everyone.
6. Play three tricks. For each trick:
   a. PLAY, as a simultaneous poll. Each player chooses one card from their own current hand. The chosen card is removed from that hand, and all played cards are then revealed to everyone.
   b. RESOLVE the trick:
      - If both the Mermaid and the Skull King were played, the player of the Mermaid wins the trick.
      - Otherwise the player of the highest-power card wins.
      - Ties cannot occur: the only equal cards are the two Escapes, and with at least 3 players at least one non-Escape card is always played.
   c. AWARD:
      - Add 1 to the winner's tricks_won.
      - If the Skull King won the trick, add 30 to its player's bonus for each Pirate played in that trick.
      - If the Mermaid won the trick and the Skull King was played in it, add 50 to the Mermaid player's bonus.
7. SCORE each player, reading their stored bid:
   - If bid is 1, 2 or 3 and tricks_won equals bid: gain 20 × bid + bonus.
   - If bid is 1, 2 or 3 and tricks_won differs from bid: lose 10 × |tricks_won − bid|. The bonus is not scored.
   - If bid is 0 and tricks_won is 0: gain 20.
   - If bid is 0 and tricks_won is 1 or more: lose 20.
8. If the round counter equals 8, the game ends. Otherwise start the next round.

There is no discussion phase.

How the winner is decided: After round 8, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Skull King: Three-Card Bids (3 to 5 players, best with 4)

Over 8 rounds, players are dealt 3 cards from an 18-card deck, bid at the same time on how many of 3 simultaneous tricks they will win, and score for bidding exactly right, with bonuses when the Skull King captures Pirates or the Mermaid captures the Skull King.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. The player's total score over all rounds.
  - each player: hand (list, starts []); only its owner sees it. The powers of the cards the player holds this round. Only the owner sees them.
  - each player: bid (number, starts 0); everyone sees it. The number of tricks the player bid this round. It is collected by a simultaneous poll, so nobody sees it until all bids are in.
  - each player: tricks_won (number, starts 0); everyone sees it. The number of tricks the player has won this round.
  - each player: bonus (number, starts 0); everyone sees it. The capture bonus the player has earned this round. It is scored only on an exact non-zero bid.
  - each player: played (number, starts -1); everyone sees it. The power of the card the player played in the current trick. It is revealed after everyone has played.
  - the table: round (number, starts 0); everyone sees it. The round counter.
  - the table: deck (list, starts [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 0, 20, 30, 31, 40]); hidden from all players. The undealt cards, listed by power. They are never revealed.
  - the table: trick (number, starts 0); everyone sees it. The number of tricks played so far this round.
  - the table: mermaid_played (bool, starts False); everyone sees it. Whether the Mermaid (20) was played in the current trick.
  - the table: skull_king_played (bool, starts False); everyone sees it. Whether the Skull King (40) was played in the current trick.
  - the table: pirates_in_trick (number, starts 0); everyone sees it. The number of Pirates (30 or 31) played in the current trick.
  - the table: max_power (number, starts 0); everyone sees it. The highest power played in the current trick.
  - parameters, each kept as a table attribute: hand_size = 3, tricks_per_round = 3, rounds = 8, bid_min = 0, bid_max = 3, deck_size = 18, number_card_min = 1, number_card_max = 12, escape_count = 2, escape_power = 0, mermaid_power = 20, pirate_a_power = 30, pirate_b_power = 31, skull_king_power = 40, exact_bid_points_per_trick = 20, missed_bid_penalty_per_trick = 10, zero_bid_success_points = 20, zero_bid_failure_penalty = 20, skull_king_bonus_per_pirate = 30, mermaid_captures_skull_king_bonus = 50

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player's score is set to 0.
  2. The round counter is set to 0.
  3. The deck list holds the 18 card powers: 1 to 12, 0, 0, 20, 30, 31 and 40.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1. For every player: tricks_won = 0, bonus = 0, hand = [], played = -1. Table: trick = 0.
  2. [update] all players. What happens: deck = [1,2,3,4,5,6,7,8,9,10,11,12,0,0,20,30,31,40]. All 18 cards are gathered; shuffling happens through the random draws.
  3. [update] each player in turn. What happens: Deal hand_size (3) cards to each player, one at a time in seat order. Each card is a random draw: it is removed from deck and appended to that player's hand. The remaining cards stay in deck, hidden.
  4. [sync] all players. What happens: Each player privately sees their own hand.
  5. [poll] all players answers: a whole number from bid_min (0) to bid_max (3). What happens: Each player's answer is stored as that player's bid. No player sees another's bid until all are in.
  6. [tell] all players. What happens: Announce every player's bid to everyone.
  7. [poll] all players answers: one card (power) from the player's own current hand. What happens: played = the chosen power. That card is removed from the player's hand.
  8. [tell] all players. What happens: Reveal every player's played card to everyone.
  9. [update] all players. What happens: Table: mermaid_played = (some player's played == 20); skull_king_played = (some player's played == 40); pirates_in_trick = count of players whose played is 30 or 31; max_power = the maximum of played over all players.
  10. [update] all players. What happens: The trick winner is: if mermaid_played and skull_king_played, the player whose played == 20; otherwise the player whose played == max_power. For the winner: tricks_won += 1. If the winner's played == 40: bonus += 30 * pirates_in_trick. If the winner's played == 20 and skull_king_played: bonus += 50. Then trick += 1.
  11. [repeat] all players. What happens: Run the play, reveal, resolve and award steps again until trick == tricks_per_round (3).
  12. [update] all players. What happens: For each player: if bid >= 1 and tricks_won == bid, score += 20 * bid + bonus; if bid >= 1 and tricks_won != bid, score -= 10 * |tricks_won - bid|; if bid == 0 and tricks_won == 0, score += 20; if bid == 0 and tricks_won >= 1, score -= 20. Announce the round's results.
  13. [check] all players. What happens: If round == rounds (8), end the game; otherwise start the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player's score is 0 and the round counter is 0.
  R2. When a round starts, then round increases by 1, and every player's tricks_won is 0, bonus is 0 and hand is empty.
  R3. When a round starts, then the deck holds all 18 cards: powers 1 to 12, two 0s (Escapes), 20 (Mermaid), 30 (Pirate A), 31 (Pirate B) and 40 (Skull King).
  R4. When cards are dealt, then each player receives exactly 3 random cards from the deck into their hand, and those cards are removed from the deck.
  R5. When cards are dealt, then a player's hand is visible only to that player, and the undealt deck is visible to no one.
  R6. When bidding, then every player at the same time chooses a whole number from 0 to 3, stored as bid, and no player sees another's bid before all are in.
  R7. When all bids are in, then every bid is announced to everyone.
  R8. When a trick is played, then every player at the same time chooses one card from their own current hand, that card is removed from the hand, and all played cards are revealed.
  R9. When both the Mermaid (20) and the Skull King (40) are played in a trick, then the Mermaid's player wins the trick.
  R10. When the Mermaid and the Skull King are not both played in a trick, then the player of the highest-power card wins it (for example, 31 beats 30, and 12 beats 0).
  R11. When a player wins a trick, then their tricks_won increases by 1.
  R12. When the Skull King wins a trick, then its player's bonus increases by 30 for each Pirate (30 or 31) in that trick: 30 for one Pirate, 60 for both.
  R13. When the Mermaid wins a trick in which the Skull King was played, then the Mermaid's player's bonus increases by 50.
  R14. When 3 tricks have been played in a round, then the round's scoring happens.
  R15. When a player bid 1, 2 or 3 and tricks_won equals the bid, then their score increases by 20 times the bid plus their bonus (for example, a bid of 2 with 2 tricks and a bonus of 30 gains 70).
  R16. When a player bid 1, 2 or 3 and tricks_won differs from the bid, then their score decreases by 10 times the difference, and the bonus is not scored (for example, a bid of 3 with 1 trick loses 20).
  R17. When a player bid 0 and won 0 tricks, then their score increases by 20.
  R18. When a player bid 0 and won 1 or more tricks, then their score decreases by 20.
  R19. When the round counter reaches 8 after scoring, then the game ends.
  R20. When the game ends, then the player with the highest score wins, and players tied for the highest share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid: how many tricks will you win this round? | asked: all players, at once | options: every player: 0, 1, 2, 3
  - Play a card for this trick | asked: all players, at once | options: each player: exactly the cards still in their own hand (3 choices in trick 1, 2 in trick 2, 1 in trick 3); two Escapes in a hand appear as two options of power 0

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 8
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After round 8, each player's standing is their total score. The highest score wins, and players tied for the highest share the win (a draw among them).
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

- each player: `score` (number, visible: public, starts 0): The player's total score over all rounds.
- each player: `bid` (number, visible: public, starts 0): The number of tricks the player bid this round. It is collected by a simultaneous poll, so nobody sees it until all bids are in.
- each player: `tricks_won` (number, visible: public, starts 0): The number of tricks the player has won this round.
- the table: `round` (number, visible: public, starts 0): The round counter.
- parameters (each must be an attribute holding this value, never a number buried in a step): hand_size = 3, tricks_per_round = 3, rounds = 8, bid_min = 0, bid_max = 3, deck_size = 18, number_card_min = 1, number_card_max = 12, escape_count = 2, escape_power = 0, mermaid_power = 20, pirate_a_power = 30, pirate_b_power = 31, skull_king_power = 40, exact_bid_points_per_trick = 20, missed_bid_penalty_per_trick = 10, zero_bid_success_points = 20, zero_bid_failure_penalty = 20, skull_king_bonus_per_pirate = 30, mermaid_captures_skull_king_bonus = 50
- the game ends with ONE ending whose `rank_by` is `you.score`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

## Guidance from the last attempt

The previous attempt had problems:

Make the BID step a single simultaneous poll of all players, with the same option list for every seat: the whole numbers from bid_min (0) to bid_max (3), built from those parameter attributes. Do not build it per seat or from anything that varies by seat, such as the hand or the seat index. Store each player's chosen number in that player's `bid`, then announce all bids. Check that seats 2 and 3 are actually offered 3 and that the chosen value lands in their `bid`.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "skull_king_three_card_bids",
    "name": "Skull King: Three-Card Bids",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Eight rounds of three cards each: bid how many of three tricks you will take, and score for bidding exactly right."
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
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tricks_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bonus",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "played",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 0, 20, 30, 31, 40]
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 0, 20, 30, 31, 40]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "mermaid_played",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "skull_king_played",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "pirates_in_trick",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_power",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_winner",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "bid_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_max",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "number_card_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "number_card_max",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "escape_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "escape_power",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "mermaid_power",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "pirate_a_power",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "pirate_b_power",
        "visible": "public",
        "type": "number",
        "initial": 31
      },
      {
        "key": "skull_king_power",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "exact_bid_points_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "missed_bid_penalty_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "zero_bid_success_points",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "zero_bid_failure_penalty",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "skull_king_bonus_per_pirate",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "mermaid_captures_skull_king_bonus",
        "visible": "public",
        "type": "number",
        "initial": 50
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting state",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": 0
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
            }
          }
        }
      ]
    },
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
      "use": "update",
      "phase": "deal",
      "label": "a new round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks_won",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bonus",
            "value": 0
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
            "key": "played",
            "value": -1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "choice",
            "value": ""
          }
        },
        {
          "set": {
            "key": "trick",
            "value": 0
          }
        }
      ],
      "text": "Round {round} of {rounds} begins."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "gather the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "deal the hands",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 5"}}},
        {"append": {"player": 5, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 5"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 5"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 5"}}},
        {"append": {"player": 5, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 5"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 5"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 5"}}},
        {"append": {"player": 5, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 5"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 5"}}}
      ],
      "text": "Each player is dealt {hand_size} cards."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "score"
      ],
      "text": "Your hand this round:"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "bid",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "bid_min"
        },
        "max": {
          "calc": "bid_max"
        }
      },
      "store": "bid",
      "text": "Round {round}: how many of the {tricks_per_round} tricks will you win? Answer a whole number from {bid_min} to {bid_max}. Nobody sees your bid until all bids are in."
    },
    {
      "use": "tell",
      "phase": "bid",
      "label": "the bids",
      "to": "all",
      "text": "All bids are in [seat, bid]: {[[p.seat, p.bid] for p in players]}."
    },
    {
      "use": "repeat",
      "label": "the tricks",
      "until": {
        "calc": "trick >= tricks_per_round"
      },
      "max": 3,
      "steps": [
        {
          "use": "poll",
          "phase": "play",
          "label": "play a card",
          "to": "acting",
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "hand"
            }
          },
          "store": "choice",
          "text": "Play one card from your hand for this trick. Cards are shown by power: 0 Escape, 1-12 numbers, 20 Mermaid, 30 Pirate A, 31 Pirate B, 40 Skull King. All cards are revealed together."
        },
        {
          "use": "update",
          "phase": "play",
          "label": "take the cards from the hands",
          "do": [
            {
              "set": {
                "players": "all",
                "key": "played",
                "value": {
                  "calc": "int(you.choice)"
                }
              }
            },
            {
              "remove": {
                "players": "all",
                "key": "hand",
                "value": {
                  "calc": "you.played"
                }
              }
            }
          ]
        },
        {
          "use": "tell",
          "phase": "play",
          "label": "the reveal",
          "to": "all",
          "text": "Cards played [seat, power]: {[[p.seat, p.played] for p in players]}."
        },
        {
          "use": "update",
          "phase": "resolve",
          "label": "read the trick",
          "do": [
            {
              "set": {
                "key": "mermaid_played",
                "value": {
                  "calc": "any(p.played == mermaid_power for p in players)"
                }
              }
            },
            {
              "set": {
                "key": "skull_king_played",
                "value": {
                  "calc": "any(p.played == skull_king_power for p in players)"
                }
              }
            },
            {
              "set": {
                "key": "pirates_in_trick",
                "value": {
                  "calc": "count(p.played == pirate_a_power or p.played == pirate_b_power for p in players)"
                }
              }
            },
            {
              "set": {
                "key": "max_power",
                "value": {
                  "calc": "max([p.played for p in players])"
                }
              }
            }
          ]
        },
        {
          "use": "update",
          "phase": "resolve",
          "label": "award the trick",
          "do": [
            {
              "set": {
                "key": "trick_winner",
                "value": {
                  "calc": "min([p.seat for p in players if p.played == mermaid_power]) if (mermaid_played and skull_king_played) else min([p.seat for p in players if p.played == max_power])"
                }
              }
            },
            {
              "adjust": {
                "players": {
                  "where": "you.seat == trick_winner"
                },
                "key": "tricks_won",
                "value": 1,
                "text": "Seat {player} wins the trick."
              }
            },
            {
              "adjust": {
                "players": {
                  "where": "you.seat == trick_winner and you.played == skull_king_power"
                },
                "key": "bonus",
                "value": {
                  "calc": "skull_king_bonus_per_pirate * pirates_in_trick"
                },
                "if": {
                  "calc": "pirates_in_trick > 0"
                },
                "text": "The Skull King captures Pirates: seat {player} earns a bonus."
              }
            },
            {
              "adjust": {
                "players": {
                  "where": "you.seat == trick_winner and you.played == mermaid_power"
                },
                "key": "bonus",
                "value": {
                  "calc": "mermaid_captures_skull_king_bonus"
                },
                "if": {
                  "calc": "skull_king_played"
                },
                "text": "The Mermaid captures the Skull King: seat {player} earns a bonus."
              }
            },
            {
              "adjust": {
                "key": "trick",
                "value": 1
              }
            },
            {
              "set": {
                "players": "all",
                "key": "choice",
                "value": ""
              }
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "score",
      "label": "score the round",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "((exact_bid_points_per_trick * you.bid + you.bonus) if you.tricks_won == you.bid else -(missed_bid_penalty_per_trick * abs(you.tricks_won - you.bid))) if you.bid >= 1 else (zero_bid_success_points if you.tricks_won == 0 else -zero_bid_failure_penalty)"
            }
          }
        }
      ],
      "text": "Round {round} scored. Tricks won [seat, bid, tricks]: {[[p.seat, p.bid, p.tricks_won] for p in players]}. Scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after the last round",
      "when": {
        "calc": "round >= rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= rounds"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 8,
    "rounds_max": 10,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "The game lasts {rounds} rounds. Every player's score starts at 0.\n\nThe deck has {deck_size} cards, each identified by its power: number cards {number_card_min} to {number_card_max} (one of each); {escape_count} Escapes of power {escape_power}; one Mermaid, power {mermaid_power}; Pirate A, power {pirate_a_power}; Pirate B, power {pirate_b_power}; and the Skull King, power {skull_king_power}.\n\nEach round all {deck_size} cards are gathered and shuffled, and {hand_size} cards are dealt to each player, one at a time in seat order. Your hand is private: only you see it. The undealt cards are never revealed.\n\nBID: all players bid at the same time, choosing a whole number from {bid_min} to {bid_max}: how many of the {tricks_per_round} tricks you will win. Nobody sees another bid until all bids are in; then every bid is announced to everyone.\n\nThen {tricks_per_round} tricks are played. In each trick every player at the same time plays one card from their own hand; the card leaves the hand, and all played cards are revealed together. If both the Mermaid and the Skull King were played, the Mermaid's player wins the trick. Otherwise the player of the highest-power card wins. The winner adds 1 to their tricks won. If the Skull King won the trick, its player gains a bonus of {skull_king_bonus_per_pirate} for each Pirate played in that trick (no Pirate, no bonus). If the Mermaid won the trick and the Skull King was played in it, the Mermaid's player gains a bonus of {mermaid_captures_skull_king_bonus}.\n\nSCORING after the three tricks: if you bid 1, 2 or 3 and your tricks won equal your bid, you gain {exact_bid_points_per_trick} times your bid plus your bonus. If you bid 1, 2 or 3 and your tricks won differ from your bid, you lose {missed_bid_penalty_per_trick} times the difference, and your bonus is not scored. If you bid 0 and won no tricks, you gain {zero_bid_success_points}. If you bid 0 and won 1 or more tricks, you lose {zero_bid_failure_penalty}. Bonuses and tricks won reset each round.\n\nThere is no discussion. After round {rounds}, the highest total score wins; players tied for the highest share the win."
}
```

Why it was refused: an option is offered and then refused (see the offer-only-what-is-allowed pattern): refused: seat 1 was offered 31 in `play_a_card`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards | refused: seat 2 was offered 4 in `play_a_card`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "skull_king_three_card_bids",
    "name": "Skull King: Three-Card Bids",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Eight rounds of three cards each: bid how many of three tricks you will take, and score for bidding exactly right."
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
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tricks_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bonus",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "played",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 0, 20, 30, 31, 40]
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 0, 20, 30, 31, 40]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "mermaid_played",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "skull_king_played",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "pirates_in_trick",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_power",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_winner",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "bid_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_max",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "number_card_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "number_card_max",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "escape_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "escape_power",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "mermaid_power",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "pirate_a_power",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "pirate_b_power",
        "visible": "public",
        "type": "number",
        "initial": 31
      },
      {
        "key": "skull_king_power",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "exact_bid_points_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "missed_bid_penalty_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "zero_bid_success_points",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "zero_bid_failure_penalty",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "skull_king_bonus_per_pirate",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "mermaid_captures_skull_king_bonus",
        "visible": "public",
        "type": "number",
        "initial": 50
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting state",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": 0
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
            }
          }
        }
      ]
    },
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
      "use": "update",
      "phase": "deal",
      "label": "a new round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks_won",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bonus",
            "value": 0
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
            "key": "played",
            "value": -1
          }
        },
        {
          "set": {
            "key": "trick",
            "value": 0
          }
        }
      ],
      "text": "Round {round} of {rounds} begins."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "gather the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "deal the hands",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 5"}}},
        {"append": {"player": 5, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 5"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 5"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 5"}}},
        {"append": {"player": 5, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 5"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 5"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}, "if": {"calc": "len(players) >= 5"}}},
        {"append": {"player": 5, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 5"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 5"}}}
      ],
      "text": "Each player is dealt {hand_size} cards."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "score"
      ],
      "text": "Your hand this round:"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "bid",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "bid_min"
        },
        "max": {
          "calc": "bid_max"
        }
      },
      "store": "bid",
      "text": "Round {round}: how many of the {tricks_per_round} tricks will you win? Answer a whole number from {bid_min} to {bid_max}. Nobody sees your bid until all bids are in."
    },
    {
      "use": "tell",
      "phase": "bid",
      "label": "the bids",
      "to": "all",
      "text": "All bids are in [seat, bid]: {[[p.seat, p.bid] for p in players]}."
    },
    {
      "use": "poll",
      "phase": "play",
      "label": "play trick 1",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "choice",
      "text": "Trick 1 of {tricks_per_round}: play one card from your hand. Cards are shown by power: 0 Escape, 1-12 numbers, 20 Mermaid, 30 Pirate A, 31 Pirate B, 40 Skull King. All cards are revealed together."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve trick 1",
      "do": [
        {"set": {"players": "all", "key": "played", "value": {"calc": "int(you.choice)"}}},
        {"remove": {"players": "all", "key": "hand", "value": {"calc": "you.played"}}},
        {"set": {"key": "mermaid_played", "value": {"calc": "any(p.played == mermaid_power for p in players)"}}},
        {"set": {"key": "skull_king_played", "value": {"calc": "any(p.played == skull_king_power for p in players)"}}},
        {"set": {"key": "pirates_in_trick", "value": {"calc": "count(p.played == pirate_a_power or p.played == pirate_b_power for p in players)"}}},
        {"set": {"key": "max_power", "value": {"calc": "max([p.played for p in players])"}}},
        {"set": {"key": "trick_winner", "value": {"calc": "min([p.seat for p in players if p.played == mermaid_power]) if (mermaid_played and skull_king_played) else min([p.seat for p in players if p.played == max_power])"}}},
        {"adjust": {"players": {"where": "you.seat == trick_winner"}, "key": "tricks_won", "value": 1}},
        {"adjust": {"players": {"where": "you.seat == trick_winner and you.played == skull_king_power"}, "key": "bonus", "value": {"calc": "skull_king_bonus_per_pirate * pirates_in_trick"}, "if": {"calc": "pirates_in_trick > 0"}, "text": "The Skull King captures Pirates: seat {player} earns a bonus."}},
        {"adjust": {"players": {"where": "you.seat == trick_winner and you.played == mermaid_power"}, "key": "bonus", "value": {"calc": "mermaid_captures_skull_king_bonus"}, "if": {"calc": "skull_king_played"}, "text": "The Mermaid captures the Skull King: seat {player} earns a bonus."}},
        {"adjust": {"key": "trick", "value": 1}},
        {"set": {"players": "all", "key": "choice", "value": ""}}
      ],
      "text": "Trick {trick}: cards played [seat, power]: {[[p.seat, p.played] for p in players]}. Seat {trick_winner} wins the trick."
    },
    {
      "use": "poll",
      "phase": "play",
      "label": "play trick 2",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "choice",
      "text": "Trick 2 of {tricks_per_round}: play one card from your hand. Cards are shown by power: 0 Escape, 1-12 numbers, 20 Mermaid, 30 Pirate A, 31 Pirate B, 40 Skull King. All cards are revealed together."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve trick 2",
      "do": [
        {"set": {"players": "all", "key": "played", "value": {"calc": "int(you.choice)"}}},
        {"remove": {"players": "all", "key": "hand", "value": {"calc": "you.played"}}},
        {"set": {"key": "mermaid_played", "value": {"calc": "any(p.played == mermaid_power for p in players)"}}},
        {"set": {"key": "skull_king_played", "value": {"calc": "any(p.played == skull_king_power for p in players)"}}},
        {"set": {"key": "pirates_in_trick", "value": {"calc": "count(p.played == pirate_a_power or p.played == pirate_b_power for p in players)"}}},
        {"set": {"key": "max_power", "value": {"calc": "max([p.played for p in players])"}}},
        {"set": {"key": "trick_winner", "value": {"calc": "min([p.seat for p in players if p.played == mermaid_power]) if (mermaid_played and skull_king_played) else min([p.seat for p in players if p.played == max_power])"}}},
        {"adjust": {"players": {"where": "you.seat == trick_winner"}, "key": "tricks_won", "value": 1}},
        {"adjust": {"players": {"where": "you.seat == trick_winner and you.played == skull_king_power"}, "key": "bonus", "value": {"calc": "skull_king_bonus_per_pirate * pirates_in_trick"}, "if": {"calc": "pirates_in_trick > 0"}, "text": "The Skull King captures Pirates: seat {player} earns a bonus."}},
        {"adjust": {"players": {"where": "you.seat == trick_winner and you.played == mermaid_power"}, "key": "bonus", "value": {"calc": "mermaid_captures_skull_king_bonus"}, "if": {"calc": "skull_king_played"}, "text": "The Mermaid captures the Skull King: seat {player} earns a bonus."}},
        {"adjust": {"key": "trick", "value": 1}},
        {"set": {"players": "all", "key": "choice", "value": ""}}
      ],
      "text": "Trick {trick}: cards played [seat, power]: {[[p.seat, p.played] for p in players]}. Seat {trick_winner} wins the trick."
    },
    {
      "use": "poll",
      "phase": "play",
      "label": "play trick 3",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "store": "choice",
      "text": "Trick 3 of {tricks_per_round}: play your last card. Cards are shown by power: 0 Escape, 1-12 numbers, 20 Mermaid, 30 Pirate A, 31 Pirate B, 40 Skull King. All cards are revealed together."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve trick 3",
      "do": [
        {"set": {"players": "all", "key": "played", "value": {"calc": "int(you.choice)"}}},
        {"remove": {"players": "all", "key": "hand", "value": {"calc": "you.played"}}},
        {"set": {"key": "mermaid_played", "value": {"calc": "any(p.played == mermaid_power for p in players)"}}},
        {"set": {"key": "skull_king_played", "value": {"calc": "any(p.played == skull_king_power for p in players)"}}},
        {"set": {"key": "pirates_in_trick", "value": {"calc": "count(p.played == pirate_a_power or p.played == pirate_b_power for p in players)"}}},
        {"set": {"key": "max_power", "value": {"calc": "max([p.played for p in players])"}}},
        {"set": {"key": "trick_winner", "value": {"calc": "min([p.seat for p in players if p.played == mermaid_power]) if (mermaid_played and skull_king_played) else min([p.seat for p in players if p.played == max_power])"}}},
        {"adjust": {"players": {"where": "you.seat == trick_winner"}, "key": "tricks_won", "value": 1}},
        {"adjust": {"players": {"where": "you.seat == trick_winner and you.played == skull_king_power"}, "key": "bonus", "value": {"calc": "skull_king_bonus_per_pirate * pirates_in_trick"}, "if": {"calc": "pirates_in_trick > 0"}, "text": "The Skull King captures Pirates: seat {player} earns a bonus."}},
        {"adjust": {"players": {"where": "you.seat == trick_winner and you.played == mermaid_power"}, "key": "bonus", "value": {"calc": "mermaid_captures_skull_king_bonus"}, "if": {"calc": "skull_king_played"}, "text": "The Mermaid captures the Skull King: seat {player} earns a bonus."}},
        {"adjust": {"key": "trick", "value": 1}},
        {"set": {"players": "all", "key": "choice", "value": ""}}
      ],
      "text": "Trick {trick}: cards played [seat, power]: {[[p.seat, p.played] for p in players]}. Seat {trick_winner} wins the trick."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "score the round",
      "when": {
        "calc": "trick >= tricks_per_round"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "((exact_bid_points_per_trick * you.bid + you.bonus) if you.tricks_won == you.bid else -(missed_bid_penalty_per_trick * abs(you.tricks_won - you.bid))) if you.bid >= 1 else (zero_bid_success_points if you.tricks_won == 0 else -zero_bid_failure_penalty)"
            }
          }
        }
      ],
      "text": "Round {round} scored. [seat, bid, tricks won, bonus]: {[[p.seat, p.bid, p.tricks_won, p.bonus] for p in players]}. Scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after the last round",
      "when": {
        "calc": "round >= rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= rounds"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 8,
    "rounds_max": 10,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "The game lasts {rounds} rounds. Every player's score starts at 0.\n\nThe deck has {deck_size} cards, each identified by its power: number cards {number_card_min} to {number_card_max} (one of each); {escape_count} Escapes of power {escape_power}; one Mermaid, power {mermaid_power}; Pirate A, power {pirate_a_power}; Pirate B, power {pirate_b_power}; and the Skull King, power {skull_king_power}.\n\nEach round all {deck_size} cards are gathered and shuffled, and {hand_size} cards are dealt to each player, one at a time in seat order. Your hand is private: only you see it. The undealt cards are never revealed.\n\nBID: all players bid at the same time, choosing a whole number from {bid_min} to {bid_max}: how many of the {tricks_per_round} tricks you will win. Nobody sees another bid until all bids are in; then every bid is announced to everyone.\n\nThen {tricks_per_round} tricks are played. In each trick every player at the same time plays one card from their own hand; the card leaves the hand, and all played cards are revealed together. If both the Mermaid and the Skull King were played, the Mermaid's player wins the trick. Otherwise the player of the highest-power card wins. The winner adds 1 to their tricks won. If the Skull King won the trick, its player gains a bonus of {skull_king_bonus_per_pirate} for each Pirate played in that trick (no Pirate, no bonus). If the Mermaid won the trick and the Skull King was played in it, the Mermaid's player gains a bonus of {mermaid_captures_skull_king_bonus}.\n\nSCORING after the three tricks: if you bid 1, 2 or 3 and your tricks won equal your bid, you gain {exact_bid_points_per_trick} times your bid plus your bonus. If you bid 1, 2 or 3 and your tricks won differ from your bid, you lose {missed_bid_penalty_per_trick} times the difference, and your bonus is not scored. If you bid 0 and won no tricks, you gain {zero_bid_success_points}. If you bid 0 and won 1 or more tricks, you lose {zero_bid_failure_penalty}. Bonuses and tricks won reset each round.\n\nThere is no discussion. After round {rounds}, the highest total score wins; players tied for the highest share the win."
}
```
````
