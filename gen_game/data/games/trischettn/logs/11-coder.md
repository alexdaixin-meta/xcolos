# 11 coder

- time: 2026-10-28T02:40:40+00:00 (170.4s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 1b7ff784e7ebc6fc, reply sha256 57beb32bf42e8e1c

## Sent

````
# Task: write the XColos game file for "Trischettn Duel"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

DECK. 24 cards in four suits (Hearts, Bells, Leaves, Acorns), each with Ten, Nine, Ace, King, Ober and Unter. Within a suit the trick-taking order from high to low is Ten, Nine, Ace, King, Ober, Unter. There are no trumps.

CARD VALUES, in thirds of a point. Ace = 3. Ten, Nine, King, Ober and Unter = 1 each. Winning the last (12th) trick of a deal = 3. Each deal therefore has 35 card-and-last-trick thirds.

MATCH. Exactly three deals of 12 tricks each, 36 tricks in all. Each trick is one round.

DEALING. At the start of each deal, shuffle the 24 cards. Deal 6 cards to each player, face down; each player sees only their own hand. The remaining 12 cards form the talon in a fixed shuffled order. The top card of the talon is turned face up and shown to both players. Each player's 'declared this deal' mark is cleared.

FIRST LEAD. Player 1 leads the first trick of deal 1, and player 2 leads the first trick of deal 2. In deal 3, the player with the lower match total leads first; if the totals are tied, player 2 leads.

EACH TRICK.
(1) Both players are shown: their own hand, the face-up talon card (if any), the number of cards left in the talon, the current scores, and every card played so far this deal.
(2) Declaration option. The leader may declare if all three hold: the leader won the previous trick of this deal (so never on the first trick of a deal), the leader has not yet declared this deal, and the leader holds at least one qualifying set. The qualifying sets are:
- three Tens, three Nines or three Aces = 9 thirds;
- all four Tens, Nines or Aces = 12 thirds, instead of the 9 for three of that rank;
- a Napoli, meaning the Ten, Nine and Ace of one suit = 9 thirds per suit.
One card may count in several sets. If the leader declares, every qualifying set in the hand at that moment is scored to the leader's deal points, and the cards forming those sets are shown to the opponent. A player can declare at most once per deal.
(3) The leader plays any card from hand face up.
(4) The follower plays a card. If the follower holds a card of the led suit they must play one; otherwise they may play any card. Only legal cards are offered.
(5) The higher card of the led suit wins the trick. The winner adds the values of both cards to their deal points. If this is the 12th trick, the winner also adds 3.
(6) If the talon is not empty, the trick winner takes the face-up talon card into hand. The loser then takes the next talon card into hand; only the loser sees it. If cards remain, the new top card is turned face up. Talon draws happen after each of the first 6 tricks of a deal. After that the hands are played out.
(7) The trick winner leads the next trick.

END OF DEAL. After the 12th trick, each player's deal points (cards, last trick and any declaration) are added to their match total, and both totals are announced.

How the winner is decided: After the third deal, the player with the higher match total in thirds wins. Equal totals are a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Trischettn Duel (2 to 2 players, best with 2)

A two-player, no-trump trick-taking duel with a 24-card deck. It runs three deals of 12 tricks, with talon draws, declarations of sets, and scoring in thirds of a point.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Cards held, each written as text such as 'Ten of Hearts'.
  - each player: deal_points (number, starts 0); everyone sees it. Thirds scored this deal from cards, the last trick and any declaration.
  - each player: match_total (number, starts 0); everyone sees it. Thirds scored over all finished deals. This is the score.
  - each player: declared_this_deal (bool, starts False); everyone sees it. Whether this player has already declared in the current deal.
  - each player: drawn_hidden_card (text, starts ''); only its owner sees it. The face-down talon card the trick loser just drew, which only that player sees.
  - the table: deck (list, starts []); hidden from all players. Cards not yet dealt during dealing. It holds all 24 cards at the start of each deal.
  - the table: talon (list, starts []); hidden from all players. Face-down talon cards in shuffled order. Drawing picks one at random.
  - the table: talon_up (text, starts ''); everyone sees it. The face-up top card of the talon, or empty if there is none.
  - the table: talon_count (number, starts 0); everyone sees it. Talon cards left, counting the face-up one.
  - the table: played_this_deal (list, starts []); everyone sees it. Every card played so far this deal.
  - the table: declared_cards_shown (list, starts []); everyone sees it. Cards shown by declarations this deal.
  - the table: deal_no (number, starts 0); everyone sees it. The current deal, from 1 to 3.
  - the table: trick_in_deal (number, starts 0); everyone sees it. Tricks completed in the current deal, from 0 to 12.
  - the table: tricks_played (number, starts 0); everyone sees it. Tricks completed in the match, from 0 to 36.
  - the table: leader (number, starts 1); everyone sees it. The seat that leads the current trick.
  - the table: last_trick_winner (number, starts 0); everyone sees it. The seat that won the previous trick of this deal, or 0 at the start of a deal.
  - the table: led_card (text, starts ''); everyone sees it. The card the leader played this trick.
  - the table: follow_card (text, starts ''); everyone sees it. The card the follower played this trick.
  - the table: trick_winner (number, starts 0); everyone sees it. The seat that won the current trick.
  - parameters, each kept as a table attribute: deck_size = 24, suits = 4, ranks_per_suit = 6, hand_size = 6, talon_size = 12, tricks_per_deal = 12, deals = 3, total_tricks = 36, talon_draw_tricks = 6, ace_value = 3, ten_value = 1, nine_value = 1, king_value = 1, ober_value = 1, unter_value = 1, last_trick_bonus = 3, thirds_per_deal = 35, three_of_rank_points = 9, four_of_rank_points = 12, napoli_points = 9, napoli_cards = 3, rank_strength_ten = 6, rank_strength_nine = 5, rank_strength_ace = 4, rank_strength_king = 3, rank_strength_ober = 2, rank_strength_unter = 1, deal1_first_leader_seat = 1, deal2_first_leader_seat = 2, deal3_tie_first_leader_seat = 2

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 and seat 2 start with match_total 0.
  2. deal_no is 0, trick_in_deal is 0 and tricks_played is 0, so the first round begins by starting deal 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: Only when trick_in_deal == 0 (start of a deal):
- deal_no += 1.
- deck = all 24 cards (Ten, Nine, Ace, King, Ober and Unter of Hearts, Bells, Leaves and Acorns).
- Each hand = []. Then 6 times for each seat, move a random card from deck to that seat's hand.
- talon = the remaining 12 cards. Move one random talon card to talon_up. talon_count = 12.
- Each deal_points = 0 and each declared_this_deal = false.
- played_this_deal = [], declared_cards_shown = [], last_trick_winner = 0.
- leader = 1 if deal_no == 1. leader = 2 if deal_no == 2. If deal_no == 3: leader = 1 if seat 1 match_total < seat 2 match_total, otherwise 2.
- Announce: 'Deal {deal_no} begins; the face-up talon card is {talon_up}; seat {leader} leads.'
  2. [sync] all players. What happens: Each player sees their own hand, talon_up, talon_count, every deal_points and match_total, played_this_deal and declared_cards_shown.
  3. [ask] the leader (seat given by leader) answers: declare or pass. What happens: Asked only when all of these hold: trick_in_deal >= 1, last_trick_winner == leader, the leader's declared_this_deal is false, and the leader's declaration value is > 0.

The declaration value is the sum of these, over the hand:
- For each rank of Ten, Nine and Ace: 12 if the hand holds 4 of that rank, 9 if it holds exactly 3, otherwise 0.
- 9 for each suit whose Ten, Nine and Ace are all in hand.
  4. [update] table. What happens: When the leader answered declare:
- The leader's deal_points += declaration value.
- The leader's declared_this_deal = true.
- Append every card forming a qualifying set to declared_cards_shown.
- Announce: 'Seat {leader} declares {value} thirds, showing {cards}.'
  5. [ask] the leader (seat given by leader) answers: one card from the leader's hand. What happens: led_card = chosen card. Remove it from the leader's hand and append it to played_this_deal. Announce: 'Seat {leader} leads {led_card}.'
  6. [ask] the follower (the seat that is not leader) answers: one legal card from the follower's hand: a card of led_card's suit if any is held, otherwise any card. What happens: follow_card = chosen card. Remove it from the follower's hand and append it to played_this_deal. Announce: 'Seat {follower} plays {follow_card}.'
  7. [update] table. What happens: Decide and score the trick:
- trick_winner = follower if follow_card has led_card's suit and a higher rank strength (Ten 6, Nine 5, Ace 4, King 3, Ober 2, Unter 1). Otherwise trick_winner = leader.
- trick_in_deal += 1 and tricks_played += 1.
- trick_winner's deal_points += value(led_card) + value(follow_card), where Ace = 3 and every other card = 1.
- If trick_in_deal == 12, trick_winner's deal_points += 3.
- last_trick_winner = trick_winner.
- Announce: 'Seat {trick_winner} wins the trick.'
  8. [update] table. What happens: Only when talon_count > 0:
- Append talon_up to trick_winner's hand. talon_count -= 1.
- Move one random talon card to the loser's hand and set the loser's drawn_hidden_card to it, seen only by the loser. talon_count -= 1.
- If talon is not empty, move one random talon card to talon_up. Otherwise talon_up = ''.
- Announce: 'Seat {trick_winner} takes the face-up card; the new face-up card is {talon_up}.'
  9. [update] table. What happens: leader = trick_winner.
  10. [update] table. What happens: Only when trick_in_deal == 12:
- Each player's match_total += deal_points.
- trick_in_deal = 0.
- Announce: 'Deal {deal_no} over. Seat 1 has {match_total}, seat 2 has {match_total}.'
  11. [check] table. What happens: End the game if tricks_played == 36, otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a deal starts, then the 24 cards are shuffled, each player receives 6 cards in hand, the other 12 form the talon, and one talon card is turned face up as talon_up.
  R2. When a deal starts, then each player's deal_points is 0, declared_this_deal is false, and played_this_deal is empty.
  R3. When deal 1 starts, then seat 1 leads; when deal 2 starts, then seat 2 leads.
  R4. When deal 3 starts, then the seat with the lower match_total leads, and if the totals are equal, seat 2 leads.
  R5. When it is the first trick of a deal, then the leader is not offered a declaration.
  R6. When the leader won the previous trick of this deal, has not declared this deal, and holds a qualifying set, then the leader is offered declare or pass; otherwise the leader is not offered a declaration.
  R7. When a leader declares holding exactly three Tens, three Nines or three Aces, then 9 thirds per such rank are added to the leader's deal_points.
  R8. When a leader declares holding all four Tens, Nines or Aces, then 12 thirds per such rank are added instead of 9.
  R9. When a leader declares holding the Ten, Nine and Ace of one suit (a Napoli), then 9 thirds per such suit are added, and a card may count in several sets.
  R10. When a leader declares, then every qualifying set in hand is scored at once, its cards are added to declared_cards_shown, declared_this_deal becomes true, and no further declaration is offered that deal.
  R11. When the leader plays, then any card in hand may be played and it is added to played_this_deal.
  R12. When the follower holds a card of the led suit, then only cards of the led suit are offered; otherwise every card in hand is offered.
  R13. When the follower plays a higher card of the led suit (Ten > Nine > Ace > King > Ober > Unter), then the follower wins the trick; otherwise the leader wins, as there are no trumps.
  R14. When a trick is won, then the winner adds the values of both cards to deal_points, with Ace = 3 thirds and Ten, Nine, King, Ober, Unter = 1 third each.
  R15. When the 12th trick of a deal is won, then the winner adds a further 3 thirds.
  R16. When a trick ends and the talon is not empty, then the winner takes talon_up into hand, the loser takes a hidden talon card that only the loser sees, and a new card is turned face up if any remain.
  R17. When 6 tricks of a deal are done, then the talon is empty and no more draws happen that deal.
  R18. When a trick ends, then its winner leads the next trick.
  R19. When the 12th trick of a deal ends, then each player's deal_points is added to match_total and both totals are announced.
  R20. When 36 tricks (3 deals) have been played, then the game ends and the higher match_total wins; equal totals are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Declaration | asked: the leader | options: When eligible (won the previous trick this deal, not yet declared this deal, holds a qualifying set): declare, pass. Otherwise the question is not asked.
  - Lead a card | asked: the leader | options: Every card in the leader's hand.
  - Follow a card | asked: the follower | options: If holding any card of the led suit: only those cards. Otherwise: every card in hand.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: tricks_played == 36
  - each player's standing: you.match_total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After three deals, the player with the higher match total in thirds wins; equal totals share the win, which is a draw.
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

- each player: `deal_points` (number, visible: public, starts 0): Thirds scored this deal from cards, the last trick and any declaration.
- each player: `match_total` (number, visible: public, starts 0): Thirds scored over all finished deals. This is the score.
- the table: `talon_up` (text, visible: public, starts ''): The face-up top card of the talon, or empty if there is none.
- the table: `played_this_deal` (list, visible: public, starts []): Every card played so far this deal.
- the table: `declared_cards_shown` (list, visible: public, starts []): Cards shown by declarations this deal.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 24, suits = 4, ranks_per_suit = 6, hand_size = 6, talon_size = 12, tricks_per_deal = 12, deals = 3, total_tricks = 36, talon_draw_tricks = 6, ace_value = 3, ten_value = 1, nine_value = 1, king_value = 1, ober_value = 1, unter_value = 1, last_trick_bonus = 3, thirds_per_deal = 35, three_of_rank_points = 9, four_of_rank_points = 12, napoli_points = 9, napoli_cards = 3, rank_strength_ten = 6, rank_strength_nine = 5, rank_strength_ace = 4, rank_strength_king = 3, rank_strength_ober = 2, rank_strength_unter = 1, deal1_first_leader_seat = 1, deal2_first_leader_seat = 2, deal3_tie_first_leader_seat = 2
- the game ends with ONE ending whose `rank_by` is `you.match_total`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

Fix both problems in the same attempt. (1) Remove every {name} from prompt and broadcast text except {value} and {seat}. Make the declaration prompt static, for example 'You won the last trick, have not declared this deal, and hold at least one qualifying set. Declare now? (yes/no)'. If the player needs the value or the cards, store them in a player attribute visible only to that player (for example `decl_preview_value` and `decl_preview_cards`) that appears in their state, or broadcast them in a separate step using {value}. (2) Set every scratch attribute to visibility `none` on the table, or `ally` on a player. That covers decl_answer, drawn_hidden_card, follow_card, led_card, the declaration temporaries and any leader or turn trackers. Only the interface fields (deal_points, match_total, talon_up, played_this_deal, declared_cards_shown) and each player's own hand should print. A card the loser draws privately belongs in that player's hand or in a field only they can see, not in a public table attribute. Before resubmitting, search the file for '{' in every prompt and message, and list every attribute and its visibility.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "trischettn_duel",
    "name": "Trischettn Duel",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "A two-player, no-trump trick-taking duel with 24 cards: three deals of 12 tricks, talon draws, declarations of sets, and scoring in thirds of a point."
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
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "deal_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "match_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "declared_this_deal",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "drawn_hidden_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "decl_value",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "decl_cards",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "decl_answer",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "follow_offer",
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
        "initial": []
      },
      {
        "key": "talon",
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
        "key": "talon_up",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "talon_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "played_this_deal",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "declared_cards_shown",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "deal_no",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_in_deal",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tricks_played",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader",
        "visible": "none",
        "type": "number",
        "initial": 1
      },
      {
        "key": "follower",
        "visible": "none",
        "type": "number",
        "initial": 2
      },
      {
        "key": "last_trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "follow_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "led_suit_cards",
        "visible": "none",
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
        "key": "trick_loser",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "all_cards",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ten of Hearts",
          "Nine of Hearts",
          "Ace of Hearts",
          "King of Hearts",
          "Ober of Hearts",
          "Unter of Hearts",
          "Ten of Bells",
          "Nine of Bells",
          "Ace of Bells",
          "King of Bells",
          "Ober of Bells",
          "Unter of Bells",
          "Ten of Leaves",
          "Nine of Leaves",
          "Ace of Leaves",
          "King of Leaves",
          "Ober of Leaves",
          "Unter of Leaves",
          "Ten of Acorns",
          "Nine of Acorns",
          "Ace of Acorns",
          "King of Acorns",
          "Ober of Acorns",
          "Unter of Acorns"
        ]
      },
      {
        "key": "hearts_cards",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ten of Hearts",
          "Nine of Hearts",
          "Ace of Hearts",
          "King of Hearts",
          "Ober of Hearts",
          "Unter of Hearts"
        ]
      },
      {
        "key": "bells_cards",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ten of Bells",
          "Nine of Bells",
          "Ace of Bells",
          "King of Bells",
          "Ober of Bells",
          "Unter of Bells"
        ]
      },
      {
        "key": "leaves_cards",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ten of Leaves",
          "Nine of Leaves",
          "Ace of Leaves",
          "King of Leaves",
          "Ober of Leaves",
          "Unter of Leaves"
        ]
      },
      {
        "key": "acorns_cards",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ten of Acorns",
          "Nine of Acorns",
          "Ace of Acorns",
          "King of Acorns",
          "Ober of Acorns",
          "Unter of Acorns"
        ]
      },
      {
        "key": "tens",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ten of Hearts",
          "Ten of Bells",
          "Ten of Leaves",
          "Ten of Acorns"
        ]
      },
      {
        "key": "nines",
        "visible": "none",
        "type": "list",
        "initial": [
          "Nine of Hearts",
          "Nine of Bells",
          "Nine of Leaves",
          "Nine of Acorns"
        ]
      },
      {
        "key": "aces",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ace of Hearts",
          "Ace of Bells",
          "Ace of Leaves",
          "Ace of Acorns"
        ]
      },
      {
        "key": "kings",
        "visible": "none",
        "type": "list",
        "initial": [
          "King of Hearts",
          "King of Bells",
          "King of Leaves",
          "King of Acorns"
        ]
      },
      {
        "key": "obers",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ober of Hearts",
          "Ober of Bells",
          "Ober of Leaves",
          "Ober of Acorns"
        ]
      },
      {
        "key": "unters",
        "visible": "none",
        "type": "list",
        "initial": [
          "Unter of Hearts",
          "Unter of Bells",
          "Unter of Leaves",
          "Unter of Acorns"
        ]
      },
      {
        "key": "hearts_napoli",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ten of Hearts",
          "Nine of Hearts",
          "Ace of Hearts"
        ]
      },
      {
        "key": "bells_napoli",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ten of Bells",
          "Nine of Bells",
          "Ace of Bells"
        ]
      },
      {
        "key": "leaves_napoli",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ten of Leaves",
          "Nine of Leaves",
          "Ace of Leaves"
        ]
      },
      {
        "key": "acorns_napoli",
        "visible": "none",
        "type": "list",
        "initial": [
          "Ten of Acorns",
          "Nine of Acorns",
          "Ace of Acorns"
        ]
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
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
        "initial": 6
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "talon_size",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "tricks_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "deals",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "total_tricks",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "talon_draw_tricks",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "ace_value",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "ten_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "nine_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "king_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "ober_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "unter_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "last_trick_bonus",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "thirds_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 35
      },
      {
        "key": "three_of_rank_points",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "four_of_rank_points",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "napoli_points",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "napoli_cards",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_strength_ten",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rank_strength_nine",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rank_strength_ace",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_strength_king",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_strength_ober",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rank_strength_unter",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deal1_first_leader_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deal2_first_leader_seat",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "deal3_tie_first_leader_seat",
        "visible": "public",
        "type": "number",
        "initial": 2
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "match totals start at zero",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "match_total",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "counters start at zero",
      "do": [
        {
          "set": {
            "key": "deal_no",
            "value": 0
          }
        },
        {
          "set": {
            "key": "trick_in_deal",
            "value": 0
          }
        },
        {
          "set": {
            "key": "tricks_played",
            "value": 0
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "start a deal",
      "when": {
        "calc": "trick_in_deal == 0"
      },
      "do": [
        {
          "adjust": {
            "key": "deal_no",
            "value": 1
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
            "key": "talon",
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
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "talon[int(uniform(0, len(talon)))]"
            }
          }
        },
        {
          "set": {
            "key": "talon_up",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "talon",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "talon_count",
            "value": {
              "calc": "talon_size"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "deal_points",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "declared_this_deal",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "drawn_hidden_card",
            "value": ""
          }
        },
        {
          "set": {
            "key": "played_this_deal",
            "value": []
          }
        },
        {
          "set": {
            "key": "declared_cards_shown",
            "value": []
          }
        },
        {
          "set": {
            "key": "last_trick_winner",
            "value": 0
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "deal1_first_leader_seat if deal_no == 1 else (deal2_first_leader_seat if deal_no == 2 else (1 if players[0].match_total < players[1].match_total else (2 if players[1].match_total < players[0].match_total else deal3_tie_first_leader_seat)))"
            }
          }
        }
      ],
      "text": "Deal {deal_no} begins; the face-up talon card is {talon_up}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "work out declarations",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "decl_answer",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "decl_value",
            "value": {
              "calc": "(four_of_rank_points if count(x in tens for x in you.hand) == suits else (three_of_rank_points if count(x in tens for x in you.hand) == suits - 1 else 0)) + (four_of_rank_points if count(x in nines for x in you.hand) == suits else (three_of_rank_points if count(x in nines for x in you.hand) == suits - 1 else 0)) + (four_of_rank_points if count(x in aces for x in you.hand) == suits else (three_of_rank_points if count(x in aces for x in you.hand) == suits - 1 else 0)) + (napoli_points if count(x in you.hand for x in hearts_napoli) == napoli_cards else 0) + (napoli_points if count(x in you.hand for x in bells_napoli) == napoli_cards else 0) + (napoli_points if count(x in you.hand for x in leaves_napoli) == napoli_cards else 0) + (napoli_points if count(x in you.hand for x in acorns_napoli) == napoli_cards else 0)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "decl_cards",
            "value": {
              "calc": "[c for c in you.hand if (c in tens and count(x in tens for x in you.hand) >= suits - 1) or (c in nines and count(x in nines for x in you.hand) >= suits - 1) or (c in aces and count(x in aces for x in you.hand) >= suits - 1) or (c in hearts_napoli and count(x in you.hand for x in hearts_napoli) == napoli_cards) or (c in bells_napoli and count(x in you.hand for x in bells_napoli) == napoli_cards) or (c in leaves_napoli and count(x in you.hand for x in leaves_napoli) == napoli_cards) or (c in acorns_napoli and count(x in you.hand for x in acorns_napoli) == napoli_cards)]"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "trick",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "text": "Your hand, the talon, the scores and the cards played this deal:"
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "declaration",
      "when": {
        "calc": "trick_in_deal >= 1 and last_trick_winner == leader and count(p.seat == leader and not p.declared_this_deal and p.decl_value > 0 for p in players) > 0"
      },
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": [
          "declare",
          "pass"
        ]
      },
      "store": "decl_answer",
      "text": "You won the last trick, have not declared this deal, and hold at least one qualifying set (your decl_value and decl_cards show what it is worth). Declare now, or pass? If you declare, every qualifying set in your hand is scored now, its cards are shown to your opponent, and you cannot declare again this deal. If you pass, nothing is scored and you may declare later this deal when eligible."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the declaration",
      "when": {
        "calc": "count(p.decl_answer == 'declare' for p in players) > 0"
      },
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "leader"
            },
            "key": "deal_points",
            "value": {
              "calc": "players[leader - 1].decl_value"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "leader"
            },
            "key": "declared_this_deal",
            "value": true
          }
        },
        {
          "set": {
            "key": "declared_cards_shown",
            "value": {
              "calc": "declared_cards_shown + players[leader - 1].decl_cards"
            }
          }
        }
      ],
      "text": "Seat {last_trick_winner} declares. Cards shown by declarations this deal: {declared_cards_shown}."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "lead a card",
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "lead"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
      },
      "text": "You lead this trick. Play any card from your hand, face up."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the lead",
      "do": [
        {
          "set": {
            "key": "led_card",
            "value": "$lead"
          }
        },
        {
          "remove": {
            "player": {
              "calc": "leader"
            },
            "key": "hand",
            "value": "$lead"
          }
        },
        {
          "append": {
            "key": "played_this_deal",
            "value": "$lead"
          }
        },
        {
          "set": {
            "key": "led_suit_cards",
            "value": {
              "calc": "hearts_cards if led_card in hearts_cards else (bells_cards if led_card in bells_cards else (leaves_cards if led_card in leaves_cards else acorns_cards))"
            }
          }
        },
        {
          "set": {
            "key": "follower",
            "value": {
              "calc": "[p.seat for p in players if p.seat != leader][0]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "follow_offer",
            "value": {
              "calc": "[c for c in you.hand if c in led_suit_cards] if count(c in led_suit_cards for c in you.hand) > 0 else you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "follow a card",
      "to": {
        "where": "you.seat == follower"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "follow_offer"
        }
      },
      "verify": {
        "bind": "fol"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Play a card to this trick. If you hold a card of the led suit you must play one, so only those cards are offered; otherwise any card is offered."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "decide and score the trick",
      "do": [
        {
          "set": {
            "key": "follow_card",
            "value": "$fol"
          }
        },
        {
          "remove": {
            "player": {
              "calc": "follower"
            },
            "key": "hand",
            "value": "$fol"
          }
        },
        {
          "append": {
            "key": "played_this_deal",
            "value": "$fol"
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "follower if (follow_card in led_suit_cards and (rank_strength_ten if follow_card in tens else (rank_strength_nine if follow_card in nines else (rank_strength_ace if follow_card in aces else (rank_strength_king if follow_card in kings else (rank_strength_ober if follow_card in obers else rank_strength_unter))))) > (rank_strength_ten if led_card in tens else (rank_strength_nine if led_card in nines else (rank_strength_ace if led_card in aces else (rank_strength_king if led_card in kings else (rank_strength_ober if led_card in obers else rank_strength_unter)))))) else leader"
            }
          }
        },
        {
          "set": {
            "key": "trick_loser",
            "value": {
              "calc": "[p.seat for p in players if p.seat != trick_winner][0]"
            }
          }
        },
        {
          "adjust": {
            "key": "trick_in_deal",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "tricks_played",
            "value": 1
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "deal_points",
            "value": {
              "calc": "(ace_value if led_card in aces else (ten_value if led_card in tens else (nine_value if led_card in nines else (king_value if led_card in kings else (ober_value if led_card in obers else unter_value))))) + (ace_value if follow_card in aces else (ten_value if follow_card in tens else (nine_value if follow_card in nines else (king_value if follow_card in kings else (ober_value if follow_card in obers else unter_value))))) + (last_trick_bonus if trick_in_deal == tricks_per_deal else 0)"
            }
          }
        },
        {
          "set": {
            "key": "last_trick_winner",
            "value": {
              "calc": "trick_winner"
            }
          }
        }
      ],
      "text": "Seat {trick_winner} wins the trick."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "talon draws",
      "when": {
        "calc": "talon_count > 0"
      },
      "do": [
        {
          "append": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "hand",
            "value": {
              "calc": "talon_up"
            }
          }
        },
        {
          "adjust": {
            "key": "talon_count",
            "value": -1
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "talon[int(uniform(0, len(talon)))]"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "trick_loser"
            },
            "key": "hand",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "trick_loser"
            },
            "key": "drawn_hidden_card",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "talon",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "adjust": {
            "key": "talon_count",
            "value": -1
          }
        },
        {
          "set": {
            "key": "talon_up",
            "value": "",
            "if": {
              "calc": "len(talon) == 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "talon[int(uniform(0, len(talon)))]"
            },
            "if": {
              "calc": "len(talon) > 0"
            }
          }
        },
        {
          "set": {
            "key": "talon_up",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(talon) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "talon",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(talon) > 0"
            }
          }
        }
      ],
      "text": "Seat {trick_winner} takes the face-up card; the new face-up card is {talon_up}."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "the winner leads",
      "do": [
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
      "use": "update",
      "phase": "deal end",
      "label": "end of the deal",
      "when": {
        "calc": "trick_in_deal == tricks_per_deal"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "match_total",
            "value": {
              "calc": "you.deal_points"
            }
          }
        },
        {
          "set": {
            "key": "trick_in_deal",
            "value": 0
          }
        }
      ],
      "text": "Deal {deal_no} over. Seat 1 has {players[0].match_total}, seat 2 has {players[1].match_total}."
    },
    {
      "use": "check",
      "phase": "deal end",
      "label": "after the last trick",
      "when": {
        "calc": "tricks_played >= total_tricks"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "tricks_played >= total_tricks"
      },
      "rank_by": "you.match_total",
      "text": "Winner: {result}. Final match totals in thirds: Seat 1 {players[0].match_total}, Seat 2 {players[1].match_total}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "DECK. {deck_size} cards in {suits} suits (Hearts, Bells, Leaves, Acorns), each with Ten, Nine, Ace, King, Ober and Unter. Within a suit the trick-taking order from high to low is Ten, Nine, Ace, King, Ober, Unter. There are no trumps.\n\nCARD VALUES, in thirds of a point. Ace = {ace_value}. Ten = {ten_value}, Nine = {nine_value}, King = {king_value}, Ober = {ober_value}, Unter = {unter_value}. Winning the last ({tricks_per_deal}th) trick of a deal = {last_trick_bonus}. Each deal therefore has {thirds_per_deal} card-and-last-trick thirds.\n\nMATCH. Exactly {deals} deals of {tricks_per_deal} tricks each, {total_tricks} tricks in all. Each trick is one round.\n\nDEALING. At the start of each deal, the {deck_size} cards are shuffled. Each player is dealt {hand_size} cards face down; each player sees only their own hand. The remaining {talon_size} cards form the talon in a fixed shuffled order. The top card of the talon is turned face up and shown to both players. Each player's 'declared this deal' mark is cleared and deal points start at 0.\n\nFIRST LEAD. Seat {deal1_first_leader_seat} leads the first trick of deal 1, and seat {deal2_first_leader_seat} leads the first trick of deal 2. In deal 3, the player with the lower match total leads first; if the totals are tied, seat {deal3_tie_first_leader_seat} leads.\n\nEACH TRICK.\n(1) Both players are shown: their own hand, the face-up talon card (if any), the number of cards left in the talon, the current scores, and every card played so far this deal.\n(2) Declaration option. The leader may declare if all three hold: the leader won the previous trick of this deal (so never on the first trick of a deal), the leader has not yet declared this deal, and the leader holds at least one qualifying set. The qualifying sets are: three Tens, three Nines or three Aces = {three_of_rank_points} thirds; all four Tens, Nines or Aces = {four_of_rank_points} thirds, instead of the {three_of_rank_points} for three of that rank; a Napoli, meaning the Ten, Nine and Ace of one suit = {napoli_points} thirds per suit. One card may count in several sets. If the leader declares, every qualifying set in the hand at that moment is scored to the leader's deal points, and the cards forming those sets are shown to the opponent; the leader then plays on as normal and cannot declare again this deal. If the leader passes, nothing is scored, nothing is shown, and the leader may still declare on a later trick of this deal when eligible. If the leader is not eligible, no declaration is offered. A player can declare at most once per deal.\n(3) The leader plays any card from hand face up.\n(4) The follower plays a card. If the follower holds a card of the led suit they must play one; otherwise they may play any card. Only legal cards are offered.\n(5) The higher card of the led suit wins the trick: if the follower played a higher card of the led suit, the follower wins; otherwise (a lower card, or a card of another suit) the leader wins. The winner adds the values of both cards to their deal points. If this is the {tricks_per_deal}th trick, the winner also adds {last_trick_bonus}.\n(6) If the talon is not empty, the trick winner takes the face-up talon card into hand. The loser then takes the next talon card into hand; only the loser sees it. If cards remain, the new top card is turned face up. Talon draws happen after each of the first {talon_draw_tricks} tricks of a deal. After that the hands are played out.\n(7) The trick winner leads the next trick.\n\nEND OF DEAL. After the {tricks_per_deal}th trick, each player's deal points (cards, last trick and any declaration) are added to their match total, and both totals are announced.\n\nWINNING. After the third deal, the player with the higher match total in thirds wins. Equal totals share the win, which is a draw."
}
```
````
