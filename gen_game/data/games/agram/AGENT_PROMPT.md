# Task: write the XColos game file for "Agram Match"

You are a coding agent working in the repository at /Users/alexdaixin/AAI_LAB/xcolos. Write ONE file, `gen_game/data/games/agram/game.json`: the game
below as a game definition for the XColos engine. Do not write any other file except `gen_game/data/games/agram/encode_notes.md`.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

Deck: 35 cards. Hearts 9: A,10,9,8,7,6,5,4,3. Diamonds 9: same. Clubs 9: same. Spades 8: 10,9,8,7,6,5,4,3. No kings, queens, jacks, deuces, and no ace of spades. Rank high to low in hearts/diamonds/clubs is A then 10-9-8-7-6-5-4-3; in spades 10 then 9-8-7-6-5-4-3. Suits are unranked; only the led suit matters. Match: 6 hands. Initial state: every seat match_points 0, hand number 0, no cards dealt. Dealer for hand 1 is chosen uniformly at random; dealer rotates one seat clockwise each later hand. Each hand in order: 1) Shuffle the 35 cards. 2) Deal 6 cards to each player face-down, in two batches: clockwise from left of dealer, 3 cards to each, then 3 cards to each again. Remaining stub (17 cards at 3 players, 11 at 4 players) is left face-down, never viewed, and takes no part in the hand. 3) Play 6 tricks. Trick 1 leader is the player left of the dealer. For each trick in order: a) Leader is offered all cards remaining in their hand and must play exactly one face-up. That suit becomes the led suit for this trick. b) Clockwise, each follower in turn is offered a restricted choice: if they hold at least one card of the led suit they are offered only those led-suit cards and must play one of them (following is enforced, illegal off-suit play is never offered); if they hold none of the led suit they are offered all cards remaining in their hand and must play one (any discard). c) Resolution: the highest rank of the led suit among cards played wins the trick; off-suit cards cannot win even if higher in their own rank. There are no ties because all 35 cards are distinct. The trick cards are removed and hands shrink by one. Announce the trick winner and that they lead the next trick. The trick winner leads any one card to the next trick. Tricks 1-5 score nothing except determining who leads next. 4) Hand scoring: the winner of trick 6 wins the hand outright and gains 1 match_point; every other player gains 0 for the hand. Announce hand winner. 5) Standings: announce every seat's match_points by looping seats 1 to num_players, e.g. 'Points: seat 1 X, seat 2 Y, ...'. Then redeal for the next hand with the next dealer. Information: all card plays are shown to all players as played with seat and card; hands are otherwise hidden and never shown. Private message at the start of each hand uses only this template: 'Your hand: [cards]; dealer seat D; hand k of 6; points so far: seat 1 X, seat 2 Y, ...'. Do not show build constants, deck size, empty lead_suit, stale trick_winner, or living-seats lines; trick_winner and lead_suit are shown only after they are set for the current trick. No discussion messages are used: hands stay hidden so follow/void signals must be read, and with one winner per hand cheap talk would only add noise or give hands away.

How the winner is decided: After 6 hands, the player with the most match_points (hand wins, 0-6) wins the match. If two or more players tie for most, the result is a draw. The ending announcement must list every seat 1 to num_players with its points, e.g. 'Final points: seat 1 X, seat 2 Y, seat 3 Z, seat 4 W. Winner seat N' or 'Draw among ...'.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Agram Match (3 to 4 players, best with 4)

