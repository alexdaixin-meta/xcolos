# 06 coder

- time: 2026-10-27T20:47:39+00:00 (149.5s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 001651bad2b1dc34, reply sha256 bb4e25c9c6812ff0

## Sent

````
# Task: write the XColos game file for "Skull King: Three-Card Raids"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

PLAYERS AND DECK. 3 players, seats 1, 2 and 3. The deck has 25 cards: Green 1-7 (7 cards), Yellow 1-7 (7 cards), Black 1-5 (5 cards), 2 Pirates, 2 Escapes, 1 Mermaid and 1 Skull King. Green, Yellow and Black are the suited cards. Pirates, Escapes, the Mermaid and the Skull King are special cards.

STRUCTURE. The game has 9 hands of 3 tricks each, so 27 rounds; each round is one trick. Each player's score starts at 0.

START OF EACH HAND (first trick of the hand only). Shuffle all 25 cards and deal 3 to each player, face down. Each player sees only their own cards. The other 16 cards are set aside unseen. All players then bid at the same moment, each secretly choosing a whole number from 0 to 3: the number of tricks they will win this hand. All bids are then revealed to everyone. The first leader of hand h is seat ((h-1) mod 3) + 1, so hands 1, 4 and 7 are led by seat 1, hands 2, 5 and 8 by seat 2, and hands 3, 6 and 9 by seat 3.

PLAYING A TRICK. The leader plays one card face up, then the next seat clockwise (1 to 2, 2 to 3, 3 to 1), then the third player.
- Lead suit: the suit of the first suited card played in the trick. If special cards are played before any suited card, the lead suit is set by the first suited card that follows. If no suited card is played, there is no lead suit.
- Following: once a lead suit exists, a player who holds a card of that suit must play either a card of that suit or a special card. A player with no card of that suit may play any card. Special cards may always be played.
- The engine offers each player only the cards they may legally play.

WINNING A TRICK. Check these in order:
(1) If the trick contains both the Skull King and the Mermaid, the Mermaid wins.
(2) Otherwise, if it contains the Skull King, the Skull King wins.
(3) Otherwise, if it contains a Pirate, the first Pirate played wins.
(4) Otherwise, if it contains the Mermaid, the Mermaid wins.
(5) Otherwise, if it contains any Black card, the highest Black card wins.
(6) Otherwise, if there is a lead suit, the highest card of the lead suit wins.
(7) Otherwise (all Escapes), the first card played wins.

The player who played the winning card wins the trick, adds 1 to their trick count for this hand and leads the next trick of the hand. Capture bonuses are recorded for the trick winner: +30 for each Pirate in a trick won by the Skull King, and +40 if the Mermaid wins a trick containing the Skull King. The winner, the cards played and any bonus are announced to everyone.

END OF EACH HAND (after the third trick). Each player scores:
- Exact bid of 1, 2 or 3: +20 per trick bid, plus all capture bonuses they recorded this hand.
- Exact bid of 0: +20, plus any capture bonuses they recorded this hand (normally none).
- Missed bid of 0: -20, and bonuses are lost.
- Missed bid of 1, 2 or 3: -10 per trick of difference between bid and tricks won, and bonuses are lost.

Scores are announced. Trick counts and bonuses reset to 0 for the next hand.

END OF GAME. After hand 9 (round 27), the game ends.

How the winner is decided: After 9 hands the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw among the tied players.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Skull King: Three-Card Raids (3 to 3 players, best with 3)

Three players play 9 hands of 3 tricks each. Before each hand every player secretly bids how many tricks they will win, then scores for hitting the bid exactly and loses points for missing it, with bonuses for capturing Pirates or the Skull King.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Total score across all hands.
  - each player: hand (list, starts []); only its owner sees it. Cards the player holds this hand; only the owner sees them.
  - each player: bid (number, starts 0); everyone sees it. Tricks the player bid for the current hand (0-3). Chosen secretly, then revealed.
  - each player: tricks_won (number, starts 0); everyone sees it. Tricks won so far this hand.
  - each player: bonus (number, starts 0); everyone sees it. Capture bonuses recorded this hand. Paid only if the bid is exact.
  - each player: played_card (text, starts ''); everyone sees it. The card this player played in the current trick.
  - the table: deck (list, starts ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'B1', 'B2', 'B3', 'B4', 'B5', 'Pirate', 'Pirate', 'Escape', 'Escape', 'Mermaid', 'SkullKing']); hidden from all players. The 25-card deck. After dealing, the 16 undealt cards stay here, set aside unseen.
  - the table: round (number, starts 1); everyone sees it. Current trick number in the game (1-27).
  - the table: hand_number (number, starts 1); everyone sees it. Current hand (1-9).
  - the table: trick_in_hand (number, starts 1); everyone sees it. Which trick of the hand is being played (1-3).
  - the table: leader (number, starts 1); everyone sees it. Seat that leads the current trick.
  - the table: lead_suit (text, starts ''); everyone sees it. Suit of the first suited card in the trick (Green, Yellow or Black). Empty if no suited card has been played yet.
  - the table: trick_cards (list, starts []); everyone sees it. Cards played to the current trick, in play order, each tagged with the seat that played it.
  - the table: trick_winner (number, starts 0); everyone sees it. Seat that won the most recent trick.
  - parameters, each kept as a table attribute: player_count = 3, deck_size = 25, green_cards = 7, green_max_rank = 7, yellow_cards = 7, yellow_max_rank = 7, black_cards = 5, black_max_rank = 5, pirates = 2, escapes = 2, mermaids = 1, skull_kings = 1, hands = 9, tricks_per_hand = 3, total_rounds = 27, cards_dealt_per_player = 3, cards_set_aside = 16, bid_min = 0, bid_max = 3, exact_bid_points_per_trick = 20, exact_zero_bid_points = 20, missed_zero_bid_points = -20, missed_bid_points_per_trick_difference = -10, pirate_captured_by_skull_king_bonus = 30, skull_king_captured_by_mermaid_bonus = 40, trick_win_increment = 1, starting_score = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 are seated clockwise (1 to 2, 2 to 3, 3 to 1).
  2. Every player's score is set to 0.
  3. The deck list holds all 25 cards: G1-G7, Y1-Y7, B1-B5, 2 Pirate, 2 Escape, 1 Mermaid, 1 SkullKing.
  4. round = 1, hand_number = 1, trick_in_hand = 1, leader = 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When trick_in_hand == 1: return every card in each player's hand and in trick_cards to deck. Then, for each player, draw 3 cards at random from deck into their hand (remove from deck, append to hand); the 16 cards left in deck are set aside unseen. Set each player's bid = 0, tricks_won = 0, bonus = 0. Set leader = ((hand_number - 1) mod 3) + 1.
  2. [sync] all players. What happens: When trick_in_hand == 1: each player is sent their own hand. Nobody sees another player's hand.
  3. [poll] all players answers: a whole number from 0 to 3. What happens: When trick_in_hand == 1: each player's bid is set to their answer. No bid is shown until all are in.
  4. [tell] all players. What happens: When trick_in_hand == 1: announce every seat's bid for hand {hand_number} and the first leader, seat {leader}.
  5. [update] all players. What happens: Set trick_cards = [], lead_suit = '', and each player's played_card = ''.
  6. [ask] each player in turn, starting with seat leader and going clockwise answers: one card from the player's hand that is legal to play (see offers). What happens: Remove the chosen card from the player's hand, append it (with the seat) to trick_cards, and set played_card. If lead_suit == '' and the card is Green, Yellow or Black, set lead_suit to that suit. Each player hears the cards played before them.
  7. [update] all players. What happens: Set trick_winner to the seat holding the first applicable card: (1) if trick_cards holds both SkullKing and Mermaid, the Mermaid; (2) else the SkullKing; (3) else the first Pirate played; (4) else the Mermaid; (5) else the highest Black card; (6) else, if lead_suit is not empty, the highest card of lead_suit; (7) else (all Escapes) the first card played. Add 1 to the winner's tricks_won. If the winning card is the SkullKing, add 30 to the winner's bonus for each Pirate in trick_cards. If the winning card is the Mermaid and trick_cards holds the SkullKing, add 40 to the winner's bonus. Set leader = trick_winner.
  8. [tell] all players. What happens: Announce the cards played (trick_cards), the trick_winner seat and any bonus just recorded.
  9. [update] all players. What happens: When trick_in_hand == 3, for each player: if bid >= 1 and tricks_won == bid, score += 20 * bid + bonus; if bid == 0 and tricks_won == 0, score += 20 + bonus; if bid == 0 and tricks_won > 0, score -= 20; if bid >= 1 and tricks_won != bid, score -= 10 * |bid - tricks_won|. Then set tricks_won = 0 and bonus = 0.
  10. [tell] all players. What happens: When trick_in_hand == 3: announce every seat's score after hand {hand_number}.
  11. [update] all players. What happens: round += 1. If trick_in_hand == 3, then hand_number += 1 and trick_in_hand = 1; otherwise trick_in_hand += 1.
  12. [check] all players. What happens: End the game if round > 27; otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a hand starts (trick_in_hand == 1), then each of the 3 players is dealt 3 cards at random from the 25-card deck into their hand, and the 16 undealt cards stay in deck unseen.
  R2. When cards are dealt, then each player sees only their own hand.
  R3. When a hand starts, then all players bid at the same time, each a whole number from 0 to 3, and all bids are revealed only after everyone has bid.
  R4. When hand h starts, then its first leader is seat ((h-1) mod 3) + 1: seat 1 for hands 1, 4 and 7, seat 2 for hands 2, 5 and 8, and seat 3 for hands 3, 6 and 9.
  R5. When a trick is played, then the leader plays first, then the next seat clockwise, then the third seat, each playing one card face up from their hand.
  R6. When the first suited card (Green, Yellow or Black) is played in a trick, then its suit becomes the lead suit, even if special cards were played before it.
  R7. When no suited card is played in a trick, then the trick has no lead suit.
  R8. When a lead suit exists and a player holds a card of that suit, then they are offered only cards of that suit and special cards.
  R9. When a player holds no card of the lead suit, or there is no lead suit yet, then they are offered every card in their hand.
  R10. When a trick contains both the Skull King and the Mermaid, then the Mermaid wins it.
  R11. When a trick contains the Skull King and no Mermaid, then the Skull King wins it.
  R12. When a trick contains no Skull King and at least one Pirate, then the first Pirate played wins it.
  R13. When a trick contains the Mermaid but no Skull King and no Pirate, then the Mermaid wins it.
  R14. When a trick contains no Skull King, Pirate or Mermaid but at least one Black card, then the highest Black card wins it.
  R15. When a trick contains no special card that wins and no Black card, then the highest card of the lead suit wins it.
  R16. When a trick contains only Escapes, then the first card played wins it.
  R17. When a player wins a trick, then their tricks_won rises by 1 and they lead the next trick of the hand.
  R18. When the Skull King wins a trick, then its player's bonus rises by 30 for each Pirate in that trick.
  R19. When the Mermaid wins a trick containing the Skull King, then its player's bonus rises by 40.
  R20. When a trick ends, then its cards, its winner and any bonus are announced to everyone.
  R21. When a hand ends and a player bid 1, 2 or 3 and won exactly that many tricks, then they score +20 per trick bid plus their bonus (for example, bid 2 and won 2 scores +40 plus bonus).
  R22. When a hand ends and a player bid 0 and won 0 tricks, then they score +20 plus their bonus.
  R23. When a hand ends and a player bid 0 but won at least 1 trick, then they score -20 and lose their bonus.
  R24. When a hand ends and a player bid 1, 2 or 3 but missed, then they score -10 per trick of difference and lose their bonus (for example, bid 3 and won 1 scores -20).
  R25. When a hand ends, then scores are announced and every player's tricks_won and bonus reset to 0.
  R26. When round 27 (the third trick of hand 9) has been scored, then the game ends.
  R27. When the game ends, then the player with the highest score wins, and players tied for the highest share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid at the start of a hand | asked: all seats, at once | options: 0, 1, 2 or 3
  - Card to play in a trick | asked: each seat in turn, starting with the leader | options: If lead_suit is empty (the player leads, or only special cards have been played so far): every card in their hand. If lead_suit is set and the player holds at least one card of that suit: only their cards of the lead suit plus any Pirate, Escape, Mermaid or SkullKing they hold. If lead_suit is set and the player holds no card of that suit: every card in their hand.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 27
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total score after 9 hands. The highest score wins, and players tied for the highest share the win (a draw among them).
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

