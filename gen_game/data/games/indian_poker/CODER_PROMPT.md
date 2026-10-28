# Task: write the XColos game file for "Forehead Poker Match"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 6; set `meta.players` to {"min": 4, "max": 6, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP: Each player starts with 40 chips. The pot starts at 0. The match lasts 16 hands.

CARD STRENGTH: A standard 52-card deck is used. Rank from high to low is A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2. Between equal ranks, suit decides, from high to low: Spades, Hearts, Diamonds, Clubs. No two cards are ever equal.

EACH HAND:
1. ELIGIBILITY: Any active player with fewer than 4 chips is eliminated. They take no further part, and their current chips are their final total.
2. DEAL: The full deck is shuffled and one card is dealt to each active player. Each player is privately told the card of every other active player, but never their own.
3. ANTE: Each active player pays 1 chip into the pot.
4. TALK: Every active player writes one short message (at most 40 words) at the same moment, without seeing the others. All messages are then shown to everyone. Messages may say anything, including claims about anyone's card, and none of them binds anyone.
5. FIRST BET: Every active player, at the same moment, chooses one option: Fold, Bet 1, Bet 2 or Bet 3. A player who bets pays that many chips into the pot immediately. A player who folds is out of this hand and has lost only the ante.
6. REVEAL BETS: Every player's choice from step 5 is shown to everyone. Let H be the highest bet made.
7. CALL OR FOLD: Every player who bet in step 5, at the same moment, chooses Call or Fold. Calling costs H minus that player's own step-5 bet, paid into the pot. A player whose bet was already H calls for free. Folding forfeits everything that player has put in this hand.
8. SHOWDOWN: Find the players who called.
   - Two or more callers: their cards are compared, and the caller with the strongest card wins the whole pot.
   - Exactly one caller: that player wins the whole pot without comparison.
   - No callers: the pot stays and carries over to the next hand.
   All cards are then revealed to everyone, so players can check what was said and bet.
9. Winnings are added to the winner's chips, the pot resets to 0 (unless it carried over), and the next hand begins.

END: The match ends after hand 16, or earlier if only one player is still active. Any pot remaining at that moment is discarded.

How the winner is decided: The player with the most chips at the end of the match wins. Eliminated players count with the chips they held when eliminated. If two or more players tie for the most chips, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Forehead Poker Match (4 to 6 players, best with 4)

Over 16 hands, each player sees every other player's card but never their own, talks, bets and calls; the player with the most chips at the end wins.

