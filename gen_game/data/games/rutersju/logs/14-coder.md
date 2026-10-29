# 14 coder

- time: 2026-10-28T03:38:23+00:00 (90.2s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 de67cf540e0af668, reply sha256 2f32744b5836d40a

## Sent

````
# Task: write the XColos game file for "Rutersju Twelve"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

CARDS. Use a 36-card pack with four suits (spades, hearts, diamonds, clubs). Each suit has the ranks A, K, Q, J, 10, 9, 8, 7, 6, from high to low. The diamond 7 is special: it wins any trick it is played to. Otherwise it is a diamond.

SEATS. Players sit in a fixed clockwise order, and every player starts at 0 points. The game lasts exactly 12 deals. In deal 1, seat 1 bids first. In each later deal, the first bidder is the next seat clockwise from the previous deal's first bidder.

EACH DEAL.
1. Deal. Shuffle all 36 cards and deal 3 cards face down to each player. Each player sees only their own hand. The remaining cards stay unseen for the whole deal.
2. Bid. Starting with the first bidder and going clockwise, each player in turn announces a bid of 0, 1, 2 or 3. All bids are public as soon as they are made. Every player must bid; there is no passing.
3. Declarer. The player with the highest bid becomes the declarer. If several players tie for the highest bid, the one of them who bid last becomes the declarer. The declarer's bid is the contract. All other players are opponents for this deal.
4. Play three tricks. The declarer leads the first trick. In each trick, the leader plays one card face up. Then each other player in clockwise order plays one card face up. A player who holds a card of the led suit must play a card of that suit. A player with none may play any card. If the diamond 7 is in the trick, its player wins the trick. Otherwise the highest card of the led suit wins. Each player's tricks are counted separately. The winner of a trick leads the next one. All played cards stay visible to everyone.
5. Score. Count the declarer's tricks.
   - If the declarer took exactly the contract, the declarer scores the contract plus 1 point. A contract of 0 made scores 1; a contract of 3 made scores 4.
   - If the declarer took more or fewer tricks than the contract, every opponent scores points equal to the difference between the contract and the declarer's tricks. The declarer scores nothing.
   - Opponents' own tricks are never scored.
6. Announce. Announce every player's total. Then start the next deal.

There is no discussion at any time. Players communicate only through their bids and the cards they play.

END. After the 12th deal is scored, the game ends.

How the winner is decided: After 12 deals, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Rutersju Twelve (3 to 4 players, best with 4)

A 12-deal trick-taking game: each player is dealt 3 cards, players bid 0 to 3 in turn, the highest bidder plays to take exactly that many tricks, and the opponents score when the declarer misses.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Total points so far.
  - each player: hand (list, starts []); only its owner sees it. Cards held this deal, such as 'AS' or '7D'. Only the owner sees them.
  - each player: bid (number, starts 0); everyone sees it. This deal's bid, from 0 to 3.
  - each player: tricks (number, starts 0); everyone sees it. Tricks won this deal.
  - each player: is_declarer (bool, starts False); everyone sees it. Whether this player is the declarer this deal.
  - the table: deck (list, starts 'all 36 cards: ranks A,K,Q,J,10,9,8,7,6 in suits S,H,D,C'); hidden from all players. Undealt cards. They stay unseen for the whole deal.
  - the table: deal_number (number, starts 0); everyone sees it. Number of the current deal, from 1 to 12.
  - the table: first_bidder (number, starts 0); everyone sees it. Seat that bids first this deal.
  - the table: high_bid (number, starts -1); everyone sees it. Highest bid made so far this deal.
  - the table: declarer_seat (number, starts 0); everyone sees it. Seat of the declarer this deal.
  - the table: contract (number, starts 0); everyone sees it. The declarer's bid.
  - the table: trick_number (number, starts 0); everyone sees it. Number of tricks completed this deal.
  - the table: leader_seat (number, starts 0); everyone sees it. Seat that leads the current trick.
  - the table: led_suit (text, starts ''); everyone sees it. Suit of the first card in the current trick.
  - the table: trick_cards (list, starts []); everyone sees it. Entries of the form seat:card for the trick in progress.
  - the table: played_cards (list, starts []); everyone sees it. Every card played this deal, visible to everyone.
  - parameters, each kept as a table attribute: deck_size = 36, suits = 4, ranks_per_suit = 9, hand_size = 3, tricks_per_deal = 3, deals = 12, bid_min = 0, bid_max = 3, made_bonus = 1, starting_score = 0, first_bidder_deal_1 = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are numbered 1 to N in clockwise order.
  2. Every player's score is set to 0.
  3. deal_number is set to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Add 1 to deal_number. Set first_bidder = ((deal_number - 1) mod N) + 1. Refill deck with all 36 cards. For every player, clear hand and set bid = 0, tricks = 0 and is_declarer = false. Set high_bid = -1, declarer_seat = 0, contract = 0, trick_number = 0 and led_suit = ''. Clear trick_cards and played_cards.
  2. [update] all players. What happens: Deal 3 cards to each player. Each card is drawn at random from deck, appended to that player's hand and removed from deck.
  3. [sync] all players. What happens: Each player is shown their own hand, plus deal_number, first_bidder and every score.
  4. [ask] each player in turn, clockwise, starting at first_bidder answers: a whole number from 0 to 3. What happens: Set the player's bid to the answer and broadcast it to all. If bid >= high_bid, set high_bid = bid and declarer_seat = the player's seat. Because the comparison is >=, a later equal bid takes the declarership.
  5. [update] all players. What happens: Set contract = high_bid and leader_seat = declarer_seat. Set is_declarer = true for the player at declarer_seat. Announce the declarer and the contract.
  6. [ask] each player in turn, clockwise, starting at leader_seat answers: one card from the player's hand, chosen from the legal cards (see offers). What happens: Remove the card from hand and append seat:card to trick_cards and to played_cards. If this is the first card of the trick, set led_suit to its suit. Broadcast the played card to all.
  7. [update] all players. What happens: If trick_cards contains 7D, its player wins the trick. Otherwise the highest-ranked card of led_suit wins (A>K>Q>J>10>9>8>7>6). Add 1 to the winner's tricks, set leader_seat = the winner's seat, add 1 to trick_number, clear trick_cards and set led_suit = ''. Announce the trick winner.
  8. [repeat] all players. What happens: Run the two previous steps (play a trick, resolve the trick) again until trick_number = 3.
  9. [update] all players. What happens: Let D be the player with is_declarer = true. If D.tricks = contract, add contract + 1 to D.score. Otherwise add |contract - D.tricks| to the score of every player with is_declarer = false, and D scores nothing. Opponents' own tricks are not scored.
  10. [tell] all players. What happens: Announce every player's score after deal {deal_number}.
  11. [check] all players. What happens: End the game if deal_number = 12. Otherwise continue with the next deal.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a game starts, then every player's score is 0.
  R2. When a deal starts, then all 36 cards are shuffled into deck and each player receives exactly 3 cards in hand, seen only by that player.
  R3. When cards are dealt, then the 36 - 3N undealt cards stay in deck, unseen by every player for the whole deal.
  R4. When deal 1 starts, then seat 1 bids first; when deal k > 1 starts, then the first bidder is the seat clockwise from the previous first bidder, so first_bidder = ((k - 1) mod N) + 1.
  R5. When bidding, then every player bids exactly once, in clockwise order from first_bidder, with a whole number from 0 to 3, and there is no pass.
  R6. When a bid is made, then it is shown to every player at once.
  R7. When bidding ends, then the player with the highest bid is declarer and contract equals that bid.
  R8. When two or more players tie for the highest bid, then the one of them who bid last is declarer (for example, bids 2, 2, 1, 0 in bidding order make the second bidder declarer).
  R9. When the first trick of a deal begins, then the declarer leads it.
  R10. When a player holds a card of the led suit, then that player must play a card of the led suit.
  R11. When a player holds no card of the led suit, then that player may play any card in hand.
  R12. When the diamond 7 is in a trick, then its player wins the trick, whatever suit was led.
  R13. When the diamond 7 is not in a trick, then the highest card of the led suit wins, ranking A>K>Q>J>10>9>8>7>6, and cards of other suits never win.
  R14. When a trick is won, then the winner's tricks increases by 1 and the winner leads the next trick.
  R15. When a deal is played, then exactly 3 tricks are played, and every played card stays visible to all players.
  R16. When the declarer's tricks equal the contract, then the declarer scores contract + 1 (a contract of 0 made scores 1, a contract of 3 made scores 4) and the opponents score 0.
  R17. When the declarer's tricks differ from the contract, then each opponent scores |contract - declarer tricks| and the declarer scores 0 (for example, contract 3 with 1 trick gives each opponent 2).
  R18. When scoring, then opponents' own tricks add nothing.
  R19. When a deal is scored, then every player's total is announced.
  R20. When the 12th deal is scored, then the game ends and the highest total score wins; if several players tie for the highest total, the game is a draw.
  R21. When playing, then no player may send a message; players communicate only through bids and cards.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid | asked: each player in turn from first_bidder | options: Every player is offered 0, 1, 2 or 3. No pass is offered.
  - Play a card (leader of a trick) | asked: the seat at leader_seat | options: Any card in their hand.
  - Play a card (non-leader) | asked: each other seat in clockwise order | options: A seat holding one or more cards of led_suit is offered only those cards. A seat holding no card of led_suit is offered every card in its hand.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: deal_number = 12 after the 12th deal is scored
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total score after 12 deals. The highest total wins. Players tied for the highest total share the result, which the source calls a draw.
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

- each player: `score` (number, visible: public, starts 0): Total points so far.
- each player: `bid` (number, visible: public, starts 0): This deal's bid, from 0 to 3.
- each player: `tricks` (number, visible: public, starts 0): Tricks won this deal.
- each player: `is_declarer` (bool, visible: public, starts False): Whether this player is the declarer this deal.
- the table: `deal_number` (number, visible: public, starts 0): Number of the current deal, from 1 to 12.
- the table: `declarer_seat` (number, visible: public, starts 0): Seat of the declarer this deal.
- the table: `contract` (number, visible: public, starts 0): The declarer's bid.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 36, suits = 4, ranks_per_suit = 9, hand_size = 3, tricks_per_deal = 3, deals = 12, bid_min = 0, bid_max = 3, made_bonus = 1, starting_score = 0, first_bidder_deal_1 = 1
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

Make each round one whole deal. Increment deal_number and set first_bidder = ((deal_number-1) mod N)+1. Shuffle and deal hand_size cards to each player. Run the sequential bid poll starting from first_bidder. Set the declarer to the last of the highest bidders, and set contract and is_declarer. Then play tricks_per_deal tricks using counted repetition, not one trick per round: in each trick the leader plays first, then the others follow clockwise, following suit where possible. The 7 of diamonds wins any trick it is in, otherwise the highest card of the led suit wins, and the trick winner leads the next trick. Score at the end of the same round. By then every hand is empty, the deck holds 36 - 3N cards, and the round count equals deal_number, with deals = 12 as the fixed number of rounds. Reset bid, tricks and is_declarer at the start of each deal.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "rutersju_twelve",
    "name": "Rutersju Twelve",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Twelve deals of three cards: bid 0 to 3, the highest bidder must take exactly that many tricks, and the opponents score when the declarer misses."
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
        "key": "tricks",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "is_declarer",
        "visible": "public",
        "type": "bool",
        "initial": false
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
          "AS", "KS", "QS", "JS", "10S", "9S", "8S", "7S", "6S",
          "AH", "KH", "QH", "JH", "10H", "9H", "8H", "7H", "6H",
          "AD", "KD", "QD", "JD", "10D", "9D", "8D", "7D", "6D",
          "AC", "KC", "QC", "JC", "10C", "9C", "8C", "7C", "6C"
        ]
      },
      {
        "key": "all_cards",
        "visible": "none",
        "type": "list",
        "initial": [
          "AS", "KS", "QS", "JS", "10S", "9S", "8S", "7S", "6S",
          "AH", "KH", "QH", "JH", "10H", "9H", "8H", "7H", "6H",
          "AD", "KD", "QD", "JD", "10D", "9D", "8D", "7D", "6D",
          "AC", "KC", "QC", "JC", "10C", "9C", "8C", "7C", "6C"
        ]
      },
      {
        "key": "rank_table",
        "visible": "none",
        "type": "list",
        "initial": [
          ["A", 8],
          ["K", 7],
          ["Q", 6],
          ["J", 5],
          ["1", 4],
          ["9", 3],
          ["8", 2],
          ["7", 1],
          ["6", 0]
        ]
      },
      {
        "key": "deal_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_bidder",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_bid",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "declarer_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "contract",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trick_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "played_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ranks_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deals",
        "visible": "public",
        "type": "number",
        "initial": 12
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
        "key": "made_bonus",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_bidder_deal_1",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "dealt_rounds",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "turn_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bids_made",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "plays_in_trick",
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
        "key": "cur_str",
        "visible": "none",
        "type": "number",
        "initial": -1
      },
      {
        "key": "best_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "best_strength",
        "visible": "none",
        "type": "number",
        "initial": -1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the start",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "key": "deal_number",
            "value": 0
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
      "label": "a new deal",
      "do": [
        {
          "adjust": {
            "key": "deal_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "first_bidder",
            "value": {
              "calc": "(first_bidder_deal_1 - 1 + deal_number - 1) % len(players) + 1"
            }
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
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "is_declarer",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": []
          }
        },
        {
          "set": {
            "key": "high_bid",
            "value": -1
          }
        },
        {
          "set": {
            "key": "declarer_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "contract",
            "value": 0
          }
        },
        {
          "set": {
            "key": "trick_number",
            "value": 0
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": ""
          }
        },
        {
          "set": {
            "key": "trick_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "played_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "dealt_rounds",
            "value": 0
          }
        },
        {
          "set": {
            "key": "bids_made",
            "value": 0
          }
        },
        {
          "set": {
            "key": "plays_in_trick",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_strength",
            "value": -1
          }
        },
        {
          "set": {
            "key": "turn_seat",
            "value": {
              "calc": "first_bidder"
            }
          }
        }
      ],
      "text": "Deal {deal_number} of {deals} begins. Seat {first_bidder} bids first."
    },
    {
      "use": "repeat",
      "phase": "deal",
      "label": "dealing",
      "until": {
        "calc": "dealt_rounds >= hand_size"
      },
      "max": 10,
      "steps": [
        {
          "use": "update",
          "phase": "deal",
          "label": "one card to each player",
          "do": [
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
                "player": 3,
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
                },
                "if": {
                  "calc": "len(players) >= 4"
                }
              }
            },
            {
              "append": {
                "player": 4,
                "key": "hand",
                "value": {
                  "calc": "pick"
                },
                "if": {
                  "calc": "len(players) >= 4"
                }
              }
            },
            {
              "remove": {
                "key": "deck",
                "value": {
                  "calc": "pick"
                },
                "if": {
                  "calc": "len(players) >= 4"
                }
              }
            },
            {
              "adjust": {
                "key": "dealt_rounds",
                "value": 1
              }
            }
          ]
        }
      ]
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "text": "Deal {deal_number}: your hand and the table."
    },
    {
      "use": "repeat",
      "phase": "bid",
      "label": "the bidding",
      "until": {
        "calc": "bids_made >= len(players)"
      },
      "max": 10,
      "steps": [
        {
          "use": "ask",
          "phase": "bid",
          "label": "bid",
          "to": {
            "where": "you.seat == turn_seat"
          },
          "answer": {
            "type": "number",
            "min": {
              "calc": "bid_min"
            },
            "max": {
              "calc": "bid_max"
            }
          },
          "each": {
            "do": [
              {
                "set": {
                  "player": "$seat",
                  "key": "bid",
                  "value": "$answer"
                }
              },
              {
                "set": {
                  "key": "declarer_seat",
                  "value": "$seat",
                  "if": {
                    "calc": "$answer >= high_bid"
                  }
                }
              },
              {
                "set": {
                  "key": "high_bid",
                  "value": {
                    "calc": "max(high_bid, $answer)"
                  }
                }
              },
              {
                "adjust": {
                  "key": "bids_made",
                  "value": 1
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} bids {value}."
          },
          "text": "Deal {deal_number}: bid how many of the 3 tricks you will take, a whole number from {bid_min} to {bid_max}. The highest bid so far is {high_bid} (-1 means no bid yet). The highest bidder becomes declarer; on a tie for highest, the one who bid last is declarer. There is no pass."
        },
        {
          "use": "update",
          "phase": "bid",
          "label": "next bidder",
          "do": [
            {
              "set": {
                "key": "turn_seat",
                "value": {
                  "calc": "turn_seat % len(players) + 1"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the declarer",
      "do": [
        {
          "set": {
            "key": "contract",
            "value": {
              "calc": "high_bid"
            }
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "declarer_seat"
            }
          }
        },
        {
          "set": {
            "key": "turn_seat",
            "value": {
              "calc": "declarer_seat"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == declarer_seat"
            },
            "key": "is_declarer",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "you.hand"
            }
          }
        }
      ],
      "text": "Seat {declarer_seat} is the declarer with a contract of {contract} and leads the first trick."
    },
    {
      "use": "repeat",
      "phase": "play",
      "label": "trick 1",
      "until": {
        "calc": "plays_in_trick >= len(players)"
      },
      "max": 10,
      "steps": [
        {
          "use": "ask",
          "phase": "play",
          "label": "trick 1 card",
          "to": {
            "where": "you.seat == turn_seat"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "each": {
            "do": [
              {
                "set": {
                  "key": "cur_card",
                  "value": "$answer"
                }
              },
              {
                "set": {
                  "key": "led_suit",
                  "value": {
                    "calc": "cur_card[-1]"
                  },
                  "if": {
                    "calc": "plays_in_trick == 0"
                  }
                }
              },
              {
                "set": {
                  "key": "cur_str",
                  "value": {
                    "calc": "100 if cur_card == '7D' else (sum([p[1] for p in rank_table if p[0] == cur_card[0]]) if cur_card[-1] == led_suit else -1)"
                  }
                }
              },
              {
                "set": {
                  "key": "best_seat",
                  "value": "$seat",
                  "if": {
                    "calc": "cur_str > best_strength"
                  }
                }
              },
              {
                "set": {
                  "key": "best_strength",
                  "value": {
                    "calc": "max(best_strength, cur_str)"
                  }
                }
              },
              {
                "remove": {
                  "player": "$seat",
                  "key": "hand",
                  "value": "$answer"
                }
              },
              {
                "append": {
                  "key": "trick_cards",
                  "value": {
                    "calc": "['1', '2', '3', '4'][turn_seat - 1] + ':' + cur_card"
                  }
                }
              },
              {
                "append": {
                  "key": "played_cards",
                  "value": {
                    "calc": "['1', '2', '3', '4'][turn_seat - 1] + ':' + cur_card"
                  }
                }
              },
              {
                "adjust": {
                  "key": "plays_in_trick",
                  "value": 1
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} plays {value}."
          },
          "text": "Deal {deal_number}, trick 1. Cards in this trick: {trick_cards}. Led suit: {led_suit} (empty means you lead). Play one card; you are offered only legal cards (you must follow the led suit if you can, otherwise any card). The 7 of diamonds wins any trick; otherwise the highest card of the led suit wins."
        },
        {
          "use": "update",
          "phase": "play",
          "label": "trick 1 next player",
          "do": [
            {
              "set": {
                "key": "turn_seat",
                "value": {
                  "calc": "turn_seat % len(players) + 1"
                }
              }
            },
            {
              "set": {
                "players": "all",
                "key": "offer",
                "value": {
                  "calc": "[c for c in you.hand if c[-1] == led_suit] if len([c for c in you.hand if c[-1] == led_suit]) > 0 else you.hand"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "play",
      "label": "trick 1 is won",
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "best_seat"
            },
            "key": "tricks",
            "value": 1,
            "text": "Seat {player} wins the trick and leads next."
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "best_seat"
            }
          }
        },
        {
          "set": {
            "key": "turn_seat",
            "value": {
              "calc": "best_seat"
            }
          }
        },
        {
          "adjust": {
            "key": "trick_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": ""
          }
        },
        {
          "set": {
            "key": "plays_in_trick",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_strength",
            "value": -1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "repeat",
      "phase": "play",
      "label": "trick 2",
      "until": {
        "calc": "plays_in_trick >= len(players)"
      },
      "max": 10,
      "steps": [
        {
          "use": "ask",
          "phase": "play",
          "label": "trick 2 card",
          "to": {
            "where": "you.seat == turn_seat"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "each": {
            "do": [
              {
                "set": {
                  "key": "cur_card",
                  "value": "$answer"
                }
              },
              {
                "set": {
                  "key": "led_suit",
                  "value": {
                    "calc": "cur_card[-1]"
                  },
                  "if": {
                    "calc": "plays_in_trick == 0"
                  }
                }
              },
              {
                "set": {
                  "key": "cur_str",
                  "value": {
                    "calc": "100 if cur_card == '7D' else (sum([p[1] for p in rank_table if p[0] == cur_card[0]]) if cur_card[-1] == led_suit else -1)"
                  }
                }
              },
              {
                "set": {
                  "key": "best_seat",
                  "value": "$seat",
                  "if": {
                    "calc": "cur_str > best_strength"
                  }
                }
              },
              {
                "set": {
                  "key": "best_strength",
                  "value": {
                    "calc": "max(best_strength, cur_str)"
                  }
                }
              },
              {
                "remove": {
                  "player": "$seat",
                  "key": "hand",
                  "value": "$answer"
                }
              },
              {
                "append": {
                  "key": "trick_cards",
                  "value": {
                    "calc": "['1', '2', '3', '4'][turn_seat - 1] + ':' + cur_card"
                  }
                }
              },
              {
                "append": {
                  "key": "played_cards",
                  "value": {
                    "calc": "['1', '2', '3', '4'][turn_seat - 1] + ':' + cur_card"
                  }
                }
              },
              {
                "adjust": {
                  "key": "plays_in_trick",
                  "value": 1
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} plays {value}."
          },
          "text": "Deal {deal_number}, trick 2. Cards in this trick: {trick_cards}. Led suit: {led
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `all_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `rank_table` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "rutersju_twelve",
    "name": "Rutersju Twelve",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Twelve deals of three cards: bid 0 to 3, the highest bidder must take exactly that many tricks, and the opponents score when the declarer misses."
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
        "key": "tricks",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "is_declarer",
        "visible": "public",
        "type": "bool",
        "initial": false
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
          "AS", "KS", "QS", "JS", "10S", "9S", "8S", "7S", "6S",
          "AH", "KH", "QH", "JH", "10H", "9H", "8H", "7H", "6H",
          "AD", "KD", "QD", "JD", "10D", "9D", "8D", "7D", "6D",
          "AC", "KC", "QC", "JC", "10C", "9C", "8C", "7C", "6C"
        ]
      },
      {
        "key": "deal_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_bidder",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_bid",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "declarer_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "contract",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trick_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "played_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ranks_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tricks_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deals",
        "visible": "public",
        "type": "number",
        "initial": 12
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
        "key": "made_bonus",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_bidder_deal_1",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "dealt_rounds",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "turn_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bids_made",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "plays_in_trick",
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
        "key": "cur_str",
        "visible": "none",
        "type": "number",
        "initial": -1
      },
      {
        "key": "best_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "best_strength",
        "visible": "none",
        "type": "number",
        "initial": -1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the start",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "key": "deal_number",
            "value": 0
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
      "label": "a new deal",
      "do": [
        {
          "adjust": {
            "key": "deal_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "first_bidder",
            "value": {
              "calc": "(first_bidder_deal_1 - 1 + deal_number - 1) % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "['AS', 'KS', 'QS', 'JS', '10S', '9S', '8S', '7S', '6S', 'AH', 'KH', 'QH', 'JH', '10H', '9H', '8H', '7H', '6H', 'AD', 'KD', 'QD', 'JD', '10D', '9D', '8D', '7D', '6D', 'AC', 'KC', 'QC', 'JC', '10C', '9C', '8C', '7C', '6C']"
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
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tricks",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "is_declarer",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": []
          }
        },
        {
          "set": {
            "key": "high_bid",
            "value": -1
          }
        },
        {
          "set": {
            "key": "declarer_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "contract",
            "value": 0
          }
        },
        {
          "set": {
            "key": "trick_number",
            "value": 0
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": ""
          }
        },
        {
          "set": {
            "key": "trick_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "played_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "dealt_rounds",
            "value": 0
          }
        },
        {
          "set": {
            "key": "bids_made",
            "value": 0
          }
        },
        {
          "set": {
            "key": "plays_in_trick",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_strength",
            "value": -1
          }
        },
        {
          "set": {
            "key": "turn_seat",
            "value": {
              "calc": "first_bidder"
            }
          }
        }
      ],
      "text": "Deal {deal_number} of {deals} begins. Seat {first_bidder} bids first."
    },
    {
      "use": "repeat",
      "phase": "deal",
      "label": "dealing",
      "until": {
        "calc": "dealt_rounds >= hand_size"
      },
      "max": 10,
      "steps": [
        {
          "use": "update",
          "phase": "deal",
          "label": "one card to each player",
          "do": [
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
                "player": 3,
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
                },
                "if": {
                  "calc": "len(players) >= 4"
                }
              }
            },
            {
              "append": {
                "player": 4,
                "key": "hand",
                "value": {
                  "calc": "pick"
                },
                "if": {
                  "calc": "len(players) >= 4"
                }
              }
            },
            {
              "remove": {
                "key": "deck",
                "value": {
                  "calc": "pick"
                },
                "if": {
                  "calc": "len(players) >= 4"
                }
              }
            },
            {
              "adjust": {
                "key": "dealt_rounds",
                "value": 1
              }
            }
          ]
        }
      ]
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "text": "Deal {deal_number}: your hand and the table."
    },
    {
      "use": "repeat",
      "phase": "bid",
      "label": "the bidding",
      "until": {
        "calc": "bids_made >= len(players)"
      },
      "max": 10,
      "steps": [
        {
          "use": "ask",
          "phase": "bid",
          "label": "bid",
          "to": {
            "where": "you.seat == turn_seat"
          },
          "answer": {
            "type": "number",
            "min": {
              "calc": "bid_min"
            },
            "max": {
              "calc": "bid_max"
            }
          },
          "each": {
            "do": [
              {
                "set": {
                  "player": "$seat",
                  "key": "bid",
                  "value": "$answer"
                }
              },
              {
                "set": {
                  "key": "declarer_seat",
                  "value": "$seat",
                  "if": {
                    "calc": "$answer >= high_bid"
                  }
                }
              },
              {
                "set": {
                  "key": "high_bid",
                  "value": {
                    "calc": "max(high_bid, $answer)"
                  }
                }
              },
              {
                "adjust": {
                  "key": "bids_made",
                  "value": 1
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} bids {value}."
          },
          "text": "Deal {deal_number}: bid how many of the 3 tricks you will take, a whole number from {bid_min} to {bid_max}. The highest bid so far is {high_bid} (-1 means no bid yet). The highest bidder becomes declarer; on a tie for highest, the one who bid last is declarer. There is no pass."
        },
        {
          "use": "update",
          "phase": "bid",
          "label": "next bidder",
          "do": [
            {
              "set": {
                "key": "turn_seat",
                "value": {
                  "calc": "turn_seat % len(players) + 1"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the declarer",
      "do": [
        {
          "set": {
            "key": "contract",
            "value": {
              "calc": "high_bid"
            }
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "declarer_seat"
            }
          }
        },
        {
          "set": {
            "key": "turn_seat",
            "value": {
              "calc": "declarer_seat"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == declarer_seat"
            },
            "key": "is_declarer",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "you.hand"
            }
          }
        }
      ],
      "text": "Seat {declarer_seat} is the declarer with a contract of {contract} and leads the first trick."
    },
    {
      "use": "repeat",
      "phase": "play",
      "label": "trick 1",
      "until": {
        "calc": "plays_in_trick >= len(players)"
      },
      "max": 10,
      "steps": [
        {
          "use": "ask",
          "phase": "play",
          "label": "trick 1 card",
          "to": {
            "where": "you.seat == turn_seat"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "each": {
            "do": [
              {
                "set": {
                  "key": "cur_card",
                  "value": "$answer"
                }
              },
              {
                "set": {
                  "key": "led_suit",
                  "value": {
                    "calc": "cur_card[-1]"
                  },
                  "if": {
                    "calc": "plays_in_trick == 0"
                  }
                }
              },
              {
                "set": {
                  "key": "cur_str",
                  "value": {
                    "calc": "100 if cur_card == '7D' else (sum([p[1] for p in [['A', 8], ['K', 7], ['Q', 6], ['J', 5], ['1', 4], ['9', 3], ['8', 2], ['7', 1], ['6', 0]] if p[0] == cur_card[0]]) if cur_card[-1] == led_suit else -1)"
                  }
                }
              },
              {
                "set": {
                  "key": "best_seat",
                  "value": "$seat",
                  "if": {
                    "calc": "cur_str > best_strength"
                  }
                }
              },
              {
                "set": {
                  "key": "best_strength",
                  "value": {
                    "calc": "max(best_strength, cur_str)"
                  }
                }
              },
              {
                "remove": {
                  "player": "$seat",
                  "key": "hand",
                  "value": "$answer"
                }
              },
              {
                "append": {
                  "key": "trick_cards",
                  "value": {
                    "calc": "['1', '2', '3', '4'][turn_seat - 1] + ':' + cur_card"
                  }
                }
              },
              {
                "append": {
                  "key": "played_cards",
                  "value": {
                    "calc": "['1', '2', '3', '4'][turn_seat - 1] + ':' + cur_card"
                  }
                }
              },
              {
                "adjust": {
                  "key": "plays_in_trick",
                  "value": 1
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} plays {value}."
          },
          "text": "Deal {deal_number}, trick 1. Cards in this trick: {trick_cards}. Led suit: {led_suit} (empty means you lead). Play one card; you are offered only legal cards (you must follow the led suit if you can, otherwise any card). The 7 of diamonds wins any trick; otherwise the highest card of the led suit wins."
        },
        {
          "use": "update",
          "phase": "play",
          "label": "trick 1 next player",
          "do": [
            {
              "set": {
                "key": "turn_seat",
                "value": {
                  "calc": "turn_seat % len(players) + 1"
                }
              }
            },
            {
              "set": {
                "players": "all",
                "key": "offer",
                "value": {
                  "calc": "[c for c in you.hand if c[-1] == led_suit] if len([c for c in you.hand if c[-1] == led_suit]) > 0 else you.hand"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "play",
      "label": "trick 1 is won",
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "best_seat"
            },
            "key": "tricks",
            "value": 1,
            "text": "Seat {player} wins the trick and leads next."
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "best_seat"
            }
          }
        },
        {
          "set": {
            "key": "turn_seat",
            "value": {
              "calc": "best_seat"
            }
          }
        },
        {
          "adjust": {
            "key": "trick_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": ""
          }
        },
        {
          "set": {
            "key": "plays_in_trick",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_strength",
            "value": -1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "repeat",
      "phase": "play",
      "label": "trick 2",
      "until": {
        "calc": "plays_in_trick >= len(players)"
      },
      "max": 10,
      "steps": [
        {
          "use": "ask",
          "phase": "play",
          "label": "trick 2 card",
          "to": {
            "where": "you.seat == turn_seat"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "each": {
            "do": [
              {
                "set": {
                  "key": "cur_card",
                  "value": "$answer"
                }
              },
              {
                "set": {
                  "key": "led_suit",
                  "value": {
                    "calc": "cur_card[-1]"
                  },
                  "if": {
                    "calc": "plays_in_trick == 0"
                  }
                }
              },
              {
                "set": {
                  "key": "cur_str",
                  "value": {
                    "calc": "100 if cur_card == '7D' else (sum([p[1] for p in [['A', 8], ['K', 7], ['Q', 6], ['J', 5], ['1', 4], ['9', 3], ['8', 2], ['7', 1], ['6', 0]] if p[0] == cur_card[0]]) if cur_card[-1] == led_suit else -1)"
                  }
                }
              },
              {
                "set": {
                  "key": "best_seat",
                  "value": "$seat",
                  "if": {
                    "calc": "cur_str > best_strength"
                  }
                }
              },
              {
                "set": {
                  "key": "best_strength",
                  "value": {
                    "calc": "max(best_strength, cur_str)"
                  }
                }
              },
              {
                "remove": {
                  "player": "$seat",
                  "key": "hand",
                  "value": "$answer"
                }
              },
              {
                "append": {
                  "key": "trick_cards",
                  "value": {
                    "calc": "['1', '2', '3', '4'][turn_seat - 1] + ':' + cur_card"
                  }
                }
              },
              {
                "append": {
                  "key": "played_cards",
                  "value": {
                    "calc": "['1', '2', '3', '4'][turn_seat - 1] + ':' + cur_card"
                  }
                }
              },
              {
                "adjust": {
                  "key": "plays_in_trick",
                  "value": 1
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} plays {value}."
          },
          "text": "Deal {deal_number}, trick 2. Cards in this trick: {trick_cards}. Led suit: {led_suit} (empty means you lead). Play one card; you are offered only legal cards (you must follow the led suit if you can, otherwise any card). The 7 of diamonds wins any trick; otherwise the highest card of the led suit wins."
        },
        {
          "use": "update",
          "phase": "play",
          "label": "trick 2 next player",
          "do": [
            {
              "set": {
                "key": "turn_seat",
                "value": {
                  "calc": "turn_seat % len(players) + 1"
                }
              }
            },
            {
              "set": {
                "players": "all",
                "key": "offer",
                "value": {
                  "calc": "[c for c in you.hand if c[-1] == led_suit] if len([c for c in you.hand if c[-1] == led_suit]) > 0 else you.hand"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "play",
      "label": "trick 2 is won",
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "best_seat"
            },
            "key": "tricks",
            "value": 1,
            "text": "Seat {player} wins the trick and leads next."
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "best_seat"
            }
          }
        },
        {
          "set": {
            "key": "turn_seat",
            "value": {
              "calc": "best_seat"
            }
          }
        },
        {
          "adjust": {
            "key": "trick_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": ""
          }
        },
        {
          "set": {
            "key": "plays_in_trick",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_strength",
            "value": -1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "repeat",
      "phase": "play",
      "label": "trick 3",
      "until": {
        "calc": "plays_in_trick >= len(players)"
      },
      "max": 10,
      "steps": [
        {
          "use": "ask",
          "phase": "play",
          "label": "trick 3 card",
          "to": {
            "where": "you.seat == turn_seat"
          },
          "answer": {
            "type": "choice",
            "options": {
              "attribute": "offer"
            }
          },
          "each": {
            "do": [
              {
                "set": {
                  "key": "cur_card",
                  "value": "$answer"
                }
              },
              {
                "set": {
                  "key": "led_suit",
                  "value": {
                    "calc": "cur_card[-1]"
                  },
                  "if": {
                    "calc": "plays_in_trick == 0"
                  }
                }
              },
              {
                "set": {
                  "key": "cur_str",
                  "value": {
                    "calc": "100 if cur_card == '7D' else (sum([p[1] for p in [['A', 8], ['K', 7], ['Q', 6], ['J', 5], ['1', 4], ['9', 3], ['8', 2], ['7', 1], ['6', 0]] if p[0] == cur_card[0]]) if cur_card[-1] == led_suit else -1)"
                  }
                }
              },
              {
                "set": {
                  "key": "best_seat",
                  "value": "$seat",
                  "if": {
                    "calc": "cur_str > best_strength"
                  }
                }
              },
              {
                "set": {
                  "key": "best_strength",
                  "value": {
                    "calc": "max(best_strength, cur_str)"
                  }
                }
              },
              {
                "remove": {
                  "player": "$seat",
                  "key": "hand",
                  "value": "$answer"
                }
              },
              {
                "append": {
                  "key": "trick_cards",
                  "value": {
                    "calc": "['1', '2', '3', '4'][turn_seat - 1] + ':' + cur_card"
                  }
                }
              },
              {
                "append": {
                  "key": "played_cards",
                  "value": {
                    "calc": "['1', '2', '3', '4'][turn_seat - 1] + ':' + cur_card"
                  }
                }
              },
              {
                "adjust": {
                  "key": "plays_in_trick",
                  "value": 1
                }
              }
            ]
          },
          "broadcast": {
            "to": "all",
            "text": "Seat {seat} plays {value}."
          },
          "text": "Deal {deal_number}, trick 3. Cards in this trick: {trick_cards}. Led suit: {led_suit} (empty means you lead). Play one card; you are offered only legal cards (you must follow the led suit if you can, otherwise any card). The 7 of diamonds wins any trick; otherwise the highest card of the led suit wins."
        },
        {
          "use": "update",
          "phase": "play",
          "label": "trick 3 next player",
          "do": [
            {
              "set": {
                "key": "turn_seat",
                "value": {
                  "calc": "turn_seat % len(players) + 1"
                }
              }
            },
            {
              "set": {
                "players": "all",
                "key": "offer",
                "value": {
                  "calc": "[c for c in you.hand if c[-1] == led_suit] if len([c for c in you.hand if c[-1] == led_suit]) > 0 else you.hand"
                }
              }
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "play",
      "label": "trick 3 is won",
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "best_seat"
            },
            "key": "tricks",
            "value": 1,
            "text": "Seat {player} wins the trick."
          }
        },
        {
          "set": {
            "key": "leader_seat",
            "value": {
              "calc": "best_seat"
            }
          }
        },
        {
          "adjust": {
            "key": "trick_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": ""
          }
        },
        {
          "set": {
            "key": "plays_in_trick",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "best_strength",
            "value": -1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "score",
      "label": "score the deal",
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "declarer_seat"
            },
            "key": "score",
            "value": {
              "calc": "contract + made_bonus"
            },
            "if": {
              "calc": "sum([p.tricks for p in players if p.is_declarer]) == contract"
            },
            "text": "Seat {player} made the contract and scores."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.is_declarer and sum([p.tricks for p in players if p.is_declarer]) != contract"
            },
            "key": "score",
            "value": {
              "calc": "abs(contract - sum([p.tricks for p in players if p.is_declarer]))"
            },
            "text": "Opponent seat {player} scores from the missed contract."
          }
        }
      ],
      "text": "Deal {deal_number} is scored. Contract {contract} by seat {declarer_seat}."
    },
    {
      "use": "tell",
      "phase": "score",
      "label": "the totals",
      "to": "all",
      "text": "Scores after deal {deal_number} [seat, score]: {[[p.seat, p.score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after the last deal",
      "when": {
        "calc": "deal_number >= deals"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "deal_number >= deals"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "CARDS. A {deck_size}-card pack with {suits} suits (spades S, hearts H, diamonds D, clubs C). Each suit has {ranks_per_suit} ranks: A, K, Q, J, 10, 9, 8, 7, 6, from high to low. The diamond 7 (7D) is special: it wins any trick it is played to. Otherwise it is a diamond.\n\nSEATS. Players sit in a fixed clockwise order (seat 1, 2, 3, 4), and every player starts at {starting_score} points. The game lasts exactly {deals} deals. In deal 1, seat {first_bidder_deal_1} bids first. In each later deal, the first bidder is the next seat clockwise from the previous deal's first bidder.\n\nEACH DEAL.\n1. Deal. All 36 cards are shuffled and {hand_size} cards are dealt face down to each player. Each player sees only their own hand. The remaining cards stay unseen for the whole deal.\n2. Bid. Starting with the first bidder and going clockwise, each player in turn announces a bid from {bid_min} to {bid_max}. All bids are public as soon as they are made. Every player must bid; there is no passing.\n3. Declarer. The player with the highest bid becomes the declarer. If several players tie for the highest bid, the one of them who bid last becomes the declarer. The declarer's bid is the contract. All other players are opponents for this deal.\n4. Play {tricks_per_deal} tricks. The declarer leads the first trick. In each trick, the leader plays one card face up. Then each other player in clockwise order plays one card face up. A player who holds a card of the led suit must play a card of that suit. A player with none may play any card. If the diamond 7 is in the trick, its player wins the trick. Otherwise the highest card of the led suit wins; cards of other suits never win. Each player's tricks are counted separately. The winner of a trick leads the next one. All played cards stay visible to everyone.\n5. Score. Count the declarer's tricks. If the declarer took exactly the contract, the declarer scores the contract plus {made_bonus} point (a contract of 0 made scores 1; a contract of 3 made scores 4) and the opponents score nothing. If the declarer took more or fewer tricks than the contract, every opponent scores points equal to the difference between the contract and the declarer's tricks, and the declarer scores nothing. Opponents' own tricks are never scored.\n6. Announce. Every player's total is announced. Then the next deal starts.\n\nThere is no discussion at any time. Players communicate only through their bids and the cards they play.\n\nEND. After deal {deals} is scored, the game ends. The player with the highest total wins; if two or more players tie for the highest total, they share the result (a draw)."
}
```
````