35-card trick game over 6 hands of 6 tricks where only trick 6 of each hand scores 1 point and most points wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. face-down cards dealt for current hand, shrinks by one each trick
  - each player: match_points (number, starts 0); everyone sees it. hands won, 0-6, only trick 6 winner per hand scores
  - the table: deck (list, starts ['HA', 'H10', 'H9', 'H8', 'H7', 'H6', 'H5', 'H4', 'H3', 'DA', 'D10', 'D9', 'D8', 'D7', 'D6', 'D5', 'D4', 'D3', 'CA', 'C10', 'C9', 'C8', 'C7', 'C6', 'C5', 'C4', 'C3', 'S10', 'S9', 'S8', 'S7', 'S6', 'S5', 'S4', 'S3']); hidden from all players. 35-card Agram deck, distinct cards, shuffled each hand
  - the table: stub (list, starts []); hidden from all players. undealt remainder, 17 at 3 players and 11 at 4 players, never viewed
  - the table: hand_number (number, starts 0); everyone sees it. current hand 1 to 6
  - the table: dealer_seat (number, starts 0); everyone sees it. dealer seat for current hand, random for hand 1 then rotates clockwise
  - the table: trick_number (number, starts 0); everyone sees it. current trick 1 to 6 within hand
  - the table: lead_suit (text, starts ''); everyone sees it. suit led by leader for current trick, shown only after set
  - the table: trick_plays (list, starts []); everyone sees it. face-up cards played this trick with seat
  - the table: trick_winner_seat (number, starts 0); everyone sees it. winner of current trick, leads next trick, shown only after set
  - parameters, each kept as a table attribute: num_hands = 6, tricks_per_hand = 6, cards_per_player = 6, deal_batch_size = 3, deck_size = 35, points_per_hand_win = 1, stub_3p = 17, stub_4p = 11

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every seat starts with match_points 0 and hand_number 0 with no cards dealt.
  2. Build the 35-card deck: hearts A,10,9,8,7,6,5,4,3 and diamonds same and clubs same and spades 10,9,8,7,6,5,4,3 with no kings queens jacks deuces and no ace of spades.
  3. Choose dealer_seat for hand 1 uniformly at random.
  4. Rank is A then 10-9-8-7-6-5-4-3 in hearts diamonds clubs and 10 then 9-8-7-6-5-4-3 in spades, suits unranked.
  5. No discussion messages are used.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [initialize] all players. What happens: if hand_number==0 then set each match_points to 0 and build deck of 35 cards
  2. [update] all players. What happens: hand_number+=1; if hand_number==1 keep random dealer_seat else dealer_seat rotates one clockwise; shuffle deck; deal 6 cards to each hand in two batches of 3 clockwise from left of dealer; set stub to remainder; set trick_number to 0; clear lead_suit and trick_plays
  3. [sync] all players. What happens: send each seat private hand: Your hand list plus dealer_seat plus hand_number of 6 plus all match_points
  4. [ask] trick leader answers: {'type': 'choice', 'options': 'all cards remaining in hand'}. What happens: leader plays one card from hand to trick_plays; set lead_suit to its suit; trick_number+=1 for first play of trick
  5. [ask] each player in turn answers: {'type': 'choice', 'options': 'led-suit cards only if holding any else all remaining hand cards'}. What happens: each follower clockwise plays one card from hand to trick_plays following lead_suit when possible
  6. [update] all players. What happens: set trick_winner_seat to seat with highest rank of lead_suit among trick_plays; remove trick cards; shrink each hand by one; clear lead_suit for next trick after announcement
  7. [tell] all players. What happens: announce trick_winner_seat and played cards with seats and that winner leads next trick
  8. [repeat] all players. What happens: repeat leader play and follower play and resolve and announce until trick_number==6
  9. [update] all players. What happens: if trick_number==6 then trick 6 winner trick_winner_seat gains 1 match_points; others gain 0
  10. [tell] all players. What happens: announce hand winner and standings Points seat 1 to num_players with match_points
  11. [check] all players. What happens: continue redealing with next dealer until hand_number==6 else end match

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the deck is built, then it has 35 cards: hearts A,10,9,8,7,6,5,4,3 and diamonds same and clubs same and spades 10,9,8,7,6,5,4,3 with no ace of spades.
  R2. When ranks compare, then in hearts diamonds clubs A beats 10 beats 9 beats 8 beats 7 beats 6 beats 5 beats 4 beats 3 and in spades 10 beats 9 beats 8 beats 7 beats 6 beats 5 beats 4 beats 3.
  R3. When suits compare, then suits are unranked and only the led suit matters.
  R4. When the match starts, then every seat has match_points 0 and hand_number 0 with no cards dealt and the match lasts 6 hands.
  R5. When hand 1 starts, then dealer_seat is chosen uniformly at random and each later hand dealer rotates one seat clockwise.
  R6. When each hand starts, then shuffle the 35 cards.
  R7. When dealing, then deal 6 cards to each player in two batches of 3 clockwise from left of dealer.
  R8. When dealing is done, then the stub of 17 cards at 3 players or 11 cards at 4 players is left face-down never viewed and takes no part.
  R9. When each hand is played, then play 6 tricks and trick 1 leader is the player left of the dealer.
  R10. When the leader plays, then they must play exactly one face-up card from all cards remaining in hand and that suit becomes lead_suit.
  R11. When a follower holds at least one card of lead_suit, then they are offered only those led-suit cards and must play one of them.
  R12. When a follower holds none of lead_suit, then they are offered all cards remaining in hand and must play one discard.
  R13. When a trick resolves, then the highest rank of lead_suit among cards played wins and off-suit cards cannot win.
  R14. When a trick ends, then trick cards are removed and hands shrink by one and the winner is announced and leads any one card to the next trick.
  R15. When tricks 1 to 5 end, then they score nothing except determining who leads next.
  R16. When trick 6 ends, then its winner wins the hand outright and gains 1 match_point and every other player gains 0.
  R17. When a hand ends, then announce every seat match_points seats 1 to num_players and redeal with the next dealer.
  R18. When cards are played, then all plays are shown to all with seat and card and hands are otherwise hidden and never shown.
  R19. When each hand starts, then each seat gets private message Your hand cards dealer seat D hand k of 6 points seats 1 to num_players with no other lines.
  R20. When the match ends after 6 hands, then the player with most match_points wins and a tie for most is a draw with Final points listing seats 1 to num_players.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - leader play | asked: trick leader | options: all cards remaining in leader hand: must play exactly one to set lead_suit
  - follower play when holding led suit | asked: each follower in clockwise turn | options: only led-suit cards in hand: must follow, off-suit never offered
  - follower play when void in led suit | asked: each follower in clockwise turn | options: all cards remaining in hand: any discard

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_number==6
  - the result is one of: seat 1, seat 2, seat 3, seat 4, draw
  - how the result is decided: seat with max match_points wins the match; if two or more tie for max then draw; announce Final points seat 1 to num_players with points plus Winner seat N or Draw among seats
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
rounds it says a match may run at most) and `limits.rounds_max` to at least that. The `end` rules fire the real endings from the state; add one more
ending that fires when the cap is reached and decides the winner as the script says, so a match that hits the cap still ends with a result.