STATE (every item below must exist in the file):
  - each player: chips (number, starts 40); everyone sees it. The player's chip stack. This is the score. It freezes when the player is eliminated.
  - each player: active (bool, starts True); everyone sees it. Whether the player is still in the match. It becomes false when the player starts a hand with fewer than 4 chips.
  - each player: card (text, starts ''); everyone but its owner sees it. The card dealt this hand, such as 'Q of Hearts'. Every other player sees it; the owner does not.
  - each player: card_value (number, starts 0); everyone but its owner sees it. The card's strength from 1 (2 of Clubs) to 52 (A of Spades), worked out as rank_index*4 + suit_index. rank_index runs 0 for 2 up to 12 for A. suit_index is Clubs 1, Diamonds 2, Hearts 3, Spades 4. It is 0 when no card is held.
  - each player: bet (number, starts 0); everyone sees it. The step-5 bet this hand: 0 for a fold, otherwise 1 to 3.
  - each player: folded (bool, starts False); everyone sees it. Whether the player folded in step 5 or step 7 of this hand.
  - each player: called (bool, starts False); everyone sees it. Whether the player called in step 7 of this hand.
  - each player: shown_card (text, starts ''); everyone sees it. The player's card, revealed to everyone after the showdown. It is empty before then.
  - the table: deck (list, starts 'the 52 standard cards'); hidden from all players. The shuffled deck that cards are dealt from. It is refilled to all 52 cards every hand.
  - the table: pot (number, starts 0); everyone sees it. The chips in the pot. It carries over when nobody calls.
  - the table: hand_number (number, starts 0); everyone sees it. The number of hands completed so far.
  - the table: high_bet (number, starts 0); everyone sees it. H, the highest step-5 bet this hand. It is 0 if everyone folded.
  - the table: caller_count (number, starts 0); everyone sees it. How many players called in step 7.
  - the table: best_value (number, starts 0); hidden from all players. The highest card_value among this hand's callers. It is 0 if there are no callers.
  - parameters, each kept as a table attribute: starting_chips = 40, starting_pot = 0, hands = 16, elimination_below = 4, ante = 1, bet_min = 1, bet_max = 3, message_max_words = 40, deck_size = 52, cards_per_player = 1, suits_per_rank = 4

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Each player gets 40 chips and is marked active.
  2. The pot is set to 0 and hand_number to 0.
  3. The deck list is filled with the 52 standard cards.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: ELIGIBILITY: every active player with chips < 4 gets active = false, and their chips stay as their final total. Then every player is reset for the hand: bet = 0, folded = false, called = false, card = '', card_value = 0, shown_card = ''. On the table, high_bet, caller_count and best_value are set to 0.
  2. [check] all players. What happens: The game ends if the number of players with active = true is 1 or fewer. Any pot is discarded.
  3. [update] all players. What happens: DEAL: deck is reset to all 52 cards. Each active player draws one card at random: it is removed from deck and its name is set as card, with its strength as card_value.
  4. [sync] all players. What happens: Each player is sent their state. They see the card and card_value of every other active player, but not their own.
  5. [update] all players. What happens: ANTE: each active player pays 1: chips -= 1 and pot += 1.
  6. [poll] every active player answers: short text, at most 40 words. What happens: TALK: once every message is in, each one is broadcast to all as 'Seat {seat} says: {value}'. No message binds anyone.
  7. [poll] every active player answers: one of: Fold, Bet 1, Bet 2, Bet 3. What happens: FIRST BET: answers are collected simultaneously and stored. Nothing is shown until all are in.
  8. [update] every active player. What happens: On Fold: bet = 0 and folded = true. On Bet k: bet = k, chips -= k and pot += k. Then high_bet = the largest bet among active players.
  9. [tell] all players. What happens: REVEAL BETS: every player's step-5 choice (bet or fold) and H = high_bet are announced to everyone.
  10. [poll] every active player with bet >= 1 answers: one of: Call, Fold. What happens: CALL OR FOLD: answers are collected simultaneously. This step is skipped if nobody bet.
  11. [update] every player asked in the previous step. What happens: On Call: called = true, chips -= (high_bet - bet) and pot += (high_bet - bet); the cost is 0 if bet = high_bet. On Fold: folded = true, and nothing put in this hand is returned. Then caller_count = the number of players with called = true, and best_value = the highest card_value among players with called = true (0 if there are none).
  12. [update] all players. What happens: SHOWDOWN: if caller_count >= 1, the player with called = true and card_value = best_value gets chips += pot, and then pot = 0. If caller_count = 0, pot is unchanged and carries over. Every player who was dealt a card gets shown_card = card. Then hand_number += 1.
  13. [tell] all players. What happens: All cards (shown_card), the callers, the winner of the pot (or that it carried over), the pot and everyone's chips are announced.
  14. [check] all players. What happens: The game ends if hand_number >= 16 or the number of players with active = true is 1 or fewer. Any remaining pot is discarded.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the match starts, then each player has 40 chips, the pot is 0 and hand_number is 0.
  R2. When a hand begins and an active player has fewer than 4 chips, then that player becomes inactive, takes no further part, and keeps those chips as their final total.
  R3. When a hand begins and an active player has 4 or more chips, then that player stays active.
  R4. When a hand is dealt, then the deck is refilled to 52 cards and each active player receives exactly one card, removed from the deck.
  R5. When cards are dealt, then each player can see the card of every other active player but never their own.
  R6. When cards are compared, then rank decides first (A high, 2 low) and suit breaks ties (Spades > Hearts > Diamonds > Clubs), so the A of Spades is strongest and the 2 of Clubs weakest.
  R7. When the ante is taken, then each active player loses 1 chip and the pot grows by 1 per active player.
  R8. When talk happens, then every active player submits one message of at most 40 words simultaneously, and all messages are then shown to everyone.
  R9. When a player chooses Bet k (k = 1, 2 or 3) in the first bet, then their chips fall by k and the pot rises by k immediately.
  R10. When a player folds in the first bet, then they are out of the hand, have lost only the 1-chip ante, and are not asked to call.
  R11. When all first bets are in, then every choice is revealed to everyone and H is the highest bet made.
  R12. When a player who bet b calls, then they pay H - b chips into the pot, which is 0 if b = H.
  R13. When a player who bet folds at the call step, then they forfeit everything they put in this hand and nothing is returned.
  R14. When two or more players call, then the caller with the highest card strength wins the whole pot and the pot becomes 0.
  R15. When exactly one player calls, then that player wins the whole pot without comparison and the pot becomes 0.
  R16. When no player calls (including when everyone folded in the first bet), then the pot stays and carries over to the next hand.
  R17. When the showdown ends, then every dealt card is revealed to everyone.
  R18. When 16 hands have been completed, then the match ends and any remaining pot is discarded.
  R19. When only one or no player is active, then the match ends early and any remaining pot is discarded.
  R20. When the match ends, then the player with the most chips wins, eliminated players count with their chips at elimination, and players tied for the most share a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - TALK message | asked: every active player | options: free text of at most 40 words. Eliminated players are not asked.
  - FIRST BET | asked: every active player | options: Fold, Bet 1, Bet 2, Bet 3 (every active player has at least 3 chips after the ante, so all four are always affordable). Eliminated players are not asked.
  - CALL OR FOLD | asked: every active player whose step-5 bet was 1, 2 or 3 | options: Call, Fold. Players who folded in step 5 and eliminated players are not asked.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_number >= 16 or (count of players with active = true) <= 1
  - each player's standing: you.chips (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their chips at the end. Eliminated players count with the chips they held when eliminated. The most chips wins, and players tied for the most share a draw.
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

When only one option is left (the last unused action, the only legal card), still ask the question: the engine answers a choice with one
option for the seat, with no model call, and records it as the seat's move. Do not skip the question with a `when` and set the answer
yourself: that move is then missing from the match, and a test that scripts it fails.

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

- each player: `chips` (number, visible: public, starts 40): The player's chip stack. This is the score. It freezes when the player is eliminated.
- each player: `active` (bool, visible: public, starts True): Whether the player is still in the match. It becomes false when the player starts a hand with fewer than 4 chips.
- each player: `shown_card` (text, visible: public, starts ''): The player's card, revealed to everyone after the showdown. It is empty before then.
- the table: `pot` (number, visible: public, starts 0): The chips in the pot. It carries over when nobody calls.
- the table: `hand_number` (number, visible: public, starts 0): The number of hands completed so far.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_chips = 40, starting_pot = 0, hands = 16, elimination_below = 4, ante = 1, bet_min = 1, bet_max = 3, message_max_words = 40, deck_size = 52, cards_per_player = 1, suits_per_rank = 4
- the game ends with ONE ending whose `rank_by` is `you.chips`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