- each player: `score` (number, visible: public, starts 0): Total score across all hands.
- each player: `bid` (number, visible: public, starts 0): Tricks the player bid for the current hand (0-3). Chosen secretly, then revealed.
- each player: `tricks_won` (number, visible: public, starts 0): Tricks won so far this hand.
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 3, deck_size = 25, green_cards = 7, green_max_rank = 7, yellow_cards = 7, yellow_max_rank = 7, black_cards = 5, black_max_rank = 5, pirates = 2, escapes = 2, mermaids = 1, skull_kings = 1, hands = 9, tricks_per_hand = 3, total_rounds = 27, cards_dealt_per_player = 3, cards_set_aside = 16, bid_min = 0, bid_max = 3, exact_bid_points_per_trick = 20, exact_zero_bid_points = 20, missed_zero_bid_points = -20, missed_bid_points_per_trick_difference = -10, pirate_captured_by_skull_king_bonus = 30, skull_king_captured_by_mermaid_bonus = 40, trick_win_increment = 1, starting_score = 0
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

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "skull_king_three_card_raids",
    "name": "Skull King: Three-Card Raids",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, nine hands of three tricks: bid your tricks in secret, hit the bid exactly, and capture Pirates or the Skull King for bonuses."
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
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
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
          "G1",
          "G2",
          "G3",
          "G4",
          "G5",
          "G6",
          "G7",
          "Y1",
          "Y2",
          "Y3",
          "Y4",
          "Y5",
          "Y6",
          "Y7",
          "B1",
          "B2",
          "B3",
          "B4",
          "B5",
          "Pirate",
          "Pirate",
          "Escape",
          "Escape",
          "Mermaid",
          "SkullKing"
        ]
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trick_in_hand",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "lead_suit",
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
        "key": "trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "discards",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "trick_plain",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "win_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_bonus",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green_set",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "yellow_set",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "black_set",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "specials",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "player_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 25
      },
      {
        "key": "green_cards",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "green_max_rank",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "yellow_cards",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "yellow_max_rank",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "black_cards",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "black_max_rank",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "pirates",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "escapes",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "mermaids",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "skull_kings",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 27
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cards_set_aside",
        "visible": "public",
        "type": "number",
        "initial": 16
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
        "key": "exact_bid_points_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "exact_zero_bid_points",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "missed_zero_bid_points",
        "visible": "public",
        "type": "number",
        "initial": -20
      },
      {
        "key": "missed_bid_points_per_trick_difference",
        "visible": "public",
        "type": "number",
        "initial": -10
      },
      {
        "key": "pirate_captured_by_skull_king_bonus",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "skull_king_captured_by_mermaid_bonus",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "trick_win_increment",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "set the table",
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
            "key": "deck",
            "value": {
              "calc": "['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'B1', 'B2', 'B3', 'B4', 'B5', 'Pirate', 'Pirate', 'Escape', 'Escape', 'Mermaid', 'SkullKing']"
            }
          }
        },
        {
          "set": {
            "key": "green_set",
            "value": {
              "calc": "['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7']"
            }
          }
        },
        {
          "set": {
            "key": "yellow_set",
            "value": {
              "calc": "['Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7']"
            }
          }
        },
        {
          "set": {
            "key": "black_set",
            "value": {
              "calc": "['B1', 'B2', 'B3', 'B4', 'B5']"
            }
          }
        },
        {
          "set": {
            "key": "specials",
            "value": {
              "calc": "['Pirate', 'Escape', 'Mermaid', 'SkullKing']"
            }
          }
        },
        {
          "set": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": 1
          }
        },
        {
          "set": {
            "key": "leader",
            "value": 1
          }
        }
      ],
      "text": "Seats 1, 2 and 3 sit clockwise (1 to 2, 2 to 3, 3 to 1). Every score starts at {starting_score}."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "deal the hand",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "deck + discards"
            }
          }
        },
        {
          "set": {
            "key": "discards",
            "value": []
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
            "players": "all",
            "key": "hand",
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
            "players": "all",
            "key": "bid",
            "value": 0
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
            "key": "leader",
            "value": {
              "calc": "(hand_number - 1) % player_count + 1"
            }
          }
        }
      ],
      "text": "Hand {hand_number} of {hands}: the 25 cards are shuffled and each player is dealt {cards_dealt_per_player} cards face down. The other {cards_set_aside} cards are set aside unseen."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your cards",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand"
      ],
      "text": "Your cards for this hand:"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "the bids",
      "when": {
        "calc": "trick_in_hand == 1"
      },
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
      "text": "Hand {hand_number}: your cards are {hand}. Secretly bid how many of this hand's {tricks_per_hand} tricks you will win, a whole number from {bid_min} to {bid_max}. No bid is shown until everyone has bid."
    },
    {
      "use": "tell",
      "phase": "bid",
      "label": "bids revealed",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "all",
      "text": "Bids for hand {hand_number}: Seat 1 bid {players[0].bid}, Seat 2 bid {players[1].bid}, Seat 3 bid {players[2].bid}. Seat {leader} leads the first trick."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "clear the trick",
      "do": [
        {
          "set": {
            "key": "trick_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "trick_plain",
            "value": []
          }
        },
        {
          "set": {
            "key": "lead_suit",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": ""
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
      "use": "ask",
      "phase": "trick",
      "label": "the lead",
      "to": {
        "where": "you.seat == leader"
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
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": {
                "calc": "[$seat, $answer]"
              }
            }
          },
          {
            "append": {
              "key": "trick_plain",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "discards",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "lead_suit",
              "value": {
                "calc": "'Green' if $answer in green_set else ('Yellow' if $answer in yellow_set else 'Black')"
              },
              "if": {
                "calc": "lead_suit == '' and ($answer in green_set or $answer in yellow_set or $answer in black_set)"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "you.hand if (lead_suit == '' or not any(c in (green_set if lead_suit == 'Green' else (yellow_set if lead_suit == 'Yellow' else black_set)) for c in you.hand)) else [c for c in you.hand if c in specials or c in (green_set if lead_suit == 'Green' else (yellow_set if lead_suit == 'Yellow' else black_set))]"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}: you lead. Your legal cards: {offer}. Play one card face up."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the second card",
      "to": {
        "where": "you.seat == leader % player_count + 1"
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
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": {
                "calc": "[$seat, $answer]"
              }
            }
          },
          {
            "append": {
              "key": "trick_plain",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "discards",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "lead_suit",
              "value": {
                "calc": "'Green' if $answer in green_set else ('Yellow' if $answer in yellow_set else 'Black')"
              },
              "if": {
                "calc": "lead_suit == '' and ($answer in green_set or $answer in yellow_set or $answer in black_set)"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "you.hand if (lead_suit == '' or not any(c in (green_set if lead_suit == 'Green' else (yellow_set if lead_suit == 'Yellow' else black_set)) for c in you.hand)) else [c for c in you.hand if c in specials or c in (green_set if lead_suit == 'Green' else (yellow_set if lead_suit == 'Yellow' else black_set))]"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}. Played so far [seat, card]: {trick_cards}. Lead suit: {lead_suit}. Your legal cards: {offer}. Play one card face up."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the third card",
      "to": {
        "where": "you.seat == (leader + 1) % player_count + 1"
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
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "trick_cards",
              "value": {
                "calc": "[$seat, $answer]"
              }
            }
          },
          {
            "append": {
              "key": "trick_plain",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "discards",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "lead_suit",
              "value": {
                "calc": "'Green' if $answer in green_set else ('Yellow' if $answer in yellow_set else 'Black')"
              },
              "if": {
                "calc": "lead_suit == '' and ($answer in green_set or $answer in yellow_set or $answer in black_set)"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "you.hand if (lead_suit == '' or not any(c in (green_set if lead_suit == 'Green' else (yellow_set if lead_suit == 'Yellow' else black_set)) for c in you.hand)) else [c for c in you.hand if c in specials or c in (green_set if lead_suit == 'Green' else (yellow_set if lead_suit == 'Yellow' else black_set))]"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}. Played so far [seat, card]: {trick_cards}. Lead suit: {lead_suit}. Your legal cards: {offer}. Play one card face up."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "who takes the trick",
      "do": [
        {
          "set": {
            "key": "win_card",
            "value": {
              "calc": "'Mermaid' if ('Mermaid' in trick_plain and 'SkullKing' in trick_plain) else ('SkullKing' if 'SkullKing' in trick_plain else ('Pirate' if 'Pirate' in trick_plain else ('Mermaid' if 'Mermaid' in trick_plain else (max([c for c in trick_plain if c in black_set]) if any(c in black_set for c in trick_plain) else (max([c for c in trick_plain if c in (green_set if lead_suit == 'Green' else (yellow_set if lead_suit == 'Yellow' else black_set))]) if lead_suit != '' else 'Escape')))))"
            }
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "min([((p.seat - leader) % player_count) * 10 + p.seat for p in players if p.played_card == win_card]) % 10"
            }
          }
        },
        {
          "set": {
            "key": "last_bonus",
            "value": {
              "calc": "(count(c == 'Pirate' for c in trick_plain) * pirate_captured_by_skull_king_bonus) if win_card == 'SkullKing' else (skull_king_captured_by_mermaid_bonus if (win_card == 'Mermaid' and 'SkullKing' in trick_plain) else 0)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "tricks_won",
            "value": {
              "calc": "trick_win_increment"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "bonus",
            "value": {
              "calc": "last_bonus"
            },
            "if": {
              "calc": "last_bonus > 0"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "trick_winner"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "trick result",
      "to": "all",
      "text": "Trick {trick_in_hand} of hand {hand_number}: cards played [seat, card] {trick_cards}. Seat {trick_winner} wins the trick with {win_card}. Bonus recorded: {last_bonus}."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "score the hand",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "(exact_bid_points_per_trick * you.bid + you.bonus) if (you.bid >= 1 and you.tricks_won == you.bid) else ((exact_zero_bid_points + you.bonus) if (you.bid == 0 and you.tricks_won == 0) else (missed_zero_bid_points if you.bid == 0 else missed_bid_points_per_trick_difference * abs(you.bid - you.tricks_won)))"
            }
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
        }
      ]
    },
    {
      "use": "tell",
      "phase": "score",
      "label": "scores after the hand",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "to": "all",
      "text": "Scores after hand {hand_number}: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}."
    },
    {
      "use": "update",
      "phase": "advance",
      "label": "next trick",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "hand_number",
            "value": {
              "calc": "1 if trick_in_hand == tricks_per_hand else 0"
            }
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": {
              "calc": "1 if trick_in_hand == tricks_per_hand else trick_in_hand + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "advance",
      "label": "after the last trick",
      "when": {
        "calc": "round > total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > total_rounds"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}."
    }
  },
  "limits": {
    "rounds": 27,
    "rounds_max": 30,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "PLAYERS AND DECK. 3 players, seats 1, 2 and 3, seated clockwise (1 to 2, 2 to 3, 3 to 1). The deck has {deck_size} cards: Green 1-{green_max_rank} ({green_cards} cards), Yellow 1-{yellow_max_rank} ({yellow_cards} cards), Black 1-{black_max_rank} ({black_cards} cards), {pirates} Pirates, {escapes} Escapes, {mermaids} Mermaid and {skull_kings} Skull King. Green, Yellow and Black are the suited cards. Pirates, Escapes, the Mermaid and the Skull King are special cards.\n\nSTRUCTURE. The game has {hands} hands of {tricks_per_hand} tricks each, so {total_rounds} rounds; each round is one trick. Each player's score starts at {starting_score}.\n\nSTART OF EACH HAND. Shuffle all {deck_size} cards and deal {cards_dealt_per_player} to each player, face down. Each player sees only their own cards. The other {cards_set_aside} cards are set aside unseen. All players then bid at the same moment, each secretly choosing a whole number from {bid_min} to {bid_max}: the number of tricks they will win this hand. All bids are then revealed to everyone. The first leader of hand h is seat ((h-1) mod 3) + 1, so hands 1, 4 and 7 are led by seat 1, hands 2, 5 and 8 by seat 2, and hands 3, 6 and 9 by seat 3.\n\nPLAYING A TRICK. The leader plays one card face up, then the next seat clockwise, then the third player.\n- Lead suit: the suit of the first suited card played in the trick. If special cards are played before any suited card, the lead suit is set by the first suited card that follows. If no suited card is played, there is no lead suit.\n- Following: once a lead suit exists, a player who holds a card of that suit must play either a card of that suit or a special card. A player with no card of that suit may play any card. Special cards may always be played.\n- You are offered only the cards you may legally play.\n\nWINNING A TRICK. Check these in order:\n(1) If the trick contains both the Skull King and the Mermaid, the Mermaid wins.\n(2) Otherwise, if it contains the Skull King, the Skull King wins.\n(3) Otherwise, if it contains a Pirate, the first Pirate played wins.\n(4) Otherwise, if it contains the Mermaid, the Mermaid wins.\n(5) Otherwise, if it contains any Black card, the highest Black card wins.\n(6) Otherwise, if there is a lead suit, the highest card of the lead suit wins.\n(7) Otherwise (all Escapes), the first card played wins.\nThe player who played the winning card wins the trick, adds {trick_win_increment} to their trick count for this hand and leads the next trick of the hand. Capture bonuses are recorded for the trick winner: +{pirate_captured_by_skull_king_bonus} for each Pirate in a trick won by the Skull King, and +{skull_king_captured_by_mermaid_bonus} if the Mermaid wins a trick containing the Skull King. The winner, the cards played and any bonus are announced to everyone.\n\nEND OF EACH HAND (after the third trick). Each player scores:\n- Exact bid of 1, 2 or 3: +{exact_bid_points_per_trick} per trick bid, plus all capture bonuses they recorded this hand.\n- Exact bid of 0: +{exact_zero_bid_points}, plus any capture bonuses they recorded this hand (normally none).\n- Missed bid of 0: {missed_zero_bid_points}, and bonuses are lost.\n- Missed bid of 1, 2 or 3: {missed_bid_points_per_trick_difference} per trick of difference between bid and tricks won, and bonuses are lost.\nScores are announced. Trick counts and bonuses reset to 0 for the next hand.\n\nEND OF GAME. After hand {hands} (round {total_rounds}), the game ends. The player with the highest total score wins. If two or three players tie for the highest total, they share the win."
}
```
````