## The interface the file must use

Independent tests were written against these names and you cannot see them, so use them exactly.

- each player: `match_points` (number, visible: public, starts 0): hands won, 0-6, only trick 6 winner per hand scores
- parameters (each must be an attribute holding this value, never a number buried in a step): num_hands = 6, tricks_per_hand = 6, cards_per_player = 6, deal_batch_size = 3, deck_size = 35, points_per_hand_win = 1, stub_3p = 17, stub_4p = 11
- the game ends with exactly one of these results, named exactly: `seat 1`, `seat 2`, `seat 3`, `seat 4`, `draw`
- anything else the game needs to keep track of is yours to design: name it as you like.

## How the platform works

- The complete file format is documented in `design/actions.md`. Read all of it: every key an action accepts is listed there,
  and the loader refuses any other.
- Complete example games to imitate, in `xcolos/games/library/`:
  * xcolos/games/library/rps.json
  * xcolos/games/library/auction.json
  The `auction` example ends with a model-decided `winner`; do NOT copy that part. End with a `result` and a calc condition
  as `rps` does.
- The outcome must be decided by arithmetic: every ending's `when` is a calc condition, no prose conditions; no step uses `llm`
  and every step uses `text`. Choices made at the same moment are a `poll`.
- ENDING STATEMENT: the end screen announces the result only: who won (or that it was a draw) and the final figures that decided it,
  using placeholders such as `{players[0].score}` and `{target}`. Keep it to a line or two. Do NOT retell the game, and do NOT use
  `llm` in an ending: no summary of what each player did or of the turning points.

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
3. A `check` with `when` and `against`, and the endings in `end`, comparing `players[0].score` and `players[1].score`.
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
        "seat_1_wins",
        "seat_2_wins",
        "draw"
      ]
    }
  ],
  "end": {
    "seat_1_wins": {
      "when": {
        "calc": "players[0].score > players[1].score"
      },
      "result": "seat 1",
      "text": "Seat 1 wins."
    },
    "seat_2_wins": {
      "when": {
        "calc": "players[1].score > players[0].score"
      },
      "result": "seat 2",
      "text": "Seat 2 wins."
    },
    "draw": {
      "when": {
        "calc": "players[0].score == players[1].score"
      },
      "result": "draw",
      "text": "A draw."
    }
  }
}
```

## Check your work

Run this from the repository root, and keep fixing `game.json` until it prints `ok` (give up after about 8 attempts and say
what blocks you):

    python3 -m gen_game verify agram game

It runs the loader, checks the outcome is arithmetic, and plays the game with random seats. It tells you the problem when it
fails. Then check that the game plays the RULES in the script:

    python3 -m gen_game verify agram rules

It plays the game through independent scenarios, one per rule, and names each rule that is broken, in its own words, with what it
expected and what the game did. Fix the game until it prints `ok` too. (If it says no scenarios have been written yet, skip it.)
The scenarios are written by someone else from the rules alone, so the rules list is your checklist: read it, and do not guess.

Do NOT read `gen_game/data/games/agram/scenarios.json` or anything under `gen_game/data/games/agram/history/`, and do not edit code. When you are done, write
`gen_game/data/games/agram/encode_notes.md`: where the rules were ambiguous or the platform could not do what they ask, and what you chose.
If the platform genuinely cannot express something the rules REQUIRE, say so there plainly instead of faking it.
